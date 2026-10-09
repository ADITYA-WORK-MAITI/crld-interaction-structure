"""
Collective Reinforcement-Learning Dynamics (CRLD) for N agents in a count-symmetric
stochastic social dilemma.

Framework: Barfuss, Donges & Kurths (2019) Phys Rev E 99:043305; Barfuss (2022)
Neural Comput Appl 34:1653. The deterministic-limit policy update is their Eq. (2).

The contribution of this module is computational, not theoretical. Evaluating the
strategy-average TD error nominally costs M^(N-1) operations per agent per state,
because it sums over every joint action of the other agents. When the stage game is
count-symmetric -- payoffs and transitions depend on the other agents only through
how many chose each action, not which ones -- the count vector is a sufficient
statistic and the same expectation is a Poisson-binomial average costing O(N) terms.
Agents are NOT required to share a policy; the Poisson-binomial dynamic program
handles fully heterogeneous policies exactly, so symmetry-broken states remain
reachable.

Two code paths compute the same quantity:
    dense=False -- the reduction, O(N^3 Z) per iteration
    dense=True  -- brute force over all M^(N-1) joint actions, O(N M^N Z)
`validate_reduction` asserts they agree to machine precision. That assertion is the
evidence for the complexity claim; without it this module proves nothing.

Variant: the policy-evaluation ("expected SARSA") form of the strategy-average TD
error is the default. The Q-learning form of Barfuss (2022, Eq. 4) is available via
variant="q". The choice is reported with every result, per the requirement that the
recording convention be stated explicitly.
"""

from __future__ import annotations
import itertools
import numpy as np

COOPERATE, DEFECT = 0, 1


# --------------------------------------------------------------------------
# Environment
# --------------------------------------------------------------------------

class EcologicalDilemma:
    """Two-state public-goods dilemma with resource collapse and recovery, played on
    an interaction graph.

    States: 0 = prosperous, 1 = degraded.
    Actions: 0 = cooperate (contribute 1), 1 = defect (contribute 0).

    Agent i's PAYOFF depends on its own local group -- itself plus its graph
    neighbours -- through the fraction of that group which cooperated:

        payoff_i = r_s * g(local cooperating fraction) - cost * [a_i = cooperate]

    The environment STATE is a shared resource, so it responds to the global
    cooperation count k across all N agents:

        prosperous -> prosperous   with probability  g(k / N)
        degraded   -> prosperous   with probability  recovery * g(k / N)

    `graph="complete"` makes the local group the whole population and recovers the
    fully connected dilemma. `graph="ring"` gives every agent a fixed degree, so the
    local group size does not grow with N -- which is the structural condition the
    convergence results of Hussain et al. (2023) require, and the case the companion
    note names as the one its testbed does not cover.

    `g` is linear (identity on the fraction) or a smooth threshold at cooperation
    fraction `threshold` with the given steepness. A linear public good gives the
    stage game a dominant action; the threshold is what admits several equilibria.

    Ergodic with no absorbing state whenever recovery > 0 and policies are interior,
    which is the condition CRLD requires (Barfuss et al. 2019).
    """

    n_states = 2

    def __init__(self, n_agents: int, r_prosperous: float = 3.0,
                 degraded_factor: float = 0.2, recovery: float = 0.5,
                 cost: float = 1.0, threshold: float | None = None,
                 steepness: float = 20.0, graph: str = "complete", degree: int = 2):
        if not 1.0 < r_prosperous:
            raise ValueError(f"need r > 1 for a dilemma; got r={r_prosperous}")
        if graph == "complete" and not r_prosperous < n_agents:
            raise ValueError(
                f"complete graph needs r < N; got r={r_prosperous}, N={n_agents}")
        self.N = n_agents
        self.r = np.array([r_prosperous, r_prosperous * degraded_factor])
        self.recovery = recovery
        self.cost = cost
        self.threshold = threshold
        self.steepness = steepness
        self.graph = graph
        self.degree = n_agents - 1 if graph == "complete" else degree
        if graph == "complete":
            self.neighbours = [np.array([j for j in range(n_agents) if j != i])
                               for i in range(n_agents)]
        elif graph == "ring":
            if degree % 2 or degree >= n_agents:
                raise ValueError("ring degree must be even and < N")
            half = degree // 2
            self.neighbours = [np.array([(i + d) % n_agents
                                         for d in list(range(-half, 0)) + list(range(1, half + 1))])
                               for i in range(n_agents)]
        else:
            raise ValueError(f"unknown graph {graph!r}")
        if self.graph == "complete" and self.degree != n_agents - 1:
            raise AssertionError("complete graph degree mismatch")
        self.group_size = self.degree + 1
        self.params = dict(r_prosperous=r_prosperous, degraded_factor=degraded_factor,
                           recovery=recovery, cost=cost, threshold=threshold,
                           steepness=steepness, graph=graph, degree=self.degree)
        self._build()

    def _production(self, frac):
        """Fraction of the public good produced at a given cooperating fraction."""
        if self.threshold is None:
            return frac
        return 1.0 / (1.0 + np.exp(-self.steepness * (frac - self.threshold)))

    def _build(self) -> None:
        N, m = self.N, self.group_size
        # local payoff table, indexed [state, own action, cooperators in local group]
        kl = np.arange(m + 1)
        gl = self._production(kl / m)
        self.reward = np.empty((2, 2, m + 1))
        for s in range(2):
            public = self.r[s] * gl
            self.reward[s, COOPERATE] = public - self.cost
            self.reward[s, DEFECT] = public
        # global transition table, indexed [state, global cooperators, next state]
        kg = np.arange(N + 1)
        gg = self._production(kg / N)
        self.transition = np.empty((2, N + 1, 2))
        self.transition[0, :, 0] = gg
        self.transition[0, :, 1] = 1.0 - gg
        self.transition[1, :, 0] = self.recovery * gg
        self.transition[1, :, 1] = 1.0 - self.recovery * gg

    def reward_given_neighbours(self, s, a_i, n_nbr):
        """Payoff when n_nbr of agent i's neighbours cooperate."""
        return self.reward[s, a_i, n_nbr + (1 if a_i == COOPERATE else 0)]

    def transition_given_others(self, s, a_i, n_others):
        """Transition row given agent i's action and the count among all others."""
        return self.transition[s, n_others + (1 if a_i == COOPERATE else 0), :]


# --------------------------------------------------------------------------
# Poisson-binomial machinery -- this is where the M^(N-1) sum is avoided
# --------------------------------------------------------------------------

def poisson_binomial_pmf(p: np.ndarray) -> np.ndarray:
    """PMF of the number of successes among independent Bernoulli(p_j). O(n^2)."""
    pmf = np.zeros(len(p) + 1)
    pmf[0] = 1.0
    for j, pj in enumerate(p):
        pmf[1:j + 2] = pmf[1:j + 2] * (1.0 - pj) + pmf[0:j + 1] * pj
        pmf[0] *= (1.0 - pj)
    return pmf


def leave_one_out_pmfs(p: np.ndarray) -> np.ndarray:
    """For each j, the PMF of successes among all trials except j. Shape (n, n).

    Prefix/suffix convolution. Dividing the full PMF by (1-p_j + p_j x) would be
    cheaper and is numerically unstable as p_j approaches 0 or 1.
    """
    n = len(p)
    if n == 1:
        return np.ones((1, 1))
    prefix = [np.array([1.0])]
    for j in range(n - 1):
        prefix.append(np.convolve(prefix[-1], [1.0 - p[j], p[j]]))
    suffix = [np.array([1.0])]
    for j in range(n - 1, 0, -1):
        suffix.append(np.convolve(suffix[-1], [1.0 - p[j], p[j]]))
    suffix.reverse()
    out = np.empty((n, n))
    for j in range(n):
        out[j] = np.convolve(prefix[j], suffix[j])
    return out


# --------------------------------------------------------------------------
# Strategy-average quantities
# --------------------------------------------------------------------------

def _averages_counts(X, env):
    """Strategy averages via count sufficiency.

    Rewards need the Poisson-binomial over agent i's NEIGHBOURS only -- O(deg^2) --
    while the shared-resource transition needs the leave-one-out over all other
    agents -- O(N^2). On a bounded-degree graph the reward term stops growing with N.
    """
    N, Z, M = X.shape
    R_bar = np.empty((N, Z, M))
    T_bar_i = np.empty((N, Z, M, Z))
    T_bar = np.empty((Z, Z))
    n_others = np.arange(N)
    n_nbr = np.arange(env.degree + 1)
    for s in range(Z):
        p_coop = X[:, s, COOPERATE]
        loo = leave_one_out_pmfs(p_coop)                 # over all others (N, N)
        full = poisson_binomial_pmf(p_coop)
        T_bar[s] = full @ env.transition[s]
        if env.graph == "complete":
            nbr_pmf = loo                                 # neighbours are all others
        else:
            nbr_pmf = np.empty((N, env.degree + 1))
            for i in range(N):
                nbr_pmf[i] = poisson_binomial_pmf(p_coop[env.neighbours[i]])
        for a in range(M):
            R_bar[:, s, a] = nbr_pmf @ env.reward_given_neighbours(s, a, n_nbr)
            T_bar_i[:, s, a, :] = loo @ env.transition_given_others(s, a, n_others)
    return R_bar, T_bar_i, T_bar


def _averages_dense(X, env):
    """Same quantities by explicit enumeration of all M^(N-1) joint actions."""
    N, Z, M = X.shape
    R_bar = np.zeros((N, Z, M))
    T_bar_i = np.zeros((N, Z, M, Z))
    T_bar = np.zeros((Z, Z))
    for s in range(Z):
        for i in range(N):
            others = [j for j in range(N) if j != i]
            nbr = set(int(j) for j in env.neighbours[i])
            for combo in itertools.product(range(M), repeat=N - 1):
                prob = 1.0
                for j, a_j in zip(others, combo):
                    prob *= X[j, s, a_j]
                if prob == 0.0:
                    continue
                n_oth = sum(1 for a_j in combo if a_j == COOPERATE)
                n_nb = sum(1 for j, a_j in zip(others, combo)
                           if a_j == COOPERATE and j in nbr)
                for a in range(M):
                    coop = 1 if a == COOPERATE else 0
                    R_bar[i, s, a] += prob * env.reward[s, a, n_nb + coop]
                    T_bar_i[i, s, a, :] += prob * env.transition[s, n_oth + coop, :]
        for combo in itertools.product(range(M), repeat=N):
            prob = 1.0
            for j, a_j in enumerate(combo):
                prob *= X[j, s, a_j]
            if prob == 0.0:
                continue
            k = sum(1 for a_j in combo if a_j == COOPERATE)
            T_bar[s] += prob * env.transition[s, k, :]
    return R_bar, T_bar_i, T_bar


# --------------------------------------------------------------------------
# The CRLD map
# --------------------------------------------------------------------------

def _td_error(X, R_bar, T_bar_i, T_bar, gamma, beta, variant):
    Z = X.shape[1]
    inv = np.linalg.inv(np.eye(Z) - gamma * T_bar)
    R_state = np.einsum('isa,isa->is', X, R_bar)
    V = (1.0 - gamma) * (R_state @ inv.T)
    if variant == "value":
        nxt = V
    elif variant == "q":
        Q = (1.0 - gamma) * R_bar + gamma * np.einsum('isab,ib->isa', T_bar_i, V)
        for _ in range(500):
            Q_new = (1.0 - gamma) * R_bar + gamma * np.einsum(
                'isab,ib->isa', T_bar_i, Q.max(axis=2))
            if np.max(np.abs(Q_new - Q)) < 1e-14:
                Q = Q_new
                break
            Q = Q_new
        nxt = Q.max(axis=2)
    else:
        raise ValueError(f"unknown variant {variant!r}")
    delta = (1.0 - gamma) * R_bar + gamma * np.einsum('isab,ib->isa', T_bar_i, nxt)
    return delta - np.log(X) / beta


def step(X, env, alpha=0.05, beta=25.0, gamma=0.9, variant="value", dense=False):
    """One iteration of the CRLD map, Barfuss et al. (2019) Eq. (2)."""
    avg = _averages_dense(X, env) if dense else _averages_counts(X, env)
    delta = _td_error(X, *avg, gamma=gamma, beta=beta, variant=variant)
    num = X * np.exp(alpha * beta * (delta - delta.max(axis=2, keepdims=True)))
    return num / num.sum(axis=2, keepdims=True)


def random_policies(N, Z=2, M=2, rng=None, eps=1e-3):
    rng = np.random.default_rng() if rng is None else rng
    X = rng.dirichlet(np.ones(M), size=(N, Z))
    X = np.clip(X, eps, 1 - eps)
    return X / X.sum(axis=2, keepdims=True)


def trajectory(X0, env, n_steps, burn_in=0, **kw):
    """Iterate the map; returns post-burn-in trajectory of shape (T, N, Z, M)."""
    X = X0.copy()
    out = []
    for t in range(n_steps):
        X = step(X, env, **kw)
        if t >= burn_in:
            out.append(X.copy())
    return np.asarray(out)


# --------------------------------------------------------------------------
# Validation
# --------------------------------------------------------------------------

def validate_reduction(n_agents=(2, 3, 4, 5, 6), n_trials=3, seed=0, tol=1e-12,
                       variant="value", graph="complete", degree=2, **env_kw):
    """Assert the count reduction equals brute-force enumeration to machine precision.

    This is the load-bearing test for the complexity claim. It is run for every graph
    family used, because the reduction is a different computation on each.
    """
    rng = np.random.default_rng(seed)
    worst, records = 0.0, []
    for N in n_agents:
        if graph == "ring" and (degree >= N or degree % 2):
            continue
        kw = dict(env_kw)
        kw.setdefault("r_prosperous", min(3.0, N - 0.5) if graph == "complete" else 3.0)
        env = EcologicalDilemma(N, graph=graph, degree=degree, **kw)
        for _ in range(n_trials):
            X = random_policies(N, rng=rng)
            a = step(X, env, variant=variant, dense=False)
            b = step(X, env, variant=variant, dense=True)
            err = float(np.max(np.abs(a - b)))
            worst = max(worst, err)
            records.append((N, err))
            assert err < tol, f"reduction mismatch at N={N}, graph={graph}: {err:.3e}"
    return {"max_abs_error": worst, "records": records, "variant": variant,
            "graph": graph, "degree": degree}

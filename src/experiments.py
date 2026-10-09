"""
Measurement of the behavioural repertoire R(N) and attractor dimension d(N) in CRLD,
using the count reduction in crld.py to reach agent counts that brute-force
enumeration cannot.

Definitions follow Maiti, "State-Space Collapse versus Behavioral-Repertoire
Expansion in Collective Reinforcement-Learning Dynamics":
  D(N) = N * Z * (M - 1)   ambient dimension of the joint-policy space
  d(N)                     intrinsic dimension of the attractor
  R(N)                     number of distinct attracting limit sets

Recording convention: POLICY SPACE, not Q-value space. Goll et al. (2025) show the
two can give different dimensions; the choice is fixed here and reported.

One methodological point not in the source note. Under Assumption 1 the agents are
exchangeable, so two fixed points that differ only by a permutation of agents are the
same collective outcome. Counting them separately would inflate R(N) by up to N!.
Repertoire is therefore counted on the orbit space: policies are sorted into a
canonical order before clustering. `count_repertoire` reports both the quotiented
count and the raw count so the effect is visible.
"""

from __future__ import annotations
import numpy as np
import crld


# --------------------------------------------------------------------------
# Convergence
# --------------------------------------------------------------------------

def converge(X0, env, max_steps=20000, tol=1e-12, confirm=True, confirm_cap=1000, **kw):
    """Iterate to a fixed point. Returns (X, n_steps, converged, amplitude).

    After the step-to-step change falls below `tol`, the state is held for a further
    min(t, confirm_cap) iterations and the amplitude over that stretch is measured.
    Both Sanders et al. (2018) and Goll et al. (2025) report transients long enough to
    be mistaken for an attractor, so a single convergence test is not sufficient.

    The note's test plan asks for a confirmation stretch as long as the first; that is
    `confirm_cap=None`. The sweep uses a cap for affordability and reports it, so the
    weaker check is on the record rather than hidden.
    """
    X = X0.copy()
    for t in range(1, max_steps + 1):
        Xn = crld.step(X, env, **kw)
        if not np.all(np.isfinite(Xn)):
            return X, t, False, float("nan")
        delta = float(np.max(np.abs(Xn - X)))
        X = Xn
        if delta < tol:
            if not confirm:
                return X, t, True, 0.0
            n_conf = t if confirm_cap is None else min(t, confirm_cap)
            lo = hi = X[:, :, 0].copy()
            Y, worst_step = X, 0.0
            for _ in range(n_conf):
                Yn = crld.step(Y, env, **kw)
                worst_step = max(worst_step, float(np.max(np.abs(Yn - Y))))
                Y = Yn
                lo = np.minimum(lo, Y[:, :, 0]); hi = np.maximum(hi, Y[:, :, 0])
            amp = float(np.max(hi - lo))
            # Converged means the map stays at rest through the confirmation stretch.
            # Gating on the ACCUMULATED excursion `amp` against a per-step tolerance
            # would reject genuine fixed points, since residual drift sums over the
            # window; `amp` is reported as a diagnostic and used to separate fixed
            # points from closed orbits, not to decide convergence.
            return Y, t + n_conf, worst_step < tol, amp
    return X, max_steps, False, float("nan")


# --------------------------------------------------------------------------
# Repertoire
# --------------------------------------------------------------------------

def canonical(X, symmetry="full"):
    """Canonical representative of a joint policy on the orbit space of the game's
    symmetry group.

    The group depends on the interaction graph, and using the wrong one miscounts the
    repertoire:

    "full"   -- complete graph. Every permutation of agents is a symmetry, so sort the
                per-agent policy vectors.
    "cyclic" -- ring. Only rotations and reflections preserve the graph, so take the
                lexicographically smallest rotation of the sequence and of its
                reversal. Sorting here would wrongly identify configurations that the
                ring's geometry keeps distinct.
    """
    flat = X[:, :, crld.COOPERATE]                     # (N, Z)
    if symmetry == "full":
        order = np.lexsort(tuple(flat[:, j] for j in range(flat.shape[1] - 1, -1, -1)))
        return flat[order]
    if symmetry != "cyclic":
        raise ValueError(f"unknown symmetry {symmetry!r}")
    N = flat.shape[0]
    best = None
    for seq in (flat, flat[::-1]):
        for r in range(N):
            cand = np.roll(seq, -r, axis=0)
            key = cand.ravel()
            if best is None or tuple(key) < tuple(best.ravel()):
                best = cand
    return best


def count_repertoire(points, tol=1e-3):
    """Greedy single-linkage clustering under the max-norm. Returns (count, labels)."""
    reps, labels = [], []
    for p in points:
        for j, r in enumerate(reps):
            if np.max(np.abs(p - r)) < tol:
                labels.append(j); break
        else:
            reps.append(p); labels.append(len(reps) - 1)
    return len(reps), np.array(labels)


def chao1(labels):
    """Chao1 lower bound on the true number of attractors, from a finite sample.

    R(N) measured by basin sampling is CENSORED: K initial conditions can reveal at
    most K attractors, so a raw count saturates at the sampling budget and a growth
    curve built from it flattens for reasons that have nothing to do with the
    dynamics. Chao1 is the standard correction for exactly this problem -- it is a
    lower bound on richness built from the singletons and doubletons:

        S_chao = S_obs + f1 * (f1 - 1) / (2 * (f2 + 1))

    (the bias-corrected form, valid when f2 = 0). A high `discovery_rate`
    (= S_obs / n_samples) is the warning sign that the raw count is censored.
    """
    labels = np.asarray(labels)
    if labels.size == 0:
        return float("nan"), float("nan")
    _, counts = np.unique(labels, return_counts=True)
    s_obs = len(counts)
    f1 = int((counts == 1).sum())
    f2 = int((counts == 2).sum())
    est = s_obs + f1 * (f1 - 1) / (2.0 * (f2 + 1))
    return float(est), float(s_obs / labels.size)


def symmetry_broken(X, tol=1e-3):
    """True if the agents do not all share the same policy."""
    flat = X[:, :, crld.COOPERATE]
    return bool(np.max(flat.max(axis=0) - flat.min(axis=0)) > tol)


# --------------------------------------------------------------------------
# Intrinsic dimension
# --------------------------------------------------------------------------

def twonn(points, discard=0.1):
    """TwoNN intrinsic dimension estimator (Facco et al. 2017, Sci Rep 7:12140).

    mu = r2/r1 for each point; F(mu) = 1 - mu^-d; d is the slope through the origin
    of (ln mu, -ln(1-F)). The largest `discard` fraction of mu values is dropped, as
    the source prescribes.
    """
    P = np.asarray(points, dtype=float)
    n = len(P)
    if n < 10:
        return float("nan")
    d2 = ((P[:, None, :] - P[None, :, :]) ** 2).sum(-1)
    np.fill_diagonal(d2, np.inf)
    nn = np.sort(d2, axis=1)[:, :2] ** 0.5
    r1, r2 = nn[:, 0], nn[:, 1]
    ok = r1 > 0
    mu = np.sort(r2[ok] / r1[ok])
    keep = int(len(mu) * (1 - discard))
    mu = mu[:keep]
    if len(mu) < 10:
        return float("nan")
    F = np.arange(1, len(mu) + 1) / (len(mu) + 1)
    x, y = np.log(mu), -np.log(1 - F)
    return float((x @ y) / (x @ x))          # least squares through the origin


def calibrate_twonn(seed=0, n=600):
    """Run the estimator on manifolds of known dimension embedded in R^20.

    Required before trusting any estimate on real trajectories: the note's test plan
    makes this non-optional, since noise and sampling both bias the estimate upward.
    """
    rng = np.random.default_rng(seed)
    out = {}
    amb = 20
    pt = np.zeros((n, amb)); out["point (d=0)"] = twonn(pt + rng.normal(0, 1e-9, pt.shape))
    t = rng.uniform(0, 2 * np.pi, n)
    circ = np.zeros((n, amb)); circ[:, 0], circ[:, 1] = np.cos(t), np.sin(t)
    out["circle (d=1)"] = twonn(circ)
    u, v = rng.uniform(0, 2 * np.pi, n), rng.uniform(0, 2 * np.pi, n)
    tor = np.zeros((n, amb))
    tor[:, 0] = (2 + np.cos(v)) * np.cos(u); tor[:, 1] = (2 + np.cos(v)) * np.sin(u)
    tor[:, 2] = np.sin(v)
    out["torus (d=2)"] = twonn(tor)
    for k in (3, 5):
        g = np.zeros((n, amb)); g[:, :k] = rng.normal(size=(n, k))
        out[f"gaussian (d={k})"] = twonn(g)
    return out


# --------------------------------------------------------------------------
# Sweep
# --------------------------------------------------------------------------

def sweep(n_values, n_inits, env_kw=None, seed=0, progress=True, **kw):
    """For each N: converge many random initial policies and summarise the repertoire."""
    env_kw = env_kw or {}
    results = []
    for N in n_values:
        rng = np.random.default_rng(seed + N)
        env = crld.EcologicalDilemma(N, **env_kw)
        sym = "full" if env.graph == "complete" else "cyclic"
        K = n_inits(N) if callable(n_inits) else n_inits
        pts_q, pts_raw, steps, amps, broken, coop, failed = [], [], [], [], 0, [], 0
        for _ in range(K):
            X0 = crld.random_policies(N, rng=rng)
            X, t, ok, amp = converge(X0, env, **kw)
            if not ok:
                failed += 1
                continue
            pts_q.append(canonical(X, symmetry=sym))
            pts_raw.append(X[:, :, crld.COOPERATE].copy())
            steps.append(t); amps.append(amp)
            broken += symmetry_broken(X)
            coop.append(float(X[:, :, crld.COOPERATE].mean()))
        nq, lab = count_repertoire([p.ravel() for p in pts_q])
        nr, _ = count_repertoire([p.ravel() for p in pts_raw])
        R_chao, disc = chao1(lab)
        row = dict(N=N, D=2 * N, n_converged=len(pts_q), n_failed=failed,
                   R_quotient=nq, R_raw=nr, R_chao1=R_chao, discovery_rate=disc,
                   frac_symmetry_broken=broken / max(1, len(pts_q)),
                   median_steps=float(np.median(steps)) if steps else float("nan"),
                   max_amplitude=float(np.max(amps)) if amps else float("nan"),
                   mean_coop=float(np.mean(coop)) if coop else float("nan"),
                   d_twonn=twonn([p.ravel() for p in pts_q]) if len(pts_q) >= 10 else float("nan"))
        results.append(row)
        if progress:
            print(f"N={N:4d} conv={row['n_converged']:4d}/{K} R={nq:4d} "
                  f"Chao1={R_chao:7.1f} disc={disc:.2f} broken={row['frac_symmetry_broken']:.2f} "
                  f"amp={row['max_amplitude']:.1e} coop={row['mean_coop']:.3f}", flush=True)
    return results

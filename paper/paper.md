# Attractor count in collective reinforcement-learning dynamics depends on interaction structure, not on population size

**Aditya Maiti**
Independent research, New Delhi, India.
ORCID [0009-0004-2501-1459](https://orcid.org/0009-0004-2501-1459)

October 2026. Technical report.

---

## Abstract

Collective Reinforcement-Learning Dynamics describes many agents learning at the same time as a deterministic map on the space of joint policies. Studying it at large agent counts is held to be hard, because evaluating the map appears to cost a sum over every joint action of the other agents. This report makes three points.

First, that cost is avoidable in the setting the framework is usually studied in. When payoffs depend on the other agents only through how many chose each action, the action counts are a sufficient statistic. The required expectation is then a Poisson-binomial average over a number of terms linear in the agent count. Agents do not have to share a policy for this to hold. A reference implementation that enumerates all joint actions agrees with the reduced one to machine precision, and a deliberately broken reduction fails the same test. One hundred agents become routine. Two hundred agents take thirteen milliseconds per iteration.

Second, with that cost removed, two standing conjectures about how the dynamics scale were tested. The attractor dimension conjecture holds, but only in a trivial way. Every attractor found was a fixed point, at every agent count, on every interaction structure, under both learning rules tested. The intrinsic dimension is therefore zero, and the conjecture is true by arithmetic rather than by discovery.

Third, the conjecture that the number of distinct stable outcomes grows with the agent count is false under all-to-all coupling and true under sparse coupling. In a fully connected threshold public-goods dilemma, the number of attractors falls to one by twenty agents and cooperation collapses to 0.0025. A ring of degree two uses the same environment, the same learning rule and the same parameters. There the attractor count grows. Cooperation stays near 0.32 up to one hundred agents. A ring of degree four lies between the two. The controlling quantity is the expected benefit of cooperating. It falls as one over the agent count when each payoff depends on every other agent. It stays constant when it depends on a bounded neighbourhood.

---

## 1. Introduction

When several agents learn at once, each one adapts to a target the others keep moving. Barfuss, Donges and Kurths [1] showed that the average behaviour of such a system has a deterministic limit. Policies are held fixed for a batch of interactions, updated on the batch average, and the batch size is sent to infinity. What remains is a deterministic map on the space of joint policies. Barfuss [2] developed the framework further and connected it to replicator dynamics.

The map is well understood for two agents. It is much less understood for many. Barfuss et al. [3] name large collectives as an open problem and attribute the difficulty to a joint state-action space that grows exponentially.

Two quantities describe how such a system scales. The first is the dimension of the space the joint policy lives in. For `N` agents, `Z` states and `M` actions this is `D(N) = N Z (M - 1)`, which grows linearly. The second is the intrinsic dimension of the attractor the dynamics settle onto, written `d(N)`. Nothing forces the second to track the first. A third quantity is the number of distinct stable outcomes the system can reach, written `R(N)`.

A companion note [4] states two conjectures about these quantities. Collapse says that `d(N)/D(N)` tends to zero. Expansion says that `R(N)` keeps growing. The note states both as conjectures, specifies a test, and does not run it. The stated reason is the cost of evaluating the map.

This report runs the test. Section 3 shows the cost is not what it appears to be. Sections 5 and 6 report what the measurements found.

## 2. The dynamics

A stochastic game has `N` agents, `Z` environment states, and `M` actions per agent per state. Each agent follows a memoryless policy `X_i(s, a)`, the probability of taking action `a` in state `s`. The joint policy factorises across agents.

Agents learn by temporal-difference updates with a Boltzmann policy of intensity `beta`, learning rate `alpha` and discount factor `gamma`. In the deterministic limit the policy update is

    X_i(s, a) <- X_i(s, a) exp[alpha beta delta_i(s, a)] / sum_b X_i(s, b) exp[alpha beta delta_i(s, b)]

where `delta_i` is the strategy-average temporal-difference error [1, 2]. Two forms of that error are used here. The policy-evaluation form is the default. The Q-learning form of Barfuss [2] is used as a robustness check.

Computing `delta_i` requires the expected reward and the expected transition, averaged over what every other agent might do. Written directly, that average sums over `M^(N-1)` joint actions for each agent in each state. This is the term that makes large `N` look out of reach.

## 3. The cost is avoidable

### 3.1 The observation

Consider a game in which each agent's payoff and the state transition depend on the other agents only through how many of them chose each action, not through which ones did. Games with this property are called anonymous games and have been studied for a long time. Blonski [5] characterised the binary-action case. Daskalakis and Papadimitriou [6, 7] used the same property to compute approximate equilibria in time polynomial in the number of players. In the evolutionary setting the matching idea is a population game, where payoffs depend on the distribution of actions across the population [8].

Symmetric social dilemmas are anonymous games. The reward in a public-goods game depends on the number of contributors. The transition of a shared resource depends on the total level of cooperation. This is also the setting in which Collective Reinforcement-Learning Dynamics has mostly been studied.

For an anonymous game the sum over joint actions collapses. Let `p_j` be the probability that agent `j` cooperates in the current state. The number of cooperators among the agents other than `i` follows a Poisson-binomial distribution with parameters `{p_j : j != i}`. The expected reward for agent `i` is a sum over counts rather than over joint actions:

    Rbar_i(s, a) = sum over n of P_i(n) R(s, a, n)

Here `P_i` is that Poisson-binomial distribution and `n` runs from zero to `N - 1`.

Two things matter. The distribution is computed by a standard dynamic program in time quadratic in the number of agents. And the agents are not required to share a policy. The dynamic program takes each agent's own probability as input, so fully heterogeneous policies are handled exactly. Symmetry-broken states stay reachable. This separates the reduction from mean-field methods such as Yang et al. [9], which replace the population by an average agent and are approximate.

For each agent the leave-one-out distribution is obtained by prefix and suffix convolution. Dividing the full-population distribution by one agent's factor would be faster and is numerically unstable when a probability approaches zero or one. The whole update costs `O(N^3 Z)` operations. This is polynomial, not exponential.

For more than two actions the counts form a vector and the number of terms is `O(N^(M-1))`, still polynomial in `N` for a fixed action set.

### 3.2 This is an observation, not a new method

Count sufficiency in anonymous games is established [5, 6, 7]. The Poisson-binomial dynamic program is standard. What this report adds is the application to the deterministic-limit map of Collective Reinforcement-Learning Dynamics. Doing so removes the specific barrier named as open in [3], for the class of games the framework is studied in. The barrier is real for general stochastic games. It does not bind here.

### 3.3 Verification

Correctness is asserted, not assumed. Two code paths compute the same quantity. One uses the reduction. The other enumerates every joint action of the other agents and is used for nothing else. A test compares them on random heterogeneous policies.

| interaction graph | learning rule | largest absolute difference |
|---|---|---|
| complete | policy evaluation | 2.2e-16 |
| complete | Q-learning | 2.8e-16 |
| ring, degree 2 | policy evaluation | 2.2e-16 |
| ring, degree 2 | Q-learning | 2.2e-16 |
| ring, degree 4 | policy evaluation | 2.2e-16 |
| ring, degree 4 | Q-learning | 2.2e-16 |

Agreement is at machine precision in all six cases.

A test that cannot fail proves nothing. A negative control replaces the leave-one-out distribution with the full-population one. This is a plausible shortcut and it is wrong. The same test rejects it, with a mismatch of 7.4e-3.

### 3.4 Measured cost

| agents | enumeration | reduction | ratio |
|---|---|---|---|
| 8 | 38.6 ms | 0.74 ms | 52 |
| 12 | 1051 ms | 0.89 ms | 1185 |
| 16 | 22304 ms | 0.96 ms | 23250 |
| 50 | not run, 5.6e14 terms per agent per state | 2.7 ms | |
| 200 | not run, 8.0e59 terms per agent per state | 12.7 ms | |

## 4. The environment

The stage game is a two-state public-goods dilemma with resource collapse and recovery. The states are prosperous and degraded. Each agent either contributes one unit or contributes nothing.

Each agent's payoff depends on its local group, meaning itself and its neighbours on an interaction graph. If a fraction `f` of the local group contributes, every member of that group receives `r_s g(f)`, and contributors pay a cost of one. The multiplier `r_s` is lower in the degraded state. The shared resource responds to the global level of cooperation. The probability of being prosperous next step is `g(k/N)` from the prosperous state and `recovery * g(k/N)` from the degraded one, where `k` is the total number of contributors.

The production function `g` is either the identity, giving a linear public good, or a smooth threshold at a cooperation fraction. A linear public good gives the stage game a dominant action and therefore a single equilibrium. The threshold is what allows several.

A complete graph makes the local group the whole population. A ring of fixed degree keeps the local group the same size however many agents there are.

Parameters are held fixed as the agent count varies, which is what the conjectures require. Throughout, `r = 3`, the degraded multiplier is 0.2, the recovery rate is 0.5, the threshold is at half cooperation, `alpha = 0.05`, `beta = 120` and `gamma = 0.95`. The agent count starts at four, because a dilemma needs `1 < r < N`.

## 5. What was measured and how

Trajectories are recorded in policy space, not in Q-value space. Goll et al. [10] show the two can give different dimensions, so the choice is fixed and stated.

A run is called converged when the largest single-iteration change falls below 1e-12 and the map then stays at rest through a further confirmation stretch. Sanders et al. [11] and Goll et al. [10] both report transients long enough to be mistaken for attractors, so one convergence test is not enough.

Attractors are counted on the orbit space of the symmetry group, and the group depends on the graph. On a complete graph every permutation of agents is a symmetry, so the per-agent policies are sorted. On a ring only rotations and reflections preserve the structure, so the canonical form is the least rotation of the sequence and of its reversal. Using the wrong group inflates the count. Without any quotient, six agents produced eighty-eight raw outcomes where three distinct ones exist.

Counting attractors by sampling starting points has a ceiling. With `K` starting points at most `K` attractors can appear. The discovery rate, meaning distinct attractors divided by converged runs, shows when that ceiling binds. The Chao1 richness estimator is reported where it applies.

Intrinsic dimension was to be estimated with the TwoNN method of Facco et al. [12]. It was calibrated first on manifolds whose dimension is known. At two thousand samples it returns 1.03, 2.17, 3.04, 5.11 and 8.13 for true dimensions one, two, three, five and eight. At six hundred samples it reads forty to fifty per cent high. No estimate below two thousand samples should be quoted.

## 6. Results

### 6.1 A linear public good has one attractor everywhere

Sixteen parameter settings were tested at ten agents, crossing four exploration intensities with four discount factors. All 384 runs converged to the same fully symmetric fixed point. Mean cooperation rises with the discount factor, from 0.000 to 0.456, but the number of attractors is one in every case.

This is expected once stated. A linear public good gives the stage game a dominant action. The remaining results use the threshold form.

### 6.2 Every attractor found is a fixed point

No limit cycle, quasi-periodic orbit or chaotic set was found anywhere in this study. Across every run on every graph the excursion over the confirmation stretch stayed below 1.6e-10. The largest single value was 1.53e-10, on a degree-two ring at fourteen agents.

Some runs did not settle inside the iteration budget. Fifteen such cases were taken from four different configurations and run far past the budget. All fifteen reached fixed points. The largest single-iteration change afterwards was 1.3e-15, a few units in the last place of double precision.

This is a search result, not a proof. Non-convergent runs were sampled rather than enumerated. The correct statement is that no non-point attractor was found, not that none exists. For every attractor the study did reach, the intrinsic dimension is zero.

The collapse conjecture is therefore satisfied, and satisfied trivially. A fixed point has dimension zero in any ambient space. The interesting version of the conjecture, in which an attractor that is not a point occupies a vanishing fraction of the space, has no instance here to test.

Figure 1 collects the four results of this section.

### 6.3 Under all-to-all coupling the repertoire contracts

| agents | 4 | 6 | 8 | 10 | 14 | 20 | 28 | 40 | 56 | 80 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| attractors | 3 | 3 | 4 | 4 | 2 | 1 | 1 | 1 | 1 | 1 | 1 |
| cooperation | 0.712 | 0.559 | 0.449 | 0.364 | 0.150 | 0.0025 | 0.0025 | 0.0025 | 0.0025 | 0.0025 | 0.0025 |

The number of attractors peaks at four and falls to one by twenty agents. Cooperation collapses at the same point and stays collapsed to one hundred agents. The expansion conjecture is false here.

### 6.4 Under sparse coupling the repertoire grows

The same environment on a ring of degree two, with identical parameters:

| agents | 6 | 8 | 10 | 14 | 20 | 28 | 40 | 56 | 80 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|
| attractors observed | 3 | 4 | 8 | 9 | 14 | 32 | 44 | 39 | 33 | 24 |
| converged runs | 46 | 120 | 120 | 103 | 120 | 69 | 50 | 39 | 33 | 24 |
| discovery rate | 0.07 | 0.03 | 0.07 | 0.09 | 0.12 | 0.46 | 0.88 | 1.00 | 1.00 | 1.00 |
| cooperation | 0.658 | 0.630 | 0.606 | 0.551 | 0.357 | 0.345 | 0.335 | 0.328 | 0.322 | 0.319 |

Every attractor on the ring is symmetry-broken. Cooperation does not collapse. At one hundred agents it is 0.319 on the ring against 0.0025 on the complete graph.

The attractor counts must be read with care above twenty-eight agents. The discovery rate reaches one, meaning every converged run found an outcome no other run found. From forty agents the observed count equals the number of converged runs almost exactly. The apparent fall from forty-four to twenty-four therefore tracks the shrinking sample budget. It says nothing about the dynamics. Chao1 gives lower bounds of 144 at forty agents and several hundred beyond. With no repeated outcomes these are extrapolations. They mean only that the true count is far larger than observed.

The defensible statement is this. The attractor count grows. It is measured reliably to twenty agents, where it rises from three to fourteen. At twenty-eight agents it is at least thirty-two. Beyond that it exceeds what this sampling budget can count. No growth law is fitted.

### 6.5 Degree four lies between

At ten agents a degree-four ring has five attractors, against eight for degree two and four for the complete graph. At forty agents it has at least thirty-two, with cooperation at 0.33538 against 0.33540 for degree two. The effect is graded by neighbourhood size rather than switched on by sparsity.

One degree-four point is excluded. At twenty agents only seven of seventy runs converged inside the budget, which is too few to count attractors from. Five of those non-convergent runs are among the fifteen diagnosed in section 6.2, and all five are slow transients.

### 6.6 The mechanism

The expected benefit of cooperating is the multiplier times the expected increase in the public good caused by one agent switching to cooperate. For a threshold fixed in the cooperating fraction, that increase is about the steepness divided by four times the local group size. The benefit therefore falls as one over the local group size, against a cost that does not change.

| coupling | benefit of cooperating |
|---|---|
| all-to-all, 4 agents | 1.115 |
| all-to-all, 100 agents | 0.124 |
| ring of degree 2, any agent count | 1.448 |
| ring of degree 4, any agent count | 1.033 |

The cost is one. Under all-to-all coupling the benefit crosses below the cost as agents are added. On a ring it never does, because the local group never grows. Degree four sits just above the cost, which fits its intermediate position.

Evaluated at a half-cooperating population the crossing occurs near six agents, while the repertoire does not collapse until about fourteen to twenty. The scaling and the direction are right. The crossing point is not, because the attractor is not at half cooperation and several outcomes persist past the naive crossing. The argument explains the collapse. It does not predict its location.

### 6.7 The contrast survives the learning rule

Twenty agents were rerun with the Q-learning form of the temporal-difference error. Forty starting points were used on each graph, and all of them converged. The complete graph gives one attractor and cooperation 0.0025. The degree-two ring gives eleven attractors and cooperation 0.3574.

The qualitative contrast is reproduced. One outcome under all-to-all coupling, many outcomes under sparse coupling, with cooperation collapsed in the first case and sustained in the second.

Cooperation agrees closely but not equally well on the two graphs. On the complete graph the two learning rules give 0.00247488 and 0.00247488, differing by 2e-12. On the ring they give 0.35696 and 0.35744, differing by 5e-4, which is agreement to three decimal places. The ring value is a mean over attractors, and the two rules sampled different numbers of them, so exact agreement is not expected there.

The attractor counts should not be compared directly across the two learning rules, because the sample budgets differ. The policy-evaluation runs used 120 starting points on the ring and found fourteen outcomes, at a discovery rate of 0.12. The Q-learning runs used forty and found eleven, at a discovery rate of 0.28. A smaller sample finding proportionally more new outcomes is the censoring effect described in section 6.4. Eleven against fourteen is therefore neither a match nor a disagreement, and the counts carry no weight here. The robustness claim rests on the qualitative contrast and on the cooperation levels.

## 7. Relation to earlier work

Galla and Farmer [13] found high-dimensional chaotic attractors in two-player games as the number of available moves grows. Sanders et al. [11] found that the stable region shrinks to nothing as the number of players grows, so chaos should become typical in games with many players. Neither effect appeared here. Both studies draw payoffs at random. This environment is structured, symmetric and cooperative, which is the regime where Sanders et al. themselves report many fixed points rather than chaos.

Hussain et al. [14] give a condition for Q-learning in network games to converge to a unique equilibrium. It depends on network structure and is independent of the number of agents. The quantity that controls it is a norm of the interaction matrix. That norm stays at two on a ring however many agents are added, and grows as `N - 1` on a complete graph. The present result is consistent with that and supplies a mechanism in terms of individual incentive.

Amiet et al. [15] and Tachikawa [16] both report that the number of stable outcomes grows with system size. Tachikawa studies a lattice of coupled oscillators, where each unit has bounded degree, which is the case reproduced here. Amiet et al. draw payoffs independently for each player, which also keeps individual incentive from washing out. Neither supports growth under all-to-all coupling, and this report gives a reason.

The dependence of cooperation on group size is itself long established. Olson [17] argued that larger groups supply less of a collective good, because each member's share of the benefit falls while the cost of contributing does not. The mechanism in section 6.6 is that argument measured inside a learning dynamic. The contribution here is not that finding but its consequence for the two scaling conjectures.

## 8. Limits

The result rests on one environment family with two production functions. A payoff that scales with the absolute rather than the fractional level of cooperation would preserve individual incentive as agents are added and could change the outcome.

The ring attractor counts are censored above twenty-eight agents, as section 6.4 states. The growth is established over a shorter range than the contraction it is contrasted with.

Non-convergent runs were sampled, not enumerated. Two hundred and thirty-seven runs failed to settle inside the budget across the whole study. Fifteen of them were diagnosed.

Two learning rules were tested, and the Q-learning check covers one agent count. Trajectories were recorded in policy space only.

No non-trivial attractor dimension was obtained, because no non-point attractor was found. The calibrated estimator is implemented and unused on real trajectories for that reason. A dimension estimate does appear in the saved sweep output. It is computed on converged endpoints, which from twenty agents onward agree with each other to one or two units in the last place of double precision. It therefore measures rounding scatter about a single point rather than an attractor, and it should not be used.

## 9. Reproduction

Code, data and figures are deposited with this report under the same DOI, and are also at https://github.com/ADITYA-WORK-MAITI/crld-interaction-structure. The verification stage runs in about a minute:

    python run_all.py verify

It asserts that the reduction equals enumeration on every graph and both learning rules, asserts that a deliberately broken reduction fails, and checks that the orbit-space quotient follows each graph's symmetry group. Everything else rests on it.

Trial counts are listed per agent count in the runner rather than computed from a formula, because changing one changes the measured attractor count. A traceability document maps every number above to the file that produces it, and states what is not traceable.

Environment: Python 3.13.15 and numpy 2.5.3. Seeds are fixed. The measurement sweeps take several hours on four cores.

## References

[1] W. Barfuss, J. F. Donges, J. Kurths. Deterministic limit of temporal difference reinforcement learning for stochastic games. Physical Review E 99(4):043305, 2019. doi:10.1103/PhysRevE.99.043305

[2] W. Barfuss. Dynamical systems as a level of cognitive analysis of multi-agent learning. Neural Computing and Applications 34(3):1653-1671, 2022. doi:10.1007/s00521-021-06117-0

[3] W. Barfuss et al. Collective cooperative intelligence. PNAS 122(25):e2319948121, 2025. doi:10.1073/pnas.2319948121

[4] A. Maiti. State-space collapse versus behavioral-repertoire expansion in collective reinforcement-learning dynamics. Unpublished note, 2026. Both conjectures are restated in full in section 1 of this report, so the argument here does not depend on access to it.

[5] M. Blonski. Anonymous games with binary actions. Games and Economic Behavior 28(2):171-180, 1999. doi:10.1006/game.1998.0699

[6] C. Daskalakis, C. H. Papadimitriou. Computing equilibria in anonymous games. 48th Annual IEEE Symposium on Foundations of Computer Science, 2007. doi:10.1109/FOCS.2007.24

[7] C. Daskalakis, C. H. Papadimitriou. Approximate Nash equilibria in anonymous games. Journal of Economic Theory 156:207-245, 2015. doi:10.1016/j.jet.2014.02.002

[8] W. H. Sandholm. Population games and deterministic evolutionary dynamics. Handbook of Game Theory with Economic Applications 4:703-778, 2015. doi:10.1016/B978-0-444-53766-9.00013-6

[9] Y. Yang, R. Luo, M. Li, M. Zhou, W. Zhang, J. Wang. Mean field multi-agent reinforcement learning. ICML 2018. arXiv:1802.05438

[10] D. Goll, J. Heitzig, W. Barfuss. Deterministic model of incremental multi-agent Boltzmann Q-learning: transient cooperation, metastability, and oscillations. arXiv:2501.00160, 2025.

[11] J. B. T. Sanders, J. D. Farmer, T. Galla. The prevalence of chaotic dynamics in games with many players. Scientific Reports 8:4902, 2018. doi:10.1038/s41598-018-22013-5

[12] E. Facco, M. d'Errico, A. Rodriguez, A. Laio. Estimating the intrinsic dimension of datasets by a minimal neighborhood information. Scientific Reports 7:12140, 2017. doi:10.1038/s41598-017-11873-y

[13] T. Galla, J. D. Farmer. Complex dynamics in learning complicated games. PNAS 110(4):1232-1236, 2013. doi:10.1073/pnas.1109672110

[14] A. Hussain, D. Leonte, F. Belardinelli, G. Piliouras. Stability of multi-agent learning: convergence in network games with many players. arXiv:2307.13922, 2023.

[15] B. Amiet, A. Collevecchio, M. Scarsini, Z. Zhong. Pure Nash equilibria and best-response dynamics in random games. Mathematics of Operations Research 46(4):1552-1572, 2021. doi:10.1287/moor.2020.1102

[16] M. Tachikawa. Multiplicity of limit cycle attractors in coupled heteroclinic cycles. Progress of Theoretical Physics 109(1):133-138, 2003. doi:10.1143/PTP.109.133

[17] M. Olson. The Logic of Collective Action: Public Goods and the Theory of Groups. Harvard University Press, 1965. doi:10.4159/9780674041660

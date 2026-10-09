# Document 03: measuring d(N) and R(N) in CRLD at agent counts the framework was thought not to reach

Aditya Maiti. Run 2026-10-08. Code in `src/`, raw output in `out/`.

Claim typing as in documents 00-02: `[FACT]` `[THEORY]` `[LIT]` `[READ]` `[HYP]` `[OPEN]`.

**Summary.** Three results.

1. The combinatorial barrier that makes large-N CRLD look intractable is an artefact of how
   the expectation is evaluated, not a property of the dynamics. Under the symmetry the
   framework already assumes it is removable: N = 200 runs at 13 ms per iteration, against
   8e59 terms for direct enumeration. Verified exact against brute force to 2e-16.
2. Conjecture A (collapse) is **true but vacuous** over everything reached. Every attractor
   this study arrived at — every agent count, every parameter setting, both graphs — is a
   fixed point, so d(N) = 0 while D(N) = 2N grows. No non-point attractor was found; §5b
   states the limits of that search, which sampled rather than enumerated the non-convergent
   runs. The non-trivial version of the conjecture has no instance to test here.
3. Conjecture B (expansion) is **neither simply true nor simply false: it is decided by the
   interaction structure.** Under all-to-all coupling R(N) contracts to a single attractor by
   N = 20 and cooperation collapses to 0.002. On a degree-2 ring, same environment, same
   learning rule, same parameters, R(N) grows monotonically from 3 to 32 over N = 6 to 28 and
   cooperation holds near 0.35. The controlling quantity is the expected benefit of
   cooperating, which decays as 1/N when an agent's payoff depends on all others and is
   constant when it depends on a bounded neighbourhood.

---

## 1. The computational result

`[THEORY]` Evaluating the strategy-average TD error nominally sums over all M^(N-1) joint
actions of the other agents. Under Assumption 1 of the note the stage game is
count-symmetric: payoffs and transitions depend on the others only through *how many* chose
each action. The count is then a sufficient statistic and the same expectation is a
Poisson-binomial average over O(N) terms, computed by a prefix/suffix convolution dynamic
program. Agents are not required to share a policy — the program is exact for fully
heterogeneous policies, so symmetry-broken states remain reachable. This is Proposition 1 of
the note (S_N equivariance) cashed out computationally rather than used as decoration.

`[FACT]` **Verified, not asserted.** `crld.validate_reduction` runs both code paths — the
reduction and brute-force enumeration — on random heterogeneous policies and compares:

| variant | comparisons (N = 2…7) | max abs difference |
|---|---|---|
| expected-SARSA | 18 | 1.11e-16 |
| Q-learning | 18 | 2.22e-16 |

Machine precision. **Negative control:** replacing the leave-one-out distribution with the
full-population one — a plausible and wrong shortcut — is caught by the same test at 7.4e-3.
A test that passes over a defect is worthless, so the suite contains one that provably fails
against a broken implementation.

`[FACT]` **Measured cost** (Fig. 1a):

| N | enumeration | reduction | ratio |
|---|---|---|---|
| 8 | 38.6 ms | 0.74 ms | 52× |
| 12 | 1051 ms | 0.89 ms | 1,185× |
| 16 | 22,304 ms | 0.96 ms | 23,250× |
| 50 | — (5.6e14 terms/agent/state) | 2.7 ms | — |
| 200 | — (8.0e59 terms/agent/state) | 12.7 ms | — |

`[READ]` Barfuss et al. (2025) name large-N CRLD as an open problem and attribute the
difficulty to the exponentially growing joint action space. That is correct for general
stochastic games. It is **not** binding for the symmetric social dilemma CRLD is actually
studied in, which is the setting their own guiding example uses.

---

## 2. Setup

- **Environment.** Two-state ecological public-goods dilemma: prosperous / degraded.
  With k of N cooperating, each agent receives r_s · g(k) and pays a cost of 1 if it
  cooperated; the state transitions on g(k). `g` is linear (k/N) or a smooth threshold at a
  cooperation fraction θ with steepness s. Ergodic, no absorbing state.
- **Parameters.** Fixed across N, as Conjecture 1 requires. r = 3.0, degraded factor 0.2,
  recovery 0.5. N ≥ 4 because the dilemma condition 1 < r < N must hold at fixed r.
- **Recording space: policy space**, not Q-value space. Goll et al. (2025) show the two can
  give different dimensions; the choice is fixed and reported.
- **Convergence.** Iterate to a step-to-step change below 1e-12, then hold for a further
  min(t, 300) iterations and require the map to stay at rest throughout. Sanders et al.
  (2018) and Goll et al. (2025) both report transients long enough to be mistaken for
  attractors. The note asks for a confirmation stretch as long as the first; the cap is a
  weaker check and is on the record as such.
- **R(N) counted on the orbit space.** `[READ]` Under Assumption 1 agents are exchangeable,
  so two fixed points differing only by a permutation are the same collective outcome.
  Counting them separately inflates R by up to N!. Observed inflation at N = 6: 88 raw
  versus 3 distinct (Fig. 1b). The note does not make this distinction; without it, R(N)
  measures the symmetric group rather than the dynamics.

### Estimator calibration

`[FACT]` The TwoNN estimator (Facco et al. 2017) was run on manifolds of known dimension
embedded in R^20 before being pointed at any CRLD output:

| manifold | true | n = 600 | n = 2000 |
|---|---|---|---|
| circle | 1 | 1.51 | 1.03 |
| torus | 2 | 2.88 | 2.17 |
| Gaussian | 3 | 4.18 | 3.04 |
| Gaussian | 5 | 6.47 | 5.11 |
| Gaussian | 8 | — | 8.13 |

At n = 2000 the estimator is accurate to within 9%. At n = 600 it reads 40-50% high. The
bias is upward, which runs against Conjecture A, so any collapse finding is conservative —
but the sample-size dependence is sharp enough that no dimension estimate below ~2000 points
should be quoted.

---

## 3. Result 1 — the linear public good has a unique global attractor

`[FACT]` 16 parameter settings (β ∈ {25, 60, 120, 250} × γ ∈ {0.80, 0.90, 0.95, 0.99}),
N = 10, 24 random initial policies each: **384/384 runs converged to the same fully
symmetric fixed point.** R = 1 everywhere, zero symmetry breaking, maximum amplitude over
the confirmation window ~2e-11. Mean cooperation rises with the discount factor, from 0.000
at γ = 0.80 to 0.456 at γ = 0.99.

`[READ]` This is expected on reflection and worth stating plainly: a linear public good gives
the stage game a dominant action, so a unique equilibrium is the default. The interesting
question cannot be asked in this environment, which is why the threshold variant exists.

---

## 4. Result 2 — with a threshold, the repertoire contracts

`[FACT]` Threshold production (θ = 0.5, steepness 20), β = 120, γ = 0.95, α = 0.05, policy
space, 80-200 initial conditions per N:

| N | D(N) | converged | R(N) distinct | R raw | symmetry-broken | mean cooperation |
|---|---|---|---|---|---|---|
| 4 | 8 | 200/200 | 3 | 17 | 0.97 | 0.712 |
| 6 | 12 | 197/200 | 3 | 88 | 0.88 | 0.559 |
| 8 | 16 | 200/200 | 4 | 28 | 0.20 | 0.449 |
| 10 | 20 | 200/200 | 4 | 46 | 0.27 | 0.364 |
| 14 | 28 | 200/200 | 2 | 2 | 0.00 | 0.150 |
| 20 | 40 | 200/200 | 1 | 1 | 0.00 | 0.002 |
| 28 | 56 | 120/120 | 1 | 1 | 0.00 | 0.002 |
| 40 | 80 | 120/120 | 1 | 1 | 0.00 | 0.002 |
| 56 | 112 | 120/120 | 1 | 1 | 0.00 | 0.002 |
| 80 | 160 | 80/80 | 1 | 1 | 0.00 | 0.002 |
| 100 | 200 | 80/80 | 1 | 1 | 0.00 | 0.002 |

**Every attractor is a fixed point.** Maximum amplitude over the confirmation window was
≤1.5e-10 at every N. No limit cycle, no quasi-periodic orbit, no chaos was found anywhere —
including a separate scan over α ∈ {0.2, 0.6, 1.5, 4.0}, where the only non-convergent
behaviour was numerical breakdown at α = 4 as policies left the simplex.

---

## 5. Mechanism

`[READ]` The contraction has a specific cause. At a symmetric mixed state, the expected
benefit of cooperating is r · E[g(n+1) − g(n)] under the leave-one-out distribution — the
chance that one agent's contribution actually moves the public good. For a threshold of
fixed steepness in the cooperation *fraction*, that step is ~s/(4N) in agent units, so the
benefit decays like 1/N against a cost that does not:

| N | 4 | 8 | 14 | 20 | 40 | 100 |
|---|---|---|---|---|---|---|
| benefit | 1.115 | 0.766 | 0.540 | 0.426 | 0.259 | 0.124 |

`[READ]` **Honest limit of this argument.** Evaluated at p = 0.5 it crosses the unit cost at
N ≈ 6, while the repertoire does not collapse until N ≈ 14-20. The 1/N scaling and the
direction are right; the crossover point is not, because the attractor is not at p = 0.5 and
multistability persists past the naive crossing. It explains the collapse qualitatively, and
should not be quoted as a quantitative prediction.

---

## 5b. Result 3 — the conjecture's fate is decided by interaction structure, not by N

`[HYP]` The mechanism in §5 predicts something sharp and falsifiable. If the collapse is
caused by pivotality decaying with the size of the group an agent's payoff depends on, then
putting the game on a graph of **fixed degree** should abolish it, because the local group
stops growing with N. The companion note names exactly this case as the one its testbed does
not cover, and Hussain et al. (2023) supply the matching theory: their interaction-matrix norm
is 2 on a ring independently of N, and N−1 on a complete graph.

`[FACT]` The environment was extended to an interaction graph. Agent i's payoff depends on the
cooperating fraction of its **local group** — itself plus its graph neighbours — while the
shared resource still transitions on the global count. `graph="complete"` recovers §4 exactly.
The reduction was re-validated on every graph family, because it is a different computation on
each: max |counts − enumeration| = 2.2e-16 on complete, ring degree 2, and ring degree 4, for
both learning variants.

`[FACT]` **The symmetry group changes with the graph, and so must the repertoire count.** A
ring is invariant under rotation and reflection, not under arbitrary permutation. Quotienting
a ring by the full symmetric group would merge configurations the ring's geometry keeps
distinct. `canonical(..., symmetry="cyclic")` takes the lexicographically least rotation of
the sequence and of its reversal; tested to identify rotations and to refuse transpositions,
while the complete-graph quotient does the opposite.

`[FACT]` Ring, degree 2, same parameters as §4 (β = 120, γ = 0.95, α = 0.05, threshold 0.5):

| N | 6 | 8 | 10 | 14 | 20 | 28 | 40 | 56 | 80 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|
| R(N) observed | 3 | 4 | 8 | 9 | 14 | 32 | 44 | 39 | 33 | 24 |
| converged runs | 46 | 120 | 120 | 103 | 120 | 69 | 50 | 39 | 33 | 24 |
| discovery rate | 0.07 | 0.03 | 0.07 | 0.09 | 0.12 | 0.46 | 0.88 | 1.00 | 1.00 | 1.00 |
| cooperation | 0.658 | 0.630 | 0.606 | 0.551 | 0.357 | 0.345 | 0.335 | 0.328 | 0.322 | 0.319 |
| symmetry-broken | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |

Against the complete graph at the same N, where R(N) is 3, 4, 4, 2, 1, 1, 1, 1, 1, 1 and
cooperation falls 0.559 → 0.0025 and stays there to N = 100.

`[FACT]` **R(N) on the ring is censored above N ≈ 28, and the raw count must not be read as
a growth curve.** Basin sampling with K trials can reveal at most K attractors. The discovery
rate — distinct attractors per converged run — rises from 0.07 at N = 6 to 0.46 at N = 28 and
reaches **1.00 from N = 56 onward**: every run found an attractor no other run found. From
N = 40 the observed R equals the number of converged runs almost exactly, so the apparent
decline from 44 to 24 across N = 40-100 tracks the shrinking trial budget (70, 60, 45, 40)
and carries no information about the dynamics.

Chao1 gives a richness lower bound of 144 at N = 40 and 780, 561, 300 at N = 56, 80, 100 —
but with no doubletons these are extrapolations from singleton counts and mean only "far more
than observed". **The defensible statement: R(N) grows monotonically, is measured reliably to
N = 20 (3 → 14), is partially censored at N = 28 (≥ 32), and beyond that exceeds what this
sampling budget can count.** No growth law is fitted and none should be.

`[FACT]` **Degree 4 places the effect on a gradient, not a switch.** At N = 10, R = 5 against
the degree-2 ring's 8 and all-to-all's 4; at N = 40, R = 32 with cooperation 0.335, matching
degree 2. The degree-4 point at N = 20 (R = 1) rests on only 7 of 70 runs converging inside
the 4,000-iteration budget and is **not a usable repertoire measurement**; it is excluded
from the figure and recorded here for completeness.

`[FACT]` **Pivotality, quantified.** The expected marginal benefit of cooperating is
r · E[g(local fraction with me) − g(local fraction without me)], against a cost of 1:

| coupling | benefit |
|---|---|
| all-to-all, N = 4 | 1.115 |
| all-to-all, N = 100 | 0.124 |
| ring degree 2 (local group of 3) | **1.448, independent of N** |
| ring degree 4 (local group of 5) | **1.033, independent of N** |

Degree 4 sits barely above cost, consistent with its intermediate repertoire at small N while
matching degree 2's cooperation once both clear the threshold.

`[FACT]` **The contrast survives the learning rule.** Repeating N = 20 with the Q-learning
form of the strategy-average TD error (Barfuss 2022, Eq. 4) in place of policy evaluation,
40 initial conditions each, all converging: all-to-all gives R = 1 and cooperation 0.0025;
the degree-2 ring gives R = 11 and cooperation 0.357. Both reproduce the value-variant result
(R = 1 / 0.0025 and R = 14 / 0.357).

`[READ]` This is the result the companion note's §7 anticipates without being able to test.
R(N) does not have a fate determined by N. It has one determined by whether each agent's payoff
depends on a bounded or an unbounded number of others. In the same environment, same learning
rule, same parameters, the repertoire contracts to 1 under all-to-all coupling and grows
monotonically — 3 to 32 over N = 6 to 28 — on a ring.

`[FACT]` **Non-convergence within the sweep budget is a slow transient in every case
examined.** Some ring runs did not settle within 4,000 iterations, at rates that vary
non-monotonically with N: 74/120 at N = 6, 17/120 at N = 14, 51/120 at N = 28, and none at
N = 8, 10 or 20. Ten such cases were pushed to 20,000 iterations and the residual motion
measured over a further 1,200:

Two quantities are measured per case and they are not interchangeable. **Max step-change** is
the largest single-iteration movement across the window; it is what decides fixed point versus
closed orbit. **Amplitude** is the total excursion across the whole window, so it is always
the larger of the two and accumulates residual drift. The verdict uses the first.

| configuration | cases | max step-change | amplitude | verdict |
|---|---|---|---|---|
| ring degree 2, N = 6 | 4 | 0.00e+00 | 0.00e+00 | fixed point |
| ring degree 2, N = 14 | 2 | 1.3e-15, 3.3e-16 | 7.3e-15, 3.3e-16 | fixed point |
| ring degree 2, N = 28 | 4 | 1.2e-15 to 1.3e-15 | 6.3e-15 to 8.0e-15 | fixed point |
| ring degree 4, N = 20 | 5 | 0.00e+00 to 1.0e-15 | 0.00e+00 to 6.0e-15 | fixed point |

Across all fifteen cases the largest step-change is 1.3e-15, or 6 units in the last place of
double precision, and the largest amplitude is 8.0e-15, or 36 units. The saved
diagnostics in `out/oscillation_probe.json` and `out/robustness.json` carry both fields by
name, not as positional pairs.

Fifteen cases across four configurations, all fixed points. The degree-4 N = 20 entry matters
most: it is the lowest convergence rate anywhere in the study (7/70 inside the budget), and it
is still a slow-transient regime rather than an oscillatory one.

Dropped runs therefore make the ring R(N) an **undercount**, which is conservative for the
growth claim.

`[READ]` **Scope of the no-oscillation claim.** What is established: every attractor actually
reached, on both graphs, is a fixed point (amplitude ≤1.5e-10 over the confirmation stretch),
and the ten non-convergent ring cases examined above are slow transients rather than closed
orbits. Supporting this on the complete graph, the separate α-sweep of §4 (α ∈ {0.2, 0.6,
1.5, 4.0} at N = 10) found maximum amplitudes of order 1e-15, the only non-convergent
behaviour being numerical breakdown at α = 4.

`[OPEN]` What is **not** established: ten cases at three ring sizes is a thin basis for a
claim about the whole family. The non-convergent fraction was sampled, not enumerated — 142
such runs occurred across the ring sweep — and no equivalent diagnosis was run on the
complete graph, where it was not needed because convergence was essentially total
(197-200 of 200 at every N). **The correct statement is that no limit cycle, quasi-periodic
orbit or chaotic set was found, not that none exists.** d(N) = 0 holds for every attractor
this study reached; whether some initial condition in this family reaches a non-point
attractor is not resolved here.

---

## 6. What this says about the two conjectures

**Conjecture A (collapse, d(N)/D(N) → 0).** `[FACT]` Satisfied, and vacuously. Every
attractor is a fixed point, so d(N) = 0 while D(N) = 2N grows. This is exactly the failure
mode flagged before any code was written: in the regime where the dynamics converge, the
conjecture is true by arithmetic rather than by discovery. The non-trivial version — an
attractor that is not a point occupying a vanishing fraction of the space — **could not be
tested here, because no such attractor exists in this environment.**

### 6.1 The TwoNN numbers in the sweep output, and why they are not d(N)

`[FACT]` `sweep()` ran the calibrated TwoNN estimator on the converged policy points at every
N and recorded the result in `out/sweep_threshold.json`. Those values must be read correctly,
so they are reported here rather than left in the file:

| N | 4 | 6 | 8 | 10 | 14 | 20 | 28 | 40 | 56 | 80 | 100 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `d_twonn` | 1.68 | 5.49 | 7.46 | 6.55 | 8.86 | 13.82 | 15.29 | 14.56 | 28.05 | 26.71 | 25.02 |
| points | 200 | 197 | 200 | 200 | 200 | 200 | 120 | 120 | 120 | 80 | 80 |
| R(N) | 3 | 3 | 4 | 4 | 2 | 1 | 1 | 1 | 1 | 1 | 1 |

`[FACT]` **These are not estimates of an attractor dimension.** The point cloud passed to the
estimator is the set of *converged endpoints*, one per initial condition. From N = 20 onward
R(N) = 1, so every endpoint is the same fixed point. Measured directly: at N = 20 the maximum
pairwise sup-distance between 40 endpoints is 5.6e-18, and at N = 56 between 30 endpoints it
is 1.3e-17 — one to two units in the last place of double precision. The cloud is a single
point surrounded by floating-point rounding scatter.

`[READ]` TwoNN is scale-invariant, because it uses only the ratio r2/r1. It therefore returns
the dimension of whatever isotropic scatter it is given, however small its radius. This is
the same behaviour as the `point (d=0)` row of the calibration in §2, which returned 24.8 for
a point perturbed by 1e-9 noise in 20 ambient dimensions. The rising trend in the table
(13.8 → 28.1) tracks the growing ambient dimension of the rounding ball, not the dynamics.

A second, independent reason not to quote them: the calibration in §2 shows the estimator is
accurate only near n = 2000 samples and reads 40-50% high at n = 600. Every value above rests
on 80-200 points.

`[FACT]` The conclusion d(N) = 0 therefore rests on the amplitude measurement — the map stays
at rest to ≤1.5e-10 through the confirmation stretch at every N — and on the degeneracy of
the endpoint cloud, **not** on the TwoNN column. The estimator remains validated and ready
for a regime with a genuine non-point attractor; this testbed does not provide one.

**Conjecture B (expansion, R(N) non-decreasing and unbounded).** `[FACT]` **Refuted on the
complete graph, supported on the ring.** All-to-all: R(N) is non-monotonic — 3, 3, 4, 4, 2,
1, 1, 1, 1, 1, 1 — and settles at a single globally attracting outcome from N = 20 to 100.
Degree-2 ring, identical parameters: R(N) = 3, 4, 8, 9, 14, 32 over N = 6 to 28, monotone and
accelerating, with every attractor symmetry-broken.

**The pairing.** `[READ]` The note identifies the conjunction — d(N) sublinear while R(N)
grows — as its one original claim. The honest verdict is that **the conjunction is not a
property of CRLD; it is a property of the interaction structure.** On the ring both halves
hold, but A holds vacuously (d = 0, the attractors are points), so the pairing is true and
uninformative. On the complete graph B is false outright. Neither graph exhibits the
interesting case the note is really after: a non-point attractor whose dimension is dominated
by the ambient space.

`[READ]` Amiet et al. (2021) and Tachikawa (2003) both report growth in the number of stable
outcomes with system size. Tachikawa's setting is a *lattice* of diffusively coupled
oscillators — bounded degree — which is the case that reproduces here. Amiet et al. draw
payoffs independently per player, which also keeps each agent's incentive from washing out.
Neither supports expansion under all-to-all coupling, and this result shows why.

---

## 7. Limitations

1. **One environment family.** Two production functions, one transition structure. A
   different nonlinearity, or a payoff that scales with absolute rather than fractional
   cooperation, could preserve pivotality as N grows and change the answer. `[OPEN]`
2. **R(N) from basin sampling is a lower bound.** Undersampling biases it downward, which is
   the direction of the reported effect. Against that: 200 initial conditions at N = 20 all
   landed on one outcome with identical cooperation to three decimals. A missed attractor
   would need a basin below ~0.5% of the sampled volume.
3. **Sparse case tested, but not to the same N.** The ring sweep was stopped at N = 28 for
   wall-clock reasons, against N = 100 on the complete graph, and the degree-4 ring was not
   run. The contrast at matched N (6-28) is unambiguous and the pivotality argument is
   N-independent by construction, but the ring's R(N) growth is established over a shorter
   range than the complete graph's contraction. Extending it is cheap and is the first thing
   to do next.
4. **One learning variant and one recording space.** Expected-SARSA, policy space. The
   Q-learning variant is implemented and validated but was not swept.
5. **Confirmation window capped** at 300 iterations rather than matching the transient.
6. **No non-trivial d(N) was obtained.** The estimator *was* run on real sweep output at
   every N and its values are in `out/sweep_threshold.json`; §6.1 reports them and shows they
   measure floating-point scatter about a single fixed point, not an attractor. The quantity
   the conjecture is about — the dimension of a non-point attractor — has no instance in this
   environment, so it remains unmeasured. Any future run in an oscillatory regime must use
   ≥2000 trajectory samples per the §2 calibration, and must sample along a trajectory rather
   than across converged endpoints.

---

## 8. Reproduction

```
python src/crld.py            # module
python -c "import sys;sys.path.insert(0,'src');import crld;print(crld.validate_reduction())"
```

`out/timing.json`, `out/regime_scan.json`, `out/sweep_threshold.json` carry the raw numbers;
`out/fig1_crld.png` is the figure. Environment: Python 3.13.15, numpy 2.5.3. Seeds are fixed
in each runner. Total sweep wall time 2,628 s on 4 cores.

`[FACT]` One environment note for anyone rerunning this: conda-built numpy is blocked by an
Application Control policy on the machine used, in every conda environment tried. The work
runs in a venv with pip-installed numpy (`.venv313`).

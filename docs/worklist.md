# ANC — Remaining work, itemised

Drafted 2026-10-08. Companion to `00_charter.md`. Unit of estimate is a **working session**,
not a day or a week — sessions vary and I will not invent calendar precision.

## Distance, stated honestly

| Target | Condition | Estimate |
|---|---|---|
| **End line, Branch B** (prior-art survey, outcome A defended) | Reachable regardless of what the scans find | **5–7 sessions** |
| **End line, Branch A** (model + prototype + experiment) | Requires a candidate to survive Phase L | **12–20 sessions** |
| **Finish line at A** (nothing useful, with evidence) | Same as Branch B — a defended A *is* crossing it | **5–7 sessions** |
| **Finish line at B–E** | Requires a survivor *and* a positive experimental result | Not estimable. May be unreachable. |

`[READ]` Current completion: Level 1 axes scanned 8 of 11. Level 2 scanned 0 of 1. Code
written 0 lines. Experiments run 0. The elimination loop has completed one iteration out of an
unknown number, terminating at step 3.

`[READ]` My read on the branch probabilities, which is a judgement and not a measurement: low
that any Level 1 axis survives, moderate that the Level 2 topology hypothesis survives contact
with graph-rewriting and neuroevolution prior art. More likely than not, this project lands on
Branch B.

---

## PHASE L — finish the literature boundary

**Gate: nothing in Phases F/I/E/R may start until L is complete.** The cost of being wrong
here is an implementation of someone else's paper, which is the mistake Phase L exists to
prevent and which it has already prevented once.

### L1 — Scan the Level 2 topology hypothesis (→ document 03) · 1–2 sessions

- **L1.1** Decompose the hypothesis into independently checkable clauses:
  (a) the coupling set changes over time; (b) the change is driven locally with no global
  objective; (c) the structure rather than node state carries the computational content;
  (d) there is a task, a measure, and a baseline.
- **L1.2** Build the search vocabulary in the field's own terms, not mine: adaptive networks ·
  coevolutionary networks · structural plasticity · rewiring dynamics · network
  self-organisation · graph rewriting · dynamic graph computation · self-assembling networks ·
  neural developmental programs · indirect encoding · developmental encoding · network
  morphogenesis · amorphous computing.
- **L1.3** Check these named prior-art risks explicitly, because each could close a clause:
  - NEAT / neuroevolution of augmenting topologies — topology changes, but under an
    evolutionary outer loop with a fitness function, i.e. a global objective. Closes (b)?
  - HyperNEAT and indirect encodings.
  - Graph rewriting systems, including Wolfram-style models where rewriting *is* the
    computation. **Highest risk to clause (c).**
  - Neural architecture search — topology search under a global objective.
  - Self-assembling neural networks and neural developmental programs (Risi's group).
  - Lindenmayer systems and developmental encodings.
  - Amorphous computing (Abelson et al.).
  - Chemical reaction network computing / molecular programming.
  - Dynamic and temporal graph neural networks.
  - Growing-network models (preferential attachment) — structure without computation.
  - Self-organising maps — topology-preserving but on a fixed lattice.
- **L1.4** Resolve every candidate against Crossref and arXiv; record raw results in `lit/`.
- **L1.5** Check claims against paper bodies, not abstracts, for anything that closes a clause.
- **L1.6** Branch at loop step 3.

### L2 — Scan the three remaining Level 1 axes (→ document 04) · 1–2 sessions

- **L2.1** Stochastic / unreliable transmission as a computational resource. Named risks:
  stochastic computing, sampling-based neural codes, noise-as-a-resource results.
- **L2.2** Intracellular and molecular state. Named risks: molecular computing, chemical
  reaction network computation, cellular-computation literature.
- **L2.3** Morphogenetic computation. Named risks: bioelectric pattern formation, neural
  cellular automata, morphogenetic engineering.
- **L2.4** Resolve, check bodies, branch.

### L3 — Recall statement · 0.5 session

- **L3.1** Document which instruments were used (Crossref bibliographic query, arXiv API,
  web search), and their observed failure modes — my keyword sweeps returned mostly noise and
  the decisive finding came from a web search, which bounds what any "not found" claim means.
- **L3.2** State explicitly what a `[OPEN]` marker does and does not license.

---

## PHASE F — formalisation · 2–3 sessions · **only if a candidate survives L**

- **F0** Adversarial re-scan of the survivor using vocabulary deliberately different from the
  one that found it open. A candidate that survives only one vocabulary has not survived.
- **F1** Restate the candidate as a definition, not a paragraph.
- **F2** State variables: per individual, per coupling, per collective. Types and ranges.
- **F3** Inputs and outputs — including whether the system has input/output boundaries at all,
  which the brief explicitly says not to assume.
- **F4** Update rule for the dynamics.
- **F5** Adaptation rule, separately from F4.
- **F6** Parameters, ranges, units.
- **F7** Initial conditions and how they are drawn.
- **F8** Assumptions, stated as a numbered list so each can be attacked.
- **F9** Computational complexity per update step, and the scaling in system size.
- **F10** Derive at least one consequence that differs from the baselines. **If no such
  consequence can be derived, stop — there is nothing to test and the model is decoration.**
- **F11** Observables, and the known failure modes of each measurement.
- **F12** Falsifiable prediction with null and alternative that exhaust the outcome space.

---

## PHASE I — implementation · 3–5 sessions

- **I1** Environment: numpy only to begin. Pinned versions. **Note the hardware: 4 cores,
  4 GiB RAM with almost none free.** Every experiment must be sized for that, and that
  constraint gets reported rather than discovered halfway through.
- **I2** Core data structures for individuals and couplings.
- **I3** The update step, with inline assertions on shapes and invariants.
- **I4** Determinism: seed management, plus a test that the same seed gives a bit-identical
  trajectory.
- **I5** Unit tests per equation — **and at least one test that provably fails against a
  deliberately broken implementation.** A test suite that passes over a defect is worthless;
  that is the documented lesson from the CCP project.
- **I6** A conserved quantity or invariant checked every step.
- **I7** Reference implementations of each baseline: matched fixed-structure control, echo
  state network, linear recurrent model at matched parameter count.
- **I8** Calibrate every measure on objects whose answer is known analytically before pointing
  it at real output.
- **I9** Configuration files, not hardcoded constants.
- **I10** Run manifest per experiment: seed, config hash, revision, timestamp, runtime.

---

## PHASE E — experiments · 3–5 sessions

- **E1** Define the smallest task that discriminates the model from the baselines.
- **E2** Define measures, and state each one's bias direction before running anything.
- **E3** Pilot: does anything happen at all.
- **E4** Bounded parameter sweep, reported in full including the regions where it failed.
- **E5** Baselines at matched parameter count *and* matched compute.
- **E6** Ablations removing one clause of the model at a time.
- **E7** Transient check — run long enough to separate metastable from asymptotic behaviour,
  and report run lengths. This is the trap documented in the CRLD note.
- **E8** Multiple seeds; report the distribution, never the best run.
- **E9** Negative controls: shuffled input, frozen adaptation, randomised structure.
- **E10** State plainly what was not resolved at the scale actually reached.

---

## PHASE R — reporting · 2–3 sessions

- **R1** Decide Branch A or B on the evidence.
- **R2** Draft.
- **R3** Traceability map: every number to the file that produces it.
- **R4** Reference audit: every citation resolved against Crossref/arXiv, every load-bearing
  claim checked against the source body.
- **R5** A single script that regenerates every number and figure.
- **R6** Limitations naming what was not tested and what the scan could have missed.
- **R7** Repo hygiene: README, LICENSE, CITATION.cff, pinned dependencies.
- **R8** Venue decision: arXiv, Zenodo, workshop.

---

## Infrastructure, outstanding

- **X1** `git init` — blocked, git is not on the sandbox PATH. Run it yourself, or I work
  files-only.
- **X2** Licence not yet chosen.
- **X3** Disk and memory headroom on the machine is near zero. Worth clearing before Phase I.

---

## The two ways this goes wrong

1. **Phase L is too shallow and something "survives" that was already done.** Mitigation: F0.
2. **Branch B is treated as failure and the scope inflates to avoid it.** Mitigation: the
   charter says a defended outcome A crosses the finish line. Hold to that.

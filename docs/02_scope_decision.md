# ANC — Document 02: the Level 1 route is closed, and what follows

Aditya Maiti, ANC project. Drafted 2026-10-08. Follows document 01.

**Status.** This records a negative result from the literature phase. No model has been
implemented. Claim typing as in document 01: `[FACT]` `[THEORY]` `[LIT]` `[READ]` `[HYP]`
`[OPEN]`.

---

## 1. The question this document answers

Document 01 ended with one surviving candidate for ANC v0.1, stated deliberately narrowly:

> Can a population of couplings, each of which (i) carries internal state on more than one
> timescale, (ii) adapts only to regulate its own transmitted activity toward a set-point,
> with no global objective and no external optimiser at any timescale, and (iii) may be
> created or removed, perform a computation that a fixed-weight network of the same node
> count cannot?

Document 01 rated confidence that this was unoccupied as low-to-moderate, and named the
homeostatic and self-organised-criticality literature as the place it was most likely to
already exist. That scan has now been run.

**It already exists. Every clause, and the conjunction.**

---

## 2. What occupies each clause

| Clause of the v0.1 proposal | Occupying prior work | Verdict |
|---|---|---|
| Memory carried in coupling state rather than node activity | `[LIT]` **Mongillo, Barak & Tsodyks (2008), "Synaptic Theory of Working Memory", *Science*.** Working memory held in short-term synaptic facilitation during periods when the neurons are not firing — memory in the synapses, not the activity. Continuing line: Mongillo & Tsodyks (2024, 2026) | **Closed.** This is the canonical reference and it is seventeen years old. |
| Local plasticity + homeostasis as the *only* adaptation, no global objective, readout fitted separately | `[LIT]` **Lazar, Pipa & Triesch (2009), "SORN: a Self-organizing Recurrent Neural Network", *Front Comput Neurosci*.** Recurrent connectivity self-organises under spike-timing plasticity, intrinsic plasticity and synaptic normalisation; no optimiser touches the recurrent weights | **Closed.** Architecturally this is the v0.1 sketch. |
| Set-point regulation as an objective in its own right | `[LIT]` **Triesch (2007), "Synergies Between Intrinsic and Synaptic Plasticity Mechanisms", *Neural Computation*** — intrinsic plasticity driving a unit toward a target output distribution | **Closed.** |
| Coupling internal state driving the collective into a computationally useful regime | `[LIT]` **Levina, Herrmann & Geisel (2007), "Dynamical synapses causing self-organized criticality in neural networks", *Nature Physics*** | **Closed.** |
| Criticality signatures arising from the self-organisation itself | `[LIT]` **Del Papa, Priesemann & Triesch (2017), *PLOS ONE*** — criticality signatures in SORN | **Closed.** |
| Structural plasticity — couplings created and removed | `[LIT]` **Zheng, Dimitrakakis & Triesch (2013), *PLoS Comput Biol***; Miner & Triesch (2015) | **Closed.** |
| Quantifying how much information sits in connections vs firing | `[LIT]` Fan & Mysore (2024) | **Closed**, even the attribution measure. |
| Couplings as dynamical degrees of freedom on equal footing with nodes | `[LIT]` Clark & Abbott (2024) *Phys Rev X*; Aitken & Mihalas (2023) *eLife* (document 01 §4) | **Closed.** |

`[READ]` The attribution argument I had intended as the clean diagnostic — make nodes
memoryless linear sums so that any memory is provably in the couplings — is the structure of
the Mongillo et al. delay-period result. There is no residual there.

---

## 3. The result, stated plainly

`[READ]` **ANC's Level 1 programme, as scoped in document 01, is a rediscovery.** The route
"take what the artificial neuron discards about synapses, make the synapse the computational
individual, let it self-organise without an optimiser" is not an opening. It is a mature
subfield with canonical papers in *Science*, *Nature Physics*, *Phys Rev X* and *eLife*,
spanning 2007 to 2024.

The project brief asks for this to be recorded as a result rather than buried, and it is one:
a negative result that cost one session and no implementation, obtained before any code was
written. That is the literature phase working correctly.

---

## 4. What was *not* scanned

`[OPEN]` Precision matters here, because "Level 1 is closed" would overstate what was
checked. Scanned and occupied: dendritic computation, short-term synaptic dynamics,
multi-timescale synaptic state, synapse-as-dynamical-variable, homeostatic set-point
regulation, self-organised criticality, neuromodulation, glia.

Not scanned:

1. **Stochasticity and unreliable transmission as a computational resource** — synaptic
   failure rates are high in cortex and the ANN discards this entirely.
2. **Intracellular / molecular state** as computation inside the individual, on timescales
   below plasticity and above transmission.
3. **Morphogenetic and developmental computation** — the process that *builds* the collective
   rather than the one that runs on it.

`[READ]` My prior is that (1) and (2) are also occupied — stochastic computing and molecular
computation are both established fields — and that (3) is the thinnest. I would not bet the
project on any of them without the same scan this document reports.

---

## 5. Where the opening actually appears to be

`[READ]` One structural feature is shared by almost everything catalogued in documents 01 and
02, and it is worth naming because the brief asks exactly this question at Level 2.

**Nearly all of it fixes the node set and treats topology as scaffolding rather than as the
computation.** Reservoirs and liquid state machines fix it. Clark & Abbott use a fixed random
graph. Mongillo et al. fix it. Neural cellular automata fix a grid. Graph neural networks fix
the graph. SORN permits structural plasticity, but on a fixed node set, with a fixed readout,
and the structural change is a mechanism that supports the computation rather than being it.

`[LIT]` The literature that does treat topology as a state variable — Gross & Blasius (2007),
adaptive coevolutionary networks — sits in complex systems and is not used as a computational
substrate with a task, a measure, and a baseline.

`[HYP]` The gap, stated as a hypothesis and nothing more: *a system in which the change of the
coupling structure is the computation, rather than a mechanism that tunes a substrate on which
some other computation runs.* This is Level 2 of the brief, it is where the brief says ANC's
distinctive question lives, and it is the one place the scan did not keep running into
occupying work.

**This has not been scanned yet.** It is a hypothesis about where to look next, not a claim of
novelty. Document 03 should test it the same way document 01 and 02 tested the last one, and
should be expected to kill it.

---

## 6. Options

1. **Scan the Level 2 topology hypothesis (§5) before anything else.** Same method, one
   session. Recommended — it is the only lead that has not already failed, and it is cheap.
2. **Reframe ANC as a comparative study.** The substrates catalogued here — SORN, liquid state
   machines, Mongillo-type synaptic memory, Clark–Abbott coupled dynamics, physical learning
   networks — have never been compared on common tasks with a common measure of where
   information is held. That is a real, publishable artifact and it needs no novel primitive.
3. **Scan the three unscanned Level 1 axes (§4)** before conceding Level 1.

`[READ]` Options 1 and 2 are compatible: the comparison in option 2 would supply the baselines
that any option-1 result would need anyway.

---

## 7. Record

**Established this session.** Eight Level 1 mechanism axes and the full v0.1 conjunction are
occupied by published work. ANC has no novelty claim on the computational individual as
scoped.

**Uncertain.** Whether §5 survives; whether the three §4 axes are open.

**Not done.** No model, no mathematics, no code, no experiment. Deliberately — writing an
implementation of the document-01 proposal would have been reimplementing SORN.

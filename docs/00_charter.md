# ANC — Document 00: charter

Aditya Maiti. Drafted 2026-10-08, after documents 01 and 02. Numbered 00 because it orients
the others, not because it came first.

Claim typing as elsewhere: `[FACT]` `[THEORY]` `[LIT]` `[READ]` `[HYP]` `[OPEN]`.

---

## 1. The question

Artificial neural networks came from an aggressive simplification of a biological neuron,
made when almost nothing was known about what that neuron computes. The simplification became
an independent computational lineage. ANC asks what happens if that abstraction is performed
again, with current biology, at two levels — the computational individual, and the collective
interaction between individuals — while refusing to assume the result must inherit the
ontology of conventional neural networks.

The project does not assume the answer is a new paradigm. It assumes the answer is decidable.

---

## 2. Start line — where the project actually stands

Not "a blank idea". One route has been eliminated and one named.

**Established.** Eight candidate mechanisms for the computational individual were mapped
against prior art with verified records (document 01). All eight are occupied. The specific
v0.1 proposal that survived the first pass — couplings with multi-timescale state, adapting
only toward their own set-point, no global objective, mutable coupling set — was then closed
clause by clause (document 02). The closing references are canonical, not obscure: *Science*
2008, *Nature Physics* 2007, *Phys Rev X* 2024, *eLife* 2023, plus the SORN line from 2009.

**Not established.** Anything about Level 2. The topology hypothesis in document 02 §5 is
unscanned. Three Level 1 axes are also unscanned: stochastic transmission, intracellular
molecular state, morphogenetic computation.

**Exists.** Three documents, ~40 verified reference records, this repository. No model, no
mathematics, no code, no experiment.

`[READ]` The honest reading of the start line: the project has spent one session and bought a
negative result that would otherwise have cost a month of implementation. That is the
literature phase doing its job, not the project failing.

---

## 3. The path — the elimination loop

One loop, run repeatedly, designed so that failure is cheap and arrives early.

1. **State a candidate narrowly enough to be killable.** Not "synapses are interesting" but a
   sentence with clauses that can each be checked against prior art.
2. **Scan.** Resolve every record against Crossref or arXiv. Report recall honestly — say
   "not found by me", never "does not exist".
3. **Branch.** Occupied → record as a negative result, name who occupies it, return to 1.
   Open → continue.
4. **Formalise.** State variables, interactions, update rules, adaptation rule, parameters,
   assumptions, observables. Smallest sufficient model.
5. **Implement the minimum that tests the claim.** Not an architecture. A prototype.
6. **One diagnostic experiment**, with baselines that could beat it and ablations that remove
   one clause each.
7. **Report whatever happened.**

`[READ]` The loop has run once. It terminated at step 3. Cost: one session. That cost is the
design target — if an iteration starts costing weeks before reaching step 3, the candidate was
stated too vaguely at step 1.

---

## 4. End line — the artifact

The thing that exists when the work stops. There are two branches and both are real.

**Branch A — a candidate survives the scan.** A short paper: the formal model, a minimal
prototype, one diagnostic experiment, baselines, ablations. The claim is narrow by
construction — "mechanism X yields property Y that a fixed-weight network of matched size
does not" — and the paper stands whether Y is found or not found, provided the experiment
could have detected it.

**Branch B — nothing survives.** A systematic prior-art map: *re-deriving the computational
individual from modern neuroscience, and what already occupies each axis.* Documents 01 and
02 are already two thirds of this. It is a survey with a thesis — that the abstraction space
the ANN left open has since been filled, and by whom — and it needs no novel primitive to be
worth reading.

`[READ]` Branch B is a genuine end line, not a consolation. It is also the branch currently
better supported by evidence. The project should stop pretending otherwise if the next two
scans come back occupied.

**What the end line is not.** It is not a framework, a paradigm, a library, or a system. Any
of those would mean the scope grew without the evidence growing.

---

## 5. Finish line — the question settled

Different target, longer horizon. The finish line is reached when the brief's question has a
defended answer, on the outcome ladder:

- **A.** Nothing useful — the re-derivation yields no computational property worth having.
- **B.** A useful algorithm inside an existing paradigm.
- **C.** A genuinely different architecture.
- **D.** A different computational substrate.
- **E.** A new computational framework.

`[READ]` Crossing the finish line at **A, with evidence**, is crossing it. The failure mode is
not landing on A; the failure mode is landing on C–E by assertion. Documents 01 and 02 are
evidence toward A for the individual, and say nothing yet about the collective.

**The end line is reachable in months. The finish line may not be reachable at all**, and the
project is not structured to require it. Do not let the second one hold the first one hostage.

---

## 6. Literature and concepts

The spine. Anchors are verified records; full list in document 01 §6.

### The assumption under attack

`[READ]` The single structural commitment that organises everything else: ANNs split fast
transient state (activations) from slow stored parameters (weights) updated by an external
optimiser. Biology has no such split. Every Level 1 candidate in this project is a way of
attacking that split, and every one so far has been occupied by someone who got there first.

### Level 1 — the computational individual

| Concept | Anchor | Status |
|---|---|---|
| Dendritic computation — the neuron is not a point nonlinearity | Poirazi et al. 2003; London & Häusser 2005; Gidon et al. 2020 (*Science*); Poirazi & Papoutsi 2020 | Occupied in ML by Beniaguev et al. 2021; Chavlis & Poirazi 2025 (*Nat Commun*) |
| Synaptic computation — the synapse is not a scalar | Abbott & Regehr 2004 (*Nature*); Tsodyks & Markram 1997; Markram et al. 1998; Fortune & Rose 2001 | Occupied by reservoir computing: Maass et al. 2002 |
| Multi-timescale synaptic state | Fusi et al. 2005; Benna & Fusi 2016 | Is itself the computational model |
| Memory in synapses, not in activity | **Mongillo, Barak & Tsodyks 2008 (*Science*)** | Closes the attribution experiment |
| Synapse as dynamical variable co-equal with the neuron | **Clark & Abbott 2024 (*Phys Rev X*)**; Aitken & Mihalas 2023 (*eLife*) | Closes the ontological inversion |
| Homeostatic set-points, intrinsic plasticity | Turrigiano 2008; Marder & Goaillard 2006; Zhang & Linden 2003; Triesch 2007 | Closes set-point-as-objective |
| Self-organisation without an optimiser | **Lazar, Pipa & Triesch 2009 (SORN)**; Levina et al. 2007 (*Nat Phys*); Del Papa et al. 2017; Zheng et al. 2013 | Closes the whole v0.1 architecture |
| Edge of chaos / criticality as computation | Bertschinger & Natschläger 2004 | Established |
| Learning without backpropagation | Scellier & Bengio 2017; Lillicrap et al. 2020; Stern & Murugan 2023; Dillavou et al. 2024 (*PNAS*) | Active competitive field |
| Neuromodulation; glia | Bargmann 2012; Marder 2012; Miconi et al. 2018; Kozachkov et al. 2023 (*PNAS*) | Occupied |

### Level 2 — the collective

| Concept | Anchor | What it still assumes |
|---|---|---|
| Reservoir / liquid state computing | Maass et al. 2002 | Fixed topology, trained readout |
| Neural cellular automata | Mordvintsev et al. 2020; Randazzo et al. 2020 | One local rule, but backprop-trained, fixed grid |
| Adaptive / coevolutionary networks — topology as a state variable | Gross & Blasius 2007 | Complex systems; no task, measure, or baseline |
| Collective RL dynamics | Barfuss et al. 2019; Barfuss 2022; Barfuss et al. 2025 (*PNAS*) | Agents as policy vectors, fixed action set, external reward |
| Collective intelligence in deep learning | Ha & Tang 2022 | Conventional nets, collective training |
| Basal cognition / morphogenetic computing | Levin, TAME | Conceptual; little directly implementable |

### The live hypothesis

`[HYP]` Nearly everything above fixes the node set and treats topology as scaffolding rather
than as the computation. The open question is whether a system exists in which *the change of
coupling structure is the computation*, not a mechanism that tunes a substrate some other
computation runs on. Unscanned. Expected to fail the same way the last one did.

---

## 7. Immediate next step

Document 03: scan the §6 hypothesis by the same method. One session. Branch at step 3 of the
loop.

---

## 8. Standing rules

- Every claim carries a type marker. A hypothesis never reads as a finding.
- Novelty is claimed only after naming the closest existing work and the difference.
- Recall is reported honestly. "Not found by me" is the strongest available statement.
- A negative result is written up, not buried.
- Be enough, but don't be extra.

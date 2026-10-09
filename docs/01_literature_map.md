# ANC — Literature map and novelty boundary (v0.1 scoping)

Aditya Maiti, ANC project. Document 01. Drafted 2026-10-08.

**Status of this document.** This is a literature map and a scoping recommendation. No ANC
model has been implemented and no experiment has been run. Nothing below is an experimental
result.

**Claim typing used throughout.** `[FACT]` established empirical biology · `[THEORY]`
established computational/mathematical result · `[LIT]` what an existing paper does ·
`[READ]` my reading of the field, could be wrong · `[HYP]` ANC hypothesis, untested ·
`[OPEN]` identified gap, not yet verified exhaustively.

**Method.** 35 works were resolved against Crossref and the arXiv API; every record in §6
was confirmed to exist with the stated author, year and venue. Recall is *not* complete —
keyword scanning of Crossref and arXiv for conceptual queries returned mostly noise, and the
single most important finding in this document (§4) came from a web search, not from the
systematic scan. Treat §5 `[OPEN]` markers as "not found by me", not as "does not exist".

---

## 1. What the conventional artificial neuron discards

The baseline to be re-derived. In the standard unit `y = σ(Σ wᵢxᵢ + b)`:

| Discarded | Biological counterpart |
|---|---|
| Spatial structure of integration | Dendritic compartments, branch-local nonlinearity |
| Any internal state of the connection | Synaptic vesicle pools, receptor state, multi-timescale traces |
| Any timescale other than "now" | Short-term facilitation/depression, consolidation cascades |
| Plasticity of the unit's own transfer function | Intrinsic excitability plasticity |
| A self-maintained operating point | Homeostatic set-points, synaptic scaling |
| Global context signals | Neuromodulation |
| Mutability of the connection set | Structural plasticity, pruning |
| Locality of the learning signal | Backpropagation is non-local |

This list is uncontroversial and is the common starting point for the entire
biologically-plausible-ML literature. **It is not an ANC contribution.** Listing it is only
useful for identifying which entries are still computationally unexploited — which is what
§2–§3 do.

---

## 2. Candidate mechanisms for the ANC computational individual

For each axis: strength of the biological evidence, what ANNs discard, the closest existing
computational translation, and whether the axis is still open.

| # | Axis | Bio evidence | Closest existing computational work | Verdict |
|---|---|---|---|---|
| A | Dendritic compartmentalisation and branch-local nonlinearity | `[FACT]` Strong. Poirazi et al. 2003; London & Häusser 2005; Stuart & Spruston 2015; Gidon et al. 2020 (single human L2/3 dendrites compute XOR-like functions); Poirazi & Papoutsi 2020 | Beniaguev et al. 2021 (a single cortical neuron requires a 5–8 layer TCN to mimic); Jones & Kording 2021; **Chavlis & Poirazi 2025, Nat Commun** — dendritic ANNs with accuracy/robustness/parameter-efficiency claims | **Saturated.** A 2025 Nature Communications paper occupies exactly "put dendrites in an ANN". ANC adds nothing here. |
| B | Short-term synaptic dynamics as temporal filtering | `[FACT]` Strong. Abbott & Regehr 2004; Tsodyks & Markram 1997; Markram et al. 1998 (same axon signals differently to different targets); Fortune & Rose 2001 | Maass et al. 2002 — liquid state machines are built *on* Markram-type dynamic synapses | **Occupied.** Dynamic synapses as temporal filters is the founding mechanism of reservoir computing. |
| C | Multi-timescale internal synaptic state | `[FACT]` Strong. Fusi et al. 2005 (cascade); Benna & Fusi 2016 | Benna–Fusi *is* the computational model; widely reused in continual learning | **Occupied.** |
| D | Synapse as a dynamical degree of freedom on equal footing with the neuron | `[THEORY]` | **Clark & Abbott 2024, Phys Rev X**; **Aitken & Mihalas 2023, eLife** | **Occupied — see §4.** This was my leading candidate and it is taken. |
| E | Intrinsic excitability plasticity | `[FACT]` Strong. Zhang & Linden 2003; Marder & Goaillard 2006 | Scattered intrinsic-plasticity work in SNN/reservoir settings; no landmark ML translation found | `[OPEN]` Partial — but low-yield on its own. |
| F | Homeostatic set-point regulation as an objective | `[FACT]` Strong. Turrigiano 2008; Marder & Goaillard 2006 (degenerate parameter sets, same function) | Homeostatic regulation appears widely as a *stabiliser* for other learning rules | `[OPEN]` Partial — the gap is set-point regulation as *the* objective, not as a stabiliser. Not exhaustively checked. |
| G | Neuromodulation / global gating | `[FACT]` Strong. Bargmann 2012; Marder 2012 | Miconi et al. 2018 (differentiable plasticity) and neuromodulated variants; Najarro & Risi 2020 | **Occupied**, and all of it keeps backprop as the outer loop. |
| H | Glial participation in computation | `[FACT]` Moderate | Kozachkov et al. 2023, PNAS — transformers from neurons and astrocytes | **Occupied.** |

### Learning without an external optimiser (cuts across all axes)

`[LIT]` Scellier & Bengio 2017 (equilibrium propagation); Lillicrap et al. 2020 (review of
backprop's biological implausibility); Stern & Murugan 2023 (learning in physical systems
with no neurons); Dillavou et al. 2024, PNAS (an analog network that learns with no
processor). `[READ]` This is an **active and competitive field**, not an opening. Equilibrium
propagation and physical learning networks still have a separate training phase with clamped
boundary conditions; that is the one structural feature they share which ANC could drop.

---

## 3. The collective (Level 2)

| Approach | Representative work | What it assumes that ANC need not |
|---|---|---|
| Neural cellular automata | Mordvintsev et al. 2020 (Distill); Randazzo et al. 2020 | One shared local rule — but its parameters are trained by backprop |
| Adaptive / coevolutionary networks | Gross & Blasius 2007, J R Soc Interface | Topology couples to node state; established in complex systems, *not* used as a computational substrate for learning |
| Collective RL dynamics | Barfuss et al. 2019; Barfuss 2022; Barfuss et al. 2025 | Agents are policy vectors; interaction is joint action in a stochastic game; learning is TD |
| Collective intelligence in deep learning | Ha & Tang 2022 (survey) | Mostly conventional nets with collective training schemes |
| Basal cognition / morphogenetic computing | Levin, TAME framework | Broad conceptual frame; little that is directly implementable |

`[READ]` The Barfuss lineage is the right intellectual reference for Level 2 but it inherits a
full ANN-adjacent ontology (fixed agent set, fixed action set, external reward). Gross &
Blasius is the more ontologically interesting entry, because there the topology is a state
variable — which is one of the few things ANC's brief explicitly asks to consider and which
the ML literature has largely not taken up.

---

## 4. The leading candidate, and the prior art that occupies it

`[READ]` Working from §1–§2, the sharpest single assumption to attack appeared to be the
**activity/weight dichotomy**: ANNs split fast transient state (activations) from slow stored
parameters (weights) updated by an external optimiser, and biology has no such clean split.
The natural ANC move was to invert the ontology — make the *coupling* the computational
individual, carrying its own multi-timescale state, and reduce nodes to passive summing
junctions.

**This is substantially occupied, and by Abbott's group.**

- `[LIT]` **Clark & Abbott (2024), "Theory of Coupled Neuronal-Synaptic Dynamics", Phys Rev X
  14, 021001.** They treat neurons and synapses as mutually coupled dynamic variables on
  equal footing, using dynamic mean-field theory, and identify regimes in which synapses
  rather than neurons drive the network's behaviour. Their framing states outright that a
  network may be better described by the states of its synapses than of its neurons.
- `[LIT]` **Aitken & Mihalas (2023), "Neural population dynamics of computing with synaptic
  modulations", eLife 12:e83035.** They study a network that relies *solely* on synaptic
  modulation during inference to carry task-relevant information — the "multi-plasticity
  network" — explicitly against the convention of RNNs with frozen weights.

`[READ]` This is the finding the brief's novelty-discipline section exists for. The idea is
not merely adjacent; it is the thing itself, published, in strong venues, within the last two
years. ANC must not claim it.

**What those two papers still assume**, and therefore what is *not* settled by them:

1. Clark & Abbott is an analysis of dynamical regimes in random networks with a fixed
   plasticity rule. There is no task, no objective, and no adaptation of the rule.
2. Aitken & Mihalas train the synaptic-modulation network's parameters by backpropagation.
   The outer loop is still a conventional optimiser.
3. Neither has a per-coupling homeostatic set-point, and neither lets the coupling set change.

---

## 5. Residual open space

`[OPEN]` After §4, what is left is narrower and should be stated narrowly:

> Can a population of couplings, each of which (i) carries internal state on more than one
> timescale, (ii) adapts only to regulate *its own* transmitted activity toward a set-point,
> with no global objective and no external optimiser at any timescale, and (iii) may be
> created or removed, perform a computation that a fixed-weight network of the same node
> count cannot?

`[READ]` Each clause is individually unoriginal. (i) is Benna & Fusi. (ii) is Turrigiano's
biology plus the homeostatic-SNN literature. (iii) is structural plasticity, and topology-as-
state is Gross & Blasius. The conjunction — specifically the absence of *any* external
objective, which distinguishes it from equilibrium propagation and from physical learning
networks, both of which retain a clamped training phase — is what I did not find occupied.

**Confidence that this is open: low-to-moderate.** The homeostatic/self-organised-criticality
literature in spiking networks is large and I have not systematically scanned it. Before any
implementation commitment, that scan must be done, and it is the next literature task.

---

## 6. Verified references

All records below were resolved against Crossref or arXiv on 2026-10-08.

**Dendritic computation.** Poirazi, Brannon & Mel (2003) *Neuron* — 10.1016/s0896-6273(03)00149-1 ·
London & Häusser (2005) *Annu Rev Neurosci* 28 — 10.1146/annurev.neuro.28.061604.135703 ·
Gidon et al. (2020) *Science* — 10.1126/science.aax6239 ·
Stuart & Spruston (2015) *Nat Neurosci* — 10.1038/nn.4157 ·
Poirazi & Papoutsi (2020) *Nat Rev Neurosci* — 10.1038/s41583-020-0301-7

**Dendrites in ANNs.** Beniaguev, Segev & London (2021) *Neuron* — 10.1016/j.neuron.2021.07.002 ·
Jones & Kording (2021) *Neural Comput* — 10.1162/neco_a_01390 ·
Chavlis & Poirazi (2025) *Nat Commun* — 10.1038/s41467-025-56297-9

**Synaptic computation and state.** Abbott & Regehr (2004) *Nature* — 10.1038/nature03010 ·
Tsodyks & Markram (1997) *PNAS* · Markram, Wang & Tsodyks (1998) *PNAS* ·
Fortune & Rose (2001) *Trends Neurosci* ·
Fusi, Drew & Abbott (2005) *Neuron* · Benna & Fusi (2016) *Nat Neurosci* — 10.1038/nn.4401

**Synapse-driven computation (the occupying prior art).**
Clark & Abbott (2024) *Phys Rev X* 14:021001 — 10.1103/physrevx.14.021001 ·
Aitken & Mihalas (2023) *eLife* 12:e83035 — 10.7554/eLife.83035

**Homeostasis and intrinsic plasticity.** Marder & Goaillard (2006) *Nat Rev Neurosci* — 10.1038/nrn1949 ·
Turrigiano (2008) *Cell* — 10.1016/j.cell.2008.10.008 ·
Zhang & Linden (2003) *Nat Rev Neurosci* — 10.1038/nrn1248

**Neuromodulation.** Bargmann (2012) *BioEssays* · Marder (2012) *Neuron*

**Learning without backprop.** Scellier & Bengio (2017) *Front Comput Neurosci* — 10.3389/fncom.2017.00024 ·
Lillicrap et al. (2020) *Nat Rev Neurosci* — 10.1038/s41583-020-0277-3 ·
Stern & Murugan (2023) *Annu Rev Condens Matter Phys* · Dillavou et al. (2024) *PNAS*

**Plastic / fast-weight networks.** Miconi, Stanley & Clune (2018) arXiv:1804.02464 ·
Ba et al. (2016) arXiv:1610.06258 · Najarro & Risi (2020) arXiv:2007.02686

**Reservoir / liquid state.** Maass, Natschläger & Markram (2002) *Neural Comput*

**Glia.** Kozachkov, Kastanenka & Krotov (2023) *PNAS* — 10.1073/pnas.2219150120

**Collective.** Mordvintsev et al. (2020) *Distill* — 10.23915/distill.00023 ·
Randazzo et al. (2020) *Distill* — 10.23915/distill.00027.002 ·
Gross & Blasius (2007) *J R Soc Interface* — 10.1098/rsif.2007.1229 ·
Ha & Tang (2022) *Collective Intelligence* — 10.1177/26339137221114874 ·
Levin, TAME — 10.31234/osf.io/t6e8p ·
Barfuss et al. (2019) *Phys Rev E*; Barfuss (2022) *Neural Comput Appl*; Barfuss et al. (2025) *PNAS*

---

## 7. What is established, uncertain, and next

**Established by this document.** Axes A, B, C, D, G, H are occupied by published work, in
several cases very recently and in strong venues. The ANC brief's instinct that "the synapse
is not a scalar" is correct biology and is *already* a live computational research programme.

**Uncertain.** Whether the §5 conjunction is genuinely unoccupied. My scan was not
systematic enough to support a novelty claim.

**Next, in order.**
1. Systematic scan of homeostatic and self-organised-criticality learning in spiking and
   non-spiking networks — the one place the §5 claim is most likely to already exist.
2. Only then: commit to a v0.1 scope and write the mathematical specification.
3. Repository scaffold and minimal implementation.

**Not done.** No model, no mathematics, no code, no experiment.

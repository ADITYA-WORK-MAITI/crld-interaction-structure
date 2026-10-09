# Interaction structure in collective reinforcement-learning dynamics

Aditya Maiti. Exploratory research, 2026.

**Paper:** [`paper/paper.pdf`](paper/paper.pdf). Source in [`paper/paper.md`](paper/paper.md).

**Archived release:** [10.5281/zenodo.23264321](https://doi.org/10.5281/zenodo.23264321)

Whether a collective of reinforcement learners ends up with many distinct
collective outcomes or just one is decided by how the agents are coupled, not by
how many of them there are. Under all-to-all coupling the repertoire contracts to
a single attractor and cooperation collapses. On a sparse ring the repertoire
keeps growing over the same range. The code, the saved results and the figure
behind every number in the paper are in this repository.

Reproduce everything with `python run_all.py all`.

An attempt to redo the abstraction that produced the artificial neuron, using current
biology, at two levels: the computational individual, and the collective interaction between
individuals. The working assumption is explicitly *not* that the result must inherit the
ontology of conventional neural networks.

Motto: be enough, but don't be extra.

## Status

**First empirical result in hand.** The Level 1 scoping candidate was closed on prior-art
grounds before any implementation (`docs/02_scope_decision.md`); the work moved to Level 2,
the collective, where it meets an existing open question in collective reinforcement-learning
dynamics. `docs/03_results.md` reports the measurement.

Three findings:

1. The combinatorial cost that makes large-N CRLD look intractable is removable under the
   symmetry the framework already assumes. N = 200 runs at 13 ms per iteration against 8e59
   terms for direct enumeration, verified exact against brute force to 2e-16.
2. Collapse holds vacuously — every attractor found, on either graph, is a fixed point.
3. Expansion is decided by interaction structure, not by agent count. Under all-to-all
   coupling the repertoire contracts to one attractor by N = 20 and cooperation dies. On a
   degree-2 ring, identical in every other respect, the repertoire grows from 3 to 32 over
   N = 6 to 28 and cooperation holds. The controlling quantity is the expected benefit of
   cooperating, which decays as 1/N under dense coupling and is constant under sparse.

## Documents

```
docs/
  00_charter.md           start line, path, end line, finish line, concept map
  01_literature_map.md    eight candidate mechanisms for the computational individual,
                          with evidence strength, closest existing work, and an
                          occupied/open verdict for each
  02_scope_decision.md    the surviving candidate from 01, the scan that closed it,
                          and where the opening now appears to be
  03_results.md           the CRLD measurement: method, verification, results, limits
  TRACEABILITY.md         every reported number mapped to the file that produces it,
                          and what is not traceable
  worklist.md             remaining work, itemised, with distance estimates

src/
  crld.py                 N-agent CRLD on an interaction graph, with the count
                          reduction, a brute-force path, and the test asserting they agree
  experiments.py          convergence, repertoire on the orbit space, richness
                          correction, TwoNN, sweeps
  make_figures.py         figures from saved results, no recomputation

run_all.py                verify | timing | calibrate | sweeps | figures | all
out/                      raw results, timings, figures
lit/                      resolved literature records
```

## Reproduce

Needs Python 3.13, numpy and matplotlib. Conda-built numpy is blocked by an Application
Control policy on the development machine; `.venv313` holds a pip-installed one.

```
.venv313\Scripts\python run_all.py verify     # ~1 min, the load-bearing checks
.venv313\Scripts\python run_all.py figures    # seconds, from saved results
.venv313\Scripts\python run_all.py sweeps     # hours
```

`verify` is the stage that matters. It asserts the count reduction equals brute-force
enumeration of all M^(N-1) joint actions on every graph family and both learning variants,
asserts that a deliberately broken reduction **fails**, and checks that the orbit-space
quotient follows each graph's symmetry group. Everything else in this repository rests on it.

Trial counts are listed per N in `run_all.TRIALS`, transcribed from the runs that produced
the committed numbers. Changing one changes R(N): the measurement is censored at the number
of converged runs, which is why `experiments.chao1` and the discovery rate are reported
alongside every count.

Every reference cited in `docs/` was resolved against Crossref or the arXiv API and confirmed
to exist with the stated author, year and venue. The raw resolution records are in `lit/`.
Where recall was incomplete, the documents say so rather than implying a systematic search.

## Claim typing

The documents mark every claim as one of `[FACT]` established empirical biology, `[THEORY]`
established computational or mathematical result, `[LIT]` what an existing paper does,
`[READ]` the author's reading of the field, `[HYP]` an untested hypothesis, `[OPEN]` an
identified gap not yet exhaustively verified.

This exists so that a negative result reads as a result and a hypothesis never reads as a
finding.

## Next

`docs/02_scope_decision.md` §6. The immediate task is to scan the Level 2 topology
hypothesis in §5 with the same method that closed the first candidate, and to expect it to
fail.

## Licence

Not yet set. Nothing here is published.

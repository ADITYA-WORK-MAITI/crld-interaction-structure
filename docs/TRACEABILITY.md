# Traceability

Every number in `docs/03_results.md` and its source. Numbers not listed here are not
traceable and should not be relied on.

## Correctness claims

| Claim | Value | Produced by | Stored in |
|---|---|---|---|
| Reduction = enumeration, complete graph | 2.2e-16 (value), 2.8e-16 (q) | `crld.validate_reduction(graph="complete")` | `out/verify.json` |
| Reduction = enumeration, ring degree 2 | 2.2e-16 both variants | `crld.validate_reduction(graph="ring", degree=2)` | `out/verify.json` |
| Reduction = enumeration, ring degree 4 | 2.2e-16 both variants | `crld.validate_reduction(graph="ring", degree=4)` | `out/verify.json` |
| Broken reduction is rejected | mismatch 7.4e-3 at N=4 | negative control in `run_all.verify` | `out/verify.json` |
| Cyclic quotient identifies rotations, refuses transpositions | assertions | `run_all.verify` | — |

`run_all.py verify` reproduces all of the above in about a minute. It is the only stage
whose failure invalidates everything else.

## Cost

| Claim | Value | Source |
|---|---|---|
| N=8 / 12 / 16 enumeration | 38.6 / 1051 / 22,304 ms | `out/timing.json` |
| N=8 / 12 / 16 reduction | 0.74 / 0.89 / 0.96 ms | `out/timing.json` |
| Ratio at N=16 | 23,250x | computed from the two rows above |
| N=200 reduction | 12.7 ms | `out/timing.json` |

## Estimator calibration

| Claim | Source |
|---|---|
| TwoNN: 1.03 / 2.17 / 3.04 / 5.11 / 8.13 at n=2000 | `experiments.calibrate_twonn(n=2000)` |
| TwoNN: 1.51 / 2.88 / 4.18 / 6.47 at n=600 | `experiments.calibrate_twonn(n=600)` |

Regenerate with `run_all.py calibrate`.

## Sweeps

| Series | N range | Stored in |
|---|---|---|
| complete graph, value variant | 4-100 | `out/sweep_threshold.json` |
| linear public good, 16 parameter settings | N=10 | `out/regime_scan.json` |
| ring degree 2, value variant | 6-28 | `out/sweep_ring.json` |
| ring degree 2, value variant | 40-100 | `out/sweep_final.json` |
| ring degree 4, value variant | 10-40 | `out/sweep_final.json` |
| Q-learning variant, N=20 | both graphs | `out/robustness.json` |
| non-convergence diagnostics | 15 cases | `out/oscillation_probe.json`, `out/robustness.json` |
| merged view of all of the above | — | `out/consolidated.json` |

Trial counts per N are listed explicitly in `run_all.TRIALS`, transcribed from the runs that
produced these files rather than recomputed from a formula. The ring degree-2 series came
from two runs with different budgets, so no single expression reproduces it. **Changing a
trial count changes R(N):** the measurement is censored at the number of converged runs.

## Figures

`out/fig_main.png` is built by `src/make_figures.py` from the sweep files above plus
`out/timing.json`. `run_all.py figures` regenerates it without recomputing anything.
Panel (b) draws points with discovery rate below 0.5 as measurements and the rest as lower
bounds; panel (d) is analytic, from `make_figures.pivotality`.

Superseded figures `out/fig1_crld.png` and `out/fig2_structure.png` are kept as a record of
intermediate states and are not cited by the report.

## Not traceable

- Wall-clock timings quoted in the report were measured on one 4-core machine under varying
  load and will not reproduce exactly.
- The `d_twonn` column in the sweep files is computed on converged endpoints. As §6.1 of the
  report explains, it measures floating-point scatter about a fixed point and is not an
  attractor dimension. It is retained in the files for transparency, not for use.
- `out/sweep_final.json` is from an interrupted run: the degree-4 N=80 point and two of the
  four Q-variant points were not reached. The report does not cite them.

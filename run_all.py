"""Regenerate every number and figure in docs/03_results.md.

    python run_all.py verify     # the load-bearing correctness checks, ~1 min
    python run_all.py timing     # cost scaling, ~2 min
    python run_all.py calibrate  # estimator calibration on known manifolds, ~1 min
    python run_all.py sweeps     # the measurement sweeps, HOURS
    python run_all.py figures    # figures from saved out/*.json, seconds
    python run_all.py all

`verify` is the one that matters: it asserts the count reduction equals brute-force
enumeration on every graph family and both learning variants, and it asserts that a
deliberately broken reduction FAILS. Everything else in this repository rests on it.

Outputs land in out/. Seeds are fixed in each stage.
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

import numpy as np
import crld
import experiments

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

PARAMS = dict(alpha=0.05, beta=120.0, gamma=0.95)
BASE_ENV = dict(r_prosperous=3.0, degraded_factor=0.2, recovery=0.5,
                threshold=0.5, steepness=20.0)
SEED = 20261008


def verify():
    """The count reduction equals brute force, and a broken one does not."""
    results = {}
    for graph, degree, ns in [("complete", 2, (4, 5, 6, 7)),
                              ("ring", 2, (5, 6, 7, 8)),
                              ("ring", 4, (6, 7, 8))]:
        for variant in ("value", "q"):
            r = crld.validate_reduction(n_agents=ns, n_trials=2, seed=3, variant=variant,
                                        graph=graph, degree=degree, **BASE_ENV)
            # a complete graph's degree is N-1, so it carries no degree label
            key = (f"complete-{variant}" if graph == "complete"
                   else f"{graph}-deg{degree}-{variant}")
            results[key] = r["max_abs_error"]
            print(f"  {key:24s} max|counts - enumeration| = {r['max_abs_error']:.2e}")

    original = crld.leave_one_out_pmfs
    crld.leave_one_out_pmfs = lambda p: np.tile(
        crld.poisson_binomial_pmf(p)[:len(p)], (len(p), 1))
    try:
        crld.validate_reduction(n_agents=(4,), n_trials=1, seed=0, variant="value")
        raise SystemExit("NEGATIVE CONTROL FAILED: a broken reduction passed the test")
    except AssertionError as exc:
        results["negative_control"] = str(exc)
        print(f"  negative control OK      broken reduction rejected: {str(exc)[:46]}")
    finally:
        crld.leave_one_out_pmfs = original

    # the orbit-space quotient must follow the graph's symmetry group
    X = crld.random_policies(6, rng=np.random.default_rng(0))
    rot = np.roll(X, 2, axis=0)
    transposed = X[[0, 2, 1, 3, 5, 4]]
    c = experiments.canonical
    assert np.allclose(c(X, "cyclic"), c(rot, "cyclic")), "ring must identify rotations"
    assert not np.allclose(c(X, "cyclic"), c(transposed, "cyclic")), \
        "ring must NOT identify transpositions"
    assert np.allclose(c(X, "full"), c(transposed, "full")), \
        "complete graph must identify transpositions"
    print("  symmetry quotient OK     cyclic identifies rotations, refuses transpositions")
    json.dump(results, open(os.path.join(OUT, "verify.json"), "w"), indent=1, default=str)


def timing():
    rng = np.random.default_rng(1)

    def best_of(fn, reps):
        return min(_timed(fn) for _ in range(reps))

    def _timed(fn):
        t0 = time.perf_counter(); fn(); return time.perf_counter() - t0

    small, large = [], []
    for N in [2, 4, 6, 8, 10, 12, 14, 16, 18]:
        env = crld.EcologicalDilemma(N, r_prosperous=min(3.0, N - 0.5))
        X = crld.random_policies(N, rng=rng)
        tc = best_of(lambda: crld.step(X, env, dense=False), 3)
        td = _timed(lambda: crld.step(X, env, dense=True)) if N <= 16 else None
        small.append((N, tc, td))
        print(f"  N={N:3d} counts {tc*1e3:8.3f} ms  dense "
              f"{(f'{td*1e3:.1f} ms' if td else 'skipped'):>12}")
    for N in [25, 50, 100, 150, 200]:
        env = crld.EcologicalDilemma(N, r_prosperous=3.0)
        X = crld.random_policies(N, rng=rng)
        t = best_of(lambda: crld.step(X, env, dense=False), 3)
        large.append((N, t))
        print(f"  N={N:3d} counts {t*1e3:8.3f} ms  (enumeration: 2^{N-1} terms/agent/state)")
    json.dump({"small": small, "large": large},
              open(os.path.join(OUT, "timing.json"), "w"), indent=1)


def calibrate():
    for n in (600, 2000):
        print(f"  n = {n}")
        for name, value in experiments.calibrate_twonn(seed=0, n=n).items():
            print(f"    {name:18s} {value:6.3f}")


# Trial counts exactly as run, transcribed per N rather than recomputed from a
# formula. The ring-d2 series was produced by two separate runs -- N <= 28 in one,
# N >= 40 in a second -- which used different budgets, so no single expression
# reproduces it. Changing any of these changes the numbers: R(N) measured by basin
# sampling is censored at the trial count (see experiments.chao1).
TRIALS = {
    "complete": {4: 200, 6: 200, 8: 200, 10: 200, 14: 200, 20: 200,
                 28: 120, 40: 120, 56: 120, 80: 80, 100: 80},
    "ring-d2": {6: 120, 8: 120, 10: 120, 14: 120, 20: 120, 28: 80,
                40: 70, 56: 60, 80: 45, 100: 40},
    "ring-d4": {10: 70, 20: 70, 40: 50, 80: 35},
    "q-complete": {20: 60, 40: 50},
    "q-ring-d2": {20: 60, 40: 50},
}

GRAPH_KW = {
    "complete": dict(graph="complete"),
    "ring-d2": dict(graph="ring", degree=2),
    "ring-d4": dict(graph="ring", degree=4),
    "q-complete": dict(graph="complete"),
    "q-ring-d2": dict(graph="ring", degree=2),
}


def sweeps():
    print("  hours of compute; see out/sweep_*.json for the saved results")
    jobs = [(tag, dict(BASE_ENV, **GRAPH_KW[tag]), N, K,
             "q" if tag.startswith("q-") else "value")
            for tag, table in TRIALS.items() for N, K in sorted(table.items())]
    rows = []
    for tag, env_kw, N, K, variant in jobs:
        row = experiments.sweep([N], K, env_kw=env_kw, seed=SEED, tol=1e-12,
                                max_steps=4000, confirm_cap=300, progress=False,
                                variant=variant, **PARAMS)[0]
        row.update(tag=tag, variant=variant)
        rows.append(row)
        print(f"  {tag:12s} N={N:4d} R={row['R_quotient']:4d} "
              f"Chao1={row['R_chao1']:7.1f} coop={row['mean_coop']:.3f}", flush=True)
        json.dump(rows, open(os.path.join(OUT, "sweep_all.json"), "w"), indent=1)


def figures():
    import make_figures
    make_figures.main(OUT)


STAGES = {"verify": verify, "timing": timing, "calibrate": calibrate,
          "sweeps": sweeps, "figures": figures}

if __name__ == "__main__":
    wanted = sys.argv[1:] or ["verify"]
    if wanted == ["all"]:
        wanted = list(STAGES)
    for name in wanted:
        if name not in STAGES:
            raise SystemExit(f"unknown stage {name!r}; choose from {list(STAGES)} or 'all'")
        print(f"\n=== {name} ===")
        STAGES[name]()

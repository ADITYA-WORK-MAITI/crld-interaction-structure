"""Build the result figures from the saved sweeps in out/.

Reads whatever sweep files are present and merges them, so the figures can be
regenerated without re-running hours of compute.
"""

import json
import os
from math import comb

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

COMPLETE, RING2, RING4, GREY = "#c1440e", "#0b5394", "#2f7d4f", "#8a8a8a"


def _load(out):
    """Collect rows from every sweep file, tagged by graph family."""
    rows = []
    for name in ("sweep_threshold.json", "sweep_ring.json", "sweep_final.json",
                 "sweep_all.json"):
        path = os.path.join(out, name)
        if not os.path.exists(path):
            continue
        blob = json.load(open(path))
        got = blob["rows"] if isinstance(blob, dict) else blob
        for r in got:
            r = dict(r)
            if "tag" not in r:
                r["tag"] = ("complete" if name == "sweep_threshold.json"
                            else f"ring-d{r.get('degree', 2)}")
            r.setdefault("variant", "value")
            rows.append(r)
    return rows


def _series(rows, tag, variant="value"):
    sel = sorted((r for r in rows if r["tag"] == tag and r["variant"] == variant),
                 key=lambda r: r["N"])
    seen, out = set(), []
    for r in sel:                      # later files win on duplicate N
        out = [x for x in out if x["N"] != r["N"]] + [r]
        seen.add(r["N"])
    out.sort(key=lambda r: r["N"])
    return out


def pivotality(group_size, p=0.5, r=3.0, s=20.0, th=0.5):
    """Expected marginal benefit of cooperating, over an agent's local group."""
    d, m = group_size - 1, group_size
    g = lambda k: 1.0 / (1.0 + np.exp(-s * (k / m - th)))
    w = np.array([comb(d, k) * p ** k * (1 - p) ** (d - k) for k in range(d + 1)])
    k = np.arange(d + 1)
    return float(r * (w * (g(k + 1) - g(k))).sum())


def main(out):
    try:
        apply_figure_style(sizes=(9, 8, 7))        # noqa: F821  (kernel helper)
    except NameError:
        plt.rcParams.update({"font.size": 8, "axes.spines.top": False,
                             "axes.spines.right": False, "figure.dpi": 150})
    rows = _load(out)
    comp = _series(rows, "complete")
    r2 = _series(rows, "ring-d2")
    r4 = _series(rows, "ring-d4")
    tim = json.load(open(os.path.join(out, "timing.json")))

    g = lambda s, k: np.array([x[k] for x in s], dtype=float)
    fig, ax = plt.subplots(2, 2, figsize=(8.6, 6.4))

    a = ax[0, 0]
    ns = [t[0] for t in tim["small"] if t[2]]
    td = [t[2] * 1e3 for t in tim["small"] if t[2]]
    nc = [t[0] for t in tim["small"]] + [t[0] for t in tim["large"]]
    tc = [t[1] * 1e3 for t in tim["small"]] + [t[1] * 1e3 for t in tim["large"]]
    a.semilogy(ns, td, "s--", color=GREY, label="enumerate joint actions")
    a.semilogy(nc, tc, "o-", color=RING2, label="count reduction")
    a.set_xlabel("agents $N$"); a.set_ylabel("time per iteration (ms)")
    a.set_title("The combinatorial cost is removable")
    a.legend(frameon=False, loc="upper left"); a.margins(0.05)

    a = ax[0, 1]
    # R(N) by basin sampling is censored: K trials reveal at most K attractors. Points
    # whose discovery rate approaches 1 are measuring the budget, not the dynamics, so
    # they are drawn as lower bounds rather than joined into the curve.
    CENSOR = 0.5

    def disc(x):
        d = x.get("discovery_rate")
        return d if d is not None else x["R_quotient"] / max(1, x["n_converged"])

    def split(series, min_conv=20):
        ok = [x for x in series if x["n_converged"] >= min_conv]
        return ([x for x in ok if disc(x) < CENSOR], [x for x in ok if disc(x) >= CENSOR])

    for series, colour, marker, name in ((comp, COMPLETE, "s", "all-to-all"),
                                         (r2, RING2, "o", "ring, degree 2"),
                                         (r4, RING4, "^", "ring, degree 4")):
        if not series:
            continue
        meas, cens = split(series)
        if meas:
            a.plot(g(meas, "N"), g(meas, "R_quotient"), marker + "-", color=colour, label=name)
        if cens:
            a.plot(g(cens, "N"), g(cens, "R_quotient"), marker, mfc="none", color=colour)
            for x in cens:
                a.annotate("", xy=(x["N"], x["R_quotient"] * 2.1),
                           xytext=(x["N"], x["R_quotient"] * 1.08),
                           arrowprops=dict(arrowstyle="->", color=colour, lw=0.8))
    a.plot([], [], "o", mfc="none", color=GREY, label="lower bound (sampling-limited)")
    a.set_xscale("log"); a.set_yscale("log")
    a.set_xlabel("agents $N$"); a.set_ylabel("distinct attractors $R(N)$")
    a.set_title("Repertoire grows only when coupling is sparse")
    a.legend(frameon=False, loc="upper left", fontsize=6.5); a.margins(0.1)

    a = ax[1, 0]
    a.plot(g(comp, "N"), g(comp, "mean_coop"), "s-", color=COMPLETE, label="all-to-all")
    a.plot(g(r2, "N"), g(r2, "mean_coop"), "o-", color=RING2, label="ring, degree 2")
    if r4:
        a.plot(g(r4, "N"), g(r4, "mean_coop"), "^-", color=RING4, label="ring, degree 4")
    a.set_xscale("log"); a.set_yscale("log")
    a.set_xlabel("agents $N$"); a.set_ylabel("cooperation at the attractor")
    a.set_title("Cooperation survives only when coupling is sparse")
    a.legend(frameon=False, loc="lower left"); a.margins(0.06)

    a = ax[1, 1]
    Nf = np.arange(4, 101)
    a.plot(Nf, [pivotality(int(N)) for N in Nf], "-", color=COMPLETE, label="all-to-all")
    a.plot(Nf, [pivotality(3)] * len(Nf), "-", color=RING2, label="ring, degree 2")
    a.plot(Nf, [pivotality(5)] * len(Nf), "-", color=RING4, label="ring, degree 4")
    a.axhline(1.0, color=GREY, lw=0.9, ls=":")
    a.text(60, 1.08, "cost of cooperating", color=GREY, fontsize=7)
    a.set_yscale("log"); a.set_xlabel("agents $N$")
    a.set_ylabel("expected benefit of cooperating")
    a.set_title("Pivotality decays as $1/N$ only under dense coupling")
    a.legend(frameon=False, loc="lower left"); a.margins(0.05)

    for axx, letter in zip(ax.ravel(), "abcd"):
        try:
            panel_letter(axx, letter)                 # noqa: F821
        except NameError:
            axx.text(-0.12, 1.06, letter, transform=axx.transAxes,
                     fontweight="bold", fontsize=10)
    fig.tight_layout()
    path = os.path.join(out, "fig_main.png")
    fig.savefig(path, dpi=300, bbox_inches="tight")
    print(f"  wrote {path}")
    return fig


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "out")

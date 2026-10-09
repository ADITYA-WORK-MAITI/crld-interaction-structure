"""Render paper.md to a PDF.

Uses the matplotlib PDF backend, because no HTML-to-PDF converter is available in
the environment this was built in. Output is plain but typeset: A4, serif body,
monospace tables, the figure placed inline, page numbers.

    python src/make_pdf.py paper/paper.md paper/paper.pdf
"""

from __future__ import annotations

import re
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

A4_W, A4_H = 8.27, 11.69
L, R, T, B = 0.95, 0.95, 0.85, 0.80          # margins, inches
TEXT_W = A4_W - L - R

BODY, H1, H2, H3, MONO, CAP = 9.3, 15.0, 11.5, 10.0, 6.9, 8.0
LEAD = {BODY: 0.152, H1: 0.235, H2: 0.185, H3: 0.162, MONO: 0.112, CAP: 0.132}
SERIF, MONOF = "DejaVu Serif", "DejaVu Sans Mono"
WRAP_BODY, WRAP_MONO = 96, 118


class Doc:
    def __init__(self, path):
        self.pdf = PdfPages(path)
        self.page_no = 0
        self._new_page()

    def _new_page(self):
        self.fig = plt.figure(figsize=(A4_W, A4_H))
        self.y = A4_H - T
        self.page_no += 1

    def _flush(self):
        self.fig.text(A4_W / 2 / A4_W, (B / 2) / A4_H, str(self.page_no),
                      ha="center", va="center", fontsize=8, color="#555")
        self.pdf.savefig(self.fig)
        plt.close(self.fig)

    def space(self, inches):
        self.y -= inches

    def need(self, inches):
        if self.y - inches < B:
            self._flush()
            self._new_page()

    def line(self, text, size=BODY, font=SERIF, weight="normal", colour="black",
             indent=0.0):
        self.need(LEAD[size])
        self.fig.text((L + indent) / A4_W, self.y / A4_H, text, fontsize=size,
                      fontfamily=font, fontweight=weight, color=colour,
                      ha="left", va="top")
        self.y -= LEAD[size]

    def para(self, text, size=BODY, font=SERIF, weight="normal", colour="black",
             wrap=WRAP_BODY, indent=0.0):
        for ln in textwrap.wrap(text, wrap) or [""]:
            self.line(ln, size, font, weight, colour, indent)

    def rule(self):
        self.need(0.10)
        self.fig.add_artist(plt.Line2D([L / A4_W, (A4_W - R) / A4_W],
                                       [self.y / A4_H] * 2,
                                       color="#bbbbbb", linewidth=0.6))
        self.y -= 0.10

    def image(self, path, caption):
        img = mpimg.imread(path)
        h_in = TEXT_W * img.shape[0] / img.shape[1]
        cap_h = LEAD[CAP] * (len(textwrap.wrap(caption, 112)) + 1)
        if self.y - (h_in + cap_h + 0.18) < B:
            self._flush(); self._new_page()
        ax = self.fig.add_axes([L / A4_W, (self.y - h_in) / A4_H,
                                TEXT_W / A4_W, h_in / A4_H])
        ax.imshow(img); ax.axis("off")
        self.y -= h_in + 0.10
        self.para(caption, CAP, SERIF, "normal", "#333333", wrap=112)
        self.space(0.08)

    def close(self):
        self._flush()
        self.pdf.close()


def strip_md(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = s.replace("**", "").replace("`", "")
    return s


def fmt_table(rows):
    """Lay a markdown table out as aligned monospace text."""
    widths = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]
    scale = 1.0
    total = sum(widths) + 3 * (len(widths) - 1)
    if total > WRAP_MONO:                     # shrink the widest column first
        scale = WRAP_MONO / total
        widths = [max(3, int(w * scale)) for w in widths]
    out = []
    for n, r in enumerate(rows):
        cells = [c[:widths[i]].ljust(widths[i]) for i, c in enumerate(r)]
        out.append("  ".join(cells).rstrip())
        if n == 0:
            out.append("  ".join("-" * w for w in widths))
    return out


def build(md_path, pdf_path, fig_path=None, fig_caption=""):
    src = open(md_path, encoding="utf-8").read().split("\n")
    doc = Doc(pdf_path)
    table, pre = [], []
    i = 0
    while i < len(src):
        raw = src[i].rstrip()
        i += 1
        if raw.startswith("|"):
            cells = [c.strip() for c in raw.strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                continue
            table.append([strip_md(c) for c in cells])
            continue
        if table:
            doc.space(0.05)
            for ln in fmt_table(table):
                doc.line(ln, MONO, MONOF)
            doc.space(0.10)
            table = []
        if raw.startswith("    ") and raw.strip():
            pre.append(raw[4:])
            continue
        if pre:
            doc.space(0.04)
            for ln in pre:
                doc.line(ln, MONO, MONOF, colour="#222222", indent=0.18)
            doc.space(0.10)
            pre = []
        if not raw.strip():
            continue
        if raw.startswith("---"):
            doc.space(0.04); doc.rule(); doc.space(0.04); continue
        m = re.match(r"(#{1,4})\s+(.*)", raw)
        if m:
            lvl, txt = len(m.group(1)), strip_md(m.group(2))
            size = {1: H1, 2: H2, 3: H3, 4: H3}[lvl]
            doc.space(0.17 if lvl <= 2 else 0.11)
            doc.need(LEAD[size] * 3)
            doc.para(txt, size, SERIF, "bold", wrap=int(WRAP_BODY * BODY / size))
            doc.space(0.05)
            if lvl == 2 and txt.startswith("6.") and fig_path:
                doc.image(fig_path, fig_caption)
            continue
        doc.para(strip_md(raw))
        doc.space(0.055)
    if table:
        for ln in fmt_table(table):
            doc.line(ln, MONO, MONOF)
    doc.close()
    return doc.page_no


if __name__ == "__main__":
    md, out = sys.argv[1], sys.argv[2]
    fig = sys.argv[3] if len(sys.argv) > 3 else None
    cap = ("Figure 1. (a) Cost per iteration of the reduction against explicit "
           "enumeration. (b) Distinct attractors against agent count. Filled markers are "
           "measurements. Open markers with arrows are lower bounds, where the discovery "
           "rate exceeds 0.5 and the count is limited by the sampling budget. "
           "(c) Cooperation at the attractor. (d) Expected benefit of cooperating, "
           "analytic, against a cost of one.")
    print("pages:", build(md, out, fig, cap))

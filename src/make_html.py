"""Render paper.md to a single self-contained HTML file.

The figure is embedded as base64 so the file can be opened or mailed on its own,
with no sibling assets. Print styling targets A4.

    python src/make_html.py paper/paper.md paper/paper.html out/fig_main.png
"""

from __future__ import annotations

import base64
import html
import re
import sys

CAPTION = ("Figure 1. (a) Cost per iteration of the reduction against explicit "
           "enumeration. (b) Distinct attractors against agent count. Filled markers are "
           "measurements. Open markers with arrows are lower bounds, where the discovery "
           "rate exceeds 0.5 and the count is limited by the sampling budget. "
           "(c) Cooperation at the attractor. (d) Expected benefit of cooperating, "
           "analytic, against a cost of one.")

CSS = """
html { font-size: 10.5pt; }
body { font-family: "Latin Modern Roman", Georgia, "Times New Roman", serif;
       max-width: 180mm; margin: 18mm auto 24mm; padding: 0 6mm;
       line-height: 1.45; color: #111; text-rendering: optimizeLegibility; }
h1 { font-size: 1.65rem; line-height: 1.25; margin: 0 0 .25em; font-weight: 700; }
h2 { font-size: 1.18rem; margin: 2.1em 0 .5em; font-weight: 700; }
h3 { font-size: 1.02rem; margin: 1.5em 0 .4em; font-weight: 700; }
p  { margin: 0 0 .75em; text-align: justify; hyphens: auto; }
hr { border: 0; border-top: 1px solid #ccc; margin: 1.6em 0; }
table { border-collapse: collapse; margin: 1em 0 1.3em; font-size: .88rem;
        width: 100%; font-variant-numeric: tabular-nums; }
th, td { border-bottom: 1px solid #ddd; padding: .32em .55em; text-align: left; }
th { border-bottom: 1.2px solid #888; font-weight: 700; }
tr:last-child td { border-bottom: 1.2px solid #888; }
code { font-family: "DejaVu Sans Mono", Consolas, monospace; font-size: .86em; }
pre { font-family: "DejaVu Sans Mono", Consolas, monospace; font-size: .82rem;
      background: #f7f7f7; border-left: 2px solid #ccc; padding: .6em .9em;
      overflow-x: auto; line-height: 1.35; }
figure { margin: 1.6em 0; }
figure img { width: 100%; height: auto; }
figcaption { font-size: .84rem; color: #333; margin-top: .6em; text-align: justify; }
a { color: #0b5; color: #14519b; text-decoration: none; }
a:hover { text-decoration: underline; }
@media print { body { margin: 0 auto; } h2 { page-break-after: avoid; }
               figure, table, pre { page-break-inside: avoid; } }
"""


def inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def build(md_path, out_path, fig_path=None):
    src = open(md_path, encoding="utf-8").read().split("\n")
    fig_tag = ""
    if fig_path:
        b64 = base64.b64encode(open(fig_path, "rb").read()).decode("ascii")
        fig_tag = ('<figure><img alt="Figure 1" src="data:image/png;base64,%s">'
                   "<figcaption>%s</figcaption></figure>" % (b64, html.escape(CAPTION)))

    body, table, pre = [], [], []
    title = "paper"

    def flush_table():
        if not table:
            return
        head, rest = table[0], table[1:]
        body.append("<table><thead><tr>"
                    + "".join("<th>%s</th>" % inline(c) for c in head)
                    + "</tr></thead><tbody>"
                    + "".join("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r)
                              + "</tr>" for r in rest)
                    + "</tbody></table>")
        table.clear()

    def flush_pre():
        if not pre:
            return
        body.append("<pre>%s</pre>" % html.escape("\n".join(pre)))
        pre.clear()

    for raw in src:
        raw = raw.rstrip()
        if raw.startswith("|"):
            flush_pre()
            cells = [c.strip() for c in raw.strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                continue
            table.append(cells)
            continue
        flush_table()
        if raw.startswith("    ") and raw.strip():
            pre.append(raw[4:])
            continue
        flush_pre()
        if not raw.strip():
            continue
        if raw.startswith("---"):
            body.append("<hr>")
            continue
        m = re.match(r"(#{1,4})\s+(.*)", raw)
        if m:
            lvl, txt = len(m.group(1)), m.group(2)
            if lvl == 1:
                title = re.sub(r"[*`]", "", txt)
            tag = "h%d" % min(lvl, 4)
            body.append("<%s>%s</%s>" % (tag, inline(txt), tag))
            if lvl == 2 and txt.strip().startswith("6.") and fig_tag:
                body.append(fig_tag)
            continue
        body.append("<p>%s</p>" % inline(raw))
    flush_table()
    flush_pre()

    doc = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
           "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
           "<title>%s</title>\n<style>%s</style>\n</head>\n<body>\n%s\n</body>\n</html>\n"
           % (html.escape(title), CSS, "\n".join(body)))
    open(out_path, "w", encoding="utf-8").write(doc)
    return len(doc)


if __name__ == "__main__":
    md, out = sys.argv[1], sys.argv[2]
    fig = sys.argv[3] if len(sys.argv) > 3 else None
    print("bytes:", build(md, out, fig))

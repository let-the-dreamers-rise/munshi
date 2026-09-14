"""Render the README's architecture diagram to docs/architecture.png (and .svg).

    python scripts/build_diagram.py

The submission asks for an architecture diagram as an image; the README holds it as mermaid, so this
renders that exact block rather than keeping a second drawing that can drift.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BLOCK = re.compile(r"```mermaid\n(.*?)```", re.S)

PAGE = """<!doctype html><html><head><meta charset="utf-8">
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<style>
  body {{ margin: 0; background: #f7f3ea; font: 16px/1.5 system-ui, "Segoe UI", sans-serif; }}
  #sheet {{ padding: 36px 40px 30px; display: inline-block; }}
  h1 {{ font: 600 22px/1.2 "Iowan Old Style", Palatino, Georgia, serif; margin: 0 0 4px; color: #1d1b16; }}
  p {{ margin: 0 0 22px; color: #6b6558; font-size: 14px; }}
</style></head><body>
<div id="sheet"><h1>Munshi &mdash; the first hour after a UPI scam, handled</h1>
<p>Bank SMS never leaves the phone. One Strands session per event, hooks around every tool call,
and a real interrupt for the family's decision.</p>
<pre class="mermaid">{0}</pre></div>
<script>mermaid.initialize({{ startOnLoad: true, theme: "base", themeVariables: {{
  background: "#f7f3ea", primaryColor: "#fffdf8", primaryTextColor: "#1d1b16", primaryBorderColor: "#b3261e",
  lineColor: "#6b6558", secondaryColor: "#e7f0ec", tertiaryColor: "#fbeae7", fontFamily: "system-ui, Segoe UI, sans-serif",
  fontSize: "15px", clusterBkg: "#efe7d8", clusterBorder: "#c9bfa8" }} }});</script>
</body></html>"""


def main():
    source = BLOCK.search((ROOT / "README.md").read_text(encoding="utf-8"))
    if not source:
        raise SystemExit("no mermaid block in README.md")
    docs = ROOT / "docs"
    html = docs / "_diagram.html"
    # The browser would eat the <br/> in the labels as markup; mermaid wants them as text.
    mermaid = source.group(1).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    html.write_text(PAGE.format(mermaid), encoding="utf-8", newline="\n")
    with sync_playwright() as play:
        browser = play.chromium.launch()
        page = browser.new_context(viewport={"width": 1600, "height": 1000}, device_scale_factor=2).new_page()
        page.goto(html.as_uri())
        page.wait_for_selector("#sheet svg", timeout=30000)
        page.wait_for_timeout(1200)
        (docs / "architecture.svg").write_text(page.inner_html("#sheet svg").join(
            ['<svg xmlns="http://www.w3.org/2000/svg" {0}>'.format(
                page.evaluate("""() => { const s = document.querySelector('#sheet svg');
                    return 'viewBox="' + (s.getAttribute('viewBox') || '') + '" width="' + s.getBoundingClientRect().width +
                           '" height="' + s.getBoundingClientRect().height + '"'; }""")), "</svg>"]),
            encoding="utf-8", newline="\n")
        page.locator("#sheet").screenshot(path=str(docs / "architecture.png"))
        browser.close()
    html.unlink()
    size = (docs / "architecture.png").stat().st_size
    print("docs/architecture.png ({0:.0f} KB) and docs/architecture.svg".format(size / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())

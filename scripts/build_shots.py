"""Screenshots for the submission gallery: 1200x800 (3:2), from the live site.

    python scripts/build_shots.py [--url https://munshi-upi.vercel.app/]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

SIZE = {"width": 1200, "height": 800}
OUT = Path(__file__).resolve().parents[1] / "docs" / "shots"


def shot(page, name, y=0):
    page.evaluate("window.scrollTo(0, {0})".format(y))
    page.wait_for_timeout(700)
    page.screenshot(path=str(OUT / (name + ".png")))
    print("  " + name + ".png")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="https://munshi-upi.vercel.app/")
    opts = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as play:
        browser = play.chromium.launch()
        context = browser.new_context(viewport=SIZE, device_scale_factor=2, color_scheme="dark",
                                      timezone_id="Asia/Kolkata", locale="en-IN")
        context.add_init_script("try{localStorage.removeItem('munshi-lang')}catch(e){}")
        page = context.new_page()

        page.goto(opts.url, wait_until="networkidle")
        shot(page, "1-hero")

        page.click("#watch")
        page.wait_for_selector(".card.urgent", timeout=90000)
        page.wait_for_timeout(1500)
        shot(page, "2-card")

        page.click("#lang")
        page.wait_for_timeout(900)
        shot(page, "3-hindi")
        page.click("#lang")
        page.wait_for_timeout(600)

        page.click(".card.urgent summary")
        page.wait_for_timeout(700)
        shot(page, "4-paperwork", y=180)

        page.click(".card.urgent .choices button.primary")
        page.wait_for_selector(".card.urgent ol.steps li", timeout=90000)
        page.wait_for_timeout(1200)
        shot(page, "5-next-steps")

        page.click("#tempt")
        page.wait_for_selector(".log li.refused", timeout=90000)
        page.wait_for_timeout(1200)
        shot(page, "6-refused")

        page.evaluate("document.getElementById('how').scrollIntoView()")
        page.wait_for_timeout(700)
        page.screenshot(path=str(OUT / "7-how-it-works.png"))
        print("  7-how-it-works.png")
        browser.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())

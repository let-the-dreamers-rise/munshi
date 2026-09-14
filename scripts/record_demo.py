"""Record the demo video: drive the live site and screencast it, so a voice-over can go on top.

    python scripts/record_demo.py [--url https://munshi-upi.vercel.app] [--out demo.mp4]

It runs the real site in a real browser (Playwright), draws a cursor so clicks are readable, and
paces every beat slowly enough to talk over. ffmpeg turns the screencast into an mp4. The beat
sheet it prints at the end lines up with ideas/munshi-video-script.md.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

SIZE = {"width": 1280, "height": 720}  # 16:9, so a submission page does not letterbox it

CURSOR = """
document.addEventListener('DOMContentLoaded', function () {
  var dot = document.createElement('div');
  dot.id = '__cursor';
  dot.style.cssText = 'position:fixed;z-index:2147483647;width:16px;height:16px;margin:-8px 0 0 -8px;' +
    'border-radius:50%;background:rgba(255,255,255,.9);box-shadow:0 0 0 2px rgba(0,0,0,.45),0 2px 8px rgba(0,0,0,.5);' +
    'pointer-events:none;transition:transform .12s ease;left:-100px;top:-100px';
  document.body.appendChild(dot);
  addEventListener('mousemove', function (e) { dot.style.left = e.clientX + 'px'; dot.style.top = e.clientY + 'px'; }, true);
  addEventListener('mousedown', function () { dot.style.transform = 'scale(.55)'; }, true);
  addEventListener('mouseup', function () { dot.style.transform = 'scale(1)'; }, true);
});
try { localStorage.removeItem('munshi-lang'); } catch (e) {}
"""


class Take:
    """One recording, with a beat sheet written as it goes."""

    def __init__(self, page):
        self.page = page
        self.started = time.time()
        self.beats = []

    def say(self, note):
        self.beats.append((time.time() - self.started, note))

    def hold(self, seconds):
        self.page.wait_for_timeout(int(seconds * 1000))

    def to(self, selector, note=None, settle=0.5):
        locator = self.page.locator(selector).first
        box = locator.bounding_box()
        if box is None:
            raise RuntimeError("nothing to point at: " + selector)
        if box["y"] < 60 or box["y"] + box["height"] > SIZE["height"] - 60:
            self.scroll_to(selector, -300, 1.0)  # a click only lands where the viewer can see it
            box = locator.bounding_box()
        self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2, steps=28)
        if note:
            self.say(note)
        self.hold(settle)
        return box

    def click(self, selector, note=None, after=1.4):
        self.to(selector, note)
        self.page.mouse.down()
        self.hold(0.12)
        self.page.mouse.up()
        self.hold(after)

    def scroll(self, to_y, seconds=1.6):
        start = self.page.evaluate("window.scrollY")
        steps = max(1, int(seconds * 30))
        for i in range(1, steps + 1):
            y = start + (to_y - start) * i / steps
            self.page.evaluate("window.scrollTo(0, {0})".format(int(y)))
            self.page.wait_for_timeout(33)

    def scroll_to(self, selector, offset=-80, seconds=1.6):
        y = self.page.evaluate("document.querySelector({0!r}).getBoundingClientRect().top + window.scrollY".format(selector))
        self.scroll(max(0, y + offset), seconds)


def perform(page, url):
    take = Take(page)
    page.goto(url, wait_until="networkidle")
    take.say("the problem: a UPI scam starts with a message, and the next hour is the only hour")
    take.hold(5.5)

    take.scroll(110, 1.6)                      # down to the two buttons, without spoiling what is below
    take.hold(4.0)
    take.scroll(0, 1.2)
    take.click("#watch", "click: Watch it happen", after=2.0)

    page.wait_for_selector(".card.urgent", timeout=90000)
    take.say("the card: what happened, in one sentence, with the first hour running")
    take.hold(6)
    take.scroll(170, 1.4)
    take.say("the evidence: every number computed from the ledger, never generated")
    take.hold(5)

    take.click("#lang", "click: Hindi -- the same card, written again", after=1.0)
    take.hold(6)
    take.click("#lang", "click: back to English", after=1.0)
    take.hold(1.5)

    take.click(".card.urgent summary", "click: the paperwork, already filled in", after=1.2)
    take.say("1930 and cybercrime.gov.in, filled in from the bank's own SMS")
    take.hold(5)
    take.scroll_to(".card.urgent .tabs", -120, 1.0)
    take.click(".card.urgent .tabs button:nth-child(2)", "click: the bank letter, with the bank's own helpline", after=1.2)
    take.hold(4.5)
    take.click(".card.urgent .tabs button:nth-child(1)", after=1.0)
    take.hold(1.0)

    take.scroll_to(".card.urgent .choices", -180, 1.2)
    take.click(".card.urgent .choices button.primary", "click: Report it now -- this resumes a paused Strands agent", after=2.0)
    page.wait_for_selector(".card.urgent ol.steps li", timeout=90000)
    take.say("the agent had stopped inside a tool call to ask; the answer resumed it")
    take.hold(5.5)
    take.to(".card.urgent a.btn.primary", "one tap to call 1930", settle=2.2)
    take.to("a[href^='https://wa.me']", "one tap to send the whole pack to family", settle=2.5)

    take.scroll_to("#log", -120, 1.4)
    take.say("every tool call it made, in the panel on the right")
    take.hold(5)

    take.click("#tempt", "click: What if it tried to pay?", after=2.0)
    page.wait_for_selector(".log li.refused", timeout=90000)
    take.scroll_to("#log", -120, 1.2)
    take.say("the red lines: the same hook refusing a model that reached for money")
    take.hold(7)
    take.scroll_to("#tempt-note", -260, 1.2)
    take.hold(5)

    take.scroll_to("#how", -40, 2.2)
    take.say("how it works: the witness, the agent, the interrupt, the portable session, the handoff")
    take.hold(6)
    for step in range(2, 6):
        take.scroll_to("#how li:nth-child({0})".format(step), -140, 1.3)
        take.hold(3.2)
    take.scroll_to("footer", -420, 1.6)
    take.hold(4)
    return take


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="https://munshi-upi.vercel.app/")
    parser.add_argument("--out", default="demo.mp4")
    parser.add_argument("--theme", default="dark", choices=["dark", "light"])
    args = parser.parse_args()

    out = Path(args.out).resolve()
    raw = out.parent / "_recording"
    shutil.rmtree(raw, ignore_errors=True)
    raw.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as play:
        browser = play.chromium.launch()
        context = browser.new_context(viewport=SIZE, record_video_dir=str(raw), record_video_size=SIZE,
                                      timezone_id="Asia/Kolkata", locale="en-IN", color_scheme=args.theme,
                                      device_scale_factor=1)
        context.add_init_script(CURSOR)
        page = context.new_page()
        take = perform(page, args.url)
        page.close()
        context.close()
        browser.close()

    webm = next(raw.glob("*.webm"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(webm), "-r", "30",
                    "-vf", "scale={0}:{1}:flags=lanczos".format(SIZE["width"], SIZE["height"]),
                    "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", str(out)], check=True)
    print("{0}  ({1:.1f} MB)".format(out, out.stat().st_size / 1e6))
    print("\nBeat sheet (seconds into the take):")
    for at, note in take.beats:
        print("  {0:5.1f}  {1}".format(at, note))
    return 0


if __name__ == "__main__":
    sys.exit(main())

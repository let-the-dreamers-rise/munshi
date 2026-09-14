"""Record a real run for the static demo on GitHub Pages.

Runs the demo with the playbook model (the real Strands loop, hooks,
interrupts and sessions), saves the inbox as the family first sees it, then
for every card and every button replays the decision in a copy of the run
and saves what came back. The page replays those recordings in the browser.
Nothing on the static page talks to a server.

    python scripts/build_pages.py        writes docs/index.html and docs/replay.js
"""

from __future__ import annotations

import json
import shutil
import sys

SHARED = ("munshi.css", "munshi.js")
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from munshi.demo import demo_household  # noqa: E402
from munshi.service import Service  # noqa: E402

MARKER = "<script>\n(function () {"


def record(work):
    home = work / "run"
    service = Service(home, household=demo_household(), model_kind="playbook")
    service.scan()
    initial = service.state()
    outcomes = {}
    for card in initial["cards"]:
        for choice, _ in card["options"]:
            copy = work / "{0}-{1}".format(card["id"], choice)
            shutil.copytree(home, copy)
            branch = Service(copy, model_kind="playbook")
            seen = len(branch.audit(last=10_000))
            decided = branch.decide(card["id"], choice)
            outcomes.setdefault(card["id"], {})[choice] = {
                "card": decided, "audit": branch.audit(last=10_000)[seen:]}
    return {"recorded_at": datetime.now().strftime("%d %b %Y, %H:%M"), "initial": initial, "outcomes": outcomes}


def _write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        data = record(Path(tmp))
    static = ROOT / "munshi" / "static"
    page = (static / "index.html").read_text(encoding="utf-8")
    if MARKER not in page:
        raise SystemExit("index.html changed: cannot find where to add the replay script")
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    for name in SHARED:
        shutil.copyfile(static / name, docs / name)
    # newline="\n" so a rebuild on Windows is not a whole-file diff against what the repo already holds.
    _write(docs / "index.html", page.replace(MARKER, '<script src="replay.js"></script>\n' + MARKER, 1))
    _write(docs / "replay.js", "window.MUNSHI_REPLAY = " + json.dumps(data, indent=1) + ";\n")
    (docs / ".nojekyll").write_text("", encoding="utf-8")
    cards = len(data["initial"]["cards"])
    print("docs/index.html and docs/replay.js: {0} cards, {1} recorded decisions".format(
        cards, sum(len(v) for v in data["outcomes"].values())))


if __name__ == "__main__":
    main()

"""Copy the shared page assets into the hosted site (and check it has what it needs)."""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATIC = ROOT / "munshi" / "static"
PUBLIC = ROOT / "site" / "public"
SHARED = ("munshi.css", "munshi.js")


def main():
    PUBLIC.mkdir(parents=True, exist_ok=True)
    for name in SHARED:
        shutil.copyfile(STATIC / name, PUBLIC / name)
    page = (PUBLIC / "index.html").read_text(encoding="utf-8")
    for name in SHARED:
        if name not in page:
            raise SystemExit("site/public/index.html does not load {0}".format(name))
    print("site/public: " + ", ".join(sorted(p.name for p in PUBLIC.iterdir())))
    return 0


if __name__ == "__main__":
    sys.exit(main())

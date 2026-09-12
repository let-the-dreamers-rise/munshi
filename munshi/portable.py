"""A whole Munshi home, small enough to keep in a browser tab.

The hosted demo keeps nothing. A run's files — the inbox, the audit log, the
paused Strands session — are packed into one string, handed to the browser,
and sent back with the family's answer. The state belongs to the household,
not to a server.
"""

from __future__ import annotations

import base64
import gzip
import json
from pathlib import Path, PurePosixPath

MAX_FILES = 400
MAX_PACKED = 400_000
MAX_UNPACKED = 4_000_000


def _safe(name):
    path = PurePosixPath(name)
    if path.is_absolute() or any(part in ("..", "") for part in path.parts) or len(path.parts) > 8:
        raise ValueError("a session file has a path it may not have: {0!r}".format(name))
    return path


def pack(files):
    if len(files) > MAX_FILES:
        raise ValueError("session has too many files")
    raw = json.dumps(files, separators=(",", ":")).encode("utf-8")
    if len(raw) > MAX_UNPACKED:
        raise ValueError("session is too large")
    packed = base64.urlsafe_b64encode(gzip.compress(raw, 6)).decode("ascii")
    if len(packed) > MAX_PACKED:
        raise ValueError("session is too large")
    return packed


def unpack(blob):
    if not isinstance(blob, str) or not blob or len(blob) > MAX_PACKED:
        raise ValueError("that is not a session")
    try:
        raw = gzip.decompress(base64.urlsafe_b64decode(blob.encode("ascii")))
    except Exception:  # noqa: BLE001 -- any malformed blob is the same answer
        raise ValueError("that is not a session") from None
    if len(raw) > MAX_UNPACKED:
        raise ValueError("session is too large")
    files = json.loads(raw)
    if not isinstance(files, dict) or len(files) > MAX_FILES:
        raise ValueError("that is not a session")
    return files


def dump_home(home):
    """Every file under `home`, as {relative posix path: text}, packed."""
    home = Path(home)
    files = {}
    for path in sorted(home.rglob("*")):
        if path.is_file() and path.suffix != ".lock":
            files[path.relative_to(home).as_posix()] = path.read_text(encoding="utf-8")
    return pack(files)


def load_home(blob, home):
    """Write a packed home back to disk. Refuses any path that would escape it."""
    home = Path(home)
    for name, text in unpack(blob).items():
        target = home / _safe(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    return home

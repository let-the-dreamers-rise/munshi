"""A lock that works across processes: the CLI, the inbox and AgentCore can all touch one home."""

from __future__ import annotations

import os
import time
from contextlib import contextmanager
from pathlib import Path

STALE_AFTER = 120.0  # seconds; a lock this old was left by a process that died


@contextmanager
def locked(path, timeout=30.0):
    lock = Path(str(path) + ".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + timeout
    while True:
        try:
            fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            try:
                if time.time() - lock.stat().st_mtime > STALE_AFTER:
                    lock.unlink()
                    continue
            except FileNotFoundError:
                continue
            if time.monotonic() > deadline:
                raise TimeoutError("{0} is locked by another Munshi process".format(path)) from None
            time.sleep(0.01)
    try:
        yield
    finally:
        os.close(fd)
        try:
            lock.unlink()
        except FileNotFoundError:
            pass

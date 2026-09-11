"""The family's inbox, on this machine only.

Bound to 127.0.0.1. Requests must name this host, and anything that changes
state must be JSON and carry an `X-Munshi` header, which a web page on
another origin cannot send without a preflight this server never answers.
"""

from __future__ import annotations

import json
import re
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .demo import demo_household
from .inbox import CARD_ID
from .service import Service

PAGE = Path(__file__).with_name("static") / "index.html"
MAX_BODY = 4096
CHOICE = re.compile(r"^[a-z]{2,12}$")


class Inbox:
    """The current demo run. Starting again makes a new folder; nothing is deleted."""

    def __init__(self, root, model_kind):
        self.root = Path(root)
        self.model_kind = model_kind
        self.lock = threading.Lock()
        self.service = None

    def start(self):
        with self.lock:
            home = self.root / datetime.now().strftime("run-%Y%m%d-%H%M%S-%f")
            self.service = Service(home, household=demo_household(), model_kind=self.model_kind)
            self.service.scan()
            return self.service.state()

    def state(self):
        with self.lock:
            return self.service.state()

    def decide(self, card_id, choice):
        with self.lock:
            self.service.decide(card_id, choice)
            return self.service.state()


def handler_for(inbox, port):
    hosts = {"127.0.0.1:{0}".format(port), "localhost:{0}".format(port)}

    class Handler(BaseHTTPRequestHandler):
        server_version = "munshi"
        sys_version = ""

        def log_message(self, fmt, *args):
            return None

        def _send(self, status, body, kind="application/json"):
            data = body if isinstance(body, bytes) else json.dumps(body).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", kind + "; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy",
                             "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; "
                             "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'")
            self.end_headers()
            self.wfile.write(data)

        def _json(self, status, data=None, error=None):
            self._send(status, {"ok": error is None, "data": data, "error": error})

        def _allowed(self):
            if self.headers.get("Host", "") not in hosts:
                self._json(403, error="this inbox only answers on 127.0.0.1")
                return False
            return True

        def do_GET(self):
            if not self._allowed():
                return
            if self.path == "/":
                self._send(200, PAGE.read_bytes(), "text/html")
            elif self.path == "/api/state":
                self._json(200, inbox.state())
            else:
                self._json(404, error="not found")

        def _body(self):
            try:
                length = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                raise ValueError("bad Content-Length") from None
            if not 0 <= length <= MAX_BODY:
                raise ValueError("request too large")
            raw = self.rfile.read(length)  # read before refusing, so the client sees the answer
            if self.headers.get("X-Munshi") != "1" or "application/json" not in self.headers.get("Content-Type", ""):
                raise PermissionError("missing the X-Munshi header or a JSON body")
            data = json.loads(raw or b"{}")
            if not isinstance(data, dict):
                raise ValueError("expected a JSON object")
            return data

        def do_POST(self):
            if not self._allowed():
                return
            try:
                data = self._body()
                if self.path == "/api/decide":
                    card, choice = str(data.get("card", "")), str(data.get("choice", ""))
                    if not CARD_ID.match(card) or not CHOICE.match(choice):
                        raise ValueError("card or choice is malformed")
                    self._json(200, inbox.decide(card, choice))
                elif self.path == "/api/restart":
                    self._json(200, inbox.start())
                else:
                    self._json(404, error="not found")
            except PermissionError as error:
                self._json(403, error=str(error))
            except (KeyError, ValueError) as error:
                self._json(400, error=str(error))
            except Exception as error:  # noqa: BLE001 -- the page shows a message instead of hanging
                self._json(500, error="Munshi hit an error: {0}".format(type(error).__name__))

    return Handler


def serve(root, model_kind=None, port=8765):
    inbox = Inbox(root, model_kind)
    state = inbox.start()
    server = ThreadingHTTPServer(("127.0.0.1", port), handler_for(inbox, port))
    pending = sum(1 for c in state["cards"] if c["status"] == "pending")
    print("Munshi's inbox: http://127.0.0.1:{0}  ({1} card(s) waiting). Ctrl+C to stop.".format(port, pending))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0

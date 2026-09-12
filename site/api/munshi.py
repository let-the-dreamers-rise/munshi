"""The hosted demo's only endpoint. Stateless: every answer carries the run back to the browser."""

import json
from http.server import BaseHTTPRequestHandler

MAX_BODY = 600_000


class handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):  # no request logging: bodies can hold someone's SMS
        return None

    def _send(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        from munshi.web import handle

        try:
            length = int(self.headers.get("Content-Length") or 0)
            if not 0 < length <= MAX_BODY:
                raise ValueError("that request is too large")
            request = json.loads(self.rfile.read(length))
            if not isinstance(request, dict):
                raise ValueError("expected a JSON object")
            self._send(200, {"ok": True, "data": handle(request), "error": None})
        except ValueError as error:
            self._send(400, {"ok": False, "data": None, "error": str(error)})
        except Exception as error:  # noqa: BLE001 -- never leak a stack trace to a stranger
            self._send(500, {"ok": False, "data": None,
                             "error": "Munshi hit an error ({0}). Try again.".format(type(error).__name__)})

    def do_GET(self):
        self._send(405, {"ok": False, "data": None, "error": "post a JSON request"})

"""The loopback inbox and the AgentCore entrypoint, end to end with the playbook model."""

import json
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from types import SimpleNamespace

import pytest

from munshi import app as agentcore
from munshi.demo import demo_household
from munshi.run import main as cli
from munshi.serve import Inbox, handler_for


@pytest.fixture()
def server(tmp_path, monkeypatch):
    monkeypatch.setenv("MUNSHI_MODEL", "playbook")
    inbox = Inbox(tmp_path, None)
    inbox.start()
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), None)
    port = httpd.server_address[1]
    httpd.RequestHandlerClass = handler_for(inbox, port)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield "http://127.0.0.1:{0}".format(port)
    httpd.shutdown()
    httpd.server_close()


def request(url, body=None, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers or {}, method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, json.loads(r.read()) if "json" in r.headers["Content-Type"] else r.read()
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read())


POST = {"Content-Type": "application/json", "X-Munshi": "1"}


def test_the_inbox_serves_the_page_and_three_cards(server):
    status, page = request(server + "/")
    assert status == 200 and b"Never moves money" in page
    status, body = request(server + "/api/state")
    assert body["ok"] and sorted(c["kind"] for c in body["data"]["cards"]) == [
        "double_charge", "renewal_due", "scam_shaped_payment"]


def test_deciding_from_the_page_resumes_the_agent(server):
    cards = request(server + "/api/state")[1]["data"]["cards"]
    scam = [c for c in cards if c["kind"] == "scam_shaped_payment"][0]
    status, body = request(server + "/api/decide", {"card": scam["id"], "choice": "report"}, POST)
    assert status == 200
    done = [c for c in body["data"]["cards"] if c["id"] == scam["id"]][0]
    assert done["status"] == "decided" and "1930" in done["outcome"]


def test_a_post_without_the_header_is_refused(server):
    cards = request(server + "/api/state")[1]["data"]["cards"]
    status, body = request(server + "/api/decide", {"card": cards[0]["id"], "choice": "report"},
                           {"Content-Type": "text/plain"})
    assert status == 403 and not body["ok"]


def test_a_foreign_host_is_refused(server):
    status, body = request(server + "/api/state", headers={"Host": "evil.example:80"})
    assert status == 403


def test_a_bad_choice_is_a_400_not_a_crash(server):
    cards = request(server + "/api/state")[1]["data"]["cards"]
    status, body = request(server + "/api/decide", {"card": cards[0]["id"], "choice": "refund"}, POST)
    assert status == 400 and "not an option" in body["error"]
    status, body = request(server + "/api/decide", {"card": "../../etc", "choice": "report"}, POST)
    assert status == 400


def test_agentcore_scan_then_decide_in_one_runtime_session(tmp_path, monkeypatch):
    monkeypatch.setenv("MUNSHI_MODEL", "playbook")
    monkeypatch.setattr(agentcore, "ROOT", tmp_path)
    ctx = SimpleNamespace(session_id="meera/../phone-1")
    payload = demo_household().to_payload()
    out = agentcore.invoke({"action": "scan", "household": payload}, ctx)
    assert out["ok"] and len(out["data"]["cards"]) == 3
    assert all(p.parent == tmp_path for p in tmp_path.iterdir())  # the session id cannot escape the root
    scam = [c for c in out["data"]["cards"] if c["kind"] == "scam_shaped_payment"][0]
    out = agentcore.invoke({"action": "decide", "card": scam["id"], "choice": "report"}, ctx)
    assert out["ok"] and out["data"]["decision"] == "report"
    assert agentcore.invoke({"action": "transfer"}, ctx)["ok"] is False


def test_the_cli_runs_the_demo_and_decides(tmp_path, capsys):
    home = str(tmp_path / "home")
    assert cli(["demo", "--home", home, "--model", "playbook"]) == 0
    shown = capsys.readouterr().out
    assert "Events: 3" in shown and "choose: report" in shown
    card = [line.split()[1] for line in shown.splitlines() if line.startswith("*") and "never paid" in line][0]
    assert cli(["decide", card, "report", "--home", home, "--model", "playbook"]) == 0
    assert "1930" in capsys.readouterr().out
    assert cli(["decide", card, "report", "--home", home, "--model", "playbook"]) == 2

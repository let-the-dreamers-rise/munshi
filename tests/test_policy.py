"""The policy is code, not a prompt: unknown tools and unexpected arguments are refused."""

import json

from strands.hooks import AfterToolCallEvent, BeforeToolCallEvent

from munshi.policy import AuditHook, PolicyHook, refusal


def before(name, args):
    return BeforeToolCallEvent(agent=None, selected_tool=None,
                               tool_use={"toolUseId": "t1", "name": name, "input": args},
                               invocation_state={})


def test_unknown_tool_is_refused():
    e = before("send_money", {"to": "kyc.update9@ybl", "amount": 12000})
    PolicyHook().check(e)
    assert e.cancel_tool and "never moves money" in e.cancel_tool


def test_known_tool_with_an_unexpected_argument_is_refused():
    e = before("payee_history", {"party": "ZOMATO", "amount": 540})
    PolicyHook().check(e)
    assert e.cancel_tool and "amount" in e.cancel_tool


def test_known_tool_with_its_arguments_passes():
    e = before("investigate_payment", {"event_id": "abc"})
    PolicyHook().check(e)
    assert e.cancel_tool is False


def test_days_must_be_a_small_integer():
    assert refusal("recent_transactions", {"days": 5000}) is not None
    assert refusal("recent_transactions", {"days": 7}) is None


def test_audit_writes_one_line_per_tool_call(tmp_path):
    path = tmp_path / "audit.jsonl"
    hook = AuditHook(path)
    e = AfterToolCallEvent(agent=None, selected_tool=None,
                           tool_use={"toolUseId": "t1", "name": "payee_history", "input": {"party": "ZOMATO"}},
                           invocation_state={}, result={"toolUseId": "t1", "status": "success",
                                                        "content": [{"text": "x" * 5000}]}, duration=0.01)
    hook.record(e)
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1
    assert rows[0]["tool"] == "payee_history" and rows[0]["status"] == "success"
    assert len(rows[0]["result"]) <= 400

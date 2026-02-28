import pytest

from task_engine.ask.ask_schema import AskSlot, AskSlotKind, AskSchema
from task_engine.ask.retry_policy import RetryPolicy, OnExceedAction


def test_ask_schema_basic_slot_grouping():
    schema = AskSchema(
        task_id="go_hospital",
        slots=[
            AskSlot(name="destination", kind=AskSlotKind.REQUIRED),
            AskSlot(name="department", kind=AskSlotKind.OPTIONAL),
            AskSlot(name="hospital_detail", kind=AskSlotKind.CLARIFY),
        ],
    )

    required = schema.required_slots()
    optional = schema.optional_slots()
    clarify = schema.clarify_slots()

    assert [s.name for s in required] == ["destination"]
    assert [s.name for s in optional] == ["department"]
    assert [s.name for s in clarify] == ["hospital_detail"]

    assert schema.has_slot("destination") is True
    assert schema.has_slot("unknown") is False
    assert schema.get_slot("department").is_optional is True


def test_ask_schema_effective_retry_policy_uses_override_if_present():
    override = RetryPolicy(interval=3.0, limit=2, on_exceed=OnExceedAction.CLARIFY)
    schema = AskSchema(task_id="go_hospital", slots=[], retry_policy=override)

    # Even if we pass a different default, the override should win.
    default = RetryPolicy(interval=10.0, limit=5, on_exceed=OnExceedAction.ABORT)
    effective = schema.effective_retry_policy(default_policy=default)

    assert effective.interval == 3.0
    assert effective.limit == 2
    assert effective.on_exceed == OnExceedAction.CLARIFY


def test_ask_schema_effective_retry_policy_falls_back_to_provided_default():
    default = RetryPolicy(interval=7.0, limit=4, on_exceed=OnExceedAction.FALLBACK)
    schema = AskSchema(task_id="go_hospital", slots=[], retry_policy=None)

    effective = schema.effective_retry_policy(default_policy=default)

    assert effective.interval == 7.0
    assert effective.limit == 4
    assert effective.on_exceed == OnExceedAction.FALLBACK


def test_ask_schema_from_dict_and_to_dict_roundtrip_like():
    data = {
        "task_id": "go_hospital",
        "slots": [
            {"name": "destination", "kind": "required", "prompt": "要去哪里？"},
            {"name": "department", "kind": "optional"},
            {"name": "hospital_detail", "kind": "clarify", "description": "具体是哪家医院"},
        ],
        "retry_policy": {
            "interval": 4.0,
            "limit": 2,
            "on_exceed": "fallback",
            "adaptive": True,
            "ai_adjust_hook": "emotion",
        },
        "meta": {"scenario": "hospital"},
    }

    schema = AskSchema.from_dict(data)
    assert schema.task_id == "go_hospital"
    assert len(schema.slots) == 3
    assert schema.required_slots()[0].name == "destination"
    assert schema.optional_slots()[0].name == "department"
    assert schema.clarify_slots()[0].name == "hospital_detail"

    effective_policy = schema.effective_retry_policy()
    assert effective_policy.interval == 4.0
    assert effective_policy.limit == 2
    assert effective_policy.on_exceed == OnExceedAction.FALLBACK
    assert effective_policy.adaptive is True
    assert effective_policy.ai_adjust_hook == "emotion"

    # Check serialisation contains key fields.
    out = schema.to_dict()
    assert out["task_id"] == "go_hospital"
    assert len(out["slots"]) == 3
    assert out["retry_policy"]["interval"] == 4.0
    assert out["retry_policy"]["on_exceed"] == "fallback"
    assert out["meta"]["scenario"] == "hospital"













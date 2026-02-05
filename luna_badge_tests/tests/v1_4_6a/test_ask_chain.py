import pytest

from task_engine.ask import (
    AskSlotKind,
    AskSlot,
    AskSchema,
    AskChainBuilder,
)


def _make_schema_for_hospital() -> AskSchema:
    return AskSchema(
        task_id="go_hospital",
        slots=[
            AskSlot(
                name="destination",
                kind=AskSlotKind.REQUIRED,
                prompt_template="你想去哪个医院？",
            ),
            AskSlot(
                name="hospital_detail",
                kind=AskSlotKind.CLARIFY,
                prompt_template="是哪个分院或具体院区？",
            ),
            AskSlot(
                name="department",
                kind=AskSlotKind.OPTIONAL,
                prompt_template="需要看哪个科室？",
            ),
        ],
    )


def test_build_chain_single_required_slot():
    schema = AskSchema(
        task_id="go_hospital",
        slots=[
            AskSlot(
                name="destination",
                kind=AskSlotKind.REQUIRED,
                prompt_template="你想去哪个医院？",
            )
        ],
    )
    builder = AskChainBuilder()
    plan = builder.build_chain(schema, now_ts=1234567890)

    assert plan.task_id == "go_hospital"
    assert plan.chain_timestamp == 1234567890
    assert len(plan.nodes) == 1
    assert plan.entry == plan.exit == plan.nodes[0]
    assert plan.edges == []

    node_id = plan.nodes[0]
    # 节点 ID 应包含时间戳 + ask + 任务 ID + 槽位名
    assert node_id.startswith("1234567890_ask_go_hospital_destination")
    assert node_id in plan.ask_nodes


def test_build_chain_sorts_slots_by_kind_priority():
    schema = _make_schema_for_hospital()
    builder = AskChainBuilder()
    plan = builder.build_chain(schema, now_ts=999999999)

    # REQUIRED -> CLARIFY -> OPTIONAL
    node_ids = plan.nodes
    assert len(node_ids) == 3

    # 提取 slot_name 部分做断言
    # 节点 ID 格式: {timestamp}_ask_{task_id}_{slot_name}
    # 需要从 "ask" 之后提取，因为 slot_name 可能包含下划线
    def extract_slot_name(node_id: str) -> str:
        # 找到 "ask" 之后的部分，格式是 {task_id}_{slot_name}
        parts = node_id.split("_ask_", 1)
        if len(parts) == 2:
            # 去掉 task_id 部分（go_hospital），剩余的就是 slot_name
            task_and_slot = parts[1]
            # task_id 是 "go_hospital"，所以去掉前两个部分
            slot_parts = task_and_slot.split("_")
            # 去掉 task_id 部分（"go", "hospital"），剩余的就是 slot_name
            return "_".join(slot_parts[2:])
        return node_id.split("_")[-1]  # fallback

    slot_names = [extract_slot_name(nid) for nid in node_ids]
    assert slot_names == ["destination", "hospital_detail", "department"]

    # entry/exit 应该对应第一/最后一个节点
    assert plan.entry == node_ids[0]
    assert plan.exit == node_ids[-1]

    # edges 应该依次连接
    assert plan.edges == [
        (node_ids[0], node_ids[1]),
        (node_ids[1], node_ids[2]),
    ]


def test_build_chain_raises_when_no_slots():
    empty_schema = AskSchema(task_id="empty_task", slots=[])
    builder = AskChainBuilder()

    with pytest.raises(ValueError):
        builder.build_chain(empty_schema, now_ts=111111111)


def test_build_chain_timestamp_default_uses_current_time(monkeypatch):
    # 通过 monkeypatch 控制 time.time 返回值
    import time as time_module

    class DummyTime:
        def __init__(self):
            self.called = False

        def time(self):
            self.called = True
            return 1700000000.9  # 将被 int() 成 1700000000

    dummy = DummyTime()
    monkeypatch.setattr(time_module, "time", dummy.time)

    schema = AskSchema(
        task_id="go_hospital",
        slots=[
            AskSlot(
                name="destination",
                kind=AskSlotKind.REQUIRED,
                prompt_template="你想去哪个医院？",
            )
        ],
    )

    builder = AskChainBuilder()
    plan = builder.build_chain(schema)

    assert dummy.called is True
    assert plan.chain_timestamp == 1700000000
    node_id = plan.nodes[0]
    assert node_id.startswith("1700000000_ask_go_hospital_destination")


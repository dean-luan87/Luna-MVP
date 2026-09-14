# tests/test_task_chain_manager.py
from core.flow_engine.flow_types import (
    FlowDefinition,
    FlowNode,
    FlowEdge,
    FlowNodeType,
    FlowContext,
    FlowInstance,
)
from core.flow_engine.runtime import FlowRuntime
from task_chain.task_chain_manager import TaskChainManager


def _dummy_node_executor(ctx: FlowContext, params):
    # 简单记录一下执行轨迹
    log = ctx.data.get("log") or []
    log.append(params.get("label", "node"))
    ctx.data["log"] = log
    return {"status": "success"}


def _make_single_step_instance(task_id: str, user_id: str) -> FlowInstance:
    node = FlowNode(
        id="n1",
        node_type=FlowNodeType.CUSTOM,
        params={"label": f"{task_id}_step"},
        executor=_dummy_node_executor,
    )
    definition = FlowDefinition(
        id=f"def_{task_id}",
        nodes={"n1": node},
        edges=[],
        entry_node_id="n1",
    )
    ctx = FlowContext(
        task_id=task_id,
        user_id=user_id,
        scene_type="test",
        intent="test",
        data={},
    )
    return FlowInstance(
        definition=definition,
        context=ctx,
        current_node_id="n1",
    )


def test_insert_subtask_pauses_parent_and_runs_child():
    runtime = FlowRuntime()
    manager = TaskChainManager(runtime=runtime)

    parent = _make_single_step_instance(task_id="parent", user_id="u1")
    runtime.start(parent)

    assert parent.finished is True
    assert parent.context.data["log"] == ["parent_step"]

    # 重置 parent 状态用于插入任务测试
    parent.finished = False
    parent.paused = False
    parent.context.data["log"] = []

    runtime._instances[parent.context.task_id] = parent  # 手动放回实例池

    child = _make_single_step_instance(task_id="child", user_id="u1")

    manager.insert_subtask(parent_task_id="parent", instance=child)

    # 插入子任务后，父任务应处于 paused 状态
    assert parent.paused is True

    # 子任务应执行完自己的一步
    assert child.context.data["log"] == ["child_step"]
    assert child.finished is True
    assert child.parent_task_id == "parent"


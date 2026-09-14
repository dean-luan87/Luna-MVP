"""
测试：HookScheduler 构建 HookExecutionPlan 的行为。

覆盖点：
- 只为模板声明的 hook_points 构建计划；
- 正确筛选出对应 hook_point 的 Piece；
- 按 priority 升序排序；
- 调用 Piece.condition(context, env) 并按返回值过滤。
"""

from typing import Dict, Any

from composition.hook_scheduler import HookScheduler, HookExecutionPlan
from pieces.registry import TaskPieceRegistry
from pieces.base_piece import TaskPiece, TaskPieceType
from patches.flow_patch import FlowPatch
from pieces.builtin.map_record_piece import create_map_record_piece
from pieces.builtin.staff_assist_piece import create_staff_assist_piece
from pieces.builtin.pre_check_piece import create_pre_check_piece
from pieces.builtin.navigation_enhance_piece import create_navigation_enhance_piece
from pieces.builtin.safety_check_piece import create_safety_check_piece


def _env_aware_condition(context: Any, env: Dict[str, Any]) -> bool:
    """用于测试 condition(env) 的条件函数。"""
    return bool(env.get("enable_pre_check", False))


def _build_dummy_patch(context: Any, env: Dict[str, Any]) -> FlowPatch:
    """占位 patch builder。"""
    from core.flow_engine.flow_types import FlowNode, FlowNodeType
    node = FlowNode(
        id="dummy",
        node_type=FlowNodeType.CUSTOM,
        params={},
    )
    return FlowPatch(
        new_nodes={"dummy": node},
        new_edges=[],
        delete_nodes=[],
        rewire_entry=None,
        rewire_exit=None,
    )


def test_build_plan_filters_by_hook_points_and_sorts_by_priority() -> None:
    registry = TaskPieceRegistry()
    # 手动注册一部分 piece
    registry.register(create_map_record_piece())
    registry.register(create_navigation_enhance_piece())
    registry.register(create_staff_assist_piece())
    registry.register(create_safety_check_piece())

    scheduler = HookScheduler(registry)

    hook_points = ["GO_BEFORE", "REGISTER_BEFORE", "NAV_BEFORE"]

    plan = scheduler.build_plan(hook_points, env={})

    go_pieces = plan.get_pieces_for("GO_BEFORE")
    reg_pieces = plan.get_pieces_for("REGISTER_BEFORE")
    nav_pieces = plan.get_pieces_for("NAV_BEFORE")

    # GO_BEFORE 只应包含 map_record_piece
    assert any(p.id == "map_record_piece" for p in go_pieces)
    # REGISTER_BEFORE 应包含 staff_assist_piece
    assert any(p.id == "staff_assist_piece" for p in reg_pieces)
    # NAV_BEFORE 应包含 navigation_enhance_piece
    assert any(p.id == "navigation_enhance_piece" for p in nav_pieces)

    # priority 应为升序
    if go_pieces:
        priorities = [p.priority for p in go_pieces]
        assert priorities == sorted(priorities)
    if reg_pieces:
        priorities = [p.priority for p in reg_pieces]
        assert priorities == sorted(priorities)
    if nav_pieces:
        priorities = [p.priority for p in nav_pieces]
        assert priorities == sorted(priorities)


def test_build_plan_respects_condition_env_filter() -> None:
    registry = TaskPieceRegistry()
    
    # 创建一个环境感知的 piece
    env_aware_piece = TaskPiece(
        id="env_aware_pre_check_piece",
        hook_point="START_BEFORE",
        piece_type=TaskPieceType.NODE,
        condition=_env_aware_condition,
        builder=_build_dummy_patch,
        priority=30,
    )
    registry.register(env_aware_piece)

    scheduler = HookScheduler(registry)

    hook_points = ["START_BEFORE"]

    # env 未开启时，不应返回该 piece
    plan_off = scheduler.build_plan(hook_points, env={"enable_pre_check": False})
    pieces_off = plan_off.get_pieces_for("START_BEFORE")
    assert len(pieces_off) == 0

    # env 开启时，应返回该 piece
    plan_on = scheduler.build_plan(hook_points, env={"enable_pre_check": True})
    pieces_on = plan_on.get_pieces_for("START_BEFORE")
    assert len(pieces_on) == 1
    assert pieces_on[0].id == "env_aware_pre_check_piece"


def test_build_plan_ignores_pieces_not_in_hook_points() -> None:
    registry = TaskPieceRegistry()
    registry.register(create_map_record_piece())  # GO_BEFORE
    registry.register(create_staff_assist_piece())  # REGISTER_BEFORE
    registry.register(create_pre_check_piece())  # START_BEFORE

    scheduler = HookScheduler(registry)

    # 只声明 GO_BEFORE，不应包含其他 hook 的 piece
    hook_points = ["GO_BEFORE"]
    plan = scheduler.build_plan(hook_points, env={})

    go_pieces = plan.get_pieces_for("GO_BEFORE")
    assert any(p.id == "map_record_piece" for p in go_pieces)

    # START_BEFORE 和 REGISTER_BEFORE 不应出现在计划中
    start_pieces = plan.get_pieces_for("START_BEFORE")
    reg_pieces = plan.get_pieces_for("REGISTER_BEFORE")
    assert len(start_pieces) == 0
    assert len(reg_pieces) == 0


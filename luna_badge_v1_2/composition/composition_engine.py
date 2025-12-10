# composition/composition_engine.py
from __future__ import annotations

from typing import Any, Dict, List, Set, Optional

from composition.patch_utils import apply_task_patch, prune_flow, validate_flow
from composition.hook_scheduler import HookScheduler
from pieces.registry import TaskPieceRegistry

from core.flow_engine.flow_types import FlowDefinition, FlowContext


class CompositionEngine:
    """
    任务链组合引擎：

    - 接收模板骨架生成的 FlowDefinition
    - 使用 HookScheduler 生成执行计划
    - 执行 builder 生成 FlowPatch
    - 按顺序应用 Patch
    - 做一次剪枝 & 验证
    """

    def __init__(self, piece_registry: Optional[TaskPieceRegistry] = None) -> None:
        self._registry = piece_registry or TaskPieceRegistry.create_default_registry()
        self._hook_scheduler = HookScheduler(self._registry)

    def compose(self, flow_def: FlowDefinition, context: FlowContext, env: Dict[str, Any] | None = None) -> FlowDefinition:
        env = env or {}

        # 1. 从 FlowDefinition.metadata 读取 hook_points
        meta_hooks: List[str] = []
        meta_raw = flow_def.metadata.get("hook_points")
        if isinstance(meta_raw, list):
            meta_hooks = list(meta_raw)

        # 2. 从 env 读取 hook_points（保持兼容之前的测试）
        env_hooks: List[str] = []
        env_raw = env.get("hook_points")
        if isinstance(env_raw, list):
            env_hooks = list(env_raw)

        # 3. 合并去重
        all_hooks: List[str] = []
        seen: Set[str] = set()
        for h in meta_hooks + env_hooks:
            if h and h not in seen:
                seen.add(h)
                all_hooks.append(h)

        # 没有 hook 的情况：直接返回，保持原有流程
        if not all_hooks:
            validate_flow(flow_def)
            return flow_def

        # 4. 使用 HookScheduler 构建执行计划
        plan = self._hook_scheduler.build_plan(all_hooks, env=env)

        # 5. 读取 hook_points_detail：attach_node 等信息
        hook_points_detail = flow_def.metadata.get("hook_points_detail", {})
        if not isinstance(hook_points_detail, dict):
            hook_points_detail = {}

        # 6. 按 hook_points 顺序应用每个 Hook 下的 Piece
        for hook_point in all_hooks:
            pieces_for_hook = plan.get_pieces_for(hook_point)
            if not pieces_for_hook:
                continue

            # 读取 attach_node
            detail = hook_points_detail.get(hook_point, {})
            attach_node = detail.get("attach_node")

            # 按计划中的顺序（已排序）应用每个 piece
            for piece in pieces_for_hook:
                # 使用统一的 build_patches 接口
                patches = piece.build_patches(flow_def, attach_node=attach_node)
                # 这里允许一个 Piece 产生多个 Patch，按顺序应用
                for patch in patches:
                    flow_def = apply_task_patch(flow_def, patch)

        flow_def = prune_flow(flow_def, context, env)
        validate_flow(flow_def)
        return flow_def

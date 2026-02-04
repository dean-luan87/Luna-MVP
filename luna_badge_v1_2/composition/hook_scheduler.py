from __future__ import annotations

"""
HookScheduler

职责：
- 根据 Flow 模板声明的 hook_points，结合 TaskPieceRegistry 中的 Piece，
  生成"在每个 Hook 上应该执行哪些 Piece、按什么顺序执行"的执行计划。

输入：
- hook_points: 模板声明的 Hook 列表，例如 ["GO_BEFORE", "REGISTER_BEFORE"]；
- registry: TaskPieceRegistry 实例；
- env: 可选的环境上下文（可以包含 scene_context / task_context / user_profile 等）。

输出：
- Dict[str, List[TaskPiece]]:
  {
      "GO_BEFORE": [piece_a, piece_b, ...],   # 按 priority 升序排序
      "REGISTER_BEFORE": [piece_c],
      ...
  }

注意：
- 只负责"选 Piece + 排序"，不负责做 patch；
- patch 仍由 CompositionEngine / patch_utils 负责。
"""

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional

from pieces.base_piece import TaskPiece
from pieces.registry import TaskPieceRegistry


@dataclass
class HookExecutionPlan:
    """
    Hook 执行计划：
    - mapping: hook_point -> List[TaskPiece]
    """

    mapping: Dict[str, List[TaskPiece]]

    def get_pieces_for(self, hook_point: str) -> List[TaskPiece]:
        return self.mapping.get(hook_point, [])


class HookScheduler:
    """
    Hook 调度器：根据 hook_points 与 PieceRegistry 构造执行计划。
    """

    def __init__(self, registry: TaskPieceRegistry) -> None:
        self._registry = registry

    def build_plan(
        self,
        hook_points: Iterable[str],
        *,
        env: Optional[Dict] = None,
    ) -> HookExecutionPlan:
        """
        生成 Hook 执行计划。

        逻辑：
        1. 只考虑模板声明的 hook_points；
        2. 从 Registry 中取出所有 Piece；
        3. 按 Piece.hook_point 进行归类，过滤掉不在 hook_points 中的；
        4. 对每个 Piece 调用 should_apply(env) 进行条件过滤；
        5. 对每个 Hook 下的 Piece 按 priority 升序排序。
        """
        hook_points_set = set(hook_points or [])

        mapping: Dict[str, List[TaskPiece]] = {hp: [] for hp in hook_points_set}

        # 遍历所有注册的 piece
        for piece in self._registry.iter_pieces():
            hook = getattr(piece, "hook_point", None)
            if not hook or hook not in hook_points_set:
                continue

            # 条件判断（当前版本 env 结构简单，后续可加入 scene_context 等）
            try:
                should = piece.condition(None, env or {})
            except TypeError:
                # 向后兼容：老版本 Piece 没有 env 参数
                try:
                    should = piece.condition(None, {})
                except Exception:
                    should = True

            if not should:
                continue

            mapping[hook].append(piece)

        # 对每个 Hook 下的 Piece 按 priority 排序
        for hook, pieces in mapping.items():
            pieces.sort(key=lambda p: getattr(p, "priority", 100))

        return HookExecutionPlan(mapping=mapping)













# pieces/registry.py
from __future__ import annotations

from typing import Dict, List, Iterable, Any

from pieces.base_piece import TaskPiece
from pieces.builtin.map_record_piece import create_map_record_piece
from pieces.builtin.staff_assist_piece import create_staff_assist_piece
from pieces.builtin.pre_check_piece import create_pre_check_piece
from pieces.builtin.navigation_enhance_piece import create_navigation_enhance_piece
from pieces.builtin.safety_check_piece import create_safety_check_piece
from pieces.builtin.ocr_detect_piece import create_ocr_detect_piece
from pieces.builtin.human_assist_piece import create_human_assist_piece


class TaskPieceRegistry:
    """
    任务积木注册中心：
    - 负责收集所有可用的 TaskPiece
    - 支持按 hook_point / 条件过滤
    """

    def __init__(self) -> None:
        self._pieces: Dict[str, TaskPiece] = {}

    # -------------------------
    # 注册 & 查询
    # -------------------------
    def register(self, piece: TaskPiece) -> None:
        if piece.id in self._pieces:
            # 简单覆盖策略，后续可加入告警/日志
            pass
        self._pieces[piece.id] = piece

    def get(self, piece_id: str) -> TaskPiece | None:
        return self._pieces.get(piece_id)

    def all_pieces(self) -> Iterable[TaskPiece]:
        return self._pieces.values()

    def iter_pieces(self) -> Iterable[TaskPiece]:
        """
        迭代当前注册的所有 Piece 实例。
        """
        return self._pieces.values()

    # -------------------------
    # 按 hook_point 过滤
    # -------------------------
    def by_hook_point(self, hook_point: str) -> List[TaskPiece]:
        return [p for p in self._pieces.values() if p.hook_point == hook_point]

    # -------------------------
    # 按 hook_point + 条件过滤
    # -------------------------
    def available_for(self, hook_point: str, context: Any, env: dict) -> List[TaskPiece]:
        result: List[TaskPiece] = []
        for piece in self._pieces.values():
            if piece.hook_point != hook_point:
                continue
            try:
                if piece.condition(context, env):
                    result.append(piece)
            except Exception:
                # 条件函数异常时，保守地认为该 piece 不可用
                continue
        return result

    # -------------------------
    # 工厂方法：创建默认注册中心
    # -------------------------
    @classmethod
    def create_default_registry(cls) -> "TaskPieceRegistry":
        """
        工厂方法：构建一个默认的积木注册中心，并注册内置 pieces。

        后续可以把其他 builtin piece 一并注册进来。
        """
        registry = cls()

        # 注册已有内置积木
        registry.register(create_map_record_piece())
        registry.register(create_staff_assist_piece())

        # 注册新增的五大通用 Piece
        registry.register(create_pre_check_piece())
        registry.register(create_navigation_enhance_piece())
        registry.register(create_safety_check_piece())
        registry.register(create_ocr_detect_piece())
        registry.register(create_human_assist_piece())

        return registry

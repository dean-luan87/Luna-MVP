from __future__ import annotations

"""
OcrDetectPiece

作用：
- 在需要依赖文字信息（站名、科室牌、标识牌等）的步骤前，
  强制插入一次 OCR 检测动作；
- 为后续场景判断 / 任务链选择 / 目标确认提供文本输入。

Hook：
- OCR_BEFORE：OCR 相关节点前。

当前版本（v1.4.5C-1）：
- 仅提供骨架与元数据，不实现具体业务逻辑。
"""

from typing import Any, Dict

from pieces.base_piece import TaskPiece, TaskPieceType
from patches.flow_patch import FlowPatch
from core.flow_engine.flow_types import FlowNode, FlowNodeType


HOOK_POINT_OCR_BEFORE = "OCR_BEFORE"


def _always_enabled(context: Any, env: Dict[str, Any]) -> bool:
    """条件：当前版本无条件启用。"""
    return True


def _build_ocr_detect_patch(context: Any, env: Dict[str, Any]) -> FlowPatch:
    """
    为当前流程插入一个"OCR 检测节点"（占位实现）。
    后续在 C-3 中再补充具体实现。
    """
    node_id = "ocr_detect"
    node = FlowNode(
        id=node_id,
        node_type=FlowNodeType.OCR_READ,
        params={
            "action": "ocr_detect",
            "description": "OCR 检测前置（占位实现）",
        },
    )
    patch = FlowPatch(
        new_nodes={node_id: node},
        new_edges=[],
        delete_nodes=[],
        rewire_entry=None,
        rewire_exit=None,
    )
    return patch


def create_ocr_detect_piece() -> TaskPiece:
    """工厂函数：返回一个 OcrDetectPiece 实例。"""
    return TaskPiece(
        id="ocr_detect_piece",
        hook_point=HOOK_POINT_OCR_BEFORE,
        piece_type=TaskPieceType.NODE,
        condition=_always_enabled,
        builder=_build_ocr_detect_patch,
        priority=60,
        description="在 OCR 相关节点前插入 OCR 检测节点的任务积木",
    )


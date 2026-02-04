# pieces/base_piece.py
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Optional, Iterable, TYPE_CHECKING

from patches.flow_patch import FlowPatch

if TYPE_CHECKING:
    from core.flow_engine.flow_types import FlowDefinition
    from composition.patch_utils import TaskPatch


class TaskPieceType(str, Enum):
    """
    TaskPiece 的类型说明：
    - NODE:     插入一个单节点
    - SUBFLOW:  插入一段子流程（多个节点+边）
    - DECORATOR:在现有节点前后包裹逻辑
    - REWRITE: 重写 / 替换一段子流程
    """
    NODE = "node"
    SUBFLOW = "subflow"
    DECORATOR = "decorator"
    REWRITE = "rewrite"


@dataclass
class TaskPiece:
    """
    TaskPiece = 一块可复用的"任务积木"。

    关键要素：
    - id:         唯一标识
    - hook_point: 要挂载到模板骨架的哪个 Hook 上
    - piece_type: 积木类型（NODE / SUBFLOW / DECORATOR / REWRITE）
    - condition:  是否在当前 context/env 下启用
    - builder:    在当前 context/env 下生成一个 FlowPatch
    - priority:   优先级，数字越小优先级越高（默认 50）
    """
    id: str
    hook_point: str
    piece_type: TaskPieceType

    # condition(context, env) -> bool
    condition: Callable[[Any, dict], bool]

    # builder(context, env) -> FlowPatch
    builder: Callable[[Any, dict], FlowPatch]

    # 新增：优先级，数字越小优先级越高
    priority: int = 50

    # 可选：简单描述，便于调试与可视化
    description: Optional[str] = None

    def build_patches(
        self,
        flow_def: "FlowDefinition",
        *,
        attach_node: Optional[str] = None,
    ) -> Iterable["TaskPatch"]:
        """
        统一的 Patch 构建接口。

        默认适配逻辑：
        - 如果子类实现了 build_task_patches(...)，优先使用；
        - 否则，如果实现了 build_patch(...)（返回 new_nodes, new_edges），则包一层 TaskPatch；
        - 再否则，尝试使用 builder(context, env) -> FlowPatch，转换为 TaskPatch；
        - 最后，返回空列表（不做任何修改）。

        这样可以渐进式迁移老 Piece，而不强迫一次性重写。
        """
        from composition.patch_utils import TaskPatch
        from core.flow_engine.flow_types import FlowNode, FlowEdge

        # 新接口优先：build_task_patches(flow_def, attach_node=...) -> Iterable[TaskPatch]
        if hasattr(self, "build_task_patches"):
            patches = self.build_task_patches(flow_def, attach_node=attach_node)
            # 假定子类返回 Iterable[TaskPatch]
            return list(patches)  # 保证是可重用的列表

        # 兼容旧接口：build_patch(flow_def) -> (new_nodes, new_edges)
        if hasattr(self, "build_patch"):
            try:
                result = self.build_patch(flow_def)
                if isinstance(result, tuple) and len(result) == 2:
                    new_nodes, new_edges = result
                    if new_nodes or new_edges:
                        # 确保 new_nodes 是 List[FlowNode]
                        if isinstance(new_nodes, dict):
                            new_nodes_list = list(new_nodes.values())
                        elif isinstance(new_nodes, list):
                            new_nodes_list = new_nodes
                        else:
                            new_nodes_list = []

                        # 确保 new_edges 是 List[FlowEdge]
                        if not isinstance(new_edges, list):
                            new_edges = []

                        return [
                            TaskPatch(
                                new_nodes=new_nodes_list,
                                new_edges=new_edges,
                                attach_node=attach_node,
                            )
                        ]
            except Exception:
                pass

        # 兼容 builder(context, env) -> FlowPatch
        try:
            # 使用空的 context 和 env 调用 builder（保持向后兼容）
            flow_patch: FlowPatch = self.builder(None, {})
            if flow_patch.new_nodes or flow_patch.new_edges:
                # 将 FlowPatch 转换为 TaskPatch
                new_nodes_list = list(flow_patch.new_nodes.values())
                return [
                    TaskPatch(
                        new_nodes=new_nodes_list,
                        new_edges=flow_patch.new_edges,
                        attach_node=attach_node,
                    )
                ]
        except Exception:
            pass

        # 默认：不产生任何 patch
        return []

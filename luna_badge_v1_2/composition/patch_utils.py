# composition/patch_utils.py
from __future__ import annotations

from typing import Any, Optional, List
from copy import deepcopy

from patches.flow_patch import FlowPatch

from core.flow_engine.flow_types import FlowDefinition, FlowContext, FlowEdge


def _verify_attach_node(flow_def: FlowDefinition, attach_node: Optional[str]) -> None:
    """
    校验 attach_node 是否存在于当前 FlowDefinition 中。

    - attach_node 为 None 时，直接返回
    - attach_node 不存在时，抛异常，避免静默失败
    """
    if attach_node is None:
        return
    if attach_node not in flow_def.nodes:
        available = ", ".join(flow_def.nodes.keys())
        raise ValueError(
            f"attach_node '{attach_node}' not found in flow_def.nodes. "
            f"Available nodes: {available}"
        )


def apply_patch(
    flow_def: FlowDefinition,
    patch: FlowPatch,
    attach_node: Optional[str] = None,
) -> FlowDefinition:
    """
    将 FlowPatch 应用到 FlowDefinition 上。

    处理顺序：
    1. 校验 attach_node 是否存在（如有）
    2. 合并 new_nodes
    3. 基于 attach_node 做"插队式重接"（只处理第一个 new_node）
    4. 合并 new_edges
    5. 删除 delete_nodes 及相关边
    6. rewire_entry / rewire_exit 后续需要时再扩展
    """
    from core.flow_engine.flow_types import FlowDefinition as FlowDefType

    # 1. attach_node 校验（在添加新节点之前，使用原始 flow_def 验证）
    _verify_attach_node(flow_def, attach_node)

    # 深拷贝避免修改原对象
    new_nodes = deepcopy(flow_def.nodes)
    new_edges = deepcopy(flow_def.edges)
    new_entry_node_id = flow_def.entry_node_id
    new_hook_points = deepcopy(flow_def.hook_points)
    new_metadata = deepcopy(flow_def.metadata)

    # 2. 新增节点
    for node_id, node in patch.new_nodes.items():
        new_nodes[node_id] = deepcopy(node)

    # 3. 基于 attach_node 的边重接逻辑
    #
    # 场景：
    #   原: attach_node -> X1, attach_node -> X2
    #   新: attach_node -> new_node -> X1, attach_node -> new_node -> X2
    #
    # 约定：
    #   - 只针对第一个 new_node 做插队（map_record 场景足够用）
    #   - 若 attach_node 没有出边，则只连接 attach_node -> new_node（不影响其它）

    if attach_node is not None and patch.new_nodes:
        new_node_ids = list(patch.new_nodes.keys())
        main_new_node_id = new_node_ids[0]

        # 找出 attach_node 的所有出边
        old_out_edges: List[FlowEdge] = [
            e for e in new_edges if e.source_id == attach_node
        ]
        other_edges: List[FlowEdge] = [
            e for e in new_edges if e.source_id != attach_node
        ]

        new_rewired_edges: List[FlowEdge] = []

        if old_out_edges:
            # attach_node 原来有出边，执行"插队重接"
            # 1) attach_node -> main_new_node （统一用 None 或 "success"，这里用 None）
            new_rewired_edges.append(
                FlowEdge(
                    source_id=attach_node,
                    target_id=main_new_node_id,
                    condition=None,
                )
            )

            # 2) main_new_node -> 每一个原 target，保留原 condition
            for old in old_out_edges:
                new_rewired_edges.append(
                    FlowEdge(
                        source_id=main_new_node_id,
                        target_id=old.target_id,
                        condition=old.condition,
                    )
                )
        else:
            # attach_node 没有出边：仅添加 attach_node -> new_node 边
            new_rewired_edges.append(
                FlowEdge(
                    source_id=attach_node,
                    target_id=main_new_node_id,
                    condition=None,
                )
            )

        # 使用"其他边 + 新重接边"替换原边集合
        new_edges = other_edges + new_rewired_edges

    # 4. 合并 patch.new_edges（patch 显式新增的边）
    # 注意：这一步在重接之后执行，可以允许显式覆盖部分关系
    for edge in patch.new_edges:
        # 检查边是否已存在
        exists = any(
            e.source_id == edge.source_id and e.target_id == edge.target_id
            for e in new_edges
        )
        if not exists:
            new_edges.append(deepcopy(edge))

    # 5. 删除节点及相关边
    if patch.delete_nodes:
        delete_set = set(patch.delete_nodes)
        for nid in delete_set:
            new_nodes.pop(nid, None)
        new_edges = [
            e for e in new_edges
            if e.source_id not in delete_set and e.target_id not in delete_set
        ]

    # 6. rewire_entry / rewire_exit 暂时不实现，如后续确有需要再启用
    if patch.rewire_entry is not None:
        # 如果新入口节点存在，则更新
        if patch.rewire_entry in new_nodes:
            new_entry_node_id = patch.rewire_entry

    # 创建新的 FlowDefinition
    return FlowDefType(
        id=flow_def.id,
        nodes=new_nodes,
        edges=new_edges,
        entry_node_id=new_entry_node_id,
        hook_points=new_hook_points,
        metadata=new_metadata,
    )


def prune_flow(
    flow_def: FlowDefinition,
    context: FlowContext | None = None,
    env: dict | None = None,
) -> FlowDefinition:
    """
    根据上下文/环境，对 FlowDefinition 做剪枝。

    当前为骨架版本：不做任何修改，直接返回。
    """
    return flow_def


def validate_flow(flow_def: FlowDefinition) -> None:
    """
    验证组合后的 FlowDefinition 是否合法。

    当前实现保持最小化：
    - 至少校验 nodes 字典与 edges 列表存在
    - 不做严格结构校验，后续可按需要补充
    """
    if not hasattr(flow_def, "nodes") or not hasattr(flow_def, "edges"):
        raise ValueError("FlowDefinition 缺少 nodes 或 edges 属性")


# ========================================
# TaskPatch 统一抽象（C-3 新增）
# ========================================

from dataclasses import dataclass
from typing import List


@dataclass
class TaskPatch:
    """
    统一的任务链 Patch 抽象。

    - new_nodes: 要新增的节点列表；
    - new_edges: 要新增的边列表；
    - attach_node: 可选插入点语义（用于边重接），如果为 None，则沿用原有 apply_patch 的默认行为。
    """

    new_nodes: List[FlowNode]
    new_edges: List[FlowEdge]
    attach_node: Optional[str] = None


def apply_task_patch(flow_def: FlowDefinition, patch: TaskPatch) -> FlowDefinition:
    """
    基于 TaskPatch 应用一次 patch。

    注意：
    - 内部仍然调用现有的 apply_patch，以保持老逻辑不变；
    - attach_node 没传则沿用 apply_patch 内部的默认行为。
    """
    # 将 TaskPatch 转换为 FlowPatch（适配现有接口）
    # FlowPatch.new_nodes 是 Dict[str, FlowNode]，需要转换
    new_nodes_dict: Dict[str, FlowNode] = {}
    for node in patch.new_nodes:
        new_nodes_dict[node.id] = node

    flow_patch = FlowPatch(
        new_nodes=new_nodes_dict,
        new_edges=patch.new_edges,
        delete_nodes=[],
        rewire_entry=None,
        rewire_exit=None,
    )

    # 调用现有的 apply_patch
    return apply_patch(
        flow_def=flow_def,
        patch=flow_patch,
        attach_node=patch.attach_node,
    )

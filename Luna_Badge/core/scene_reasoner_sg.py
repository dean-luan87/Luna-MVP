# core/scene_reasoner_sg.py
"""
基于 SceneGraph 的简单场景推理器
输出结构：
{
  "has_danger": bool,
  "has_stairs": bool,
  "primary_direction": "forward" / "left" / "right" / "stop",
  "confidence": 0.0-1.0,
  "message": "可以直接播报的一句话"
}
"""

from __future__ import annotations
from typing import Dict, Any, List

from .scene_graph import SceneGraph, SGNode, SGRelation


class SceneGraphReasoner:
    @staticmethod
    def reason(scene_graph: SceneGraph) -> Dict[str, Any]:
        nodes: List[SGNode] = scene_graph.nodes
        rels: List[SGRelation] = scene_graph.relations

        # 索引
        node_by_id = {n.id: n for n in nodes}
        regions_of_node = {n.id: [] for n in nodes}
        for r in rels:
            if r.type == "in_region":
                regions_of_node[r.source].append(r.target)

        has_danger = False
        has_stairs = False
        danger_in_front = False
        danger_left = False
        danger_right = False

        # 找出 danger 节点及其区域
        for n in nodes:
            if n.type != "danger":
                continue
            has_danger = True
            if n.cls == "stairs":
                has_stairs = True

            rids = regions_of_node.get(n.id, [])
            # 前方 = center + far/near/mid 组合
            in_center = any("region_center" in rid for rid in rids)
            in_left = any("region_left" in rid for rid in rids)
            in_right = any("region_right" in rid for rid in rids)

            if in_center:
                danger_in_front = True
            if in_left:
                danger_left = True
            if in_right:
                danger_right = True

        # 简单决策逻辑
        direction = "forward"
        msg = "当前路径安全，可以继续前进。"
        conf = 0.6

        if has_danger:
            conf = 0.8
            if danger_in_front and not (danger_left or danger_right):
                direction = "stop"
                msg = "注意，前方有危险，请暂时停下。"
            elif danger_in_front and danger_left and not danger_right:
                direction = "right"
                msg = "前方与左侧都有危险，请向右侧稍微绕行。"
            elif danger_in_front and danger_right and not danger_left:
                direction = "left"
                msg = "前方与右侧都有危险，请向左侧稍微绕行。"
            elif danger_left and not (danger_in_front or danger_right):
                direction = "forward"
                msg = "左侧有一些障碍物，当前路径仍可前行。"
            elif danger_right and not (danger_in_front or danger_left):
                direction = "forward"
                msg = "右侧有一些障碍物，当前路径仍可前行。"

        if has_stairs:
            # 优先播报台阶
            if danger_in_front:
                msg = "前方有台阶，请放慢速度，小心脚下。"
            else:
                msg = "附近有台阶，请注意脚下。"

        return {
            "has_danger": has_danger,
            "has_stairs": has_stairs,
            "primary_direction": direction,
            "confidence": conf,
            "message": msg,
        }


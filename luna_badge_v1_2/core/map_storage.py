"""
Map Storage module (v1.3).

用于预留 mini-map 能力：
- v1.3 增加支持存储 SceneGraph
- 未来可扩展为空间拓扑、室内地图等
"""

from typing import List

from core.scene_output import SceneState
from core.scene_graph import SceneGraph


class MapStorage:
    def __init__(self, max_nodes: int = 100):
        self.max_nodes = max_nodes
        self._nodes: List[SceneState] = []
        self._scene_graphs: List[SceneGraph] = []  # v1.3 新增：SceneGraph 存储

    def add_node(self, scene_state: SceneState) -> None:
        """
        将当前场景状态作为一个"地图节点"存储。
        """
        self._nodes.append(scene_state)
        if len(self._nodes) > self.max_nodes:
            self._nodes.pop(0)

    def get_recent_nodes(self, n: int = 10) -> List[SceneState]:
        """
        返回最近 n 个节点。
        """
        if n <= 0:
            return []
        return self._nodes[-n:]

    def add_scene_graph(self, scene_graph: SceneGraph) -> None:
        """
        v1.3 新增：将 SceneGraph 作为地图节点存储。
        """
        self._scene_graphs.append(scene_graph)
        if len(self._scene_graphs) > self.max_nodes:
            self._scene_graphs.pop(0)

    def get_recent_scene_graphs(self, n: int = 10) -> List[SceneGraph]:
        """
        v1.3 新增：返回最近 n 个 SceneGraph。
        """
        if n <= 0:
            return []
        return self._scene_graphs[-n:]


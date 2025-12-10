# scene_map_manager.py

import json
import time
from core.mapping.map_node import MapNode


class SceneMapManager:
    def __init__(self):
        self.current_map = []
        self.scene_id = None

    def start_new_scene(self):
        self.scene_id = f"route_{time.strftime('%Y_%m_%d_%H%M%S')}"
        self.current_map = []

    def add_node(self, node: MapNode):
        self.current_map.append(node)

    def export_map(self, output_dir="."):
        """
        导出地图为 JSON 文件
        """
        data = {
            "scene_id": self.scene_id,
            "nodes": [n.to_dict() for n in self.current_map]
        }
        filename = f"{output_dir}/{self.scene_id}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return filename

    def get_map_data(self):
        """
        获取当前地图数据（用于可视化等）
        """
        return {
            "scene_id": self.scene_id,
            "nodes": [n.to_dict() for n in self.current_map]
        }















# map_node.py


class MapNode:
    def __init__(self, node_type, direction, distance, label="", image_path=None):
        self.type = node_type
        self.direction = direction
        self.distance = distance
        self.label = label
        self.image_path = image_path

    def to_dict(self):
        return {
            "type": self.type,
            "direction": self.direction,
            "distance": self.distance,
            "label": self.label,
            "image": self.image_path
        }











class NodeBank:
    """
    长期节点存储（真正的长期记忆）
    """
    def __init__(self):
        self.nodes = {}  # {node_id: node_dict}

    def add_node(self, node):
        self.nodes[node["id"]] = node

    def get_similar_node(self, embedding):
        # TODO: similarity search
        return None


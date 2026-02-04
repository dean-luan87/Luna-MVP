class MapMergeEngine:
    """
    将新视觉节点与旧地图融合
    """
    def __init__(self, node_bank, map_cache):
        self.node_bank = node_bank
        self.map_cache = map_cache

    def merge_new_node(self, observed_node):
        # TODO: drift score / node update
        pass


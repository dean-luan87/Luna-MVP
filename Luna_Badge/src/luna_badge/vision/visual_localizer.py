class VisualLocalizer:
    """
    基于视觉 Node → 当前定位（弱SLAM）
    """
    def __init__(self, node_bank):
        self.node_bank = node_bank

    def locate(self, frame_features):
        # TODO: similarity search
        return None


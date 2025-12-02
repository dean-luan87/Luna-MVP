class SessionCache:
    """
    本次导航临时节点（施工、临时障碍）
    不写入长期地图
    """
    def __init__(self):
        self.transients = []

    def add_transient(self, node):
        self.transients.append(node)


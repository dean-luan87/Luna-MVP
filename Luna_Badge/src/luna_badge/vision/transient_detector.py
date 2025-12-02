class TransientDetector:
    """
    检测临时节点（施工/积水/倒地障碍）
    仅进入 session_cache，不进入长期地图
    """
    def detect(self, frame):
        return []


class MapCache:
    """
    供 SLAM 校正使用的短期地图缓存
    """
    def __init__(self):
        self.cache = {}

    def update(self, key, value):
        self.cache[key] = value


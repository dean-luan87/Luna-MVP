class NavigatorAdapter:
    """
    给任务链/上层模块的统一封装接口
    """
    def __init__(self, controller):
        self.controller = controller

    def run(self, start, end, maps, session_cache):
        return self.controller.navigate(start, end, maps, session_cache)


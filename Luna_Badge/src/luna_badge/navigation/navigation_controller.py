class NavigationController:
    """
    对接任务链，作为导航主入口
    """
    def __init__(self, planner, session_adjust):
        self.planner = planner
        self.session_adjust = session_adjust

    def navigate(self, start, end, long_term_map, session_cache):
        path = self.planner.plan(start, end, long_term_map)
        path = self.session_adjust.adjust(path, session_cache.transients)
        return path


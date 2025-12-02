class AuthorityRouteEngine:
    """
    选择"最权威路线"
    多次访问 → 自动选择成功率最高路线
    """
    def __init__(self, path_history):
        self.path_history = path_history

    def choose_best(self, target):
        return self.path_history.get_best_route(target)


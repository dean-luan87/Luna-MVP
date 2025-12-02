class PathHistory:
    """
    长期路线记录（用于权威路线选择）
    """
    def __init__(self):
        self.records = []  # list of {dest_id, score, path}

    def add_path(self, record):
        self.records.append(record)

    def get_best_route(self, dest_id):
        # TODO: scoring
        return None


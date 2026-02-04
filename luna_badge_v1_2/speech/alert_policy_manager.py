"""
播报策略层：
- 冷却时间
- 用户习惯
- 不同级别事件过滤
"""


class AlertPolicyManager:
    def __init__(self):
        self.history = []

    def should_speak(self, event):
        return True

    def register_speak(self, event):
        self.history.append(event)


























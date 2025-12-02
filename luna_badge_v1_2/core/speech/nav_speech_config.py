"""
Navigation Speech Config (v1.3.0)

导航语音策略配置
"""

# ========== 最小播报间隔（秒）==========

COOLDOWN = {
    "STOP": 0.5,          # 高危，可更频繁（但需要 0.5 秒防抖）
    "HARD_LEFT": 2.0,
    "HARD_RIGHT": 2.0,
    "SLIGHT_LEFT": 3.0,
    "SLIGHT_RIGHT": 3.0,
    "FORWARD": 5.0,       # 直行最不频繁，只在状态改变时提示
    "REPLAN": 2.0,
    "DEFAULT": 3.0,       # 默认冷却时间
}

# ========== 导航决策优先级（数字越大优先级越高）==========

PRIORITY = {
    "STOP": 3,            # 最高优先级
    "REPLAN": 3,          # 重规划也是最高优先级
    "HARD_LEFT": 2,
    "HARD_RIGHT": 2,
    "SLIGHT_LEFT": 1,
    "SLIGHT_RIGHT": 1,
    "FORWARD": 0,         # 最低优先级
}

# ========== 语气风格 ==========

STYLE = {
    "STOP": "alert",      # 警告语气
    "REPLAN": "alert",    # 警告语气
    "HARD_LEFT": "alert", # 稍紧急
    "HARD_RIGHT": "alert", # 稍紧急
    "SLIGHT_LEFT": "calm",  # 平稳
    "SLIGHT_RIGHT": "calm", # 平稳
    "FORWARD": "calm",    # 平稳
}

# ========== 默认中文文案模板 ==========

TEMPLATES = {
    "FORWARD": "前方可通行，请直行。",
    "SLIGHT_LEFT": "左侧稍微更通畅，请向左一点。",
    "HARD_LEFT": "左前方更通畅，请向左移动。",
    "SLIGHT_RIGHT": "右侧稍微更通畅，请向右一点。",
    "HARD_RIGHT": "右前方更通畅，请向右移动。",
    "STOP": "前方无法通行，请原地停下。",
    "REPLAN": "路径不可行，正在重新规划。",
}

# ========== STOP 高危加重提示 ==========

STOP_DANGER_MESSAGE = "前方存在危险，请立即停下。"

# ========== 调试开关 ==========

DEBUG_NAV_SPEECH = False










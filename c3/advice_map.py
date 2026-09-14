# -*- coding: utf-8 -*-
"""
C3.x v0 advice_id -> tendency mapping.
Only mapped advice_ids are eligible for learning.
"""

# v0: 启用最小子集（2-3个），其余不学
ADVICE_TO_TENDENCY = {
    "REMIND_PATH_CLEAR": "减少路径确认类语音提醒",
    "REMIND_NO_OBSTACLE": "减少无障碍状态播报",
    "CONFIRM_STRAIGHT": "降低直行确认密度",
}

ADVICE_TO_CATEGORY = {
    "REMIND_PATH_CLEAR": "提醒频率类建议",
    "REMIND_NO_OBSTACLE": "提醒频率类建议",
    "CONFIRM_STRAIGHT": "路径确认建议",
}

# 绝对禁止映射
FORBIDDEN_ADVICE_IDS = {
    "ADVISORY",
    "SAFETY_ALERT",
    "REDLINE",
    "PROTECTION",
}

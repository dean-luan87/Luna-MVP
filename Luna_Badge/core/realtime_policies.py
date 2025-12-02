"""
Luna Badge 实时响应系统 - 默认策略规则
动作格式：'action:param' 或 'action'
"""

DEFAULT_POLICY_RULES = [
    {
        "when": "vision.get('crowdLevel', 0) >= 2",
        "do": ["tts:前方拥挤，请靠右"],
        "cooldownMs": 2000,
        "priority": 90
    },
    {
        "when": "vision.get('passable', True) == False",
        "do": ["tts:前方不可通行，建议右转"],
        "priority": 95
    },
    {
        "when": "audio.get('keyword') == 'start_nav'",
        "do": ["nav.start"],
        "priority": 80
    },
    {
        "when": "vision.get('sign', {}).get('type') == 'toilet'",
        "do": ["tts:检测到洗手间，就在前方"],
        "priority": 60
    },
    {
        "when": "vision.get('stepDetected', False) == True",
        "do": ["tts:⚠️ 前方有台阶，请小心"],
        "cooldownMs": 3000,
        "priority": 95
    },
    {
        "when": "vision.get('hazardsCount', 0) > 0",
        "do": ["tts:⚠️ 检测到危险区域，请谨慎前行"],
        "cooldownMs": 3000,
        "priority": 95
    },
    {
        "when": "vision.get('direction') == 'left'",
        "do": ["tts:请向左转"],
        "cooldownMs": 2000,
        "priority": 70
    },
    {
        "when": "vision.get('direction') == 'right'",
        "do": ["tts:请向右转"],
        "cooldownMs": 2000,
        "priority": 70
    }
]


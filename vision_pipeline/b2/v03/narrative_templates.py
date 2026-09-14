# vision_pipeline/b2/v03/narrative_templates.py
from __future__ import annotations

TEMPLATES = {
    "S": "{summary}",

    "M": "{summary}。主要依据：{dominant}。",

    "L": "{summary}。窗口：{window}。主要依据：{dominant}。变化顺序：{sequence}。"
}

# 因子中文名称（你可替换成更产品化的话术）
FACTOR_CN = {
    "env": "环境",
    "path": "路面",
    "people": "人流",
    "motion": "运动状态",
    "event": "突发事件",
}


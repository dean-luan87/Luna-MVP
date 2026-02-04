# core/task_intent.py
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
import re
import uuid
import time


@dataclass
class TaskIntent:
    """
    用户任务意图的统一结构。
    """
    intent_id: str
    raw_text: str
    intent_type: str          # "NAVIGATE", "CROSS_STREET", "FIND_POI", ...
    target_name: Optional[str] = None
    target_category: Optional[str] = None  # "toilet", "registration", "store", ...
    priority: str = "normal"               # "normal" / "high"
    created_at: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        return d


class TaskIntentParser:
    """
    任务意图解析器：
    - 不做复杂场景推理
    - 只关注"你要干什么 + 找什么目标"
    """

    # 一些常见目标词的归一化映射
    TOILET_KEYWORDS = ("厕所", "卫生间", "洗手间", "WC", "wc", "restroom", "toilet")
    CROSSING_KEYWORDS = ("过马路", "过这条马路", "过对面", "过斑马线", "穿过马路")

    @classmethod
    def parse(cls, text: str) -> Optional[TaskIntent]:
        if not text:
            return None
        text = text.strip()

        intent_id = uuid.uuid4().hex[:8]
        now = time.time()

        # --- 1. 过马路相关 ---
        if any(k in text for k in cls.CROSSING_KEYWORDS):
            return TaskIntent(
                intent_id=intent_id,
                raw_text=text,
                intent_type="CROSS_STREET",
                target_name=None,
                target_category="street_crossing",
                priority="high",
                created_at=now,
            )

        # --- 2. 厕所/卫生间 ---
        if any(k in text for k in cls.TOILET_KEYWORDS):
            # 如："带我去厕所"、"帮我找洗手间"
            return TaskIntent(
                intent_id=intent_id,
                raw_text=text,
                intent_type="NAVIGATE",
                target_name="厕所",
                target_category="toilet",
                priority="high",
                created_at=now,
            )

        # --- 3. 通用导航：带我去 / 导航到 / 我想去 / 找到 ---
        # 例如：
        #  "带我去挂号窗口"
        #  "带我去711便利店"
        #  "导航到分诊台"
        #  "我想去地铁站"
        patterns = [
            r"^带我去(.+)$",
            r"^帮我找(?:到)?(.+)$",
            r"^导航(?:到)?(.+)$",
            r"^我想去(.+)$",
            r"^去(.+)$",
        ]
        for p in patterns:
            m = re.match(p, text)
            if m:
                target = m.group(1).strip()
                # 去掉多余结尾词，如"那里"、"那边"
                target = re.sub(r"(那边|那里|这边|这儿|那儿)$", "", target).strip()
                if not target:
                    # 虽然匹配了，但没有目标，视为无效
                    break

                return TaskIntent(
                    intent_id=intent_id,
                    raw_text=text,
                    intent_type="NAVIGATE",
                    target_name=target,
                    target_category=None,  # 交给后续模块做更细分类
                    priority="normal",
                    created_at=now,
                )

        # --- 4. 模糊任务：不清楚要去哪，只能当普通描述 ---
        # 后续可以扩展这里，引导用户补充
        return None


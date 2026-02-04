from dataclasses import dataclass
from typing import Optional


@dataclass
class IntentResult:
    intent: str
    answer: Optional[str] = None


class IntentParser:
    """
    简单规则解析：
    - 对 Query：识别 "是/好/结束" → yes；"不要/继续" → no
    - 对普通指令：识别 "停止导航/结束导航" 等
    """

    def parse(self, text: str) -> dict:
        lower = text.strip().lower()
        if not lower:
            return {"intent": "none"}

        if any(k in lower for k in ["是", "好的", "结束", "stop", "ok"]):
            return {"intent": "answer", "answer": "yes"}

        if any(k in lower for k in ["不用", "不要", "继续", "no"]):
            return {"intent": "answer", "answer": "no"}

        if "停止导航" in lower or "结束导航" in lower:
            return {"intent": "stop_navigation"}

        if "开始导航" in lower or "继续导航" in lower:
            return {"intent": "start_navigation"}

        return {"intent": "unknown"}


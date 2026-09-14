from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Advice:
    advice_id: str
    category: str
    text: str
    confidence: float
    evidence: Dict[str, Any]
    is_safety: bool = False


@dataclass
class AdviceTask:
    task_type: str
    context: Dict[str, Any]

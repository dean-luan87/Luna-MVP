from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List, Optional
import json


@dataclass
class TimelineFrame:
    ts: float
    entities: Dict[str, Any]
    tasks: List[Dict[str, Any]]
    c_decision: Dict[str, Any]
    signals: List[Dict[str, Any]] = field(default_factory=list)
    roi_debug: Dict[str, Any] = field(default_factory=dict)
    map_download_debug: Dict[str, Any] = field(default_factory=dict)
    roi_perception_debug: Dict[str, Any] = field(default_factory=dict)
    roi_learning_debug: Dict[str, Any] = field(default_factory=dict)
    roi_confirmation_debug: Dict[str, Any] = field(default_factory=dict)
    roi_manual_debug: Dict[str, Any] = field(default_factory=dict)
    visual_semantic_debug: Optional[Dict[str, Any]] = None
    attention_debug: Dict[str, Any] = field(default_factory=dict)
    vision_interpretation: Optional[Dict[str, Any]] = None
    pal_debug: Dict[str, Any] = field(default_factory=dict)
    pal_roi_debug: Dict[str, Any] = field(default_factory=dict)
    advice_budget_debug: Optional[Dict[str, Any]] = None

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

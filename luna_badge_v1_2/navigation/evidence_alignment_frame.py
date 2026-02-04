"""
Evidence Alignment Frame (v1.4.8 Step 9)

定义"时间 × 空间"对齐后的最小证据帧结构。

重要禁令：
- Step 9 不得参与任何实时决策
- 不允许修改 Step 4 / Step 8 的任何已有代码
- 只通过事件或公开接口读取数据
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


@dataclass
class EvidenceAlignmentFrame:
    """
    证据对齐帧：时间侧（Step 8） × 空间侧（Step 4）
    
    注意：不允许存原始图像或大文本内容。
    """
    ts: float
    scene: str
    
    # 时间侧（来自 Step 8 / Step 5）
    active_authority: str
    candidate_authority: Optional[str]
    confidence: Dict[str, float]  # {"VISUAL": 0.8, "MAP_VISION": 0.6, "GPS": 0.3}
    takeover_state: str           # IDLE / CANDIDATE / LOCKING / TAKEN / COOLDOWN
    hint_active: bool
    
    # 空间侧（来自 Step 4）
    local_map_id: Optional[str]              # 当前本地地图 ID
    recent_node_ids: List[str]               # 最近的节点 ID 列表
    landmark_ids: List[str]                  # 相关地标 ID 列表
    match_scores: Dict[str, float]           # 地标匹配分数 {"landmark_label": 0.82}
    
    # 可选解释信息
    reason_trace: List[str]
    
    def to_dict(self) -> Dict:
        """转换为字典（用于序列化）"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "EvidenceAlignmentFrame":
        """从字典创建（用于反序列化）"""
        return cls(**data)







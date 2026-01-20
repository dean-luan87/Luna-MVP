"""
Navigation Foundation Events (v1.4.8 Step 1-5)

统一事件定义，用于插桩与后续接管准备。
当前阶段：只插桩，不改变行为。
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from navigation.scene_resolver import SceneType
    from navigation.mode_manager import NavigationMode
    from navigation.position_authority_manager import PositionAuthority
    from navigation.evidence_models import AuthorityConfidenceSnapshot


# Event Topics (用于 EventBus)
TOPIC_SCENE_DECISION = "nav.scene.decision"
TOPIC_MODE_DECISION = "nav.mode.decision"
TOPIC_AUTH_DECISION = "nav.pos.authority"
TOPIC_LOCAL_MAP_UPDATED = "nav.localmap.updated"
TOPIC_LANDMARK_MATCH = "nav.localmap.landmark_match"
TOPIC_POSITION_UPDATE = "nav.position.update"
TOPIC_LANDMARK_DETECTED = "nav.landmark.detected"
TOPIC_NAV_STATE = "nav.state"

# Step 5 新增 Topics
TOPIC_EVIDENCE_INGEST = "nav.evidence.ingest"
TOPIC_CONFIDENCE_SNAPSHOT = "nav.confidence.snapshot"

# Step 6 新增 Topics
TOPIC_AUTHORITY_TAKEOVER_DECISION = "nav.authority.takeover"

# Step 7 新增 Topics
TOPIC_AUTHORITY_LOCK_HINT = "nav.authority.lock_hint"


# Step 1-4 事件（原有）

@dataclass
class PositionUpdateEvent:
    """位置更新事件"""
    ts: float
    step_index: int
    dx_m: float
    dy_m: float
    dtheta_deg: float
    visual_confidence: float
    meta: Optional[Dict[str, Any]] = None


@dataclass
class LandmarkDetectedEvent:
    """地标检测事件"""
    ts: float
    kind: str
    label: str
    confidence: float
    meta: Optional[Dict[str, Any]] = None


@dataclass
class NavStateEvent:
    """导航状态事件"""
    ts: float
    state: str
    meta: Optional[Dict[str, Any]] = None


@dataclass
class SceneDecisionEvent:
    """场景决策事件（Step 2 输出）"""
    ts: float
    scene_type: Any  # SceneType (延迟导入避免循环)
    confidence: float
    reason: str
    meta: Optional[Dict[str, Any]] = None


@dataclass
class NavModeDecisionEvent:
    """导航模式决策事件（Step 1 输出）"""
    ts: float
    mode: Any  # NavigationMode (延迟导入避免循环)
    confidence: float
    reason: str
    meta: Optional[Dict[str, Any]] = None


@dataclass
class PositionAuthorityDecisionEvent:
    """位置主权决策事件（Step 3 输出）"""
    ts: float
    authority: Any  # PositionAuthority (延迟导入避免循环)
    confidence: float
    reason: str
    meta: Optional[Dict[str, Any]] = None


@dataclass
class LocalMapUpdatedEvent:
    """本地地图更新事件（Step 4 输出）"""
    ts: float
    map_id: str
    node_count: int
    edge_count: int
    meta: Optional[Dict[str, Any]] = None


@dataclass
class LandmarkMatchEvent:
    """地标匹配事件（Step 4 输出）"""
    ts: float
    label: str
    match_score: float
    matched_node_id: Optional[str]
    reason: str
    meta: Optional[Dict[str, Any]] = None


# Step 5 新增事件

@dataclass
class EvidenceIngestEvent:
    """证据摄入事件（Step 5 输入）"""
    ts: float
    source: str          # EvidenceSource.value
    kind: str            # EvidenceKind.value
    value: float         # 0..1
    ttl_s: float         # Time To Live (秒)
    meta: Optional[Dict[str, Any]] = None


@dataclass
class AuthorityConfidenceSnapshotEvent:
    """权威置信度快照事件（Step 5 输出）"""
    ts: float
    # 如果系统 event bus 不支持嵌套 dataclass，就把 snapshot 展开成字段
    visual_score: float
    map_vision_score: float
    gps_score: float
    dominant_candidate: Optional[str]
    confidence_gap: float
    stability: float
    decay_state: Dict[str, float]
    reason_trace: list[str]
    window_s: float
    meta: Optional[Dict[str, Any]] = None


# Step 6 新增事件

@dataclass
class TakeoverDecisionEvent:
    """接管决策事件（Step 6 输出）"""
    ts: float
    target_authority: str              # "VISUAL" / "MAP_VISION" / "GPS"
    confidence: float                  # 置信度分数
    state: str                         # 状态（"TAKEN"）
    reason_trace: list[str]            # 原因追踪
    meta: Optional[Dict[str, Any]] = None


# Step 7 新增事件

@dataclass
class AuthorityLockHintEvent:
    """主权锁定提示事件（Step 7 输出）"""
    ts: float
    hint: Any  # AuthorityLockHint (延迟导入避免循环)
    meta: Optional[Dict[str, Any]] = None







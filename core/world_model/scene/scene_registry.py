# -*- coding: utf-8 -*-
"""
v1.8.5: Scene Registry（场景注册表）

职责：
- 场景锚点、连续性、切换
- 唯一"切场景"的地方
- Map / Memory 只"提供权重和证据"，不裁决

Scene 的工程定义：
- Scene = 空间锚点 + 语义锚点 + 稳态时间窗
- Scene 是"稳定感知窗口"，不是位置本身

设计原则：
- Scene 切换 ≠ 清空上下文
- Scene 之间必须存在过渡期（overlap）
- 旧 Scene 的权重渐退，新 Scene 的权重渐进

⚠️ v1.8.5 Phase B: 视觉隔离护栏

SceneRegistry 禁止接收原始视觉数据。

Forbidden:
- ❌ 不接受 frame / image / bbox / ocr_text
- ❌ 不接受 raw_text（除非来自 UserReportRouter）
- ✅ 只接受结构化输入：PositionState, MapHint, MemoryHint

违规接口检查：
- 所有 public 方法如果参数包含 image/frame/bbox/raw_text，标记为 TODO/DEPRECATED
"""

import time
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from collections import deque

from core.world_model.common.types import PositionState
from core.world_model.common.gates import should_freeze_world_writes


@dataclass
class SceneCandidate:
    """
    场景候选
    
    字段说明：
    - scene_id: 场景 ID
    - scene_type: 场景类型（sidewalk / street / building / bridge）
    - geo_anchor: 地理锚点（GPS / Map / Vision）
    - semantic_anchor: 语义锚点（人行道 / 商业街 / 医院入口 / 桥下）
    - confidence: 置信度 [0.0 ~ 1.0]
    - sources: 来源列表
    """
    scene_id: str
    scene_type: str
    geo_anchor: Dict[str, Any]
    semantic_anchor: Optional[str] = None
    confidence: float = 0.5
    sources: List[str] = field(default_factory=list)


@dataclass
class SceneState:
    """
    场景状态（当前活跃场景）
    
    字段说明：
    - scene_id: 场景 ID
    - scene_type: 场景类型
    - geo_anchor: 地理锚点
    - semantic_anchor: 语义锚点
    - confidence: 置信度
    - created_ts: 创建时间戳
    - last_update_ts: 最后更新时间戳
    """
    scene_id: str
    scene_type: str
    geo_anchor: Dict[str, Any]
    semantic_anchor: Optional[str] = None
    confidence: float = 0.5
    created_ts: float = 0.0
    last_update_ts: float = 0.0


class PendingScene:
    """
    待确认场景（用于连续性评分和稳态确认）
    
    职责：
    - 累积候选场景
    - 判断是否稳定到可以切换
    """
    
    def __init__(self, stable_duration_s: float = 3.0):
        """
        初始化待确认场景
        
        Args:
            stable_duration_s: 稳定持续时间（秒，默认 3 秒）
        """
        self.stable_duration_s = stable_duration_s
        self.candidates: deque = deque(maxlen=10)  # 最近 10 个候选
        self.first_seen_ts: Optional[float] = None
    
    def add(self, candidate: SceneCandidate, now_ts: float) -> None:
        """
        添加候选场景
        
        Args:
            candidate: 场景候选
            now_ts: 当前时间戳
        """
        self.candidates.append((candidate, now_ts))
        if self.first_seen_ts is None:
            self.first_seen_ts = now_ts
    
    def confirmed(self, now_ts: float) -> bool:
        """
        判断是否已确认（稳定到可以切换）
        
        Args:
            now_ts: 当前时间戳
        
        Returns:
            bool: 是否已确认
        """
        if len(self.candidates) < 2:
            return False
        
        if self.first_seen_ts is None:
            return False
        
        # 检查是否持续稳定足够长时间
        duration = now_ts - self.first_seen_ts
        return duration >= self.stable_duration_s
    
    def clear(self) -> None:
        """清空待确认场景"""
        self.candidates.clear()
        self.first_seen_ts = None
    
    def get_latest(self) -> Optional[SceneCandidate]:
        """
        获取最新的候选场景
        
        Returns:
            Optional[SceneCandidate]: 最新的候选场景
        """
        if not self.candidates:
            return None
        return self.candidates[-1][0]


class SceneRegistry:
    """
    场景注册表
    
    设计原则：
    - SceneRegistry 是唯一"切场景"的地方
    - Map / Memory 只"提供权重和证据"，不裁决
    - Scene 切换 ≠ 清空上下文
    - Scene 之间必须存在过渡期（overlap）
    """
    
    def __init__(self, switch_threshold: float = 0.7, stable_duration_s: float = 3.0):
        """
        初始化场景注册表
        
        Args:
            switch_threshold: 切换阈值（连续性评分，默认 0.7）
            stable_duration_s: 稳定持续时间（秒，默认 3 秒）
        """
        self.switch_threshold = switch_threshold
        self.current_scene: Optional[SceneState] = None
        self.pending_scene = PendingScene(stable_duration_s=stable_duration_s)
    
    def update(
        self,
        position_state: PositionState,
        map_hints: Optional[Dict[str, Any]] = None,
        memory_hints: Optional[Dict[str, Any]] = None,
        now_ts: Optional[float] = None,
    ) -> Optional[SceneState]:
        """
        更新场景注册表（主入口）
        
        Args:
            position_state: 位置状态
            map_hints: 地图提示（可选）
            memory_hints: 记忆提示（可选）
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
        
        Returns:
            Optional[SceneState]: 当前活跃场景
        """
        now = now_ts or time.time()
        
        # 1. 统一 Gate 规则（包 B：失衡/漂移/重定位 → 冻结场景，防止错位关联）
        if should_freeze_world_writes(position_state):
            return self.current_scene  # 冻结
        
        # 2. 生成候选 Scene（不立刻切）
        candidate = self._propose_scene(
            position=position_state,
            map_hints=map_hints or {},
            memory_hints=memory_hints or {},
            now_ts=now,
        )
        
        if candidate is None:
            return self.current_scene
        
        # 3. 连续性评分
        continuity = self._calc_continuity_score(
            self.current_scene,
            candidate,
        )
        
        if continuity < self.switch_threshold:
            # 记录候选，但不切
            self.pending_scene.add(candidate, now)
            return self.current_scene
        
        # 4. 稳态确认（时间）
        if not self.pending_scene.confirmed(now):
            return self.current_scene
        
        # 5. 切换 Scene（唯一入口）
        self.current_scene = SceneState(
            scene_id=candidate.scene_id,
            scene_type=candidate.scene_type,
            geo_anchor=candidate.geo_anchor,
            semantic_anchor=candidate.semantic_anchor,
            confidence=candidate.confidence,
            created_ts=now if self.current_scene is None else self.current_scene.created_ts,
            last_update_ts=now,
        )
        self.pending_scene.clear()
        
        return self.current_scene
    
    def _propose_scene(
        self,
        position: PositionState,
        map_hints: Dict[str, Any],
        memory_hints: Dict[str, Any],
        now_ts: float,
    ) -> Optional[SceneCandidate]:
        """
        生成候选场景
        
        Args:
            position: 位置状态
            map_hints: 地图提示
            memory_hints: 记忆提示
            now_ts: 当前时间戳
        
        Returns:
            Optional[SceneCandidate]: 场景候选
        """
        # 一期简化：从 map_hints 提取场景信息
        scene_type = map_hints.get("scene_type", "unknown")
        semantic_anchor = map_hints.get("semantic_anchor")
        
        # 生成场景 ID（稳定 hash）
        import hashlib
        key = f"{scene_type}:{semantic_anchor or 'unknown'}:{position.position[0]:.1f}:{position.position[1]:.1f}"
        scene_id = hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]
        
        # 计算置信度（基于位置稳定性和地图提示）
        confidence = position.stability_score * 0.7
        if map_hints.get("confidence"):
            confidence = max(confidence, map_hints["confidence"] * 0.3)
        
        return SceneCandidate(
            scene_id=scene_id,
            scene_type=scene_type,
            geo_anchor={
                "position": position.position,
                "stability_score": position.stability_score,
            },
            semantic_anchor=semantic_anchor,
            confidence=confidence,
            sources=["map"] if map_hints else ["position"],
        )
    
    def _calc_continuity_score(
        self,
        current: Optional[SceneState],
        candidate: SceneCandidate,
    ) -> float:
        """
        计算连续性评分
        
        Args:
            current: 当前场景状态
            candidate: 候选场景
        
        Returns:
            float: 连续性评分 [0.0 ~ 1.0]
        """
        if current is None:
            return 1.0  # 没有当前场景，直接接受
        
        # 场景类型相同
        if current.scene_type == candidate.scene_type:
            score = 0.8
        else:
            score = 0.3
        
        # 语义锚点相同
        if current.semantic_anchor == candidate.semantic_anchor:
            score += 0.2
        
        # 位置接近（简化：使用稳定性评分）
        if candidate.geo_anchor.get("stability_score", 0.0) > 0.8:
            score += 0.1
        
        return min(1.0, score)
    
    def get_current_scene(self) -> Optional[SceneState]:
        """
        获取当前活跃场景
        
        Returns:
            Optional[SceneState]: 当前活跃场景
        """
        return self.current_scene

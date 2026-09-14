# -*- coding: utf-8 -*-
"""
v1.8.5 Phase B: Scene Registry（场景注册表 - 状态机实现）

职责：
- 世界稳定性管理器
- 负责：什么时候该认为世界变了，什么时候不该

核心状态：
- Active Scene（当前生效）
- Candidate Scene（候选，尚未确认）

原则：
- 不接真实数据（Phase B Step 1）
- 只实现状态机逻辑
- 不影响 Risk / Task / Emotion 行为
"""

from __future__ import annotations
from typing import Optional
import time
import logging

from .scene_segment import SceneSegment, SceneAnchors
from .scene_inputs import SceneInputs
from .schema import SceneState
from .environment_context import EnvironmentContext

logger = logging.getLogger(__name__)

# Phase B 状态机参数
SWITCH_THRESHOLD = 0.7  # Candidate 切换阈值
MIN_STABLE_TIME = 5.0  # 最小稳定时间（秒）
CONFIDENCE_GAIN = 0.05  # 正常运行时 confidence 增量
CONFIDENCE_DECAY = 0.02  # 重叠窗口时 confidence 衰减
INITIAL_CONFIDENCE = 0.3  # 初始 confidence
CANDIDATE_INITIAL_CONFIDENCE = 0.2  # Candidate 初始 confidence


class SceneRegistry:
    """
    场景注册表（状态机实现）
    
    SceneRegistry 不是"世界理解"，而是世界稳定性管理器。
    它负责：什么时候该认为世界变了，什么时候不该。
    
    核心状态：
    - Active Scene（当前生效）
    - Candidate Scene（候选，尚未确认）
    
    不存在第三个。
    """
    
    def __init__(self):
        """初始化场景注册表"""
        self.active_scene: Optional[SceneSegment] = None
        self.candidate_scene: Optional[SceneSegment] = None
        self._scene_counter = 0  # 用于生成唯一 scene_id
    
    def _generate_scene_id(self) -> str:
        """生成唯一场景 ID"""
        self._scene_counter += 1
        return f"scene_{self._scene_counter:04d}"
    
    def _create_scene_segment(
        self,
        inputs: SceneInputs,
        lifecycle_state: str = "CANDIDATE"
    ) -> SceneSegment:
        """
        创建场景段
        
        Args:
            inputs: 场景输入
            lifecycle_state: 生命周期状态
        
        Returns:
            SceneSegment: 新创建的场景段
        """
        anchors = SceneAnchors(
            geometry_anchor=inputs.geometry_hint,
            semantic_anchor=inputs.semantic_hint,
            behavior_anchor=inputs.behavior_hint,
            memory_anchor=None  # Phase B 阶段为空
        )
        
        initial_confidence = (
            INITIAL_CONFIDENCE if lifecycle_state == "ACTIVE"
            else CANDIDATE_INITIAL_CONFIDENCE
        )
        
        # 环境上下文影响初始置信度（但不阻止创建）
        if inputs.environment_context:
            env_modifier = inputs.environment_context.compute_modifier()
            initial_confidence *= env_modifier
        
        return SceneSegment(
            scene_id=self._generate_scene_id(),
            anchors=anchors,
            confidence=initial_confidence,
            first_seen_ts=inputs.timestamp,
            last_confirmed_ts=inputs.timestamp,
            lifecycle_state=lifecycle_state
        )
    
    def _anchors_match(
        self,
        scene: SceneSegment,
        inputs: SceneInputs
    ) -> bool:
        """
        判断输入是否与场景锚点匹配（Phase B 阶段）
        
        关键原则：
        - 时间 & 天气只影响权重，不直接否定匹配
        - 夜晚 ≠ 新场景
        - 下雪 ≠ 新场景
        - 它们只会降低 confidence / 提升风险权重
        
        Args:
            scene: 场景段
            inputs: 场景输入
        
        Returns:
            bool: 是否匹配
        """
        # Phase B 阶段：简化匹配逻辑
        # 后续 Phase C 可扩展为更精细的匹配算法
        
        # 如果输入为空，认为不匹配
        if not inputs.is_valid():
            return False
        
        # 计算几何、语义、行为匹配度
        geometry_ok = self._geometry_similarity(
            inputs.geometry_hint,
            scene.anchors.geometry_anchor
        )
        semantic_ok = self._semantic_similarity(
            inputs.semantic_hint,
            scene.anchors.semantic_anchor
        )
        behavior_ok = self._behavior_similarity(
            inputs.behavior_hint,
            scene.anchors.behavior_anchor
        )
        
        # 加权求和（简化：等权重）
        base_score = (geometry_ok + semantic_ok + behavior_ok) / 3.0
        
        # 环境修正因子（时间/天气只影响权重，不直接否定匹配）
        if inputs.environment_context:
            env_modifier = inputs.environment_context.compute_modifier()
            score = base_score * env_modifier
        else:
            score = base_score
        
        # 匹配阈值
        MATCH_THRESHOLD = 0.5
        return score >= MATCH_THRESHOLD
    
    def _geometry_similarity(
        self,
        input_geometry: Optional[Dict[str, Any]],
        scene_geometry: Optional[Dict[str, Any]]
    ) -> float:
        """
        计算几何相似度（简化版）
        
        Args:
            input_geometry: 输入几何
            scene_geometry: 场景几何
        
        Returns:
            float: 相似度（0.0 ~ 1.0）
        """
        if input_geometry is None and scene_geometry is None:
            return 1.0
        if input_geometry is None or scene_geometry is None:
            return 0.0
        
        # Phase B 阶段：简化比较
        # 后续 Phase C 可扩展为更精细的几何匹配算法
        return 0.7  # 默认认为有一定相似度
    
    def _semantic_similarity(
        self,
        input_semantic: Optional[Dict[str, Any]],
        scene_semantic: Optional[Dict[str, Any]]
    ) -> float:
        """
        计算语义相似度（简化版）
        
        Args:
            input_semantic: 输入语义
            scene_semantic: 场景语义
        
        Returns:
            float: 相似度（0.0 ~ 1.0）
        """
        if input_semantic is None and scene_semantic is None:
            return 1.0
        if input_semantic is None or scene_semantic is None:
            return 0.0
        
        # Phase B 阶段：简化比较（直接比较字典）
        if input_semantic == scene_semantic:
            return 1.0
        
        # 部分匹配（例如 place_type 相同）
        if isinstance(input_semantic, dict) and isinstance(scene_semantic, dict):
            if input_semantic.get("place_type") == scene_semantic.get("place_type"):
                return 0.8
        
        return 0.0
    
    def _behavior_similarity(
        self,
        input_behavior: Optional[Dict[str, Any]],
        scene_behavior: Optional[Dict[str, Any]]
    ) -> float:
        """
        计算行为相似度（简化版）
        
        Args:
            input_behavior: 输入行为
            scene_behavior: 场景行为
        
        Returns:
            float: 相似度（0.0 ~ 1.0）
        """
        if input_behavior is None and scene_behavior is None:
            return 1.0
        if input_behavior is None or scene_behavior is None:
            return 0.5  # 行为缺失时给中等分数（保守策略）
        
        # Phase B 阶段：简化比较
        # 后续 Phase C 可扩展为更精细的行为模式匹配
        if isinstance(input_behavior, dict) and isinstance(scene_behavior, dict):
            if input_behavior.get("pattern") == scene_behavior.get("pattern"):
                return 1.0
        
        return 0.6  # 默认认为有一定相似度
    
    def _detect_structural_change(
        self,
        inputs: SceneInputs
    ) -> bool:
        """
        检测是否发生结构性变化（可能的新场景）
        
        条件（满足其一即可）：
        - semantic_anchor 发生类别变化（室外→室内）
        - geometry_anchor 连续偏离阈值
        - 行为模式发生结构性变化（直行→反复停走）
        
        Args:
            inputs: 场景输入
        
        Returns:
            bool: 是否检测到结构性变化
        """
        if not self.active_scene:
            return False
        
        # Phase B 阶段：简化检测逻辑
        # 后续 Phase C 可扩展为更精细的检测算法
        
        # 检查 semantic_hint 是否发生变化
        if inputs.semantic_hint and self.active_scene.anchors.semantic_anchor:
            # 这里可以扩展为更复杂的语义变化检测
            # 目前简化：如果 semantic_hint 不同，认为可能变化
            return inputs.semantic_hint != self.active_scene.anchors.semantic_anchor
        
        return False
    
    def update(self, inputs: SceneInputs) -> SceneState:
        """
        更新场景状态（状态机主流程）
        
        状态机流程：
        1. 初始状态：Active = None → 创建 Active Scene
        2. 正常运行：输入与 Active 一致 → confidence 增加
        3. 发现新场景：检测到结构性变化 → 创建 Candidate
        4. 重叠窗口：Active 和 Candidate 共存，confidence 演化
        5. 确认切换：Candidate 稳定 → Active 切换
        6. 回滚：Candidate 不稳定 → 丢弃 Candidate
        
        Args:
            inputs: 场景输入
        
        Returns:
            SceneState: 当前场景状态
        """
        now_ts = inputs.timestamp
        
        # === 🟢 初始状态 ===
        if self.active_scene is None:
            # 第一段稳定输入 → 创建 Active Scene
            self.active_scene = self._create_scene_segment(
                inputs,
                lifecycle_state="ACTIVE"
            )
            logger.debug(f"[SceneRegistry] 创建初始 Active Scene: {self.active_scene.scene_id}")
            return self._build_scene_state()
        
        # === 🟢 正常运行（无明显变化） ===
        if self._anchors_match(self.active_scene, inputs):
            # 新输入与 Active Scene 锚点一致
            # confidence 增加
            new_confidence = min(1.0, self.active_scene.confidence + CONFIDENCE_GAIN)
            self.active_scene.update_confidence(new_confidence, now_ts)
            
            # 如果有 Candidate，检查是否需要回滚
            if self.candidate_scene:
                # Candidate 长期不稳定，回滚
                if self.candidate_scene.confidence < 0.3:
                    logger.debug(f"[SceneRegistry] 回滚 Candidate: {self.candidate_scene.scene_id}")
                    self.candidate_scene = None
                else:
                    # Candidate 仍然存在，但 confidence 下降
                    candidate_conf = max(0.0, self.candidate_scene.confidence - CONFIDENCE_DECAY)
                    self.candidate_scene.update_confidence(candidate_conf, now_ts)
            
            return self._build_scene_state()
        
        # === 🟡 发现"可能的新场景" ===
        if self._detect_structural_change(inputs):
            # 检测到结构性变化
            if self.candidate_scene is None:
                # 创建 Candidate Scene
                self.candidate_scene = self._create_scene_segment(
                    inputs,
                    lifecycle_state="CANDIDATE"
                )
                logger.debug(f"[SceneRegistry] 创建 Candidate Scene: {self.candidate_scene.scene_id}")
            else:
                # Candidate 已存在，更新 confidence
                candidate_conf = min(1.0, self.candidate_scene.confidence + CONFIDENCE_GAIN)
                self.candidate_scene.update_confidence(candidate_conf, now_ts)
            
            # Active Scene confidence 下降（重叠窗口）
            active_conf = max(0.0, self.active_scene.confidence - CONFIDENCE_DECAY)
            self.active_scene.update_confidence(active_conf, now_ts)
            
            # === 🔵 确认切换 ===
            if self.candidate_scene.is_stable(SWITCH_THRESHOLD, MIN_STABLE_TIME):
                # Candidate 稳定，执行切换
                logger.info(
                    f"[SceneRegistry] 场景切换: {self.active_scene.scene_id} → {self.candidate_scene.scene_id}"
                )
                self.active_scene.lifecycle_state = "FADING"
                self.candidate_scene.lifecycle_state = "ACTIVE"
                self.active_scene = self.candidate_scene
                self.candidate_scene = None
                return self._build_scene_state()
        
        # === 🟠 重叠窗口（Scene Overlap Window） ===
        # Active 和 Candidate 共存，confidence 演化
        if self.candidate_scene:
            # Active confidence 下降
            active_conf = max(0.0, self.active_scene.confidence - CONFIDENCE_DECAY)
            self.active_scene.update_confidence(active_conf, now_ts)
            
            # Candidate confidence 上升
            candidate_conf = min(1.0, self.candidate_scene.confidence + CONFIDENCE_GAIN)
            self.candidate_scene.update_confidence(candidate_conf, now_ts)
        
        return self._build_scene_state()
    
    def get_active_scene(self) -> Optional[SceneSegment]:
        """
        获取当前生效的场景段
        
        Returns:
            Optional[SceneSegment]: 当前生效的场景段
        """
        return self.active_scene
    
    def get_candidate_scene(self) -> Optional[SceneSegment]:
        """
        获取候选场景段
        
        Returns:
            Optional[SceneSegment]: 候选场景段
        """
        return self.candidate_scene
    
    def get_current_scene(self) -> SceneState:
        """
        获取当前场景状态（兼容 Phase A 接口）
        
        Returns:
            SceneState: 当前场景状态
        """
        return self._build_scene_state()
    
    def _build_scene_state(self) -> SceneState:
        """
        构建场景状态（兼容 Phase A 接口）
        
        Returns:
            SceneState: 场景状态
        """
        if self.active_scene:
            return SceneState(
                scene_id=self.active_scene.scene_id,
                scene_type=None,  # Phase B 阶段为空
                geo_anchor=None,  # Phase B 阶段为空
                static_model=None,  # Phase B 阶段为空
                dynamic_model=None,  # Phase B 阶段为空
                scene_memory=None,  # Phase B 阶段为空
                confidence=self.active_scene.confidence,
                timestamp=time.time()
            )
        else:
            # 兼容 Phase A：返回默认场景
            return SceneState(
                scene_id="unknown_scene",
                scene_type=None,
                geo_anchor=None,
                static_model=None,
                dynamic_model=None,
                scene_memory=None,
                confidence=None,
                timestamp=time.time()
            )

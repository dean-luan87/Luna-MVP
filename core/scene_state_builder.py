# -*- coding: utf-8 -*-
"""
场景状态构建器（Scene State Builder）

v1.8.3: 把"瞬时识别结果"变成"可判断的状态"

职责：
- 去瞬时
- 引入"稳定度"
- 引入"是否变化"
"""

import time
from typing import Dict, List, Any, Optional
import hashlib

# v1.8.5 Phase B Step 3.1: 导入 WorldUpdate
from core.world_model.common.types import WorldUpdate


class SceneState:
    """场景状态对象"""
    
    def __init__(
        self,
        scene_id: str,
        objects: List[str],
        signs: List[str],
        risk_level: str = "low",
        stability: str = "unstable",
        last_changed: float = 0.0,
        scene_hash: Optional[str] = None
    ):
        """
        初始化场景状态
        
        Args:
            scene_id: 场景标识
            objects: 物体列表
            signs: 标志牌列表
            risk_level: 风险级别（low/medium/high）
            stability: 稳定度（unstable/stable）
            last_changed: 最后变化时间戳
            scene_hash: 场景哈希值
        """
        self.scene_id = scene_id
        self.objects = objects
        self.signs = signs
        self.risk_level = risk_level
        self.stability = stability
        self.last_changed = last_changed
        self.scene_hash = scene_hash or self._compute_hash()
    
    def _compute_hash(self) -> str:
        """计算场景哈希值"""
        content = "|".join(sorted(self.objects) + sorted(self.signs))
        return hashlib.md5(content.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "scene_id": self.scene_id,
            "objects": self.objects,
            "signs": self.signs,
            "risk_level": self.risk_level,
            "stability": self.stability,
            "last_changed": self.last_changed,
            "scene_hash": self.scene_hash,
        }


class SceneStateBuilder:
    """场景状态构建器"""
    
    def __init__(self, stability_threshold: int = 2):
        """
        初始化场景状态构建器
        
        Args:
            stability_threshold: 稳定阈值（连续相同 hash 的次数），默认 2
        """
        self.stability_threshold = stability_threshold
        self.last_scene_hash: Optional[str] = None
        self.stable_count: int = 0
        self.last_state: Optional[SceneState] = None
    
    def build_state(
        self,
        world_update: WorldUpdate,
        risk_level: Optional[str] = None
    ) -> SceneState:
        """
        构建场景状态
        
        v1.8.5 Phase B Step 3.1: 方法签名已迁移
        - 不再接收 objects/texts 等原始感知结果
        - 改为接收 WorldUpdate（结构化输入）
        
        Args:
            world_update: 世界更新（包含结构化数据）
            risk_level: 风险级别（如果为 None，则自动判断）
        
        Returns:
            SceneState: 场景状态对象
        """
        # v1.8.5 Phase B Step 3.1: 从 WorldUpdate.structured_data 中提取物体和文字信息
        structured_data = world_update.structured_data
        objects = structured_data.get("objects", [])  # YOLO 检测结果
        texts = structured_data.get("texts", [])       # OCR 识别结果
        
        # 提取物体和标志牌（内部逻辑保持不变）
        object_labels = [obj.get("label", "") for obj in objects]
        sign_texts = [text.get("text", "") for text in texts]
        
        # 计算场景哈希
        scene_hash = self._compute_scene_hash(object_labels, sign_texts)
        
        # 判断场景是否变化
        scene_changed = scene_hash != self.last_scene_hash
        
        if scene_changed:
            self.last_scene_hash = scene_hash
            self.stable_count = 0
            last_changed = time.time()
        else:
            self.stable_count += 1
            last_changed = self.last_state.last_changed if self.last_state else time.time()
        
        # 判断稳定度
        stability = "stable" if self.stable_count >= self.stability_threshold else "unstable"
        
        # 自动判断风险级别（如果未提供）
        if risk_level is None:
            risk_level = self._assess_risk_level(object_labels, sign_texts)
        
        # 生成场景 ID
        scene_id = self._generate_scene_id(object_labels, sign_texts)
        
        # 构建场景状态
        state = SceneState(
            scene_id=scene_id,
            objects=object_labels,
            signs=sign_texts,
            risk_level=risk_level,
            stability=stability,
            last_changed=last_changed,
            scene_hash=scene_hash
        )
        
        self.last_state = state
        return state
    
    def _compute_scene_hash(self, objects: List[str], signs: List[str]) -> str:
        """计算场景哈希值"""
        content = "|".join(sorted(objects) + sorted(signs))
        return hashlib.md5(content.encode()).hexdigest()
    
    def _assess_risk_level(self, objects: List[str], signs: List[str]) -> str:
        """
        评估风险级别
        
        Args:
            objects: 物体列表
            signs: 标志牌列表
        
        Returns:
            str: 风险级别（low/medium/high）
        """
        # 简单风险判断规则
        danger_keywords = ["危险", "禁止", "no_entry", "stop", "stop_sign"]
        warning_keywords = ["注意", "warning", "caution"]
        
        all_text = " ".join(objects + signs).lower()
        
        if any(keyword in all_text for keyword in danger_keywords):
            return "high"
        elif any(keyword in all_text for keyword in warning_keywords):
            return "medium"
        else:
            return "low"
    
    def _generate_scene_id(self, objects: List[str], signs: List[str]) -> str:
        """生成场景 ID"""
        if not objects and not signs:
            return "empty"
        
        primary_objects = sorted(objects)[:3]  # 取前 3 个主要物体
        primary_signs = sorted(signs)[:2]  # 取前 2 个主要标志
        
        parts = primary_objects + primary_signs
        scene_id = "_".join(parts[:3]) if parts else "unknown"
        
        return scene_id[:50]  # 限制长度
    
    def reset(self):
        """重置构建器"""
        self.last_scene_hash = None
        self.stable_count = 0
        self.last_state = None


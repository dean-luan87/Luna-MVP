# -*- coding: utf-8 -*-
"""
LV4.2: World Modeling Executor（异步）

职责：
- 构建低频、可复用的世界结构
- 不生成最终记忆，只生成候选增量

⚠️ v1.8.5 Phase B: 锁死边界

World Modeling Executor
Note:
- Schema definition deferred（B 阶段不展开）
- Only candidate generation allowed（只生成候选，不直接写世界模型）
- 广告四要素、模糊记忆等细节待后续细化

核心逻辑：
1. 稳定实体识别（建筑、出入口、通道、广告牌）
2. 内容抽取（广告/通告，粗四要素：时间、地点、品牌、功能）
3. 历史复用判断（是否已存在、是否需要更新）

⚠️ 不生成最终记忆，只生成候选增量

本模块禁止做什么：
- ❌ 禁止影响导航决策
- ❌ 禁止直接写 Library
- ❌ 禁止调用 LV4.1
- ❌ 禁止触发重拍
- ❌ 禁止修改任务态
"""

import time
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import numpy as np

# v1.8.5 Phase B Step 1.3: OCRProcessor 迁移到 ModelingExecutor
from utils.model_interfaces import OCRProcessor
# v1.8.5 Phase B Step 1.4: QwenVLProcessor 迁移到 ModelingExecutor
from utils.model_interfaces import QwenVLProcessor


@dataclass
class EntityCandidate:
    """实体候选"""
    entity_type: str  # "building" | "entrance" | "passage" | "landmark"
    entity_id: Optional[str] = None
    confidence: float = 0.0
    metadata: Dict[str, Any] = None


@dataclass
class ContentCandidate:
    """内容候选"""
    content_type: str  # "advertisement" | "notice" | "sign" | "scene_description"
    time: Optional[str] = None
    location: Optional[str] = None
    brand: Optional[str] = None
    function: Optional[str] = None
    confidence: float = 0.0
    raw_text: Optional[str] = None
    description: Optional[str] = None  # v1.8.5 Phase B Step 2.3: 场景描述（QwenVL 生成）


@dataclass
class ModelingResult:
    """
    世界建模结果
    
    字段说明：
    - entity_candidates: 实体候选列表
    - content_candidates: 内容候选列表
    - confidence: 整体置信度（"low" | "medium"）
    """
    entity_candidates: List[EntityCandidate] = None
    content_candidates: List[ContentCandidate] = None
    confidence: str = "low"  # "low" | "medium"
    
    def __post_init__(self):
        """后处理：初始化列表"""
        if self.entity_candidates is None:
            self.entity_candidates = []
        if self.content_candidates is None:
            self.content_candidates = []


class ModelingExecutor:
    """
    世界建模执行器（异步）
    
    核心逻辑：
    1. 稳定实体识别
    2. 内容抽取（子流程）
    3. 历史复用判断
    
    调度规则：
    - 异步
    - 可暂停/降频
    - 在导航激活时自动让路
    
    注意：
    - B 阶段先做空壳，不实现具体逻辑
    - 后续再细化 schema 和抽取算法
    """
    
    def __init__(
        self,
        scene_registry=None,  # SceneRegistry 实例（可选，只读）
        map_registry=None,  # MapRegistry 实例（可选，只读）
        ocr_processor=None,  # OCRProcessor 实例（可选，如果为 None 则创建默认实例）
        qwen_processor=None,  # QwenVLProcessor 实例（可选，如果为 None 则创建默认实例）
    ):
        """
        初始化世界建模执行器
        
        Args:
            scene_registry: SceneRegistry 实例（可选，只读）
            map_registry: MapRegistry 实例（可选，只读）
            ocr_processor: OCRProcessor 实例（可选，如果为 None 则创建默认实例）
            qwen_processor: QwenVLProcessor 实例（可选，如果为 None 则创建默认实例）
        """
        self.scene_registry = scene_registry
        self.map_registry = map_registry
        # v1.8.5 Phase B Step 1.3: OCRProcessor 迁移到 ModelingExecutor
        self.ocr_processor = ocr_processor or OCRProcessor()
        # v1.8.5 Phase B Step 1.4: QwenVLProcessor 迁移到 ModelingExecutor
        self.qwen_processor = qwen_processor or QwenVLProcessor()
    
    def run(
        self,
        frame: np.ndarray,
        context: Dict[str, Any],
        paused: bool = False,
        objects: Optional[List[Dict]] = None,  # v1.8.5 Phase B Step 2.3: YOLO 检测结果（用于 QwenVL）
    ) -> ModelingResult:
        """
        执行世界建模任务
        
        Args:
            frame: 输入图像帧
            context: 上下文（包含 scene, map_hint 等）
            paused: 是否暂停（导航激活时设为 True）
            objects: YOLO 检测结果（可选，用于 QwenVL 生成场景描述）
        
        Returns:
            ModelingResult: 世界建模结果
        """
        # B 阶段：先做空壳，不实现具体逻辑
        # 后续再细化 schema 和抽取算法
        
        if paused:
            # 导航激活时，返回空结果
            return ModelingResult(
                entity_candidates=[],
                content_candidates=[],
                confidence="low",
            )
        
        # v1.8.5 Phase B Step 2.2: OCR 检测迁移到 ModelingExecutor
        content_candidates = []
        texts = []  # 用于 QwenVL 生成场景描述
        if self.ocr_processor:
            try:
                # 调用 OCR 提取文字
                texts = self.ocr_processor.extract_text(frame)
                # 将 OCR 结果封装到 ContentCandidate（暂时保留 raw_texts 作为过渡字段）
                if texts:
                    for text_item in texts:
                        # 暂时将每个 OCR 结果作为一个 ContentCandidate
                        # 后续可以进一步解析为四要素（时间、地点、品牌、功能）
                        content_candidate = ContentCandidate(
                            content_type="sign",  # 默认类型，后续可细化
                            raw_text=text_item.get("text", "") if isinstance(text_item, dict) else str(text_item),
                            confidence=text_item.get("confidence", 0.5) if isinstance(text_item, dict) else 0.5,
                        )
                        content_candidates.append(content_candidate)
            except Exception:
                pass  # 静默失败，不阻塞
        
        # v1.8.5 Phase B Step 2.3: QwenVL 场景描述生成迁移到 ModelingExecutor
        if self.qwen_processor and objects is not None and texts:
            try:
                # 调用 QwenVL 生成场景描述
                description = self.qwen_processor.generate_description(frame, objects, texts)
                # 将场景描述封装到 ContentCandidate
                if description:
                    scene_description_candidate = ContentCandidate(
                        content_type="scene_description",
                        description=description,
                        confidence=0.8,  # QwenVL 生成的描述置信度
                    )
                    content_candidates.append(scene_description_candidate)
            except Exception:
                pass  # 静默失败，不阻塞
        
        # TODO: B 阶段暂不实现具体逻辑
        # 后续实现：
        # 1. 稳定实体识别
        # 2. 内容抽取（子流程）- 已添加 OCR 调用和 QwenVL 场景描述
        # 3. 历史复用判断
        
        return ModelingResult(
            entity_candidates=[],
            content_candidates=content_candidates,
            confidence="low",
        )


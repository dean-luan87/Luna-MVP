"""
Landmark Matcher (v1.4.8 StepB-3)

地标 ↔ LocalMap 节点匹配
"""

from dataclasses import dataclass
from typing import Optional, List
from navigation.landmark_observation import LandmarkType, LandmarkObservation


@dataclass
class LocalMapLandmarkNode:
    """
    LocalMap 节点最小接口（假设已存在）
    """
    node_id: str
    landmark_type: LandmarkType
    direction_hint: Optional[str]


@dataclass
class LandmarkMatchResult:
    """
    匹配结果结构
    """
    matched: bool
    node_id: Optional[str]
    score: float                # 0~1


class LandmarkMatcher:
    """
    地标匹配器
    
    职责：
    - 将视觉观测与 LocalMap 节点匹配
    - 返回匹配结果和置信度分数
    """
    
    def __init__(self, min_match_score: float = 0.6):
        """
        初始化地标匹配器
        
        Args:
            min_match_score: 最小匹配分数阈值（默认 0.6）
        """
        self.min_match_score = min_match_score
    
    def match(
        self,
        observation: LandmarkObservation,
        candidate_nodes: List[LocalMapLandmarkNode]
    ) -> LandmarkMatchResult:
        """
        匹配视觉观测与 LocalMap 节点
        
        匹配规则：
        1. landmark_type 必须一致
        2. 若存在 direction_hint，一致则加分
        3. 返回最高分匹配
        4. score < 0.6 → 视为未匹配
        
        Args:
            observation: 视觉观测
            candidate_nodes: 候选 LocalMap 节点列表
            
        Returns:
            LandmarkMatchResult: 匹配结果
        """
        if not candidate_nodes:
            return LandmarkMatchResult(
                matched=False,
                node_id=None,
                score=0.0
            )
        
        best_match: Optional[LocalMapLandmarkNode] = None
        best_score: float = 0.0
        
        # 遍历所有候选节点
        for node in candidate_nodes:
            # 1. landmark_type 必须一致
            if node.landmark_type != observation.landmark_type:
                continue
            
            # 基础分数（类型匹配）
            score = 0.5
            
            # 2. 若存在 direction_hint，一致则加分
            if observation.direction_hint and node.direction_hint:
                if observation.direction_hint == node.direction_hint:
                    score += 0.3
                else:
                    score -= 0.2  # 方向不一致，扣分
            
            # 视觉置信度加权
            score *= observation.confidence
            
            # 更新最佳匹配
            if score > best_score:
                best_score = score
                best_match = node
        
        # 4. score < 0.6 → 视为未匹配
        if best_score < self.min_match_score:
            return LandmarkMatchResult(
                matched=False,
                node_id=None,
                score=best_score
            )
        
        return LandmarkMatchResult(
            matched=True,
            node_id=best_match.node_id if best_match else None,
            score=best_score
        )







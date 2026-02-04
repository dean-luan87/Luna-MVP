# -*- coding: utf-8 -*-
"""
v1.8.4: 风险对象注册表（风险对象缓存、更新、过期与合并）

职责：
- 管理风险对象列表
- 更新风险对象状态
- 处理风险对象过期与合并
"""

import time
import logging
from typing import List, Dict, Optional
from core.risk.risk_object import RiskObject

logger = logging.getLogger(__name__)


class RiskRegistry:
    """
    风险对象注册表
    
    职责：
    - 维护风险对象列表
    - 更新风险对象状态
    - 处理风险对象生命周期
    """
    
    def __init__(self, object_ttl_seconds: float = 60.0):
        """
        初始化风险对象注册表
        
        Args:
            object_ttl_seconds: 风险对象 TTL（秒），超过此时间未更新则过期
        """
        self.risk_objects: Dict[str, RiskObject] = {}
        self.object_ttl_seconds = object_ttl_seconds
    
    def register(self, risk_object: RiskObject) -> None:
        """
        注册风险对象
        
        Args:
            risk_object: 危险对象
        """
        self.risk_objects[risk_object.risk_id] = risk_object
        logger.debug(f"[RiskRegistry] 注册风险对象: risk_id={risk_object.risk_id}")
    
    def get(self, risk_id: str) -> Optional[RiskObject]:
        """
        获取风险对象
        
        Args:
            risk_id: 风险对象 ID
        
        Returns:
            Optional[RiskObject]: 风险对象（如果不存在则返回 None）
        """
        return self.risk_objects.get(risk_id)
    
    def get_all(self) -> List[RiskObject]:
        """
        获取所有风险对象
        
        Returns:
            List[RiskObject]: 风险对象列表
        """
        return list(self.risk_objects.values())
    
    def upsert(self, risk_object: RiskObject) -> None:
        """
        插入或更新风险对象（如果已存在则更新，否则插入）
        
        Args:
            risk_object: 危险对象
        """
        if risk_object.risk_id in self.risk_objects:
            self.update(risk_object.risk_id, risk_object)
        else:
            self.register(risk_object)
    
    def update(self, risk_id: str, risk_object: RiskObject) -> None:
        """
        更新风险对象
        
        Args:
            risk_id: 风险对象 ID
            risk_object: 更新后的危险对象
        """
        if risk_id in self.risk_objects:
            self.risk_objects[risk_id] = risk_object
            logger.debug(f"[RiskRegistry] 更新风险对象: risk_id={risk_id}")
        else:
            self.register(risk_object)
    
    def remove(self, risk_id: str) -> None:
        """
        移除风险对象
        
        Args:
            risk_id: 风险对象 ID
        """
        if risk_id in self.risk_objects:
            del self.risk_objects[risk_id]
            logger.debug(f"[RiskRegistry] 移除风险对象: risk_id={risk_id}")
    
    def cleanup_expired(self, now_ts: Optional[float] = None) -> List[str]:
        """
        清理过期的风险对象
        
        Args:
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
        
        Returns:
            List[str]: 已过期的风险对象 ID 列表
        """
        if now_ts is None:
            now_ts = time.time()
        
        expired_ids = []
        for risk_id, risk_object in list(self.risk_objects.items()):
            # 检查是否过期
            if risk_object.runtime.last_update_ts:
                age = now_ts - risk_object.runtime.last_update_ts
                if age > self.object_ttl_seconds:
                    expired_ids.append(risk_id)
                    self.remove(risk_id)
        
        if expired_ids:
            logger.info(f"[RiskRegistry] 清理过期风险对象: {len(expired_ids)} 个")
        
        return expired_ids
    
    def merge_nearby_objects(
        self,
        distance_threshold_m: float = 5.0
    ) -> List[str]:
        """
        合并相近的风险对象（1.8.4 简化版）
        
        Args:
            distance_threshold_m: 距离阈值（米），小于此距离的对象将被合并
        
        Returns:
            List[str]: 被合并的风险对象 ID 列表
        
        说明：
        - 1.8.4 先不做复杂合并，只做接口预留
        - 后续可扩展：基于几何距离、风险类型等做智能合并
        """
        # 1.8.4: 暂不实现，只做接口预留
        return []


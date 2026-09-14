# -*- coding: utf-8 -*-
"""
v1.8.4: 风险对象创建工厂（RiskObjectFactory）

职责：
- 将上游识别/规则/地图输入统一转换为 RiskObject
- 1.8.4：优先支持 POINT/LINE/AREA 三种几何；字段最小闭环即可
"""

from __future__ import annotations
from typing import List, Tuple, Dict, Any, Optional
import time

from core.risk.risk_object import RiskObject, RiskGeometry, RiskRuntime
from core.risk.risk_types import RISK_TYPE_CONFIG, get_risk_config

XY = Tuple[float, float]


def _now_ts() -> float:
    """获取当前时间戳"""
    return time.time()


class RiskObjectFactory:
    """
    风险对象创建工厂
    
    将上游识别/规则/地图输入统一转换为 RiskObject
    """
    
    def make_point(
        self,
        risk_id: str,
        risk_type: str,
        xy: XY,
        confidence: float = 1.0,
        risk_class: str = "STATIC",
        meta: Optional[Dict[str, Any]] = None,
    ) -> RiskObject:
        """
        创建 POINT 类型风险对象
        
        Args:
            risk_id: 风险对象 ID
            risk_type: 风险类型（见 risk_types.py）
            xy: 点坐标 (x, y)
            confidence: 识别置信度（0~1）
            risk_class: 风险类别（STATIC/SEMI_STATIC/DYNAMIC）
            meta: 扩展元数据
        
        Returns:
            RiskObject: 风险对象
        """
        cfg = get_risk_config(risk_type)
        geom = RiskGeometry(type="POINT", points=[xy], length_m=None, area_m2=None)
        rt = RiskRuntime(
            state="DORMANT",
            last_risk_level=0.0,
            last_update_ts=_now_ts(),
            last_warn_ts=None,
            cooldown_until_ts=None,
            edge_distance_m=None,
            edge_trend="STABLE",
        )
        return RiskObject(
            risk_id=risk_id,
            risk_class=risk_class,
            risk_type=risk_type,
            geometry=geom,
            hazard_level=cfg["hazard_base"],
            confidence=confidence,
            runtime=rt,
            meta=meta or {},
        )
    
    def make_line(
        self,
        risk_id: str,
        risk_type: str,
        polyline: List[XY],
        length_m: Optional[float] = None,
        confidence: float = 1.0,
        risk_class: str = "STATIC",
        meta: Optional[Dict[str, Any]] = None,
    ) -> RiskObject:
        """
        创建 LINE 类型风险对象
        
        Args:
            risk_id: 风险对象 ID
            risk_type: 风险类型（见 risk_types.py）
            polyline: 折线点列表 [(x, y), ...]
            length_m: 折线长度（米），如果为 None 则自动计算
            confidence: 识别置信度（0~1）
            risk_class: 风险类别（STATIC/SEMI_STATIC/DYNAMIC）
            meta: 扩展元数据
        
        Returns:
            RiskObject: 风险对象
        """
        from core.risk.geometry_utils import polyline_length
        
        cfg = get_risk_config(risk_type)
        if length_m is None:
            length_m = polyline_length(polyline)
        
        geom = RiskGeometry(type="LINE", points=polyline, length_m=length_m, area_m2=None)
        rt = RiskRuntime(
            state="DORMANT",
            last_risk_level=0.0,
            last_update_ts=_now_ts(),
            last_warn_ts=None,
            cooldown_until_ts=None,
            edge_distance_m=None,
            edge_trend="STABLE",
        )
        return RiskObject(
            risk_id=risk_id,
            risk_class=risk_class,
            risk_type=risk_type,
            geometry=geom,
            hazard_level=cfg["hazard_base"],
            confidence=confidence,
            runtime=rt,
            meta=meta or {},
        )
    
    def make_area(
        self,
        risk_id: str,
        risk_type: str,
        polygon: List[XY],
        area_m2: Optional[float] = None,
        confidence: float = 1.0,
        risk_class: str = "SEMI_STATIC",
        meta: Optional[Dict[str, Any]] = None,
    ) -> RiskObject:
        """
        创建 AREA 类型风险对象
        
        Args:
            risk_id: 风险对象 ID
            risk_type: 风险类型（见 risk_types.py）
            polygon: 多边形顶点列表 [(x, y), ...]（按顺序）
            area_m2: 多边形面积（平方米），如果为 None 则不计算
            confidence: 识别置信度（0~1）
            risk_class: 风险类别（STATIC/SEMI_STATIC/DYNAMIC）
            meta: 扩展元数据
        
        Returns:
            RiskObject: 风险对象
        """
        cfg = get_risk_config(risk_type)
        geom = RiskGeometry(type="AREA", points=polygon, length_m=None, area_m2=area_m2)
        rt = RiskRuntime(
            state="DORMANT",
            last_risk_level=0.0,
            last_update_ts=_now_ts(),
            last_warn_ts=None,
            cooldown_until_ts=None,
            edge_distance_m=None,
            edge_trend="STABLE",
        )
        return RiskObject(
            risk_id=risk_id,
            risk_class=risk_class,
            risk_type=risk_type,
            geometry=geom,
            hazard_level=cfg["hazard_base"],
            confidence=confidence,
            runtime=rt,
            meta=meta or {},
        )



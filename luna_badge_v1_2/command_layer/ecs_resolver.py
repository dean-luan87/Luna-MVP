"""
ECSv1 (Enhanced Command Semantics) - 任务参数补全

当命令参数不完整时，通过记忆、POI、澄清等方式补全参数
"""

from pydantic import BaseModel
from typing import Dict, Any, Optional, Literal, List
from .semantic_normalizer import NormalizedCommand


class ResolutionResult(BaseModel):
    """
    参数补全结果
    
    Attributes:
        resolved: 是否已补全
        slots: 补全后的槽位字典
        source: 补全来源（memory / poi / user / none）
        reason: 补全原因或未补全的原因
    """
    resolved: bool
    slots: Dict[str, Any]
    source: Optional[Literal["memory", "poi", "user", "none"]] = None
    reason: Optional[str] = None


class FakeMemoryClient:
    """
    假记忆客户端（用于测试和开发）
    
    模拟用户历史记录查询
    """
    
    def __init__(self):
        # 模拟记忆数据
        self.memory_data = {
            "hospital": [
                {"name": "北京协和医院", "address": "北京市东城区", "last_visited": "2024-12-01"},
                {"name": "北京大学第一医院", "address": "北京市西城区", "last_visited": "2024-11-15"},
                {"name": "301医院", "address": "北京市海淀区", "last_visited": "2024-10-20"},
            ],
            "convenience_store": [
                {"name": "711便利店（中关村店）", "address": "北京市海淀区", "last_visited": "2024-12-05"},
                {"name": "711便利店（三里屯店）", "address": "北京市朝阳区", "last_visited": "2024-11-20"},
            ],
            "toilet": [],
            "bank": [
                {"name": "中国工商银行（中关村支行）", "address": "北京市海淀区", "last_visited": "2024-11-10"},
            ],
        }
    
    def query_recent_places(self, place_category: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        查询最近访问的相关地点
        
        Args:
            place_category: 地点类别
            limit: 返回数量限制
        
        Returns:
            List[Dict]: 地点列表，按访问时间倒序
        """
        places = self.memory_data.get(place_category, [])
        return places[:limit]


class FakePOIClient:
    """
    假 POI 客户端（用于测试和开发）
    
    模拟附近地点查询
    """
    
    def __init__(self):
        # 模拟 POI 数据
        self.poi_data = {
            "hospital": [
                {"name": "附近最近的医院", "address": "距离您 500 米", "distance": 500},
                {"name": "第二近的医院", "address": "距离您 1.2 公里", "distance": 1200},
            ],
            "convenience_store": [
                {"name": "711便利店（最近）", "address": "距离您 200 米", "distance": 200},
                {"name": "711便利店（第二近）", "address": "距离您 800 米", "distance": 800},
            ],
            "toilet": [
                {"name": "附近最近的厕所", "address": "距离您 100 米", "distance": 100},
            ],
            "bank": [
                {"name": "附近最近的银行", "address": "距离您 600 米", "distance": 600},
            ],
        }
    
    def query_nearby_pois(self, place_category: str, limit: int = 3) -> List[Dict[str, Any]]:
        """
        查询附近同类 POI
        
        Args:
            place_category: 地点类别
            limit: 返回数量限制
        
        Returns:
            List[Dict]: POI 列表，按距离排序
        """
        pois = self.poi_data.get(place_category, [])
        # 按距离排序
        sorted_pois = sorted(pois, key=lambda x: x.get("distance", 9999))
        return sorted_pois[:limit]


def resolve_slots(
    normalized: NormalizedCommand,
    memory_client: Optional[Any] = None,
    poi_client: Optional[Any] = None,
) -> ResolutionResult:
    """
    补全命令参数
    
    处理流程（顺序不能变）：
    1. MemoryResolver: 若 place_name 为空，使用 memory_client 查询最近相关地点
    2. POIResolver: 若记忆无结果，使用 poi_client 查询附近同类 POI
    3. ClarificationPrompt: 若都无结果，返回 resolved=False，需要用户澄清
    
    Args:
        normalized: 归一化后的命令
        memory_client: 记忆客户端（可选，默认使用 FakeMemoryClient）
        poi_client: POI 客户端（可选，默认使用 FakePOIClient）
    
    Returns:
        ResolutionResult: 补全结果
        
    注意：
    - 不允许 ECSv1 自行新建任务，只能补全 slots 或返回 resolved = False
    - 需要补全的意图类型：NAVIGATE, INSERT_TASK, REPLACE_TASK
    """
    # 如果不需要补全（已有完整信息或不需要地点信息）
    if normalized.intent_type in ["CANCEL_TASK", "UNKNOWN"]:
        return ResolutionResult(
            resolved=True,
            slots=normalized.slots.copy(),
            source="none",
            reason="无需补全"
        )
    
    # 如果已有 place_name，无需补全
    slots = normalized.slots.copy()
    place_category = slots.get("place_category")
    place_name = slots.get("place_name")
    
    if place_name:
        return ResolutionResult(
            resolved=True,
            slots=slots,
            source="user",
            reason="用户已提供完整地点信息"
        )
    
    # 如果没有 place_category，无法补全
    if not place_category:
        return ResolutionResult(
            resolved=False,
            slots=slots,
            source="none",
            reason="need_user_specify_target"
        )
    
    # 使用默认客户端（如果未提供）
    if memory_client is None:
        memory_client = FakeMemoryClient()
    if poi_client is None:
        poi_client = FakePOIClient()
    
    # Step 1: MemoryResolver - 查询记忆中的最近地点
    memory_places = memory_client.query_recent_places(place_category, limit=3)
    if memory_places:
        # 返回第一个候选，需要用户确认
        candidate = memory_places[0]
        slots["place_name"] = candidate.get("name")
        slots["place_address"] = candidate.get("address")
        slots["_candidates"] = memory_places  # 保存所有候选供后续使用
        return ResolutionResult(
            resolved=True,
            slots=slots,
            source="memory",
            reason=f"从记忆中找到了最近访问的 {candidate.get('name')}，需要用户确认"
        )
    
    # Step 2: POIResolver - 查询附近同类 POI
    nearby_pois = poi_client.query_nearby_pois(place_category, limit=3)
    if nearby_pois:
        # 返回最近的候选，需要用户确认
        candidate = nearby_pois[0]
        slots["place_name"] = candidate.get("name")
        slots["place_address"] = candidate.get("address")
        slots["_candidates"] = nearby_pois  # 保存所有候选供后续使用
        return ResolutionResult(
            resolved=True,
            slots=slots,
            source="poi",
            reason=f"附近最近的是 {candidate.get('name')}，需要用户确认"
        )
    
    # Step 3: ClarificationPrompt - 需要用户澄清
    return ResolutionResult(
        resolved=False,
        slots=slots,
        source="none",
        reason="need_user_specify_target"
    )


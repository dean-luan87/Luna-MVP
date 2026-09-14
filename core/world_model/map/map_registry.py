# -*- coding: utf-8 -*-
"""
v1.8.5: Map Registry（地图注册表）

⚠️ v1.8.5 Phase B: 视觉隔离护栏

MapRegistry 禁止接收原始视觉数据。

Forbidden:
- ❌ 不接受 frame / image / bbox / ocr_text
- ❌ 不接受 raw_text（除非来自 UserReportRouter）
- ✅ 只接受结构化输入：MapHint, Library hints

违规接口检查：
- 所有 public 方法如果参数包含 image/frame/bbox/raw_text，标记为 TODO/DEPRECATED

职责：
- 从 Memory / Library 提取权重，生成可用 map bias 的计算层
- 只读 Memory / Library，不写任何事实
- 输出只读 MapBias，给任务链 / 决策中台使用

MapRegistry 设计铁律：
- 只读 Memory / Library
- 不写任何事实
- 输出的是"权重建议"，不是结论

MapRegistry 只做三件事：
1. 聚合 体验记忆（Memory） → 舒适度 / 避让权重
2. 读取 已确认事实（Library） → 可通行性修正 / 风险提示
3. 输出 只读 MapBias → 给任务链 / 决策中台使用

MapRegistry 明确不做：
- ❌ 不写 Library
- ❌ 不写 Memory
- ❌ 不修改底层地图数据
- ❌ 不直接驱动行为或播报
"""

import time
from typing import List, Dict, Any, Optional

from dataclasses import dataclass
from typing import List, Optional

from core.world_model.common.types import EnvironmentContext
from core.world_model.common.db import WorldModelDB
from core.world_model.library.library_registry import LibraryRegistry, LibraryHint


@dataclass
class MapHint:
    """
    地图提示（客观世界，慢、稳）
    
    字段说明：
    - road_type: 道路类型（sidewalk / street / bridge）
    - slope: 坡度（度）
    - lighting: 照明情况（good / poor_at_night）
    - seasonal_risk: 季节性风险（snow / ice / flood）
    - scene_type: 场景类型（用于 SceneRegistry）
    - semantic_anchor: 语义锚点（用于 SceneRegistry）
    - confidence: 置信度 [0.0 ~ 1.0]
    """
    road_type: str = "unknown"
    slope: float = 0.0
    lighting: str = "unknown"
    seasonal_risk: List[str] = None
    scene_type: str = "unknown"
    semantic_anchor: Optional[str] = None
    confidence: float = 0.5
    
    def __post_init__(self):
        if self.seasonal_risk is None:
            self.seasonal_risk = []


class MapRegistry:
    """
    地图注册表
    
    MapRegistry 设计铁律：
    - 只读 Memory / Library
    - 不写任何事实
    - 输出的是"权重建议"，不是结论
    
    MapRegistry 对噪声的天然免疫：
    - LibraryHint 本身已经：慢确认、有 confidence、有生命周期
    - MapRegistry 只做线性加权 + clamp，不放大、不学习、不记忆
    - 即使 Library 里有一条错的事实，也只会产生有限影响，并会随回滚自然消失
    """
    
    def __init__(
        self,
        db: WorldModelDB,
        library: LibraryRegistry,
    ):
        """
        初始化地图注册表
        
        Args:
            db: 数据库实例（用于未来读取离线地图，当前未使用）
            library: 图书馆注册表实例（只读）
        """
        self.db = db
        self.library = library
    
    def get_map_hint(
        self,
        position: tuple,
        env_ctx: Optional[EnvironmentContext] = None,
    ) -> MapHint:
        """
        获取地图提示（客观世界，慢、稳）
        
        MapRegistry 的工程职责：
        1. 提供"这个地方通常是什么"
        2. 提供"客观危险 / 通行性"
        3. 不直接下结论
        
        Args:
            position: 位置坐标 (x, y)
            env_ctx: 环境上下文（可选）
        
        Returns:
            MapHint: 地图提示
        """
        # 一期简化：从 Library 获取相关事实，生成 MapHint
        # 未来可以从离线地图数据库读取
        
        # 默认值
        hint = MapHint(
            road_type="sidewalk",
            slope=0.0,
            lighting="good",
            seasonal_risk=[],
            scene_type="sidewalk",
            semantic_anchor="人行道",
            confidence=0.5,
        )
        
        # 根据环境上下文调整
        if env_ctx:
            if env_ctx.time_of_day == "NIGHT":
                hint.lighting = "poor_at_night"
            
            if env_ctx.season == "WINTER":
                hint.seasonal_risk.append("snow")
                hint.seasonal_risk.append("ice")
        
        return hint
    
    def compute_map_bias(
        self,
        scene_id: str,
        map_id: str,
        env_ctx: Optional[EnvironmentContext] = None,
        now_ts: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        计算 MapBias（临时对象，不落盘）
        
        Args:
            scene_id: 场景 ID
            map_id: 地图单元 ID
            env_ctx: 环境上下文（时间/天气/季节）
            now_ts: 当前时间戳（如果为 None 则使用 time.time()）
        
        Returns:
            Dict[str, Any]: MapBias 对象
                - map_id: 地图单元 ID
                - comfort_bias: 舒适度偏差 [-1.0 ~ +1.0]
                - avoid_bias: 避让偏差 [0.0 ~ 1.0]
                - risk_attention_boost: 风险注意力提升 [0.0 ~ 1.0]
                - reasons: 可追责来源列表
        """
        now = now_ts or time.time()
        
        bias = {
            "map_id": map_id,
            "comfort_bias": 0.0,
            "avoid_bias": 0.0,
            "risk_attention_boost": 0.0,
            "reasons": [],
        }
        
        # Step 1: 从 Library 拉取相关事实（只读）
        hints = self.library.get_hints(
            active_scene_id=scene_id,
            map_id=map_id,
            limit=10,
        )
        
        # Step 2: 应用事实对 MapBias 的影响
        for h in hints:
            self._apply_library_hint(bias, h, env_ctx)
        
        # Step 3: clamp（确保值在合理范围内）
        bias["comfort_bias"] = max(-1.0, min(1.0, bias["comfort_bias"]))
        bias["avoid_bias"] = max(0.0, min(1.0, bias["avoid_bias"]))
        bias["risk_attention_boost"] = max(0.0, min(1.0, bias["risk_attention_boost"]))
        
        return bias
    
    def _apply_library_hint(
        self,
        bias: Dict[str, Any],
        hint: LibraryHint,
        env_ctx: Optional[EnvironmentContext],
    ) -> None:
        """
        应用 LibraryHint 对 MapBias 的影响（事实 → Bias 的规则层）
        
        一期保守规则：
        - 封路 / 不可通行 → avoid_bias 提升
        - 易积水 / 易结冰 → risk_attention_boost 提升（天气敏感）
        - 夜间不适合行走 → avoid_bias 提升（时间敏感）
        
        Args:
            bias: MapBias 对象（会被修改）
            hint: LibraryHint 对象
            env_ctx: 环境上下文（可选）
        """
        tags = hint.tags
        conf = hint.confidence
        
        # 封路 / 不可通行
        if "road_blocked" in tags:
            bias["avoid_bias"] += 0.8 * conf
            bias["reasons"].append({
                "type": "FACT",
                "tag": "road_blocked",
                "confidence": conf,
                "source": "library",
            })
        
        # 易积水 / 易结冰
        if "flooded" in tags or "icy" in tags:
            factor = 0.6 * conf
            if env_ctx and env_ctx.weather in ("RAIN", "SNOW"):
                factor *= 1.2
            bias["risk_attention_boost"] += factor
            bias["reasons"].append({
                "type": "FACT",
                "tag": "weather_sensitive_risk",
                "confidence": conf,
                "source": "library",
            })
        
        # 夜间不适合行走
        if "low_visibility" in tags:
            if env_ctx and env_ctx.time_of_day == "NIGHT":
                bias["avoid_bias"] += 0.4 * conf
                bias["reasons"].append({
                    "type": "FACT",
                    "tag": "night_visibility",
                    "confidence": conf,
                    "source": "library",
                })


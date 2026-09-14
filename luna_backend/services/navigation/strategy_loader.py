"""
策略加载器 (StrategyLoader) v1.2.0
负责根据优先级加载所有策略组件
"""

from typing import List
from .base_strategy import BaseStrategy
from .navigation_context import NavigationContext

# 导入所有策略
# 导入通用策略
from .strategies_common import (
    DeviationCorrectionStrategy,
    ConstructionBypassStrategy,
    CrowdAvoidStrategy,
    MultiTargetNavStrategy,
)

# 导入其他策略
from .strategies.hazard_avoid import HazardAvoidStrategy
from .strategies.traffic_light import TrafficLightStrategy
from .strategies.bus_direction import BusDirectionStrategy
from .strategies.floor_zone import FloorZoneStrategy
from .strategies.destination_check import DestinationCheckStrategy
from .strategies.emotion_tone import EmotionToneStrategy

# 导入医院策略
from .strategies_hospital import (
    HospitalStageGuardStrategy,
    HospitalRegistrationStrategy,
    HospitalWaitingStrategy,
    HospitalDepartmentNavigationStrategy,
)


def load_all_strategies(context: NavigationContext, base_planner=None) -> List[BaseStrategy]:
    """
    加载所有策略（按优先级排序）
    
    策略优先级说明：
    1. 生命安全（情绪调节、施工、障碍物）- 最高优先级
    2. 基础可达（偏航、公交方向）
    3. 场景结构（楼层分区、医院场景）
    4. 体验增强（拥挤、红绿灯）
    5. 目标点确认
    
    Args:
        context: 导航上下文
        base_planner: 基础路径规划器（用于多目标规划）
    
    Returns:
        策略列表（按优先级排序）
    """
    strategies = [
        # --- 安全类最高优先级 ---
        EmotionToneStrategy(context),      # 0: 情绪调节（最高优先级，优先安抚用户）
        ConstructionBypassStrategy(context), # 1: 施工绕行
        HazardAvoidStrategy(context),      # 2: 危险规避
        
        # --- 可达性策略 ---
        DeviationCorrectionStrategy(context), # 3: 偏航纠正
        BusDirectionStrategy(context),     # 4: 公交方向
        
        # --- 多目标规划策略 ---
        MultiTargetNavStrategy(context, base_planner),  # 5: 多目标导航
        
        # --- 场景结构策略 ---
        FloorZoneStrategy(context),        # 6: 区域引导
        
        # --- 医院场景策略（如果scene_type为hospital）---
        # 这些策略会在should_execute中检查scene_type，所以可以安全添加
        HospitalStageGuardStrategy(context),  # 7: 医院阶段守卫
        HospitalRegistrationStrategy(context), # 8: 医院挂号
        HospitalWaitingStrategy(context),      # 9: 医院候诊
        HospitalDepartmentNavigationStrategy(context), # 10: 医院科室导航
        
        # --- 体验增强策略 ---
        CrowdAvoidStrategy(context),       # 11: 人群规避
        TrafficLightStrategy(context),     # 12: 红绿灯
        
        # --- 终点确认 ---
        DestinationCheckStrategy(context), # 13: 目标确认（最低优先级）
    ]
    
    return strategies


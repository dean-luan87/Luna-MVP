# v1.8.3 威胁状态语义参数设计

## 设计目标

让 `risk_assessor` 未来只做：
- 读取参数
- 计算状态
- 输出 RiskResult

**不负责**：
- 决策逻辑（由 decision_controller 负责）
- TTS 调用（由 speech_gate 负责）
- 行为策略执行（由 execute_speech_decision 负责）

---

## 1. 威胁状态语义层设计

### 1.1 核心概念

**LV2（潜在威胁环境）**:
- 检测到风险源，但用户未主动接近
- 系统"知道"但"不说"
- 状态：`POTENTIAL`

**LV1（即时威胁）**:
- 用户正在接近风险源，且满足升级条件
- 系统必须发声
- 状态：`IMMEDIATE`

---

### 1.2 ThreatMode 枚举

```python
from enum import Enum

class ThreatMode(Enum):
    """威胁模式"""
    APPROACH = "approach"  # 正在接近
    PATH_INTERSECT = "path_intersect"  # 路径交叉
    STATIC_PROXIMITY = "static_proximity"  # 静态接近
    VELOCITY_BASED = "velocity_based"  # 基于速度
```

---

### 1.3 升级条件结构

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class UpgradeCondition:
    """LV2 → LV1 升级条件"""
    # 时间条件
    ttc_threshold: Optional[float] = None  # TTC 阈值（秒），None 表示不使用
    ttc_strict: bool = True  # True: ≤ 阈值升级，False: ≥ 阈值升级
    
    # 距离条件
    distance_threshold: Optional[float] = None  # 距离阈值（米），None 表示不使用
    distance_strict: bool = True  # True: ≤ 阈值升级，False: ≥ 阈值升级
    
    # 运动趋势条件
    require_moving_towards: bool = True  # 是否要求"正在接近"
    require_velocity_increase: bool = False  # 是否要求"速度增加"
    
    # 组合逻辑
    combine_logic: str = "OR"  # "AND" 或 "OR"：多个条件如何组合
```

**示例**:
```python
# 水边风险：TTC ≤ 3.0s 或距离 ≤ 2.0m → 升级 LV1
water_upgrade = UpgradeCondition(
    ttc_threshold=3.0,
    ttc_strict=True,
    distance_threshold=2.0,
    distance_strict=True,
    require_moving_towards=True,
    combine_logic="OR"
)
```

---

### 1.4 行为策略结构

```python
@dataclass
class BehaviorPolicy:
    """行为策略"""
    # 播报策略
    should_speak: bool = True  # 是否播报
    can_interrupt: bool = True  # 是否可以打断系统播报
    can_interrupt_user: bool = False  # 是否可以打断用户说话（通常为 False）
    
    # 优先级
    speech_priority: int = 3  # 1=低，2=中，3=高（用于 speech_gate）
    
    # 去重策略
    bypass_deduplication: bool = True  # 是否绕过去重（LV1 通常为 True）
    bypass_cooldown: bool = True  # 是否绕过冷却（LV1 通常为 True）
```

---

### 1.5 风险类型威胁配置

```python
@dataclass
class ThreatStateConfig:
    """威胁状态配置"""
    # 威胁模式
    threat_mode: ThreatMode
    
    # LV2 配置（潜在威胁）
    lv2_keywords: List[str]  # 触发 LV2 的关键词
    lv2_behavior: BehaviorPolicy  # LV2 行为策略（通常 should_speak=False）
    
    # LV1 升级条件
    lv1_upgrade_condition: UpgradeCondition
    
    # LV1 配置（即时威胁）
    lv1_behavior: BehaviorPolicy  # LV1 行为策略（通常 should_speak=True）
    
    # 风险类型元信息
    risk_type: str  # 'water_edge' / 'road' / 'obstacle' / 'stair'
    priority: int = 3  # 风险类型优先级（用于多风险冲突时）
```

---

## 2. 完整 RiskConfig 扩展设计

### 2.1 扩展后的 RiskConfig

```python
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum

class ThreatMode(Enum):
    """威胁模式"""
    APPROACH = "approach"
    PATH_INTERSECT = "path_intersect"
    STATIC_PROXIMITY = "static_proximity"
    VELOCITY_BASED = "velocity_based"

@dataclass
class UpgradeCondition:
    """LV2 → LV1 升级条件"""
    ttc_threshold: Optional[float] = None
    ttc_strict: bool = True
    distance_threshold: Optional[float] = None
    distance_strict: bool = True
    require_moving_towards: bool = True
    require_velocity_increase: bool = False
    combine_logic: str = "OR"  # "AND" 或 "OR"

@dataclass
class BehaviorPolicy:
    """行为策略"""
    should_speak: bool = True
    can_interrupt: bool = True
    can_interrupt_user: bool = False
    speech_priority: int = 3
    bypass_deduplication: bool = True
    bypass_cooldown: bool = True

@dataclass
class ThreatStateConfig:
    """威胁状态配置"""
    threat_mode: ThreatMode
    lv2_keywords: List[str]
    lv2_behavior: BehaviorPolicy
    lv1_upgrade_condition: UpgradeCondition
    lv1_behavior: BehaviorPolicy
    risk_type: str
    priority: int = 3

@dataclass
class RiskConfig:
    """风险评估配置（扩展版）"""
    # 全局阈值（向后兼容）
    global_ttc_critical: float = 3.0
    global_min_safe_distance: Optional[float] = None
    
    # 威胁状态配置（新）
    threat_states: Dict[str, ThreatStateConfig] = field(default_factory=dict)
    
    def __post_init__(self):
        """初始化默认威胁状态配置"""
        if not self.threat_states:
            self.threat_states = {
                "water_edge": ThreatStateConfig(
                    threat_mode=ThreatMode.APPROACH,
                    lv2_keywords=["water", "水", "河", "湖", "池", "海", "edge", "边缘"],
                    lv2_behavior=BehaviorPolicy(
                        should_speak=False,  # LV2 不播报
                        can_interrupt=False,
                        speech_priority=1
                    ),
                    lv1_upgrade_condition=UpgradeCondition(
                        ttc_threshold=3.0,
                        ttc_strict=True,
                        distance_threshold=2.0,
                        distance_strict=True,
                        require_moving_towards=True,
                        combine_logic="OR"
                    ),
                    lv1_behavior=BehaviorPolicy(
                        should_speak=True,  # LV1 必须播报
                        can_interrupt=True,  # 可以打断系统播报
                        can_interrupt_user=False,  # 不打断用户说话
                        speech_priority=3,
                        bypass_deduplication=True,
                        bypass_cooldown=True
                    ),
                    risk_type="water_edge",
                    priority=3
                ),
                "road": ThreatStateConfig(
                    threat_mode=ThreatMode.PATH_INTERSECT,
                    lv2_keywords=["road", "路", "马路", "街道", "car", "车", "traffic", "交通"],
                    lv2_behavior=BehaviorPolicy(
                        should_speak=False,
                        can_interrupt=False,
                        speech_priority=1
                    ),
                    lv1_upgrade_condition=UpgradeCondition(
                        ttc_threshold=3.0,
                        ttc_strict=True,
                        distance_threshold=3.0,
                        distance_strict=True,
                        require_moving_towards=True,
                        combine_logic="OR"
                    ),
                    lv1_behavior=BehaviorPolicy(
                        should_speak=True,
                        can_interrupt=True,
                        can_interrupt_user=False,
                        speech_priority=3,
                        bypass_deduplication=True,
                        bypass_cooldown=True
                    ),
                    risk_type="road",
                    priority=3
                ),
                "obstacle": ThreatStateConfig(
                    threat_mode=ThreatMode.STATIC_PROXIMITY,
                    lv2_keywords=["obstacle", "障碍", "block", "阻挡", "wall", "墙"],
                    lv2_behavior=BehaviorPolicy(
                        should_speak=False,
                        can_interrupt=False,
                        speech_priority=1
                    ),
                    lv1_upgrade_condition=UpgradeCondition(
                        ttc_threshold=5.0,
                        ttc_strict=True,
                        distance_threshold=2.0,
                        distance_strict=True,
                        require_moving_towards=True,
                        combine_logic="OR"
                    ),
                    lv1_behavior=BehaviorPolicy(
                        should_speak=True,
                        can_interrupt=True,
                        can_interrupt_user=False,
                        speech_priority=2,
                        bypass_deduplication=True,
                        bypass_cooldown=True
                    ),
                    risk_type="obstacle",
                    priority=2
                ),
                "stair": ThreatStateConfig(
                    threat_mode=ThreatMode.STATIC_PROXIMITY,
                    lv2_keywords=["stair", "楼梯", "step", "台阶"],
                    lv2_behavior=BehaviorPolicy(
                        should_speak=False,
                        can_interrupt=False,
                        speech_priority=1
                    ),
                    lv1_upgrade_condition=UpgradeCondition(
                        ttc_threshold=4.0,
                        ttc_strict=True,
                        distance_threshold=1.5,
                        distance_strict=True,
                        require_moving_towards=True,
                        combine_logic="OR"
                    ),
                    lv1_behavior=BehaviorPolicy(
                        should_speak=True,
                        can_interrupt=True,
                        can_interrupt_user=False,
                        speech_priority=2,
                        bypass_deduplication=True,
                        bypass_cooldown=True
                    ),
                    risk_type="stair",
                    priority=2
                )
            }
```

---

## 3. 使用示例

### 3.1 默认配置

```python
from core.risk_assessor import RiskConfig

# 使用默认配置
config = RiskConfig()

# 访问水边风险配置
water_config = config.threat_states["water_edge"]
print(water_config.lv1_upgrade_condition.ttc_threshold)  # 3.0
print(water_config.lv1_behavior.should_speak)  # True
```

### 3.2 自定义配置

```python
from core.risk_assessor import RiskConfig, ThreatStateConfig, UpgradeCondition, BehaviorPolicy, ThreatMode

# 自定义水边风险：更严格的 TTC
custom_config = RiskConfig()
custom_config.threat_states["water_edge"].lv1_upgrade_condition.ttc_threshold = 2.0

# 或者创建全新的风险类型
custom_config.threat_states["cliff"] = ThreatStateConfig(
    threat_mode=ThreatMode.APPROACH,
    lv2_keywords=["cliff", "悬崖", "陡坡"],
    lv2_behavior=BehaviorPolicy(should_speak=False),
    lv1_upgrade_condition=UpgradeCondition(
        ttc_threshold=2.0,  # 更严格
        distance_threshold=1.0,  # 更严格
        require_moving_towards=True,
        combine_logic="OR"
    ),
    lv1_behavior=BehaviorPolicy(
        should_speak=True,
        can_interrupt=True,
        speech_priority=3
    ),
    risk_type="cliff",
    priority=3
)
```

---

## 4. assess_risk() 函数使用配置的伪代码

```python
def assess_risk(
    scene_state: Any,
    motion_state: Optional[MotionState] = None,
    config: Optional[RiskConfig] = None
) -> RiskResult:
    """
    使用配置驱动的风险评估
    """
    if config is None:
        config = RiskConfig()  # 使用默认配置
    
    # 遍历所有威胁状态配置
    for risk_type, threat_config in config.threat_states.items():
        # 1. 检查关键词（触发 LV2）
        if _matches_keywords(scene_state, threat_config.lv2_keywords):
            # 2. 检查升级条件（LV2 → LV1）
            if _check_upgrade_condition(motion_state, threat_config.lv1_upgrade_condition):
                # LV1: 即时威胁
                return RiskResult(
                    level=RiskLevel.IMMEDIATE,
                    reason=risk_type,
                    ttc=motion_state.estimated_ttc if motion_state else None,
                    distance=motion_state.estimated_distance if motion_state else None
                )
            else:
                # LV2: 潜在威胁
                return RiskResult(
                    level=RiskLevel.POTENTIAL,
                    reason=risk_type,
                    distance=motion_state.estimated_distance if motion_state else None
                )
    
    # 安全
    return RiskResult(level=RiskLevel.SAFE)
```

---

## 5. 配置参数完整清单（扩展版）

### 5.1 全局配置（2个）

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `global_ttc_critical` | `float` | `3.0` | 全局 TTC 临界值（向后兼容） |
| `global_min_safe_distance` | `Optional[float]` | `None` | 全局最小安全距离（向后兼容） |

### 5.2 威胁状态配置（每个风险类型 × 7个属性）

| 参数路径 | 类型 | 默认值 | 说明 |
|---------|------|--------|------|
| `threat_states[risk_type].threat_mode` | `ThreatMode` | `APPROACH` | 威胁模式 |
| `threat_states[risk_type].lv2_keywords` | `List[str]` | `[...]` | LV2 触发关键词 |
| `threat_states[risk_type].lv2_behavior.should_speak` | `bool` | `False` | LV2 是否播报 |
| `threat_states[risk_type].lv1_upgrade_condition.ttc_threshold` | `Optional[float]` | `3.0` | LV1 TTC 阈值 |
| `threat_states[risk_type].lv1_upgrade_condition.distance_threshold` | `Optional[float]` | `2.0` | LV1 距离阈值 |
| `threat_states[risk_type].lv1_behavior.should_speak` | `bool` | `True` | LV1 是否播报 |
| `threat_states[risk_type].lv1_behavior.can_interrupt` | `bool` | `True` | LV1 是否可打断 |

**总计**: 2 个全局 + 4 个风险类型 × 7 个属性 = **30 个可配置参数**

---

## 6. 设计优势

### 6.1 语义清晰

- ✅ **LV2 / LV1 明确分离**: 通过 `lv2_behavior` 和 `lv1_behavior` 区分
- ✅ **威胁模式明确**: `ThreatMode` 枚举定义威胁类型
- ✅ **升级条件可配置**: `UpgradeCondition` 支持灵活组合

### 6.2 可扩展性强

- ✅ **新增风险类型**: 只需在 `threat_states` 中添加新配置
- ✅ **新增威胁模式**: 只需在 `ThreatMode` 枚举中添加
- ✅ **新增升级条件**: 只需在 `UpgradeCondition` 中添加字段

### 6.3 可调试性强

```python
# 直接打印配置
config = RiskConfig()
print(config.threat_states["water_edge"])

# 输出：
# ThreatStateConfig(
#     threat_mode=ThreatMode.APPROACH,
#     lv2_keywords=['water', '水', ...],
#     lv1_upgrade_condition=UpgradeCondition(ttc_threshold=3.0, ...),
#     ...
# )
```

---

## 7. 与现有设计的兼容性

### 7.1 向后兼容

- ✅ 保留 `global_ttc_critical` 和 `global_min_safe_distance`（向后兼容）
- ✅ 现有调用 `assess_risk(scene_state, motion_state)` 仍然有效
- ✅ `config=None` 时使用默认配置

### 7.2 渐进式迁移

**阶段 1（当前）**: 使用硬编码值
**阶段 2（v1.8.3）**: 引入 `RiskConfig`，但使用默认值
**阶段 3（v1.9）**: 支持从配置文件加载自定义配置

---

## 8. 总结

### 核心设计原则

1. **语义分离**: LV2 和 LV1 有独立的配置和行为策略
2. **条件可配置**: 升级条件支持时间、距离、运动趋势的组合
3. **行为可配置**: 播报、打断、优先级都可配置
4. **类型安全**: 使用 dataclass 和 Enum，IDE 自动补全

### 未来使用方式

```python
# risk_assessor 只做三件事：
# 1. 读取参数
config = RiskConfig()  # 或从配置文件加载

# 2. 计算状态
risk_result = assess_risk(scene_state, motion_state, config)

# 3. 输出结果
return risk_result  # 包含 level, reason, ttc, distance
```

**决策和行为策略由其他模块负责**，`risk_assessor` 只负责"判断"。



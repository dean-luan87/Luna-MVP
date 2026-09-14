# v1.8.4 危险评估与告知系统 - 实现级参数表

## 一、数据结构定义

### 1. RiskObject（危险对象）

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any

class RiskClass(Enum):
    """危险类别"""
    STATIC = "STATIC"      # 静态危险（水体、台阶等）
    DYNAMIC = "DYNAMIC"    # 动态危险（车辆、人群等）

class RiskType(Enum):
    """危险类型"""
    WATER_EDGE = "WATER_EDGE"
    ROAD = "ROAD"
    STAIR = "STAIR"
    OBSTACLE = "OBSTACLE"

class GeometryType(Enum):
    """几何类型"""
    POINT = "POINT"    # 井盖、坑洞
    LINE = "LINE"      # 湖畔、护栏、台阶
    AREA = "AREA"      # 施工区、事故区

class RiskObjectState(Enum):
    """危险对象状态"""
    DORMANT = "DORMANT"      # 已感知，不提醒
    WARNED = "WARNED"        # 已触发过一次提醒
    COOLDOWN = "COOLDOWN"    # 冷却期，防重复

@dataclass
class Geometry:
    """几何信息"""
    type: GeometryType
    length_m: Optional[float] = None      # LINE 类型使用
    width_m: Optional[float] = None       # AREA 类型使用
    radius_m: Optional[float] = None      # POINT 类型使用

@dataclass
class RiskObject:
    """危险对象模型"""
    risk_id: str
    risk_class: RiskClass
    risk_type: RiskType
    geometry: Geometry
    hazard_level: float              # 0.0 ~ 1.0
    confidence: float                # 0.0 ~ 1.0
    state: RiskObjectState
    edge_distance_m: Optional[float] = None
    edge_trend: str = "STABLE"       # "APPROACHING" | "STABLE" | "RETREATING"
    last_warned_time: Optional[float] = None
```

---

### 2. RiskLevel 计算参数

```python
@dataclass
class RiskLevelParams:
    """RiskLevel 计算参数"""
    # HazardLevel 映射（基于 RiskType）
    hazard_level_map: Dict[RiskType, float] = None
    
    # ProximityFactor 计算参数
    proximity_threshold_m: float = 5.0      # 距离阈值（米）
    proximity_max_factor: float = 2.0        # 最大接近因子
    
    # TrendFactor 计算参数
    trend_approaching_factor: float = 1.5    # 接近时的趋势因子
    trend_stable_factor: float = 1.0         # 稳定时的趋势因子
    trend_retreating_factor: float = 0.8    # 远离时的趋势因子
    
    # 态势上升检测参数
    delta_risk_threshold: float = 0.3        # ΔRisk 阈值（触发警告）
    delta_risk_window_seconds: float = 2.0  # 时间窗口（秒）
    
    # 冷却期参数
    cooldown_seconds: float = 10.0           # 冷却期时长（秒）
    debounce_seconds: float = 1.0            # 去抖时间（秒）
```

---

### 3. 警告策略参数

```python
@dataclass
class AdvisoryConfig:
    """警告策略配置"""
    # 警告文本模板
    warning_templates: Dict[RiskType, str] = None
    
    # 警告触发条件
    require_risk_level_above: float = 0.5   # RiskLevel 必须高于此值
    require_delta_risk: bool = True          # 必须检测到态势上升
    
    # 一次性触发
    one_time_only: bool = True               # 是否只触发一次
    allow_repeat_on_escalation: bool = True  # 态势再次上升时是否允许重复触发
```

---

## 二、核心函数签名

### 1. HazardLevel 计算

```python
def calculate_hazard_level(
    risk_type: RiskType,
    scene_context: Dict[str, Any],
    config: RiskLevelParams
) -> float:
    """
    计算环境危险程度（HazardLevel）
    
    Args:
        risk_type: 危险类型
        scene_context: 场景上下文（包含 objects, signs 等）
        config: 计算参数
    
    Returns:
        float: HazardLevel (0.0 ~ 1.0)
    """
    # 基于 risk_type 和 scene_context 计算
    # 例如：水体 + 无护栏 → 0.8，水体 + 有护栏 → 0.5
    pass
```

---

### 2. ProximityFactor 计算

```python
def calculate_proximity_factor(
    distance_m: Optional[float],
    config: RiskLevelParams
) -> float:
    """
    计算接近因子（ProximityFactor）
    
    Args:
        distance_m: 与危险边界的距离（米）
        config: 计算参数
    
    Returns:
        float: ProximityFactor (1.0 ~ max_factor)
    """
    if distance_m is None:
        return 1.0
    
    if distance_m >= config.proximity_threshold_m:
        return 1.0
    
    # 线性插值：距离越近，因子越大
    ratio = 1.0 - (distance_m / config.proximity_threshold_m)
    return 1.0 + ratio * (config.proximity_max_factor - 1.0)
```

---

### 3. TrendFactor 计算

```python
def calculate_trend_factor(
    edge_trend: str,
    config: RiskLevelParams
) -> float:
    """
    计算趋势因子（TrendFactor）
    
    Args:
        edge_trend: 边缘趋势（"APPROACHING" | "STABLE" | "RETREATING"）
        config: 计算参数
    
    Returns:
        float: TrendFactor
    """
    if edge_trend == "APPROACHING":
        return config.trend_approaching_factor
    elif edge_trend == "RETREATING":
        return config.trend_retreating_factor
    else:
        return config.trend_stable_factor
```

---

### 4. RiskLevel 计算

```python
def calculate_risk_level(
    risk_object: RiskObject,
    motion_state: Optional[MotionState],
    config: RiskLevelParams
) -> float:
    """
    计算态势风险等级（RiskLevel）
    
    RiskLevel = HazardLevel × ProximityFactor × TrendFactor
    
    Args:
        risk_object: 危险对象
        motion_state: 运动状态（可选）
        config: 计算参数
    
    Returns:
        float: RiskLevel (0.0 ~ 理论上限)
    """
    hazard_level = risk_object.hazard_level
    
    # 计算 ProximityFactor
    distance = risk_object.edge_distance_m or motion_state.estimated_distance if motion_state else None
    proximity_factor = calculate_proximity_factor(distance, config)
    
    # 计算 TrendFactor
    trend_factor = calculate_trend_factor(risk_object.edge_trend, config)
    
    # 计算 RiskLevel
    risk_level = hazard_level * proximity_factor * trend_factor
    
    return risk_level
```

---

### 5. 态势上升检测

```python
def detect_risk_escalation(
    risk_object: RiskObject,
    current_risk_level: float,
    risk_history: List[Tuple[float, float]],  # [(timestamp, risk_level), ...]
    config: RiskLevelParams
) -> bool:
    """
    检测危险态势是否上升
    
    Args:
        risk_object: 危险对象
        current_risk_level: 当前 RiskLevel
        risk_history: 风险历史记录
        config: 计算参数
    
    Returns:
        bool: 是否检测到态势上升
    """
    if not risk_history:
        return False
    
    # 获取时间窗口内的风险记录
    now = time.time()
    window_start = now - config.delta_risk_window_seconds
    
    recent_risks = [
        (ts, rl) for ts, rl in risk_history
        if ts >= window_start
    ]
    
    if not recent_risks:
        return False
    
    # 计算最小 RiskLevel（时间窗口内）
    min_risk = min(rl for _, rl in recent_risks)
    
    # 计算 ΔRisk
    delta_risk = current_risk_level - min_risk
    
    # 判断是否超过阈值
    return delta_risk >= config.delta_risk_threshold
```

---

### 6. 警告触发判断

```python
def should_trigger_advisory(
    risk_object: RiskObject,
    current_risk_level: float,
    risk_history: List[Tuple[float, float]],
    config: RiskLevelParams,
    advisory_config: AdvisoryConfig
) -> bool:
    """
    判断是否应该触发警告
    
    Args:
        risk_object: 危险对象
        current_risk_level: 当前 RiskLevel
        risk_history: 风险历史记录
        config: RiskLevel 计算参数
        advisory_config: 警告策略配置
    
    Returns:
        bool: 是否应该触发警告
    """
    # 条件 1: RiskLevel 必须高于阈值
    if current_risk_level < advisory_config.require_risk_level_above:
        return False
    
    # 条件 2: 必须检测到态势上升（如果要求）
    if advisory_config.require_delta_risk:
        if not detect_risk_escalation(risk_object, current_risk_level, risk_history, config):
            return False
    
    # 条件 3: 状态检查
    if risk_object.state == RiskObjectState.COOLDOWN:
        return False
    
    # 条件 4: 一次性触发检查
    if advisory_config.one_time_only and risk_object.state == RiskObjectState.WARNED:
        # 如果允许在态势再次上升时重复触发
        if advisory_config.allow_repeat_on_escalation:
            # 需要检测到新的态势上升
            if not detect_risk_escalation(risk_object, current_risk_level, risk_history, config):
                return False
        else:
            return False
    
    # 条件 5: 去抖检查
    if risk_object.last_warned_time:
        now = time.time()
        if now - risk_object.last_warned_time < advisory_config.debounce_seconds:
            return False
    
    return True
```

---

### 7. 状态机更新

```python
def update_risk_object_state(
    risk_object: RiskObject,
    triggered: bool,
    config: RiskLevelParams
) -> RiskObject:
    """
    更新危险对象状态
    
    Args:
        risk_object: 危险对象
        triggered: 是否触发了警告
        config: 计算参数
    
    Returns:
        RiskObject: 更新后的危险对象
    """
    now = time.time()
    
    if triggered:
        # 触发警告 → 进入 WARNED 状态
        risk_object.state = RiskObjectState.WARNED
        risk_object.last_warned_time = now
    elif risk_object.state == RiskObjectState.WARNED:
        # WARNED 状态 → 进入 COOLDOWN
        if risk_object.last_warned_time:
            if now - risk_object.last_warned_time >= config.cooldown_seconds:
                risk_object.state = RiskObjectState.COOLDOWN
    elif risk_object.state == RiskObjectState.COOLDOWN:
        # COOLDOWN 状态 → 可以回到 DORMANT（如果风险降低）
        # 这里可以根据业务逻辑决定是否自动回到 DORMANT
        pass
    
    return risk_object
```

---

### 8. 警告文本生成

```python
def generate_advisory_text(
    risk_object: RiskObject,
    advisory_config: AdvisoryConfig
) -> str:
    """
    生成警告文本（只描述空间关系，不描述行为）
    
    Args:
        risk_object: 危险对象
        advisory_config: 警告策略配置
    
    Returns:
        str: 警告文本
    """
    template = advisory_config.warning_templates.get(risk_object.risk_type)
    if not template:
        # 默认模板
        template = "您已接近{risk_type}，请注意与边缘保持安全距离。"
    
    # 替换占位符
    text = template.format(
        risk_type=risk_object.risk_type.value,
        distance=risk_object.edge_distance_m
    )
    
    return text
```

---

## 三、默认参数值

```python
# RiskLevelParams 默认值
DEFAULT_RISK_LEVEL_PARAMS = RiskLevelParams(
    hazard_level_map={
        RiskType.WATER_EDGE: 0.8,
        RiskType.ROAD: 0.7,
        RiskType.STAIR: 0.5,
        RiskType.OBSTACLE: 0.6,
    },
    proximity_threshold_m=5.0,
    proximity_max_factor=2.0,
    trend_approaching_factor=1.5,
    trend_stable_factor=1.0,
    trend_retreating_factor=0.8,
    delta_risk_threshold=0.3,
    delta_risk_window_seconds=2.0,
    cooldown_seconds=10.0,
    debounce_seconds=1.0,
)

# AdvisoryConfig 默认值
DEFAULT_ADVISORY_CONFIG = AdvisoryConfig(
    warning_templates={
        RiskType.WATER_EDGE: "您已接近湖边，请注意与边缘保持安全距离。",
        RiskType.ROAD: "前方是道路，请注意车辆。",
        RiskType.STAIR: "前方是连续台阶，请注意脚下。",
        RiskType.OBSTACLE: "前方有障碍物，请注意避让。",
    },
    require_risk_level_above=0.5,
    require_delta_risk=True,
    one_time_only=True,
    allow_repeat_on_escalation=True,
)
```

---

## 四、与 v1.8.3 的集成点

### 1. 在 `assess_risk()` 基础上扩展

```python
def evaluate_risk_advisory(
    scene_state: Any,
    motion_state: Optional[MotionState],
    risk_objects: List[RiskObject],
    risk_history: Dict[str, List[Tuple[float, float]]],
    config: Optional[RiskLevelParams] = None,
    advisory_config: Optional[AdvisoryConfig] = None
) -> Dict[str, Any]:
    """
    v1.8.4: 危险评估与告知（基于 v1.8.3 的 assess_risk）
    
    Args:
        scene_state: 场景状态（来自 v1.8.3）
        motion_state: 运动状态（来自 v1.8.3）
        risk_objects: 危险对象列表
        risk_history: 风险历史记录 {risk_id: [(timestamp, risk_level), ...]}
        config: RiskLevel 计算参数
        advisory_config: 警告策略配置
    
    Returns:
        Dict[str, Any]: 评估结果
            - should_advisory: bool 是否应该触发警告
            - advisory_text: str 警告文本（如果应该触发）
            - risk_level: float 当前 RiskLevel
            - risk_object: RiskObject 触发的危险对象
    """
    config = config or DEFAULT_RISK_LEVEL_PARAMS
    advisory_config = advisory_config or DEFAULT_ADVISORY_CONFIG
    
    # 对每个危险对象进行评估
    for risk_object in risk_objects:
        # 计算当前 RiskLevel
        current_risk_level = calculate_risk_level(risk_object, motion_state, config)
        
        # 更新风险历史
        risk_history.setdefault(risk_object.risk_id, []).append(
            (time.time(), current_risk_level)
        )
        
        # 判断是否应该触发警告
        if should_trigger_advisory(
            risk_object, current_risk_level,
            risk_history[risk_object.risk_id],
            config, advisory_config
        ):
            # 生成警告文本
            advisory_text = generate_advisory_text(risk_object, advisory_config)
            
            # 更新状态
            risk_object = update_risk_object_state(risk_object, True, config)
            
            return {
                "should_advisory": True,
                "advisory_text": advisory_text,
                "risk_level": current_risk_level,
                "risk_object": risk_object,
            }
    
    return {
        "should_advisory": False,
        "risk_level": 0.0,
    }
```

---

### 2. 与 `DecisionController` 集成

```python
# 在 decide() 函数中
def decide(
    scene_state: SceneState,
    speech_gate: SpeechGate,
    user_state: UserState,
    motion_state: Optional[MotionState] = None,
    risk_advisory_result: Optional[Dict[str, Any]] = None  # v1.8.4 新增
) -> Dict[str, Any]:
    """
    决策函数（v1.8.3a 阶段 C + v1.8.4 危险告知）
    """
    # 决策 0: 风险评估（v1.8.3）
    risk = assess_risk(scene_state, motion_state)
    
    # 决策 0.5: 危险告知（v1.8.4，优先级低于 LV1，高于正常播报）
    if risk_advisory_result and risk_advisory_result.get("should_advisory"):
        return {
            "action": "ADVISORY",  # 新增动作类型
            "reason": "risk_advisory_escalation",
            "advisory_text": risk_advisory_result["advisory_text"],
            "risk_level": risk_advisory_result["risk_level"],
            "risk_object": risk_advisory_result["risk_object"],
            "bypass_speech_gate": False,  # 危险告知不走 bypass
        }
    
    # 后续逻辑保持不变...
```

---

## 五、实现优先级

### Phase 1：核心模型（必须）
1. ✅ `RiskObject` 数据模型
2. ✅ `HazardLevel` 计算
3. ✅ `RiskLevel` 计算（HazardLevel × ProximityFactor × TrendFactor）
4. ✅ 态势上升检测（ΔRisk）

### Phase 2：状态管理（必须）
1. ✅ 状态机实现（DORMANT → WARNED → COOLDOWN）
2. ✅ 冷却期管理
3. ✅ 去抖逻辑

### Phase 3：警告策略（必须）
1. ✅ 警告文本生成
2. ✅ 一次性触发逻辑
3. ✅ 与 `DecisionController` 集成

### Phase 4：接口预留（可选）
1. ⚠️ `SafetyBoundary` 接口定义
2. ⚠️ 世界模型接口约定
3. ⚠️ 扩展点文档



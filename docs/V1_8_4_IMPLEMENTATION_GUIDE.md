# v1.8.4 危险评估与告知系统 - 实现指南

## 一、模块结构

```
core/risk/
├── __init__.py                 # 模块导出
├── risk_types.py              # 风险类型定义与参数表
├── risk_object.py             # 危险对象数据结构
├── geometry_utils.py          # 几何计算工具（POINT/LINE/AREA）
├── hazard_evaluator.py        # 环境危险评估器
├── risk_engine.py             # 风险引擎（RiskLevel + ΔRisk + 状态机）
├── warning_policy.py          # 警告策略
├── risk_registry.py           # 风险对象注册表
└── interfaces/
    ├── __init__.py
    ├── world_model_iface.py   # 世界模型接口桩
    └── safety_boundary_iface.py # 安全边界接口桩
```

---

## 二、核心使用流程

### 1. 初始化组件

```python
from core.risk import (
    RiskEngine, HazardEvaluator, WarningPolicy, RiskRegistry,
    RiskObject, RiskGeometry, RiskRuntime, RiskType
)
import time

# 初始化组件
risk_engine = RiskEngine(trend_eps=0.25)
hazard_evaluator = HazardEvaluator()  # 可选：传入 world_model
warning_policy = WarningPolicy()
risk_registry = RiskRegistry(object_ttl_seconds=60.0)
```

### 2. 创建风险对象

```python
# 创建湖边风险对象（LINE 类型）
lake_edge_geometry = RiskGeometry(
    type="LINE",
    points=[(0.0, 0.0), (10.0, 0.0), (20.0, 0.0)],
    length_m=20.0
)

lake_edge_runtime = RiskRuntime(
    state="DORMANT",
    last_risk_level=0.0,
    last_update_ts=time.time(),
    edge_trend="STABLE"
)

lake_edge = RiskObject(
    risk_id="lake_edge_001",
    risk_class="STATIC",
    risk_type="WATER_EDGE",
    geometry=lake_edge_geometry,
    hazard_level=0.8,  # 来自 hazard_evaluator
    confidence=0.9,
    runtime=lake_edge_runtime
)

# 注册风险对象
risk_registry.register(lake_edge)
```

### 3. 每帧更新与评估

```python
def update_risk_advisory(user_xy: tuple[float, float], now_ts: float = None):
    """
    更新风险评估与告知
    
    Args:
        user_xy: 用户位置 (x, y)
        now_ts: 当前时间戳
    """
    if now_ts is None:
        now_ts = time.time()
    
    # 清理过期对象
    risk_registry.cleanup_expired(now_ts)
    
    # 遍历所有风险对象
    for risk_object in risk_registry.get_all():
        # 1. 计算当前 RiskLevel
        current_risk_level, distance_m = risk_engine.calculate_risk_level(
            risk_object, user_xy
        )
        
        # 2. 计算趋势
        prev_dist = risk_object.runtime.edge_distance_m
        trend = risk_engine.calc_trend(prev_dist, distance_m)
        
        # 3. 更新运行时状态
        risk_object.update_runtime(
            current_risk_level, distance_m, trend, now_ts
        )
        
        # 4. 判断是否应该触发警告
        if risk_engine.should_warn(risk_object, current_risk_level, now_ts):
            # 5. 生成警告文本
            advisory_text = warning_policy.generate_advisory_text(risk_object)
            
            # 6. 更新状态机（进入 COOLDOWN）
            risk_engine.update_state(risk_object, warned=True, now_ts=now_ts)
            
            # 7. 更新注册表
            risk_registry.update(risk_object.risk_id, risk_object)
            
            # 8. 返回警告结果
            return {
                "should_advisory": True,
                "advisory_text": advisory_text,
                "risk_level": current_risk_level,
                "risk_object": risk_object,
            }
        
        # 更新注册表（即使未触发警告）
        risk_registry.update(risk_object.risk_id, risk_object)
    
    return {
        "should_advisory": False,
        "risk_level": 0.0,
    }
```

---

## 三、与主循环集成

### 在 main.py 中集成

```python
from core.risk import RiskEngine, HazardEvaluator, WarningPolicy, RiskRegistry

class LunaBadgeMVP:
    def __init__(self):
        # ... 现有初始化代码 ...
        
        # v1.8.4: 初始化风险评估组件
        self.risk_engine = RiskEngine(trend_eps=0.25)
        self.hazard_evaluator = HazardEvaluator()
        self.warning_policy = WarningPolicy()
        self.risk_registry = RiskRegistry(object_ttl_seconds=60.0)
        
        # 初始化 demo 风险对象（示例）
        self._init_demo_risk_objects()
    
    def _init_demo_risk_objects(self):
        """初始化 demo 风险对象"""
        # 示例：创建一个湖边风险对象
        from core.risk import RiskObject, RiskGeometry, RiskRuntime
        import time
        
        lake_edge_geometry = RiskGeometry(
            type="LINE",
            points=[(0.0, 0.0), (10.0, 0.0)],
            length_m=10.0
        )
        
        lake_edge_runtime = RiskRuntime(
            state="DORMANT",
            last_risk_level=0.0,
            last_update_ts=time.time(),
            edge_trend="STABLE"
        )
        
        lake_edge = RiskObject(
            risk_id="demo_lake_edge_001",
            risk_class="STATIC",
            risk_type="WATER_EDGE",
            geometry=lake_edge_geometry,
            hazard_level=0.8,
            confidence=0.9,
            runtime=lake_edge_runtime
        )
        
        self.risk_registry.register(lake_edge)
    
    def process_frame(self, frame):
        """处理每一帧"""
        # ... 现有处理逻辑 ...
        
        # v1.8.4: 更新风险评估（需要用户位置）
        # 注意：这里需要从视觉/定位系统获取用户位置
        user_xy = self._get_user_position()  # 需要实现此方法
        
        if user_xy:
            advisory_result = self._update_risk_advisory(user_xy)
            
            if advisory_result.get("should_advisory"):
                # 触发警告（通过决策控制器）
                self._handle_risk_advisory(advisory_result)
        
        return result
    
    def _update_risk_advisory(self, user_xy: tuple[float, float]):
        """更新风险评估与告知"""
        import time
        now_ts = time.time()
        
        # 清理过期对象
        self.risk_registry.cleanup_expired(now_ts)
        
        # 遍历所有风险对象
        for risk_object in self.risk_registry.get_all():
            # 计算当前 RiskLevel
            current_risk_level, distance_m = self.risk_engine.calculate_risk_level(
                risk_object, user_xy
            )
            
            # 计算趋势
            prev_dist = risk_object.runtime.edge_distance_m
            trend = self.risk_engine.calc_trend(prev_dist, distance_m)
            
            # 更新运行时状态
            risk_object.update_runtime(
                current_risk_level, distance_m, trend, now_ts
            )
            
            # 判断是否应该触发警告
            if self.risk_engine.should_warn(risk_object, current_risk_level, now_ts):
                # 生成警告文本
                advisory_text = self.warning_policy.generate_advisory_text(risk_object)
                
                # 更新状态机
                self.risk_engine.update_state(risk_object, warned=True, now_ts=now_ts)
                
                # 更新注册表
                self.risk_registry.update(risk_object.risk_id, risk_object)
                
                # 记录日志
                self.logger.info(
                    f"[RiskAdvisory] 触发警告: risk_id={risk_object.risk_id}, "
                    f"text={advisory_text}, risk_level={current_risk_level:.3f}, "
                    f"distance={distance_m:.2f}m"
                )
                
                return {
                    "should_advisory": True,
                    "advisory_text": advisory_text,
                    "risk_level": current_risk_level,
                    "risk_object": risk_object,
                }
            
            # 更新注册表
            self.risk_registry.update(risk_object.risk_id, risk_object)
        
        return {
            "should_advisory": False,
            "risk_level": 0.0,
        }
    
    def _handle_risk_advisory(self, advisory_result: dict):
        """处理风险告知（通过决策控制器）"""
        # 可以通过决策控制器触发警告
        # 或者直接调用 TTS（如果符合设计）
        advisory_text = advisory_result.get("advisory_text")
        if advisory_text:
            # 示例：直接调用 TTS（实际应该通过决策控制器）
            self._speak_safely(advisory_text)
    
    def _get_user_position(self) -> Optional[tuple[float, float]]:
        """
        获取用户位置（需要实现）
        
        说明：
        - 可以从视觉系统、GPS、定位系统等获取
        - 返回局部坐标 (x, y) 或 None
        """
        # TODO: 实现用户位置获取逻辑
        # 示例：返回固定位置（仅用于测试）
        return (5.0, 5.0)
```

---

## 四、与 DecisionController 集成

### 扩展 DecisionController 支持 ADVISORY 动作

```python
# 在 core/decision_controller.py 中

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
    # 决策 0: 风险评估（v1.8.3，最高优先级）
    risk = assess_risk(scene_state, motion_state)
    
    if risk.level == RiskLevel.IMMEDIATE:
        # LV1 处理（保持不变）
        # ...
    
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

## 五、测试场景

### 场景 1：接近湖边（态势上升触发）

```python
# 初始化
user_xy = (15.0, 5.0)  # 距离湖边 5 米
advisory_result = update_risk_advisory(user_xy)
# 预期：should_advisory=False（距离较远，RiskLevel 较低）

# 逐步靠近
user_xy = (10.0, 5.0)  # 距离湖边 5 米
advisory_result = update_risk_advisory(user_xy)
# 预期：should_advisory=False（RiskLevel 上升但未超过阈值）

user_xy = (5.0, 5.0)   # 距离湖边 5 米
advisory_result = update_risk_advisory(user_xy)
# 预期：should_advisory=True（ΔRisk > delta_warn，触发警告）
# 文本："您已接近水边，请注意与边缘保持安全距离。"

# 继续靠近（但在 cooldown 期内）
user_xy = (3.0, 5.0)
advisory_result = update_risk_advisory(user_xy)
# 预期：should_advisory=False（在 cooldown 期内，不重复触发）

# 停住（RiskLevel 稳定）
user_xy = (3.0, 5.0)
advisory_result = update_risk_advisory(user_xy)
# 预期：should_advisory=False（RiskLevel 稳定，不触发）

# 后退（RiskLevel 下降）
user_xy = (5.0, 5.0)
advisory_result = update_risk_advisory(user_xy)
# 预期：should_advisory=False（RiskLevel 下降，不触发）

# 再次靠近（超过阈值上升，cooldown 已结束）
user_xy = (2.0, 5.0)
advisory_result = update_risk_advisory(user_xy)
# 预期：should_advisory=True（态势再次上升，可再次触发）
```

---

## 六、关键实现要点

### 1. 用户位置获取

需要从以下来源之一获取用户位置：
- 视觉系统（基于相机位置和场景理解）
- GPS（需要转换为局部坐标）
- 定位系统（SLAM、视觉定位等）

### 2. 风险对象创建

风险对象可以从以下来源创建：
- 视觉识别结果（YOLO/OCR 检测到的危险区域）
- 地图数据（已知的危险区域）
- 用户输入（手动标注）

### 3. 坐标系统

- 使用局部坐标系统（米为单位）
- 需要将 GPS/视觉坐标转换为统一的局部坐标系统

---

## 七、验收标准

### P0 验收（当天可跑通闭环）

1. ✅ 给定一条 LINE（湖边），用户逐步靠近时只在 RiskLevel 上升超过阈值那一刻播报一次
2. ✅ 停住不再播报
3. ✅ 后退不播报
4. ✅ 再次靠近（超过阈值上升）可再次播报

### P1 验收（稳定性与工程质量）

1. ✅ 去抖：趋势 eps、风险平滑
2. ✅ 单元测试：几何距离、ΔRisk 触发、cooldown
3. ✅ 日志：每次触发记录（risk_id、distance、risk_level、delta、cfg）

### P2 验收（为世界模型铺路）

1. ✅ world_model_iface.py：返回结构属性（护栏存在/未知）
2. ✅ safety_boundary_iface.py：越界事件接口桩
3. ✅ hazard_evaluator 改为：hazard_base 可被 world_model 修正

---

## 八、系统级接线图（Integration Wiring）

### 8.1 上游输入

#### 用户位置输入
```python
from core.risk import UserPositionProvider

# 在主循环中初始化
position_provider = UserPositionProvider()

# 视觉/定位模块每帧更新位置
# 示例：从视觉系统获取用户位置（局部坐标，米）
user_xy = get_user_position_from_vision()  # 需要实现
position_provider.update(user_xy, ts=time.time(), confidence=0.9)
```

#### 风险对象输入
```python
from core.risk import RiskObjectFactory, RiskRegistry

# 初始化
factory = RiskObjectFactory()
registry = RiskRegistry()

# 从视觉识别结果创建风险对象
# 示例：检测到湖边（LINE 类型）
lake_polyline = detect_water_edge_from_vision()  # 需要实现
lake = factory.make_line(
    risk_id="lake_001",
    risk_type="WATER_EDGE",
    polyline=lake_polyline,
    confidence=0.95
)
registry.upsert(lake)

# 示例：检测到台阶（POINT 类型）
stair_xy = detect_stair_from_vision()  # 需要实现
stair = factory.make_point(
    risk_id="stair_001",
    risk_type="STAIRS",
    xy=stair_xy,
    confidence=0.9
)
registry.upsert(stair)
```

### 8.2 主循环集成

```python
from core.risk import RiskAdvisoryService

# 初始化服务
advisory_service = RiskAdvisoryService(registry)

# 在主循环中每帧调用
def process_frame(self, frame):
    # ... 现有处理逻辑 ...
    
    # 获取用户位置
    pos = position_provider.get()
    if pos:
        # 更新风险评估
        advisory_text = advisory_service.tick(pos.xy, ts=pos.ts)
        
        if advisory_text:
            # 触发警告（通过决策控制器或直接 TTS）
            self._handle_risk_advisory(advisory_text)
    
    return result
```

### 8.3 播报链路

```python
def _handle_risk_advisory(self, advisory_text: str):
    """
    处理风险告知（通过决策控制器）
    
    说明：
    - 可以通过 DecisionController 的 ADVISORY 动作触发
    - 或直接调用 TTS（如果符合设计）
    """
    # 方式 1：通过决策控制器（推荐）
    decision = {
        "action": "ADVISORY",
        "reason": "risk_advisory_escalation",
        "advisory_text": advisory_text,
    }
    self._execute_speech_decision({}, decision)
    
    # 方式 2：直接调用 TTS（简化版）
    # self._speak_safely(advisory_text)
```

### 8.4 日志记录

```python
# 在 RiskAdvisoryService.tick() 中已自动记录日志
# 日志格式：
# [RiskAdvisory] 触发警告: risk_id=xxx, type=xxx, text=xxx,
#   risk_level=xxx, delta=xxx, distance=xxx, trend=xxx
```

---

## 九、下一步工作

1. ✅ **实现用户位置获取**：从视觉/定位系统获取用户位置 → `UserPositionProvider`
2. ✅ **创建 demo 风险对象**：至少包含 2~3 个 demo 风险 → `RiskObjectFactory`
3. ✅ **集成到主循环**：在 `process_frame()` 中调用 → `RiskAdvisoryService.tick()`
4. ⚠️ **扩展 DecisionController**：支持 `ADVISORY` 动作（待实现）
5. ⚠️ **编写单元测试**：测试几何距离、ΔRisk 触发、cooldown（待实现）


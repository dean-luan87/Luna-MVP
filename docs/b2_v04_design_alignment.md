# B2 v0.4 设计对齐分析

## 一、核心定位对齐

### ✅ 已对齐
- B2 不替代 C，只提供增强信息
- B2 输出结构化变化结果，不直接干预 C

### ⚠️ 需要调整
- **当前 v0.3**：有固定时间窗口 `[now+1s, now+8s]`
- **v0.4 要求**：B2 不独立定义时间窗口，由 C 提供

**建议**：在 `tick()` 方法中添加可选参数 `time_window: Optional[Tuple[float, float]]`，如果 C 提供则使用，否则使用默认值。

---

## 二、工作边界对齐

### ✅ 已对齐
- B2 被 gate 掉时不阻断 C（当前实现中 B2 输出不影响 C 决策）

### ⚠️ 需要明确
- **距离边界**：距离 > 3m → B2 优先，距离 ≤ 3m / 室内 → C 主导
- **当前实现**：没有距离判断逻辑

**建议**：在 `tick()` 方法中添加 `distance_to_ego: Optional[float]` 参数，根据距离决定是否处理。

---

## 三、内部结构对齐

### 3.1 B2-A：行为前视放大器（Behavior Lookahead）

**v0.4 要求输出：**
- `need_slow_down`
- `need_stop`
- `need_detour`
- `path_uncertain`
- `safe_continue`

**当前 v0.3 输出：**
- `WorldChange`（level, confidence, factors, interrupt）

**差异**：当前输出是"环境描述"，v0.4 要求"行为建议"

**建议**：在 v0.4 中添加 `BehaviorAdvice` 数据类：

```python
@dataclass
class BehaviorAdvice:
    need_slow_down: bool = False
    need_stop: bool = False
    need_detour: bool = False
    path_uncertain: bool = False
    safe_continue: bool = True
    confidence: float = 0.0
    reason: str = ""
```

### 3.2 B2-B：路况变化补丁层（Road Delta Layer）

**v0.4 关注内容：**
- 路面可通行性变化
- 台阶 / 坑洼 / 积水
- 临时障碍（施工 / 封路）
- 路口结构变化

**当前 v0.3：**
- `FactorType.PATH` 已覆盖部分内容（surface, has_path）
- 需要扩展：台阶、坑洼、积水、临时障碍

**建议**：扩展 `perception["path"]` 结构：

```python
perception["path"] = {
    "surface": "concrete" | "gravel" | "stairs" | "water" | "pothole",
    "has_path": bool,
    "obstacles": [
        {"type": "construction" | "block" | "barrier", "severity": "low" | "mid" | "high"}
    ],
    "intersection_change": bool,
}
```

### 3.3 B2-C：本地环境知识缓存（Local Knowledge Cache）

**v0.4 要求：**
- 不主动推送
- 仅在 C 查询或情境需要时使用

**当前 v0.3：**
- 没有实现此模块

**建议**：v0.4 中新增 `B2KnowledgeCache` 类，提供 `query()` 方法而非主动推送。

---

## 四、时间语义对齐

### ⚠️ 需要调整

**当前 v0.3：**
```python
def __init__(
    self,
    future_window_start: float = 1.0,
    future_window_end: float = 8.0,
    ...
):
```

**v0.4 要求：**
- B2 不独立定义时间窗口
- 所有"未来 X 秒"的语义由 C 提供

**建议**：
```python
def tick(
    self,
    frame_ts: float,
    perception: Dict[str, Any],
    time_window: Optional[Tuple[float, float]] = None,  # C 提供的时间窗口
) -> Optional[Dict[str, Any]]:
    # 如果 C 提供了时间窗口，使用 C 的；否则使用默认值
    window_start, window_end = time_window or (self.future_window_start, self.future_window_end)
```

---

## 五、param_vector 用途对齐

### ✅ 已对齐

**v0.4 要求：**
- param_vector 用于学习工具，不是实时决策工具

**当前实现：**
- `param_encoder.py` 已实现参数向量编码
- `param_regression.py` 已实现误差回归
- `param_weight_update.py` 已实现权重调整建议

**结论**：当前实现符合 v0.4 设计。

---

## 六、运行策略对齐

### ⚠️ 需要调整

**v0.4 要求：**
- 事件驱动
- 价值驱动
- 可进入只读状态（熟悉、稳定、无变化的区域自动降权或休眠）

**当前 v0.3：**
- 每帧都调用 `tick()`（时间驱动）
- 没有"只读状态"或"休眠"机制

**建议**：
1. 添加 `_should_activate()` 方法，判断是否需要激活 B2
2. 添加 `_value_score()` 方法，评估当前帧的处理价值
3. 在稳定区域自动降权或跳过处理

---

## 七、明确非目标对齐

### ✅ 已对齐

**v0.4 明确非目标：**
- 情绪建模
- 人类心理推断
- 全量世界理解

**当前 v0.3：**
- 只关注世界变化，不涉及情绪、心理、全量理解

**结论**：当前实现符合 v0.4 设计。

---

## 八、迁移建议

### 阶段 1：保持 v0.3 兼容，添加 v0.4 接口

1. **时间窗口参数化**
   - 在 `tick()` 中添加 `time_window` 参数
   - 保持向后兼容（默认使用 `[1s, 8s]`）

2. **行为建议输出**
   - 新增 `BehaviorAdvice` 数据类
   - 在 `_summarize_world_change()` 中同时输出 `WorldChange` 和 `BehaviorAdvice`

3. **距离边界判断**
   - 在 `tick()` 中添加 `distance_to_ego` 参数
   - 根据距离决定是否处理

### 阶段 2：实现 B2-A/B/C 模块化

1. **B2-A：行为前视放大器**
   - 从 `WorldChange` 转换为 `BehaviorAdvice`
   - 需要 C 的任务状态和运动状态作为输入

2. **B2-B：路况变化补丁层**
   - 扩展 `perception["path"]` 结构
   - 增强 `FactorType.PATH` 的检测逻辑

3. **B2-C：本地环境知识缓存**
   - 新增 `B2KnowledgeCache` 类
   - 提供 `query()` 接口，不主动推送

### 阶段 3：事件驱动和价值驱动

1. **事件驱动**
   - 只在检测到变化时处理
   - 稳定区域跳过处理

2. **价值驱动**
   - 评估处理价值（变化概率、影响程度）
   - 低价值场景自动降权

---

## 九、关键代码修改点

### 1. `b2_v03.py` → `b2_v04.py`

```python
def tick(
    self,
    frame_ts: float,
    perception: Dict[str, Any],
    time_window: Optional[Tuple[float, float]] = None,  # C 提供
    distance_to_ego: Optional[float] = None,  # 距离判断
    c_task_state: Optional[str] = None,  # C 任务状态
    c_motion_state: Optional[Dict[str, Any]] = None,  # C 运动状态
) -> Optional[Dict[str, Any]]:
    # 1. 距离边界判断
    if distance_to_ego is not None and distance_to_ego <= 3.0:
        return None  # C 主导
    
    # 2. 使用 C 提供的时间窗口
    window_start, window_end = time_window or (self.future_window_start, self.future_window_end)
    
    # 3. 价值驱动：评估是否需要处理
    if not self._should_activate(perception):
        return None
    
    # 4. 原有逻辑...
    
    # 5. 输出行为建议（B2-A）
    behavior_advice = self._generate_behavior_advice(
        world_change, c_task_state, c_motion_state
    )
    
    return {
        "world_change": world_change,
        "behavior_advice": behavior_advice,
    }
```

### 2. 新增 `behavior_advice.py`

```python
@dataclass
class BehaviorAdvice:
    need_slow_down: bool = False
    need_stop: bool = False
    need_detour: bool = False
    path_uncertain: bool = False
    safe_continue: bool = True
    confidence: float = 0.0
    reason: str = ""

def generate_behavior_advice(
    world_change: WorldChange,
    c_task_state: Optional[str],
    c_motion_state: Optional[Dict[str, Any]],
) -> BehaviorAdvice:
    """从 WorldChange 生成行为建议"""
    # 实现逻辑...
```

---

## 十、总结

### ✅ 已对齐的部分
1. B2 不替代 C，只提供增强信息
2. param_vector 用于学习工具
3. 明确非目标（情绪、心理、全量理解）

### ⚠️ 需要调整的部分
1. 时间窗口应由 C 提供，而非 B2 独立定义
2. 输出应从"环境描述"转为"行为建议"
3. 需要距离边界判断（>3m vs ≤3m）
4. 需要事件驱动和价值驱动机制
5. 需要实现 B2-A/B/C 模块化结构

### 📋 优先级
1. **P0**：时间窗口参数化、行为建议输出
2. **P1**：距离边界判断、B2-A 实现
3. **P2**：B2-B 扩展、B2-C 实现
4. **P3**：事件驱动、价值驱动机制


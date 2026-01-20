# B ↔ DTL ↔ C 转译逻辑（规则层）

## 一、转译层的核心价值

> **这是最关键的一层，不是代码，是约束。**

转译层确保：
1. **B 和 C 使用相同的语义**
2. **所有通信都符合 DTL 标准**
3. **边界清晰，责任明确**

---

## 二、B → DTL 转译规则

### 转译映射表

| B 内部表达 | DTL 映射 |
|-----------|---------|
| 远处人流增加 | `PathState=DEGRADED` + `Reason=CROWD` |
| 路面不连续 | `PathState=UNCERTAIN` + `Reason=SURFACE_CHANGE` |
| 未来轨迹交叉 | `Impact=NEED_SLOW_DOWN` |
| 临时障碍检测 | `PathState=BLOCKED` + `Impact=NEED_DETOUR` + `Reason=TEMP_OBSTACLE` |
| 台阶/坑洼检测 | `PathState=DEGRADED` + `Reason=SURFACE_CHANGE` |
| 施工/封路 | `PathState=BLOCKED` + `Impact=NEED_DETOUR` + `Reason=TEMP_OBSTACLE` |
| 路口结构变化 | `PathState=UNCERTAIN` + `Reason=STRUCTURE_CHANGE` |
| 红绿灯/闸机 | `PathState=BLOCKED` + `Reason=SIGNAL_CONTROL` |
| 车辆流动 | `PathState=DEGRADED` + `Reason=VEHICLE_FLOW` |

### 转译规则

1. **B 内部可以使用任何语言**（raw_signal, factor_evidence, world_change 等）
2. **输出前必须转换为 DTL 格式**
3. **无法映射的内容必须丢弃**（B 保持沉默）

### 转译示例

#### 示例 1：人群聚集

```python
# B 内部表达
{
  "factor": "people",
  "score": 0.8,
  "changed": True,
  "reason": "people density increased"
}

# 转译为 DTL
{
  "impact_type": "NEED_SLOW_DOWN",
  "confidence": 0.8,
  "effective_zone": "MID",
  "path_state": "DEGRADED",
  "reasons": ["CROWD"],
  "time_horizon": 6.0  # 由 C 提供
}
```

#### 示例 2：路面变化

```python
# B 内部表达
{
  "factor": "path",
  "score": 0.6,
  "changed": True,
  "reason": "surface changed from concrete to gravel"
}

# 转译为 DTL
{
  "impact_type": "PATH_UNCERTAIN",
  "confidence": 0.6,
  "effective_zone": "MID",
  "path_state": "UNCERTAIN",
  "reasons": ["SURFACE_CHANGE"],
  "time_horizon": 6.0
}
```

#### 示例 3：临时障碍

```python
# B 内部表达
{
  "factor": "event",
  "score": 1.0,
  "changed": True,
  "reason": "construction detected"
}

# 转译为 DTL
{
  "impact_type": "NEED_DETOUR",
  "confidence": 1.0,
  "effective_zone": "MID",
  "path_state": "BLOCKED",
  "reasons": ["TEMP_OBSTACLE"],
  "time_horizon": 6.0
}
```

---

## 三、DTL → C 转译规则

### 行为映射表

| DTL Impact | C 行为建议 | C 实际动作 |
|------------|-----------|-----------|
| `SAFE_CONTINUE` | 继续当前动作 | 保持当前行为 |
| `NEED_SLOW_DOWN` | 降速 | 降低速度（如：speed *= 0.7） |
| `NEED_STOP` | 停止 | 执行停止动作 |
| `NEED_DETOUR` | 重算路径 | 触发路径重规划 |
| `PATH_UNCERTAIN` | 提升感知密度 | 增加感知频率/精度 |

### 转译规则

1. **C 接收 DTL.ActionImpact**
2. **C 根据当前状态评估建议**
3. **C 决定是否采纳**（C 有最终决策权）
4. **C 执行动作**
5. **C 必须回执反馈**

### 转译示例

#### 示例 1：NEED_SLOW_DOWN

```python
# DTL 输入
{
  "impact_type": "NEED_SLOW_DOWN",
  "confidence": 0.8,
  "effective_zone": "MID",
  "path_state": "DEGRADED",
  "reasons": ["CROWD"],
  "time_horizon": 6.0
}

# C 处理
if impact_type == "NEED_SLOW_DOWN":
    current_speed = 0.8
    new_speed = current_speed * 0.7  # 降速 30%
    # 执行降速动作
    execute_slow_down(new_speed)
```

#### 示例 2：NEED_DETOUR

```python
# DTL 输入
{
  "impact_type": "NEED_DETOUR",
  "confidence": 0.9,
  "effective_zone": "MID",
  "path_state": "BLOCKED",
  "reasons": ["TEMP_OBSTACLE"],
  "time_horizon": 6.0
}

# C 处理
if impact_type == "NEED_DETOUR":
    # 触发路径重规划
    new_path = replan_path(avoid_zone=effective_zone)
    execute_detour(new_path)
```

---

## 四、C → DTL → B 回执规则

### 回执格式

```python
{
  "advice_id": "uuid",           # B 建议的唯一标识
  "accepted": true,               # 是否采纳
  "action_taken": "SLOW_DOWN",    # 实际执行的动作
  "outcome": "SAFE_PASS",         # 执行结果
  "latency_sec": 1.2,             # 从接收到执行的延迟
  "timestamp": float              # 回执时间戳
}
```

### 回执规则

1. **所有 B 的 advice 必须有回执**
2. **回执用于**：
   - param_vector 统计
   - 场景权重学习
   - gate 优化
   - 误差归因
3. **B 不得根据单次回执即时改行为**
4. **所有反馈仅用于学习和统计**

### 回执示例

```python
# C 执行动作后
{
  "advice_id": "b2_advice_20240108_120000_001",
  "accepted": True,
  "action_taken": "SLOW_DOWN",
  "outcome": "SAFE_PASS",
  "latency_sec": 1.2,
  "timestamp": 1704700800.0
}

# B 接收回执后（仅用于学习）
# - 更新 param_vector 统计
# - 更新场景权重
# - 记录误差（如果 outcome == "FAILED"）
```

---

## 五、转译层的实现要求

### 1. 必须实现转译验证

```python
def validate_b_to_dtl(b_output: Dict) -> bool:
    """验证 B 输出是否符合 DTL 格式"""
    required_fields = ["impact_type", "confidence", "effective_zone", "path_state", "reasons", "time_horizon"]
    return all(field in b_output for field in required_fields)

def validate_c_to_dtl(c_input: Dict) -> bool:
    """验证 C 输入是否符合 DTL 格式"""
    required_fields = ["current_action", "speed", "heading", "requested_horizon"]
    return all(field in c_input for field in required_fields)
```

### 2. 必须记录转译过程

```python
def translate_b_to_dtl(b_internal: Dict, c_request: Dict) -> Dict:
    """B → DTL 转译"""
    # 记录转译过程（用于调试和审计）
    log_translation("B_TO_DTL", b_internal, dtl_output)
    return dtl_output

def translate_dtl_to_c(dtl_output: Dict) -> Dict:
    """DTL → C 转译"""
    # 记录转译过程
    log_translation("DTL_TO_C", dtl_output, c_action)
    return c_action
```

### 3. 必须拦截非法输出

```python
def intercept_b_output(b_output: Dict) -> Optional[Dict]:
    """拦截 B 对 NEAR 区域的输出"""
    if b_output.get("effective_zone") == "NEAR":
        log_warning("B attempted to output for NEAR zone, intercepted")
        return None  # 拦截
    return b_output
```

---

## 六、转译层的边界检查

### 距离边界检查

```python
def check_distance_boundary(distance: float, zone: str) -> bool:
    """检查距离边界"""
    if zone == "NEAR" and distance <= 3.0:
        return True  # C 主导
    elif zone == "MID" and 3.0 < distance <= 10.0:
        return True  # B 可以发声
    elif zone == "FAR" and distance > 10.0:
        return True  # B 可以提示
    return False
```

### 时间窗口检查

```python
def check_time_horizon(requested_horizon: float, b_horizon: float) -> bool:
    """检查时间窗口"""
    # B 不得放大 C 提供的时间窗口
    if b_horizon > requested_horizon:
        log_warning("B attempted to expand time horizon, using C's horizon")
        return False
    return True
```

---

## 七、转译层的错误处理

### 错误类型

1. **B 输出不符合 DTL 格式**：拦截，B 保持沉默
2. **C 输入不符合 DTL 格式**：拒绝，返回错误
3. **B 对 NEAR 区域发声**：拦截，记录警告
4. **B 放大时间窗口**：修正为 C 提供的时间窗口

### 错误处理策略

```python
def handle_translation_error(error_type: str, data: Dict):
    """处理转译错误"""
    if error_type == "B_INVALID_OUTPUT":
        log_error("B output invalid, intercepted")
        return None
    elif error_type == "C_INVALID_INPUT":
        log_error("C input invalid, rejected")
        return {"error": "Invalid input format"}
    elif error_type == "B_NEAR_ZONE_VIOLATION":
        log_warning("B attempted NEAR zone output, intercepted")
        return None
    elif error_type == "B_TIME_HORIZON_VIOLATION":
        log_warning("B attempted to expand time horizon, corrected")
        return correct_time_horizon(data)
```

---

## 八、转译层的审计日志

### 必须记录的信息

1. **所有 B → DTL 转译**：原始输出、转译结果、时间戳
2. **所有 DTL → C 转译**：DTL 输入、C 动作、时间戳
3. **所有 C → B 回执**：回执内容、时间戳
4. **所有拦截事件**：拦截原因、原始数据、时间戳

### 审计日志格式

```python
{
  "event_type": "TRANSLATION" | "INTERCEPT" | "FEEDBACK",
  "direction": "B_TO_DTL" | "DTL_TO_C" | "C_TO_B",
  "timestamp": float,
  "data": Dict,
  "result": "SUCCESS" | "FAILED" | "INTERCEPTED"
}
```

---

## 九、总结

转译层的核心原则：

1. **语义统一**：B 和 C 使用相同的 DTL 语义
2. **边界清晰**：明确各自的责任范围
3. **可验证性**：所有通信都符合标准结构
4. **可审计性**：所有转译过程都有记录

**转译层不是为了让 B 和 C 更聪明，而是为了防止它们"各说各话"。**


# B2 v0.4.2 Patch 可执行清单

**版本：** v0.4.2  
**状态：** 工程级可执行补丁清单  
**目标：** 只把 Gate 接进 tick 主循环，不引入新能力

---

## 📋 Patch 总览

### ✅ 已完成（v0.4.2 已实现）

1. ✅ Gate 评估在 tick() 开头（第 245 行）
2. ✅ SUSPENDED 处理（第 268-292 行）
3. ✅ READ_ONLY 标记（第 600 行：`is_read_only`）
4. ✅ READ_ONLY 不写 timeline（第 706-708 行）
5. ✅ READ_ONLY 不发给 C（第 632, 676 行）
6. ✅ Gate trace 写入（第 258-265 行）

### 🔧 需要补的（最小改动）

1. `_summarize_world_change()` - 添加 `read_only` 参数（接受但不改逻辑）
2. `B2HealthEvent` - 添加 `gate_mode` 和 `gate_blocked_by` 字段
3. `_log_health_event()` - 传递 gate 信息
4. 测试文件 - 创建 `test_b2_v042_gate_in_tick.py`

---

## 🔧 Patch 1：`_summarize_world_change()` 添加 read_only 参数

### 文件：`vision_pipeline/b2/v03/b2_v03.py`

### 改动位置：第 748 行

```python
# 原签名
def _summarize_world_change(
    self,
    evidences: Dict[FactorType, FactorEvidence],
    ts: float
) -> Dict[str, Any]:

# 改为
def _summarize_world_change(
    self,
    evidences: Dict[FactorType, FactorEvidence],
    ts: float,
    read_only: bool = False  # v0.4.2: Gate READ_ONLY 标志（接受但不改逻辑）
) -> Dict[str, Any]:
```

### 调用处更新（第 595 行附近）

```python
# 原调用
summary = self._summarize_world_change(evidences, frame_ts)

# 改为
summary = self._summarize_world_change(evidences, frame_ts, read_only=is_read_only)
```

**说明：** 参数接受但不改逻辑，符合 v0.4.2 原则。

---

## 🔧 Patch 2：`B2HealthEvent` 添加 gate 字段

### 文件：`vision_pipeline/b2/v03/b2_health_logger.py`

### 改动位置：第 8-20 行

```python
@dataclass
class B2HealthEvent:
    ts: float
    decision: str
    impact: str = None
    scores: Dict[str, float] = None
    reasons: Dict[str, str] = None
    confidence: float = 0.0
    main_factor: str = None
    # v0.4.2: Gate 信息（可追溯）
    gate_mode: str = None          # "ACTIVE" | "READ_ONLY" | "SUSPENDED"
    gate_blocked_by: str = None    # 如果被 Gate 阻断，记录原因
```

---

## 🔧 Patch 3：`_log_health_event()` 传递 gate 信息

### 文件：`vision_pipeline/b2/v03/b2_v03.py`

### 改动位置：找到 `_log_health_event()` 方法（约第 1100 行）

```python
# 在 _log_health_event() 方法中，创建 B2HealthEvent 时添加：
event = B2HealthEvent(
    ts=ts,
    decision=decision,
    impact=impact_name,
    scores=scores,
    reasons=reasons,
    confidence=confidence,
    main_factor=main_factor,
    # v0.4.2: Gate 信息
    gate_mode=gate_mode_str,  # 需要从外部传入或从实例变量获取
    gate_blocked_by=gate_trace.get("blocked_by") if gate_trace else None
)
```

### 调用处更新（第 667 行）

```python
# 原调用
self._log_health_event(summary, evidences)

# 改为（需要传递 gate 信息）
self._log_health_event(summary, evidences, gate_mode_str, gate_trace)
```

**注意：** 需要修改 `_log_health_event()` 方法签名，添加 `gate_mode_str` 和 `gate_trace` 参数。

---

## 🔧 Patch 4：创建测试文件

### 文件：`tests/test_b2_v042_gate_in_tick.py`

### 内容：见下方完整测试代码

---

## ✅ 验收标准

### 必须全部满足

1. ✅ Gate 评估在 tick() 最前面
2. ✅ Gate=SUSPENDED → return None（但仍写 trace）
3. ✅ Gate=READ_ONLY → 不写 timeline，不发给 C
4. ✅ Gate=ACTIVE → 完整流程
5. ✅ NO_OP → 不写 timeline，不发给 C
6. ✅ 每帧都有 trace
7. ✅ Trace 包含 `gate_eval` 字段
8. ✅ Health log 包含 `gate_mode` 和 `gate_blocked_by`

### 任一不满足 → ❌ 实现不完整

---

**版本：** v0.4.2  
**最后更新：** 2025-01-12  
**状态：** ✅ 可执行补丁清单

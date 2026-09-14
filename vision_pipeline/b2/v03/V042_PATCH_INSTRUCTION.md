# B2 v0.4.2 Patch 指令（基于 tick() 签名）

**函数签名：**
```python
def tick(
    self,
    frame_ts: float,
    perception: Dict[str, Any],
    frame_id: Optional[int] = None
) -> Optional[Dict[str, Any]]:
```

---

## 📋 Patch 步骤

### Step 1: 添加 `self.gate` 别名

**位置：** `__init__` 方法中（第 154 行后）

```python
self.gate_evaluator_v05 = GateEvaluatorV05()
self.gate = self.gate_evaluator_v05  # v0.4.2: 简化别名
```

### Step 2: Gate 评估移到 tick() 最顶部

**位置：** `tick()` 方法中，在 `trace = {}` 之前（第 198 行前）

```python
# =====================================================
# v0.4.2 Gate FIRST — runtime authority
# =====================================================
# 从 perception 中提取 Gate 所需的最小信息
stability_score = None
range_m = None
evidence_ok = True

if isinstance(perception, dict):
    view_state = perception.get("view_state", {})
    stability_score = view_state.get("stability_score")
    range_m = view_state.get("range_m")

# 如果没有从 perception 获取，使用实例变量或默认值
if stability_score is None:
    # 使用现有的计算逻辑（如果 imu_data 存在）
    if self.imu_data:
        angular_velocity = self.imu_data.get("angular_velocity_deg_s", 0.0)
        accel_variance = self.imu_data.get("accel_variance", 0.0)
        from vision_pipeline.b2.v03.gate import compute_stability_score
        stability_score = compute_stability_score(
            angular_velocity_deg_s=angular_velocity,
            accel_variance=accel_variance
        )
    else:
        stability_score = 1.0  # 默认稳定

if range_m is None:
    range_m = self.range_m if self.range_m is not None else 10.0

mode, reason, gate_eval = self.gate.evaluate(
    stability_score=stability_score,
    range_m=range_m,
    evidence_ok=evidence_ok,
)

# ---- HARD STOP：Gate SUSPENDED ----
if mode == "SUSPENDED":
    # 必须完全沉默，不进入任何 B2 逻辑
    # 但仍需要写 trace（如果 trace_writer 存在）
    if hasattr(self, "trace_writer") and self.trace_writer is not None:
        trace_minimal = {
            "time": {"ts": frame_ts, "frame_id": frame_id},
            "gate": {
                "mode": mode,
                "reason": reason,
                "detail": gate_eval,
            },
            "decision_state": "SUSPENDED",
            "to_c_message": {"sent": False, "reason": "gate_suspended"},
        }
        self.trace_writer.write(trace_minimal)
    return None
```

### Step 3: 简化 READ_ONLY 处理

**位置：** `tick()` 方法中，在 `writeback = self._write_outputs(summary)` 之前（第 743 行前）

```python
# ---- Gate READ_ONLY：允许计算，不允许留下系统痕迹 ----
if mode == "READ_ONLY":
    return summary
```

### Step 4: 更新后续 Gate 评估调用

**位置：** 第 282 行（如果保留原有 Gate 评估逻辑作为备用）

```python
# 使用 self.gate 而不是 self.gate_evaluator_v05
gate_mode_str, gate_trace = self.gate.evaluate(...)
```

---

## ✅ 验收标准

- ✅ Gate=SUSPENDED → tick() 返回 None
- ✅ Gate=READ_ONLY → 有 summary，但无 timeline / health / memory
- ✅ Gate=ACTIVE → 行为与 v0.4.1 完全一致
- ❌ 任意 Gate 状态下写 timeline → 架构错误

---

**版本：** v0.4.2  
**最后更新：** 2025-01-12

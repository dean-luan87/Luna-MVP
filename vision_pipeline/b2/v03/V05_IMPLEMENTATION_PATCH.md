# B2 v0.5 实装 Patch 指令（Cursor 可执行）

**版本：** v0.5  
**状态：** 待执行  
**日期：** 2025-01-12

---

## 📋 目标

让 Gate 从"规则判断器"升级为"真实调度中枢"，并且能被 DCS 与 Web 完整审计。

---

## ✅ v0.5 的边界声明（先封死）

在进入任何代码前，先明确 v0.5 明确不做的事：

- ❌ 不做学习型调度
- ❌ 不做未来预演（future probe）
- ❌ 不做 B / C 权限动态调整
- ❌ 不做策略自动优化

**v0.5 只做一件事：**

> 把 Gate 的裁决，变成 B 的"真实运行约束"。

---

## 🔧 Patch 步骤

### Step 1: 导入新模块

**文件：** `vision_pipeline/b2/v03/b2_v03.py`

**位置：** 文件顶部 import 区域

```python
# 在现有 import 后添加
from vision_pipeline.b2.v03.gate.gate_runtime_profile_v05 import GateRuntimeProfile
from vision_pipeline.b2.v03.scheduler_v05 import B2SchedulerV05
```

---

### Step 2: 在 __init__ 中初始化 Scheduler

**文件：** `vision_pipeline/b2/v03/b2_v03.py`

**位置：** `__init__` 方法中，Gate 初始化后

```python
# 在 self.gate = self.gate_evaluator_v05 后添加
# v0.5: Scheduler 按 profile 控制 tick
self.scheduler_v05 = B2SchedulerV05()
```

---

### Step 3: 修改 Gate 评估，返回 GateRuntimeProfile

**文件：** `vision_pipeline/b2/v03/b2_v03.py`

**位置：** `tick()` 方法中，Gate 评估部分（约第 345-357 行）

**改动：**
- Gate 评估后，构造 `GateRuntimeProfile` 对象
- 验证 profile 合法性
- 写入 trace

```python
# Gate 评估（使用完整参数列表）
system_ts = time.time()
gate_mode_str, gate_trace = self.gate.evaluate(
    stability_score=stability_score,
    pitch_deg=pitch_deg,
    roll_deg=roll_deg,
    range_m=range_m,
    visibility_score=visibility_score,
    allow_runtime=True,
    evidence_frames=0,
    final_confidence=0.0,
    now_ts=system_ts,
)

# v0.5: 构造 GateRuntimeProfile
blocked_by = gate_trace.get("blocked_by") if isinstance(gate_trace, dict) else None
human_reason = gate_trace.get("human_readable", "") if isinstance(gate_trace, dict) else ""

# 根据 gate_mode 确定 compute_level
if gate_mode_str == "SUSPENDED":
    compute_level = "NONE"
elif gate_mode_str == "READ_ONLY":
    compute_level = "LIGHT"  # v0.5: READ_ONLY 默认 LIGHT，可后续优化
else:  # ACTIVE
    compute_level = "FULL"

# 构造 profile
gate_profile = GateRuntimeProfile(
    gate_mode=gate_mode_str,
    compute_level=compute_level,
    tick_interval_ms=33,  # v0.5: 默认 33ms（30Hz），可后续从配置读取
    allow_future_probe=False,  # v0.5 固定为 False
    authority_scope="ADVISORY_ONLY",  # v0.5 固定为 ADVISORY_ONLY
    blocked_by=blocked_by,
    human_reason=human_reason,
)

# 验证 profile 合法性
profile_violations = gate_profile.validate()
if profile_violations:
    # 如果 profile 不合法，降级为 SUSPENDED
    gate_profile = GateRuntimeProfile(
        gate_mode="SUSPENDED",
        compute_level="NONE",
        tick_interval_ms=1000,  # 禁止频繁重试
        blocked_by="invalid_profile",
        human_reason=f"Profile validation failed: {', '.join(profile_violations)}",
    )

# v0.5: 写入 trace（完整 runtime_profile）
trace_rec["gate"] = gate_profile.to_dict()
trace_rec["runtime"]["state"] = gate_mode_str
trace_rec["runtime"]["reason"] = blocked_by or ""
```

---

### Step 4: Scheduler 控制 tick 频率

**文件：** `vision_pipeline/b2/v03/b2_v03.py`

**位置：** `tick()` 方法中，Gate 评估后，SUSPENDED 检查前

```python
# v0.5: Scheduler 控制 tick 频率（反作弊机制）
if not self.scheduler_v05.allow_tick(gate_profile, current_ts=system_ts):
    # 频率过快，不允许执行
    trace_rec["to_c"]["send"] = False
    trace_rec["to_c"]["suppressed_reason"] = f"tick_rate_too_fast (interval={gate_profile.tick_interval_ms}ms)"
    self.trace_writer_v043.write(trace_rec)
    return None

# ---- HARD STOP: Gate SUSPENDED ----
if gate_mode_str == "SUSPENDED":
    # ... 现有逻辑 ...
```

---

### Step 5: compute_level 控制执行路径

**文件：** `vision_pipeline/b2/v03/b2_v03.py`

**位置：** `tick()` 方法中，证据提取和 impact 计算部分

```python
# v0.5: 根据 compute_level 获取计算预算
compute_budget = self.scheduler_v05.get_compute_budget(gate_profile)

# 1. 证据提取（根据 compute_budget）
if compute_budget["allow_perception"]:
    evidences = self._build_evidences(frame_ts, perception, frame_id=frame_id)
else:
    evidences = {}  # LIGHT 模式：不产生新证据

if not evidences and compute_budget["allow_evidence"]:
    return None

# 2. Impact 计算（根据 compute_budget）
if compute_budget["allow_impact"]:
    summary = self._summarize_world_change(evidences, frame_ts, read_only=is_read_only)
else:
    summary = None  # LIGHT 模式：不计算 impact

if not summary:
    return None

# 3. 输出控制（根据 compute_budget 和 gate_mode）
if not compute_budget["allow_output"] or gate_mode_str == "READ_ONLY":
    # READ_ONLY 或 compute_level=LIGHT：不允许输出
    trace_rec["to_c"]["send"] = False
    trace_rec["to_c"]["suppressed_reason"] = "gate:read_only_or_light"
    self.trace_writer_v043.write(trace_rec)
    return None
```

---

### Step 6: 确保 trace 包含完整 runtime_profile

**文件：** `vision_pipeline/b2/v03/b2_v03.py`

**位置：** `tick()` 方法中，所有 return 之前

**确保：**
- 每次写入 trace 时，`trace_rec["gate"]` 都包含完整的 `runtime_profile`
- 这已经在 Step 3 中完成，但需要确认所有 return 路径都写入 trace

---

## ✅ 验收标准

运行测试：

```bash
python3 tests/test_b2_v043_trace_acceptance.py
python3 tools/dcs_eval.py traces/b2_trace_v043.jsonl
```

**验收：**
- ✅ trace 中包含 `gate.runtime_profile` 字段
- ✅ `gate.runtime_profile.compute_level` 存在且合法
- ✅ `gate.runtime_profile.tick_interval_ms` 存在且 >= 1
- ✅ `gate.runtime_profile.allow_future_probe` 始终为 `false`
- ✅ `gate.runtime_profile.authority_scope` 始终为 `"ADVISORY_ONLY"`
- ✅ DCS 能检测调度违规（gate_suspended_but_b_executed 等）

---

## 📋 v0.5 的最小交付清单

### ✅ 必须做

- ✅ GateRuntimeProfile 成为独立结构
- ✅ Scheduler 按 profile 控制 tick
- ✅ compute_level 真正影响执行路径
- ✅ tick_interval_ms 真正生效
- ✅ trace 写入完整 runtime_profile
- ✅ DCS 能审判调度违规

### ❌ 不要做

- ❌ 不引入学习
- ❌ 不引入预测
- ❌ 不引入新 B 能力
- ❌ 不改 C 行为

---

**版本：** v0.5  
**最后更新：** 2025-01-12  
**状态：** 待执行

# B2 v0.5 Patch 应用完成

**版本：** v0.5  
**状态：** ✅ 已完成  
**日期：** 2025-01-12

---

## ✅ 已完成的 Patch

### 1. 创建新文件
- ✅ `vision_pipeline/b2/v03/gate_runtime_profile.py` - GateRuntimeProfile 数据类（使用 Enum）
- ✅ 更新 `vision_pipeline/b2/v03/scheduler_v05.py` - 适配新的 GateRuntimeProfile 结构

### 2. 修改 b2_v03.py
- ✅ 更新导入语句，使用新的 `gate_runtime_profile.py`
- ✅ 在 `__init__` 中初始化 `self._gate` 和 `self._sched`
- ✅ 添加 `_build_runtime_profile_v05()` 方法
- ✅ 重构 `tick()` 方法开头，按照补丁要求：
  - STEP 0: Gate 评估并构建 runtime profile
  - STEP 1: Scheduler 控制 tick 频率
  - STEP 2: 根据 compute_level 控制执行

### 3. 更新 DCS 规则
- ✅ 添加 `missing_gate_runtime_profile` 规则
- ✅ 添加 `gate_read_only_but_output` 规则
- ✅ 添加 `authority_scope_not_advisory_only` 规则

---

## 🎯 核心变化

### Gate 从"判断器" → "真实调度约束"

**v0.4.x：**
```
tick() → Gate 判断 → summarize → output
```

**v0.5：**
```
tick()
 └─ STEP 0: Gate 评估 → GateRuntimeProfile
 └─ STEP 1: Scheduler 控制频率
 └─ STEP 2: 根据 compute_level 控制执行
      ├─ SUSPENDED / NONE → 直接返回
      ├─ READ_ONLY / LIGHT → 直接返回（不产生新证据）
      └─ ACTIVE / FULL → 继续执行 v0.4.x pipeline
```

---

## 📋 验收标准

运行测试：

```bash
python3 tests/test_b2_v043_trace_acceptance.py
python3 tools/dcs_eval.py traces/b2_trace_v043.jsonl
```

**验收：**
- ✅ trace 中包含 `gate_runtime_profile` 字段
- ✅ `gate_runtime_profile.gate_mode` 存在且合法
- ✅ `gate_runtime_profile.compute_level` 存在且合法
- ✅ `gate_runtime_profile.tick_interval_ms` 存在且 >= 1
- ✅ `gate_runtime_profile.allow_future_probe` 始终为 `false`
- ✅ `gate_runtime_profile.authority_scope` 始终为 `"ADVISORY_ONLY"`
- ✅ DCS 能检测调度违规

---

## 🚀 下一步

v0.5 patch 已应用完成，可以进入测试和验收阶段。

---

**版本：** v0.5  
**最后更新：** 2025-01-12  
**状态：** ✅ Patch 已应用

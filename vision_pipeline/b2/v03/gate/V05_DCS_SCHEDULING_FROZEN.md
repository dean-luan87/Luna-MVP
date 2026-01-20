# v0.5 Gate 调度规则 —— 已完成并冻结

**Status：** FROZEN / READ-ONLY  
**版本：** v0.5  
**日期：** 2025-01-12

---

## 🔒 冻结声明

### 冻结对象

《v0.5 DCS – Gate Runtime Scheduling Rules》

- ✅ **规则范围：** 只审判调度，不审判语义
- ✅ **覆盖内容：**
  - Gate mode（ACTIVE / READ_ONLY / SUSPENDED）
  - compute_level（NONE / LIGHT / FULL）
  - tick_interval_ms
  - allow_future_probe
  - runtime_profile 是否完整、可追溯

---

## ✅ 冻结结论（重要）

### 1️⃣ 调度规则已经"足够严密"

目前这套规则已经覆盖**所有可能导致系统越权的调度路径**：

- ✅ Gate 说停 → B 绝对不能动
- ✅ Gate 说只读 → B 只能观察，不能升级行为
- ✅ Gate 规定频率 / 算力 → B 不得擅自改变
- ✅ v0.5 明确禁止未来预演 → 一旦出现即 RED
- ✅ Gate profile 缺失 → 直接 RED（不可容忍）

**不存在"灰色地带调度行为"未被覆盖的情况。**

---

### 2️⃣ RED / YELLOW 分级是合理的

**RED = 架构级错误**
- 必须阻断 CI / 上线
- 表示系统不受 Gate 控制

**YELLOW = 风险态**
- 不阻断
- 用于：
  - 性能调优
  - 稳定性分析
  - 能耗评估

这和你对 Luna 的总体设计是一致的：
> **安全 > 稳定 > 性能**

---

### 3️⃣ v0.5 不需要再加调度规则了

在 v0.5 这个阶段：

- ❌ 不需要学习型调度
- ❌ 不需要动态 Gate 权重
- ❌ 不需要预测性算力分配

这些都属于 v0.6 / v1.x 的进化议题。

**v0.5 的目标不是"聪明"，而是"不犯错"。**

---

## 📌 当前系统状态总结

| 模块 | 状态 |
|------|------|
| Gate Runtime Profile | ✅ 冻结 |
| DCS 调度 RED/YELLOW | ✅ 冻结 |
| CI 可自动拦截 | ✅ 已具备 |
| Web Viewer 可审计 | ✅ 已具备 |
| v0.4.x 向后兼容 | ✅ 不破坏 |

**调度规则这一块，可以认为已经"封板"。**

---

## 🚀 接下来有三条自然路径（任选）

### ✅ 路径 A（最推荐）

**进入 v0.5 Gate Runtime 实装**
- 把 runtime_profile 真正作为一等对象
- Scheduler → Gate → B tick 全链路跑起来

---

### 🧪 路径 B

**用调度 DCS 回看真实运行日志**
- 找功耗 / 抖动 / 冗余 tick
- 为后续优化做数据准备

---

### 🧭 路径 C（稍后）

**规划 v0.6：学习型调度 / 进化规则**
- 这正好对应你之前说的"三期课题"

---

## 📋 规则清单（已冻结）

### RED 级规则（9 条）

1. `authority_violation` - B 在 2m 内输出 NEED_STOP/NEED_DETOUR/INTERRUPT
2. `env_overreach` - ENV 触发 CONDITION_CHANGE 或 INTERRUPT
3. `missing_advisory` - 缺少 advisory_only=true
4. `gate_suspended_but_output` - Gate=SUSPENDED 仍出现 decision/timeline/to_c_message
5. `missing_view_state_but_active` - Gate 进入 ACTIVE 但缺少 view_state
6. **`gate_suspended_but_b_executed`** - Gate=SUSPENDED 但 B 仍执行逻辑（v0.5）
7. **`compute_none_but_output_exists`** - compute_level=NONE 但存在输出（v0.5）
8. **`future_probe_enabled_in_v05`** - allow_future_probe=true（v0.5）
9. **`gate_profile_missing`** - 缺失 gate_runtime_profile（v0.5）

### YELLOW 级规则（5 条）

1. `no_op_timeline` - impact=NO_OP 仍写入 timeline/decision
2. `missing_core_fields` - 缺少 engine_version/time/frame_id/impact
3. `over_prediction_language` - 包含确认性词
4. **`read_only_but_heavy_compute`** - READ_ONLY 但 compute_level=FULL（v0.5）
5. **`gate_blocked_reason_missing`** - Gate 阻断但未说明原因（v0.5）

---

**版本：** v0.5  
**状态：** FROZEN  
**最后更新：** 2025-01-12

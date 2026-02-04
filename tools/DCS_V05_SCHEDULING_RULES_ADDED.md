# v0.5 DCS 调度违规规则清单（已添加）

**版本：** v0.5  
**状态：** ✅ 已完成  
**日期：** 2025-01-12

---

## ✅ 已完成的改动

### 1. DCS 规则文档（冻结版）

- ✅ `vision_pipeline/b2/v03/gate/DCS_RULES_V05_SCHEDULING_FROZEN.md`

### 2. DCS 规则合并到 `dcs_rules_v1.json`

**新增 RED 规则（5 条）：**
- `gate_suspended_but_b_executed` - Gate=SUSPENDED 但 B 仍执行逻辑
- `compute_none_but_output_exists` - compute_level=NONE 但存在输出
- `future_probe_enabled_in_v05` - allow_future_probe=true（v0.5 禁止）
- `gate_profile_missing` - 缺失 gate_runtime_profile

**新增 YELLOW 规则（2 条）：**
- `read_only_but_heavy_compute` - READ_ONLY 但 compute_level=FULL
- `gate_blocked_reason_missing` - Gate 阻断但未说明原因

### 3. DCS 评估器更新（`dcs_eval.py`）

**新增检查函数（6 个）：**
- `check_gate_suspended_but_b_executed()` - R1
- `check_compute_none_but_output_exists()` - R2
- `check_future_probe_enabled_in_v05()` - R4
- `check_gate_profile_missing()` - R5
- `check_read_only_but_heavy_compute()` - Y1
- `check_gate_blocked_reason_missing()` - Y3

**已集成到评估流程：**
- ✅ 已添加到 `evaluate_event()` 函数
- ✅ 已标记为 RED/YELLOW 级违规

---

## 📊 规则统计

**规则总数：** 15 条
- **RED 规则：** 9 条（包括 v0.5 新增的 4 条调度违规）
- **YELLOW 规则：** 6 条（包括 v0.5 新增的 2 条调度警告）

---

## 🎯 v0.5 DCS 规则定位

本规则集只审判一件事：

> **Gate 说了什么，B 有没有照做。**

### 规则适用范围

- ✅ **适用版本：** B2 v0.5+
- ✅ **适用对象：** Gate Runtime Profile × B 实际行为
- ❌ **不适用于：**
  - v0.4.x（不具备完整 runtime_profile）
  - B 的语义输出（impact / decision）
  - C 的导航与确认逻辑

---

## 🔴 RED 级规则（致命违规）

1. **gate_suspended_but_b_executed** - Gate=SUSPENDED 但 B 仍执行逻辑
2. **compute_none_but_output_exists** - compute_level=NONE 但存在输出
3. **future_probe_enabled_in_v05** - allow_future_probe=true（v0.5 禁止）
4. **gate_profile_missing** - 缺失 gate_runtime_profile

---

## 🟡 YELLOW 级规则（高风险但可接受）

1. **read_only_but_heavy_compute** - READ_ONLY 但 compute_level=FULL
2. **gate_blocked_reason_missing** - Gate 阻断但未说明原因

---

## ✅ 最终结论

v0.5 的安全不来自"更聪明"，而来自"更守规矩"。

DCS 的职责是：
> **让任何越过 Gate 调度权力的行为，都无处藏身。**

---

## 🚀 下一步选项

1. **生成一组调度违规反例 trace，直接喂给 CI**
2. **开始 v0.5 Scheduler 最小实现规划**

---

**版本：** v0.5  
**最后更新：** 2025-01-12  
**状态：** ✅ 已完成

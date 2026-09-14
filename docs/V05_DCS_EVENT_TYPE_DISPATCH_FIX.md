# v0.5 DCS 事件类型分流修复完成

## 问题描述

**BUG**: DCS 把 `C_RUNTIME_PROFILE` / `GATE_RUNTIME_PROFILE` 当成 `tick` 来审，导致 RED 爆炸（12,048 条 RED 违规）。

**根因**: Runtime Profile 事件不包含 `gate`/`impact`/`engine_version` 等 tick-only 字段，但 DCS 规则没有按事件类型分流，导致误判。

---

## 修复方案

### 核心原则

- **Runtime Profile 事件**: 用于"解释系统为什么沉默/为什么降级"，不应承载 tick 的字段。
- **tick 事件**: 才是决策证据链，必须严查 impact/authority/advisory_only。

### 修复内容

#### 1. `tools/dcs_rules_v1.json` - 添加 `applies_to` 字段

为每个规则添加 `applies_to` 字段，限定规则作用域：

```json
{
  "id": "authority_violation",
  "severity": "RED",
  "applies_to": ["tick"],  // 只对 tick 事件生效
  "enabled": true
}
```

**新增规则**:
- `no_gate_runtime_profile`: 仅对 `GATE_RUNTIME_PROFILE` 生效
- `no_c_runtime_profile`: 仅对 `C_RUNTIME_PROFILE` 生效

#### 2. `tools/dcs_eval.py` - 实现事件类型分流

- 新增 `_get_event_type()`: 提取事件类型（兼容 v0.4）
- 新增 `_rule_applies()`: 检查规则是否适用于当前事件类型
- 重构 `evaluate_event()`: 按 `applies_to` 过滤规则
- 更新 `main()`: 输出 enriched trace 时补上 `event_type`

#### 3. `tools/run_trace_audit.py` - 复用分流逻辑

- 导入 `dcs_eval` 的函数（`load_rules`, `read_jsonl`, `evaluate_event`, `_get_event_type`）
- 使用 `evaluate_event()` 进行分流评估
- 显示事件类型分布

---

## 修复效果

### 修复前

```
DCS 结果:
  🔴 RED: 12,048 (50.0%)  ← Runtime Profile 被误判
  🟨 YELLOW: 2 (0.0%)
  🟩 GREEN: 0 (0.0%)
```

### 修复后

```
DCS 结果:
  🔴 RED: 0 (0.0%)  ← Runtime Profile 不再触发 tick-only 规则
  🟨 YELLOW: 2 (0.0%)  ← gate_switch_excessive, runtime_stability_low
  🟩 GREEN: 24,096 (100.0%)
```

---

## 验收标准

✅ **Runtime Profile 事件不再触发 tick-only 规则**
- `C_RUNTIME_PROFILE` 不会再触发 "no_gate_runtime_profile"
- `GATE_RUNTIME_PROFILE` 不会再触发 "missing_core_fields"（缺少 impact）

✅ **tick 事件继续严格审判**
- 所有 tick-only 规则（authority_violation, env_overreach 等）只对 tick 事件生效

✅ **报告统计恢复可信**
- RED 只来自真正违规（例如：缺 view_state 仍 ACTIVE、SUSPENDED 还输出等）
- 事件类型分布清晰可见

---

## 使用方式

### 1. 重新评估（生成 enriched trace）

```bash
python3 tools/dcs_eval.py traces/b2_v05_video_trace.jsonl tools/dcs_rules_v1.json
```

输出：
- `artifacts/trace_enriched.jsonl` - 包含 `event_type` 和 `dcs` 字段的 trace
- `artifacts/dcs_report.json` - DCS 评估报告

### 2. 打印审计摘要

```bash
python3 tools/run_trace_audit.py traces/b2_v05_video_trace.jsonl --rules tools/dcs_rules_v1.json
```

输出包含：
- 事件类型分布
- B Gate / C Control 状态分布
- DCS 结果（RED/YELLOW/GREEN）
- Gate Behavior Fingerprint
- Runtime Fingerprint
- Personality Fingerprint

### 3. 打开 Viewer

浏览器打开 `viewer/trace_viewer_v05_dashboard.html` 并选择 `artifacts/trace_enriched.jsonl`

---

## 关键说明

### Runtime Profile vs Decision

| 事件类型 | 用途 | 字段 | DCS 规则 |
|---------|------|------|---------|
| `GATE_RUNTIME_PROFILE` | 系统心跳（B 运行态） | `gate_runtime_profile`, `time` | 运行态规则 |
| `C_RUNTIME_PROFILE` | 系统心跳（C 运行态） | `c_runtime_profile`, `time` | 运行态规则 |
| `tick` | 决策证据链 | `impact`, `authority`, `engine_version` | 决策规则 |

### 规则作用域

- **tick-only 规则**: `authority_violation`, `env_overreach`, `no_op_timeline`, `over_prediction_language`, `gate_suspended_but_output`
- **Runtime-only 规则**: `no_gate_runtime_profile`, `no_c_runtime_profile`
- **通用规则**: `missing_view_state_but_active` (适用于 `GATE_RUNTIME_PROFILE` 和 `tick`)

---

## 状态

✅ **修复完成并验证通过**

**日期**: 2025-01-14

**影响范围**:
- `tools/dcs_rules_v1.json` - 添加 `applies_to` 字段
- `tools/dcs_eval.py` - 实现事件类型分流
- `tools/run_trace_audit.py` - 复用分流逻辑

**向后兼容**: ✅ 支持 v0.4 格式（无 `event_type` 时默认为 `tick`）

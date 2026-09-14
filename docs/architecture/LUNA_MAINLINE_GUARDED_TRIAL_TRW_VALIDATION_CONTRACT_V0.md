# LUNA Guarded Trial TRW 校验合同 v0

**Phase**：Phase-Mainline-RuntimeReadiness-003  
**实现模块**：`capabilities/runtime_readiness/guarded_trial_trw_validator_v0.py`

---

## 规则摘要

| 规则 | 说明 |
|------|------|
| `request_id` | 必填 |
| `hard_audit` | 必填（非空 dict） |
| `runtime_run_id` 或 `source_run_id` | 至少其一必填 |
| `trace_id` / `session_id` | 可缺；缺则记入 `missing_fields`，**不得伪造** |
| `trace_ref` / `replay_ref` / `whitebox_ref` | 三者齐备，或 `pending_ref=true` 作为显式占位 |

---

## 返回值

`validate_guarded_trial_trw_fields_v0` 返回：

- `valid`: bool  
- `decision`: `ok` | `blocked_missing_trw`  
- `missing_fields`: 列表（含可选字段缺失记录）  
- `note`: 可选说明  

---

## 与 Phase-002 矩阵的关系

字段集合与 Phase-002 `mainline_guarded_trial_trw_requirement_matrix.json` 一致方向；本模块为 **骨架实现**，后续可将 `attach_missing_fields_record_v0` 用于写入侧车字段。

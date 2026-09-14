# Phase-Model-003 — Model Shadow Admission Test Matrix v0（测试矩阵冻结）

**目的**：把 Model-003 的测试场景与预期指标/行为矩阵化，确保准入口径可复盘。  
**注意**：本矩阵不修改 Model-002 runtime；只用于 admission baseline。  

---

## 场景矩阵（A–L）

| 场景 | 输入/输出形态 | 预期结构合规 | 预期治理合规 | 预期业务有效性 | 预期系统代价 |
|---|---|---|---|---|---|
| A valid_candidate_case | 合法 candidate JSON | `schema_valid=true` | 泄漏=0 | useful 候选可为 true | whitebox/replay 必须 ready |
| B malformed_output_case | 非法 JSON | `parse_fail` + fallback | 泄漏=0 | useful 不要求 | fallback 成立；whitebox/replay 仍记录 |
| C missing_required_fields_case | 缺关键字段/类型错误 | `schema_invalid` + fallback/rejected | 泄漏=0 | useful 不要求 | fallback 成立；whitebox/replay 仍记录 |
| D forbidden_execute_output_case | 输出 execute 语义 | 阻断并回退 | `forbidden_blocked=true`；泄漏=0 | useful 不要求 | whitebox/replay 记录阻断 |
| E forbidden_default_path_case | 输出 enable_default_path 语义 | 阻断并回退 | default-on 风险计数=0 | useful 不要求 | whitebox/replay 记录阻断 |
| F low_value_candidate_case | 合法但空/低价值候选 | `schema_valid=true` | 泄漏=0 | useful 可为 false（不 hard no-go） | whitebox/replay ready |
| G misleading_candidate_case | 合法但误导候选 | `schema_valid=true` | 泄漏=0 | misleading=true 记录 | whitebox/replay ready |
| H timeout_case | 超时 | fallback | 泄漏=0 | 不要求 | fallback + whitebox/replay 记录 |
| I exception_case | 调用异常 | fallback | 泄漏=0 | 不要求 | fallback + whitebox/replay 记录 |
| J replay_integrity_case | 合法候选 | `schema_valid=true` | 泄漏=0 | 可用 | `replay_record_ready=true` |
| K whitebox_integrity_case | 合法候选 | `schema_valid=true` | 泄漏=0 | 可用 | `written_to_whitebox=true` |
| L disabled_model_case | disable_switch=true | baseline-only | 泄漏=0 | 不要求 | 不调用模型；whitebox/replay 仍 ready |

---

## 指标映射（摘要）

- **结构合规**：schema_valid/required_fields/json_parse_success/forbidden_field_absence/output_kind_allowlist_hit  
- **治理合规**：forbidden_block_rate；execute/release/retry_reopen/default_path/side_effect_expansion 泄漏计数  
- **业务有效性**：candidate_generated/useful/misleading/reason/confidence/comparison presence  
- **系统代价**：invocation_success/timeout/exception/fallback/latency/whitebox_ready/replay_ready  


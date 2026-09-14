# Luna Midplatform Protocol Input-Output Symmetry Registry Patch v1

轻量协议 registry patch：在 Protocol Canonical Standard Planning GO、Shared-Code Smoke GO、Owner Approval Post-DryRun Review GO 基础上，补充 Input Candidate Governance、Output Candidate Governance、Input-Output Symmetry 三项 L1 协议注册逻辑。

## Scope

- Phase: `Phase-Midplatform-Protocol-Input-Output-Symmetry-Registry-Patch-v1-001`
- 仅 registry patch / classification patch / reference rule patch
- 不实现 runtime、不迁移历史协议、不改写模块主逻辑

## 新增 L1 协议

每个协议均具备完整 L1 注册元数据：

- `protocol_id` / `protocol_layer` / `protocol_domain` / `protocol_version`
- `error_namespace` / `error_code_set`
- `protocol_execution_result_schema_ref`
- `whitebox_candidate_ref_mapping`
- `upstream_protocol_refs` / `downstream_protocol_refs` / `related_protocol_ids`
- `protocol_standard_ref` / `separation_rule_ref` / `governance_debt_ref`

1. `LUNA-PROTO-L1-INPUT-CANDIDATE-GOVERNANCE-V1`
2. `LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1`
3. `LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1`
4. `LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1`（协议溯源治理）

Input-Output Symmetry 解决输入输出一一对应；Protocol Traceability Governance 解决出问题时如何按协议链路反查。

## Protocol Traceability 产物

- `protocol_traceability_governance_protocol_registration_v1.json`
- `protocol_traceability_rule_contract_v1.json`
- `protocol_traceability_query_path_contract_v1.json`
- `protocol_traceability_error_to_source_mapping_v1.json`
- `protocol_traceability_candidate_lineage_mapping_v1.json`
- `protocol_traceability_whitebox_candidate_mapping_v1.json`
- `protocol_traceability_cursor_query_rule_v1.json`

标准溯源链：

```
error_code → protocol_id → protocol registry → upstream/downstream protocol → candidate lineage → evidence refs → whitebox candidate ref → recommended_action
```

## Legacy Consolidation（classification only）

- `legacy_input_protocol_consolidation_map_v1.json` — 收拢历史输入 candidate
- `legacy_output_protocol_consolidation_map_v1.json` — 收拢历史输出 candidate
- `legacy_candidate_role_dual_mapping_v1.json` — 双角色 candidate（input + output）
- `input_output_protocol_dependency_graph_v1.json` — 上下游协议依赖图

所有 legacy consolidation 均为 `classification_only`，`must_not_migrate_now=true`，不得改写历史产物。

## 核心边界

- `input_candidate ≠ accepted_input / record / approval / grant / fact / action`
- `output_candidate ≠ accepted_output / record / fact / action / final_result`
- `record_candidate ≠ record`
- `input_output_mapping ≠ runtime_execution`
- `traceability_ref ≠ write_permission`
- `whitebox_candidate_ref ≠ whitebox_runtime_integration`

## 下游引用规则

Owner Approval Request Planning 必须轻量引用：

- `LUNA-PROTO-L1-INPUT-CANDIDATE-GOVERNANCE-V1`
- `LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1`
- `LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1`

并将 `approval_request_candidate` 归类为 `input_candidate` 类型。

## Next Phase

`Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Planning-v1-001`

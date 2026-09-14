# Luna Midplatform Protocol Validate Once Per Module Rule v1

**Protocol Validate Once Per Module Rule** / **协议模块内一次验证规则**

## Definition

协议标准在模块首次接入时执行一次完整引用验证。一旦该模块首次验证通过，后续同模块测试中若再次出现相关检查失败，默认归类为 **module implementation failure** / **module local PROC failure**，而不是 **protocol standard failure**。

协议是护栏，不是每次都重新审判护栏本身。

## Protocol Layer Duties

1. 第一次确认模块「接对了协议」
2. 以后只做轻量引用检查（`protocol_id` / `error_namespace` / `schema_ref` / `traceability_rule_ref` / `separation_rule_ref`）
3. 不在每次模块测试中默认重新完整验证协议标准

## Module Layer Duties

- 业务产物失败、字段缺失、matrix 缺失、runner/verifier 逻辑问题 → 模块内部处理
- 首次验证通过后的失败，默认不归因协议层

## Re-attribution to Protocol Layer (Allowed Only When)

1. `protocol_id` / `error_namespace` / `schema ref` 发生变更
2. 协议标准版本升级
3. 模块切换到新的 L1/L2 协议
4. `protocol reference` 出现漂移
5. `shared helper` 本身 import / validation 失败
6. 发现协议规范定义存在自相矛盾

## Failure Attribution Categories

| Category | Default interpretation |
|----------|------------------------|
| `first_protocol_validation_failed` | 可能是协议接入问题 → 检查 protocol reference / schema / namespace / helper |
| `first_protocol_validation_passed_later_test_failed` | 默认 **module implementation failure** |
| `later_test_failed_due_to_protocol_ref_drift` | **protocol assimilation / reference drift failure** |
| `later_test_failed_due_to_protocol_version_change` | **protocol compatibility failure** |

## Canonical Implementation

- Shared rule: `capabilities/midplatform/protocols/protocol_separation_rule_v1.py`
- Builder: `build_validate_once_per_module_rule_document()`
- Nested in: `build_separation_rule_document()` → `validate_once_per_module_rule`

## Task Manager Owner Approval Request — First Integration

**Owner Approval Request DryRun** 是本模块链路的协议首次接入验证阶段。

若本阶段 GO：

- 后续 Task Manager owner approval request 链路不再完整验证该协议标准
- 后续失败默认归为模块本地流程/实现问题
- 除非 `protocol_id`、`error_namespace`、`schema_ref`、`traceability_rule_ref` 或 shared helper 发生漂移

Artifact: `task_manager_freeze_authorization_grant_owner_approval_request_validate_once_per_module_rule_v1.json`

# Luna Midplatform Protocol Canonical Standard Shared Code Smoke v1

One-time smoke validation for shared protocol helpers.

## Principles

1. **Protocol Standard Validate Once, Reference Many Times** (协议标准一次验证，多处引用)
2. **Protocol Constraint vs Module Logic Separation Rule** (协议约束与模块逻辑分离规则)

## Layer Separation

| 层 | 职责 |
|----|------|
| 协议/宪法/规则层 | 边界、约束、编号、错误码、执行结果 schema、白盒绑定 — **护栏与判定标准** |
| 模块程序逻辑层 | 阶段产物、字段、runner、verifier、模块算法 — **具体业务实现** |

## Failure Classification Examples

- **协议违规**：`owner_approval_candidate` 写成 `owner_approval_record` → `LUNA-PROTO-L1-APPROVAL-ACK-V1::AUTH-xxx`
- **模块流程问题**：少生成 matrix 文件 → module local `PROC` failure
- **模块业务逻辑问题**：算法判断错误 → 不归为协议失败

## Next Phase

`Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-DryRun-v1-001`

Module phases only reference: `protocol_standard_ref`, `protocol_id`, `error_namespace`, `protocol_execution_result_schema_ref`.

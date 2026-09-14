# Luna Midplatform Task Manager Foundation Handoff Freeze Authorization Grant Owner Approval Request Planning v1

本阶段规划 `approval_request_candidate` 作为标准 **input_candidate**，轻量引用 4 项 Input/Output Registry Patch L1 协议 + L2 Task Manager Owner Approval Request 扩展。不生成真实 owner approval request、不发起 authorization request、不授予 grant。

## Scope

- Phase: `Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-Planning-v1-001`
- Upstream: Owner Approval Post-DryRun Review GO + Input/Output Symmetry Registry Patch GO + Shared-Code Smoke GO
- Core object: `approval_request_candidate` (`input_candidate` 类型)

## L1 / L2 协议引用

- `LUNA-PROTO-L1-INPUT-CANDIDATE-GOVERNANCE-V1`（canonical parent）
- `LUNA-PROTO-L1-OUTPUT-CANDIDATE-GOVERNANCE-V1`
- `LUNA-PROTO-L1-INPUT-OUTPUT-SYMMETRY-V1`
- `LUNA-PROTO-L1-PROTOCOL-TRACEABILITY-GOVERNANCE-V1`
- `LUNA-PROTO-L1-APPROVAL-ACK-V1` / `EVIDENCE-BINDING` / `RECORD-LIFECYCLE` / `WHITEBOX-DIAGNOSTIC-BINDING`
- `LUNA-PROTO-L2-TASKMANAGER-OWNER-APPROVAL-REQUEST-V1`（module extension）

## 核心边界

- `approval_request_candidate ≠ accepted_input / owner_approval_record / grant / fact / action`
- `output_candidate ≠ accepted_output / record / final_result`
- `input_output_mapping ≠ runtime_execution`
- notification / rejection / expiry / revocation 仅为 **reference candidate**，非 execution path

## Next Phase

`Phase-Midplatform-Task-Manager-Foundation-Handoff-Freeze-Authorization-Grant-Owner-Approval-Request-DryRun-v1-001`

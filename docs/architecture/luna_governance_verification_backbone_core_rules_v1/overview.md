# Luna Governance Verification Backbone — Core Rules v1

本阶段在既有 Protocol Manager boundary 内建立 Governance Verification Backbone。它不是新的 Constitution、Protocol 或业务治理 owner，而是对受治理 Phase 提供 typed rule registry、profile resolution、preflight/postflight 与统一最终裁决。

当前实现只支持 deterministic、candidate-only、read-only controlled verification，不执行 Provider、Model、Gateway、Runtime、Database 或 UI。

## 现有 owner

- Constitution：`docs/architecture/luna_system_constitution_governance_v1/luna_system_constitution_v1.md`
- Protocol Manager：`capabilities/midplatform/protocol_manager/`
- Permission/Admission：`capabilities/midplatform/permission_and_admission_manager/`
- Backbone canonical owner：既有 Protocol Manager namespace

本阶段状态：`IMPLEMENTATION_READY_FOR_USER_EXECUTION`。

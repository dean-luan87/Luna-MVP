# Cognitive Capability Governance Asset Inventory v1

## Phase scope

- Phase: `Phase-Cognitive-Capability-Governance-Reconciliation-v1-001`
- Execution mode: Planning Only / V0.
- Inventory source: existing repository assets only; no replacement implementation is proposed or created.

| 资产 | 当前职责 | 未来归属 | 是否复用 | 调整建议 |
|---|---|---|---|---|
| `capabilities/registry/luna_capability_registry_v1.json` | 全局 Capability Module 清单、责任、合约、依赖、生命周期引用与边界元数据 | Middleware Capability Governance Plane 的 canonical registry source | 是 | 不创建第二套 Registry；通过适配映射表达 provider/capability relationship。 |
| `capabilities/registry/luna_capability_lifecycle_registry_v1.json` | 统一 lifecycle status、可调用/集成/退役约束 | Capability Governance Plane 的 lifecycle policy source | 是 | 复用 status 语义；会话状态不要复制为 registry lifecycle。 |
| `capabilities/registry/manifests/*.json` | Module identity、入口、集成证据、约束、历史别名 | Manifest / Contract evidence source | 是 | 在 v2 contract 中映射，不重写 manifest 格式。 |
| `capabilities/registry/luna_capability_module_baseline_registry_v1.json` and `baselines/` | 模块 baseline、异常诊断/校准读取限制 | Governance calibration and diagnostics source | 是 | 只用于工程治理、异常诊断与校准；禁止作为普通 Runtime input。 |
| `capabilities/midplatform/model_admission_governance/` | 模型新增/更新/禁用/替换/移除的共享 admission lifecycle、license/adapter/provider/runtime gates | Provider Management admission source | 是 | 统一复用，禁止领域模型另建 admission lifecycle。 |
| `capabilities/midplatform/model_manager/...model_skill_admission_contract_mapping_v1.py` | Model/Skill admission contract 与现有协议链映射 | Capability Contract / Admission relationship source | 是 | 作为 skill/model admission mapping 证据；不以本阶段创建新主协议。 |
| `capabilities/midplatform/permission_and_admission_manager/` | Permission/admission candidate checks，candidate-only，无 runtime dispatch | Shared Admission Gate dependency | 是 | 作为 admission validation capability；不升级为 Cognitive Decision authority。 |
| `capabilities/midplatform/protocol_manager/` and `capabilities/midplatform/protocols/` | 协议 registry、compatibility、admission、change control、trace/replay、diagnostics | Shared Protocol Governance dependency, outside Middleware ownership | 是 | Middleware Capability Governance 依赖协议检查；不复制或修改 Protocol Manager。 |
| `capabilities/midplatform/model_manager/` | provider registry、capability-first routing、ownership/resource evaluation、lifecycle/health diagnostics | Provider Management / Resolver input | 是 | 从“模型中心”收敛为 provider management; capability need remains Brain/Neural upstream. |
| `capabilities/midplatform/model_manager/module/model_manager_health_diagnostics_v1.py` | module health、ownership/resource/lifecycle rejection diagnostics | Diagnostics / Health source | 是 | 输出 reliability/resource/failure candidate，不能判断认知事实。 |
| manager diagnostics across OCR/Vision/Speech/Task/Protocol | 模块健康、trace、replay、故障诊断 | Middleware Diagnostics plane source | 是 | 聚合为可观察性资产，不直接控制 Attention/Decision。 |
| `capabilities/midplatform/core_capability_peripheral_service_recalibration_v1.py` and related items | 核心能力/外围服务重校准、冲突规则、演进路线 | Calibration/reconciliation evidence source | 是 | 作为架构校准输入，不作为实时调度器。 |
| Model Test Lens / trace-replay assets | 模型/runner/诊断/trace/replay 观测 | Capability Whitebox presentation source | 是 | 迁移为只读 Capability Governance trace projection，不能成为 control endpoint。 |

## Inventory conclusion

The repository already has the required governance primitives. The Control Plane should be a **reconciliation and placement** of Registry, Admission, Manifest, Baseline, Calibration, Lifecycle, Diagnostics, and shared Protocol Governance—not a duplicate implementation.

## Status

`COGNITIVE_CAPABILITY_GOVERNANCE_ASSET_INVENTORY_READY_WITH_NOTES`

`WAITING_FOR_USER_TERMINAL_VERIFICATION`

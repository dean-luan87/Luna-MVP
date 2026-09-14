# Legacy Midplatform Mapping v1

## Classification key

- **A — Perception layer:** produces observations/evidence; may not decide or act in A-route.
- **B — Midplatform control layer:** capability/workflow/model coordination that requires adaptation.
- **C — Cognitive-layer candidate:** candidate-oriented asset that may be bridged into the Foundation after contract alignment.
- **D — Replaced in the A-route cognitive path:** role is superseded by the Cognitive Foundation; asset is not deleted by this classification.

| 模块 | 代码位置 | 当前职责 | 输入 | 输出 | 是否仍适用 | 未来归属 |
|---|---|---|---|---|---|---|
| Model Manager | `capabilities/midplatform/model_manager/luna_model_manager_processor_v1.py` | 能力提供者查询、模型路由、评估、准入规划 | Situation / Agent-plan / capability need candidates | model routing / provider / admission candidates | 是；不得成为认知权威 | **B → MIGRATE**：Capability Composition 与 Resource Modulation 的能力目录提供者 |
| Capability Registry | `capabilities/midplatform/model_manager/registries/capability_registry_v1.json`; `capabilities/registry/luna_capability_registry_v1.json` | 声明能力、生命周期、模块 API | capability id / lifecycle metadata | availability / provider metadata | 是 | **B → KEEP/MIGRATE**：只读能力清单，供 Kernel/Composer 产生 capability-bundle candidate |
| Model Router | `capabilities/midplatform/model_manager/engines/model_routing_engine_v1.py`; `.../field_perception_orchestrator/...requirement_adapter_v1.py` | 将视觉需求归一化并提出模型需求/提供者路线 | visual capability plan / budget | model requirement / route candidate | 部分适用 | **B → REPLACE (cognitive control role)**：未来由 Attention + Kernel 决定是否需要能力；旧 Router 仅提供候选和 provider lookup |
| Task Manager | `capabilities/midplatform/core/task_manager/module/`; `capabilities/midplatform/task_manager_core_orchestration_*` | 任务分解、能力路由、依赖、恢复与结果汇聚 | task / capability requirements | orchestration / routing candidates | 是，但不应控制认知资源 | **B → MIGRATE**：保留为外部任务/工作流协调；A-route 由 Organization + Process Composer 组织认知过程 |
| Vision / field perception | `capabilities/midplatform/field_perception_orchestrator/`; `capabilities/vision/`; `capabilities/model_perception/` | 视觉能力需求、帧输入规划、感知候选 | frame / visual request | visual candidate / requirement | 是 | **A → MIGRATE**：经 Visual Adapter 转为 EvidenceCandidate |
| OCR pipeline | `capabilities/model_ocr/`; `capabilities/ocr_bridge/`; `capabilities/model_ocr/yolo_ocr_bridge_v0.py` | 检测辅助文字区域、OCR provider 选择、OCR evidence pack | detections / image / frame metadata | OCR crop proposal / text evidence result | 是 | **A → MIGRATE**：输出受 Evidence Admission 管理的 OCR evidence；不得直连理解、决策或行动 |
| Detection / segmentation | `capabilities/model_perception/`; Model Test Lens adapter/runner assets | 目标检测、分割候选、评估与可视化 | frame / runner request | detection or segmentation result envelope | 是 | **A → MIGRATE**：Perception evidence source |
| SLAM pipeline | `capabilities/midplatform/model_test_lens/adapters/slam/`; `.../local_runner_bridge/runners/` | SLAM 输出评估、诊断与受限 runner bridge | video / SLAM output | metric / diagnostic / runner candidate | 是 | **A → MIGRATE**：空间 evidence source；不得直接规划路线 |
| Evidence pipeline | `capabilities/ocr_bridge/ocr_evidence_*`; `capabilities/model_integration/model_candidate_adapter_v0.py` | 封装模型/ OCR 结果为 evidence pack 或 model candidate | model output / OCR output | evidence pack / candidate | 部分适用 | **C → MIGRATE**：对齐 `cognitive.evidence.EvidenceCandidate`，统一 source, scope, uncertainty, trace |
| Information processing core | `capabilities/midplatform/information_processing_core_contracts_v1.py`; `...controlled_implementation_v1.py` | Candidate-only 原始信息处理规划 | raw information input candidate | information-processing result candidate | 是 | **C → MIGRATE**：可作为 Information Field 上游候选适配器；避免第二套内部表示权威 |
| Field / context / world / simulation candidate modules | `capabilities/cognitive_flow/field_kernel/`; `current_cognitive_context/`; `current_world_representation_integration/`; `simulation/` | 既有场、上下文、世界表示和模拟规划 | candidate inputs | candidate outputs | 部分适用，存在平行实现风险 | **C → MIGRATE/CONSOLIDATE**：映射至根 `cognitive/` 合约；禁止形成双运行时或双 Attention authority |
| Rule / policy checks | `runtime/gates.py`; `capabilities/governance/`; protocol and validation policies | 安全、协议、准入、治理检查 | runtime / request / policy input | pass, block, validation result | 是 | **B → KEEP**：外部安全/合规边界；不替代 Cognitive Kernel 的候选治理 |
| Decision layer | `runtime/main_loop.py`; `c.controller.decide`; decision-validation planning assets | 旧运行链中的决策或决策验证 | system snapshot | decision / execution intent or validation record | 在 A-route 中不适用为认知权威 | **D → REPLACE (role only)**：A-route 保留 Evaluation/Decision Support Candidate 与 human/executor boundary；不删除旧链路 |
| Action layer | `execution/c_veto_adapter.py`; `capabilities/governance/runtime/navigation_governance_action_*`; voice action proposals | 旧执行意图、受治理动作发布或 action proposal | decision / approval / action request | execution intent / action status | 仅作为未来外部执行边界适用 | **D → DEPRECATE (A-route direct use)**：未来只能接收经权限控制的外部执行候选，不能被认知模块直接调用 |

## Key reassessment

The old midplatform contains useful capability governance and diagnostics. The architectural change is not “discard all old code”; it is the removal of direct control authority from capability, model-router, task-manager, and legacy decision paths. The A-route requires the sequence:

`capability output → EvidenceCandidate → admission / attention → cognitive candidate flow`

not:

`capability output → model router/task manager → decision/execution`.

**Current legacy-midplatform status: `MIGRATE`, with Decision role `REPLACE` and direct Action use `DEPRECATE`.**

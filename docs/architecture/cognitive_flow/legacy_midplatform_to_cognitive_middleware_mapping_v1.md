# Legacy Midplatform to Cognitive Middleware Mapping v1

## Source basis

This mapping is derived from `code_inventory_report.md`, `old_midplatform_mapping.md`, `cognitive_code_alignment_review.md`, and `migration_recommendation.md`. A status changes a future architectural role only; it does not authorize code movement, deletion, or implementation.

| 旧模块 | 新归属 | 处理方式 | 原因 |
|---|---|---|---|
| Model Manager | Capability Manager + Capability Registry | `MIGRATE` | 保留 provider lookup、能力评估、模型准入元数据；移除其对认知选择的潜在控制权。 |
| Capability Registry | Capability Registry | `KEEP` | 已具备能力和生命周期目录价值；未来作为只读 capability availability 输入。 |
| Model Router | Capability Manager 的 provider-resolution 子职责 | `REPLACE` | Brain 的 Attention + Kernel 决定是否需要信息；Router 仅在已准入需求下提出 provider 选择。 |
| Task Manager | 外部 workflow/task coordination | `MIGRATE` | 保留任务依赖、恢复、外部协调；不再承担 Cognitive Process 或 Attention 调度。 |
| Vision / field perception | Hardware Manager + Model Adapter | `MIGRATE` | 作为视觉原始信号与能力提供者，输出统一 evidence。 |
| OCR pipeline / OCR bridge | Model Adapter + Evidence Gateway | `MIGRATE` | OCR 结果应统一为带 source/scope/uncertainty 的 Evidence Candidate。 |
| Detection / segmentation assets | Model Adapter + Evidence Gateway | `MIGRATE` | 作为视觉 evidence provider，不直接影响 decision。 |
| SLAM adapters/runners | Hardware Manager + Model Adapter + Diagnostics | `MIGRATE` | 空间信息、健康与诊断应进入 evidence/reliability 边界，不能直接规划路线。 |
| Device capture/archive adapters | Hardware Manager | `MIGRATE` | 设备/采集生命周期属于 embodiment，不属于 Brain。 |
| Information Processing Core | Evidence Gateway 上游候选适配层 | `MIGRATE` | 可复用 candidate-only 处理边界，但需对齐唯一 Evidence Candidate 合约。 |
| Legacy evidence packs | Evidence Gateway | `MIGRATE` | 统一证据语义，避免平行 evidence/truth 表达。 |
| Model Test Lens / runner bridge | Diagnostics + Cognitive Whitebox | `KEEP` / `MIGRATE` | 适合作为只读观测与受控测试工具，不成为 cognitive control path。 |
| Rule / policy / protocol checks | 外部 governance guard | `KEEP` | 安全与合规检查继续独立存在，不能取代 Cognitive Kernel。 |
| Field/context/world/simulation candidate modules | Brain-side candidate compatibility review | `MIGRATE` | 与根 `cognitive/` 概念重叠；先做合约映射，禁止双运行时。 |
| Fixed-loop legacy runtime | Legacy operational runtime outside A-route | `REPLACE` | 固定 100ms 循环与 decision/execution 链不符合事件驱动 Candidate-only Cognitive Runtime。 |
| Direct decision path | Future external decision boundary only | `REPLACE` | A-route 只产生 Evaluation / Decision Support Candidate。 |
| Direct action/execution-intent path | Future permission-controlled executor boundary only | `DEPRECATE` | 禁止从 A-route Brain 或 Middleware 直接触发。 |

## Migration guard

No legacy module becomes a Cognitive Middleware module merely by being moved into a new directory. Migration requires a future approved contract-alignment review that proves:

1. Candidate-only output;
2. explicit provenance, uncertainty, and trace;
3. no Goal, Attention, Truth, Decision, Action, or State-mutation authority;
4. CNP boundary compatibility;
5. V0/V1 regression evidence appropriate to that future phase.

## Status

`LEGACY_MIDPLATFORM_TO_COGNITIVE_MIDDLEWARE_MAPPING_READY_WITH_NOTES`

`WAITING_FOR_USER_TERMINAL_VERIFICATION`

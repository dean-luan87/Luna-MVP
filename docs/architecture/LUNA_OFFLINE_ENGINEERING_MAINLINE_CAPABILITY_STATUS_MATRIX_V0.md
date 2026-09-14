# LUNA Offline Engineering Mainline Capability Status Matrix v0

## Phase

- Phase-EngineeringFlow-Closure（Offline Engineering Mainline Closure v0）

## Legend

- **done**：已完成并纳入离线工程主链闭环
- **offline-only**：仅离线评测可用，不允许 runtime
- **minimal-runtime**：仅“离线 runner 内部最小 runtime 化”（candidate-only / 审计用），非真实 runtime
- **regression-baseline**：已固化为回归验收基线（EF-006）
- **out-of-scope**：明确不在本主线闭环范围
- **future**：未来分支（未授权/未实现/需治理入口）

## Matrix

| Capability / Module | Status | Notes / Boundary |
|---|---|---|
| EF-001 Offline mainline integration plan | done | 集成计划冻结，禁止扩展政策已立 |
| EF-002 Offline perception source policy (YOLO default) | done + offline-only | default 仅限 phone_local 离线评测；失败必须 fail-closed 到 baseline_mock |
| YOLO pinned_local weights readiness | done + offline-only | 权重固定本地；仅 shadow candidate；不进入 runtime |
| PerceptionEval default entry point | done + offline-only | source policy 审计字段必须保留 |
| EF-003 SceneContext gates v0 | done + minimal-runtime | 仅离线 runner 内 gate_result / gated_perception_candidate；禁止下游动作 |
| SceneTask candidate generator (v0 minimal) | done + minimal-runtime | 仅 candidate；不引入新能力 |
| Fusion candidate generator (v0 minimal) | done + minimal-runtime | 仅 candidate；不接地图/记忆扩展 |
| Output candidate generator (v0 minimal) | done + minimal-runtime | 禁止真实 TTS；allows_execute_now 必须 false |
| EF-004 unified offline mainline runner | done + regression-baseline | 一键离线主链；不进入 runtime |
| trace / replay / whitebox index | done + regression-baseline | 必须生成且可追溯 |
| EF-005 unified observability report | done + regression-baseline | md/json 双报告 + refs 不断裂 |
| EF-006 regression acceptance | done + regression-baseline | 硬门槛阻断后续；允许波动项仅限检测数量等 |
| controlled_live_stream pipeline | out-of-scope | 本闭环明确禁止 |
| real runtime default path | out-of-scope | 本闭环明确禁止 |
| navigation execution / side effects | out-of-scope | 明确禁止 |
| real TTS | out-of-scope | 明确禁止 |
| tracking / depth / OCR / dynamic enhancement | out-of-scope | 明确禁止（未来需分支治理） |
| OCR mainline | future | 需要单独分支与验收入口 |
| Scene belief / evidence arbitration | future | 需要治理入口与评测合同 |
| stronger SceneContext runtime gates | future | 只能先离线增强，需再走回归基线 |
| sample expansion beyond 3 | future | 需定义样本扩容策略与门槛 |
| controlled_live preparation | future | 需要严格治理入口与证据契约 |
| dependency isolation / autoupdate hardening | future | 依赖隔离与可复现策略增强 |
| model upgrade admission policy | future | 需要准入矩阵与 go/no-go |
| runtime integration readiness | future | 需要独立阶段与禁止项复核 |


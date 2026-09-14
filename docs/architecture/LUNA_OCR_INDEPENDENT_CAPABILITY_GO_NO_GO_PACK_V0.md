# LUNA OCR Independent Capability Go/No-Go Pack v0

## Phase

- Phase-ModelOCR-001（OCR Independent Capability Definition v0）

## Decision

- Decision: **GO**（definition-only；允许进入 ModelOCR-002 inventory 阶段）

## What was produced (docs)

- `docs/architecture/LUNA_OCR_INDEPENDENT_CAPABILITY_DEFINITION_V0.md`
- `docs/architecture/LUNA_OCR_INPUT_OUTPUT_CONTRACT_V0.md`
- `docs/architecture/LUNA_OCR_OBSERVATION_CONTROL_POLICY_V0.md`
- `docs/architecture/LUNA_OCR_SIGNAL_AND_TRACE_REQUIREMENTS_V0.md`

## Frozen statements (must remain true)

- 本阶段只做 OCR 独立能力定义，不实现 runtime
- 不接 YOLO（不做 OCR+YOLO 联动）
- 不接中台（不做 Scene Belief / Evidence Arbitration 实现）
- 不接 SceneTask/Fusion/Output
- 不进入 controlled_live_stream
- 不进入 full controlled trial
- 不开放真实用户测试
- 不执行导航动作
- 不真实播报（real TTS）

## GO criteria (definition-only)

满足以下即 GO：

- OCR 职责边界清楚（只读文字候选证据；不做导航决策）
- 输入边界清楚（禁止 execution/governance override/default-on）
- 输出合同清楚（candidate-only；allows_execute_now=false；real_tts_invoked=false）
- 观察控制方案清楚（full_frame_low_frequency / region_focused / task_hint_guided）
- 禁止项清楚（禁止导航指令/执行语义/释放 side effects 等）
- trace/replay/whitebox 要求清楚
- fallback/not_available 规则清楚（fail-closed）
- 后续阶段路线清楚（先 OCR 独立闭环，再 YOLO×OCR 协同，再中台仲裁）

## NO_GO criteria

出现任一即 NO_GO：

- OCR 被允许直接产生导航指令
- OCR 被允许绕过 SceneContext 形成结论/执行
- OCR 被允许直接进入 SceneTask/Fusion/Output
- OCR 输出未包含 allows_execute_now=false 或 real_tts_invoked=false 的硬约束
- OCR 没有 fallback/not_available 规则
- 本阶段实现 runtime 或直接接 YOLO/中台

## Recommended next phase

- ModelOCR-002：Existing OCR Inventory & Adapter Mapping（仅做 inventory 与适配映射定义/盘点）


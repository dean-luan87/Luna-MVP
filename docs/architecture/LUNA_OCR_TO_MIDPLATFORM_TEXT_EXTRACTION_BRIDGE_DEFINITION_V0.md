# LUNA — OCR Raw Text → MidPlatform Text Extraction Bridge Definition v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-001** — 定义 OCR raw text 进入 MidPlatform evidence layer 的离线桥接合同与边界（Definition/Contract Only）。

## Primary goal

把 OCR offline 产物（raw text candidates/segments/签名与证据链）在 MidPlatform 侧做“仅处理变化信息”的治理：去重、delta 判断、reuse/partial_update/full_reprocess 决策，并输出 `MidPlatformTextExtractionCandidate`（仍不做最终语义/导航/执行）。

## Non-governance boundaries（冻结约束）

- 不实现 runtime：不接真实 runtime、不接 MidPlatform 真正执行链、不写入 SceneTask/Fusion/Output。
- 不接下游：不把候选事实直接消费给任务链执行。
- 不做文本语义提炼：`semantic_summary` 必须为 `null`（或不生成）。
- 不执行导航动作：`navigation_action = null`。
- 不真实播报/不触发 real TTS。
- 不修改既有 `YOLO closed_v0` / `OCR closed_v0`。

## Responsibilities (who does what)

### OCR（raw text provider）
- 产生：`raw_text_candidates`、`raw_text_joined`、`raw_text_segments`
- 产生证据：`reading_direction_candidate`、`line_order_status`
- 产出：trace/replay/whitebox 引用（不做语义）

### YOLO × OCR Offline Bridge（candidate producer）
- 产生：`OCRCropProposal` 对应的 bridge 结果（包含 raw text）
- 产生：`crop_signature` 初始值、source attribution（YOLO 与 OCR provider/policy）

### MidPlatform Evidence Layer（只做 evidence governance 与去重复用）
- 接收：`MidPlatformOCREvidenceInput`（输入合同见 `LUNA_MIDPLATFORM_OCR_EVIDENCE_INPUT_CONTRACT_V0.md`）
- 执行：delta control（见 `LUNA_SCENE_INFORMATION_DELTA_CONTROL_POLICY_V0.md`）
- 执行：signature 规则与 reuse/partial/full 策略（见 `LUNA_OCR_TEXT_SIGNATURE_AND_REUSE_POLICY_V0.md`）
- 输出：`MidPlatformTextExtractionCandidate`（候选合同见 `LUNA_MIDPLATFORM_TEXT_EXTRACTION_CANDIDATE_CONTRACT_V0.md`）

### TaskChain
- 只提供任务目标/上下文
- 只接收 `task_relevant_text_candidate`
- 不直接消费 OCR 原文证据、不直接调 OCR/YOLO、不做 runtime 决策

## Bridge contracts (接线合同)

1. OCR raw text → MidPlatform evidence input：`MidPlatformOCREvidenceInput`
2. MidPlatform delta control：`SceneInformationDeltaControl`
3. MidPlatform text extraction candidate output：`MidPlatformTextExtractionCandidate`

## Evidence & signatures（去重核心）

- `crop_signature`：用于判断同一区域是否复用
- `text_signature`：用于判断文字是否变化
- `layout_signature`：用于判断版面是否变化
- `object_signature`：用于判断视觉对象是否变化

所有签名的 hash 输入必须记录 source fields（不能只有 hash 值）。

## Output invariants（输出不变量）

- `candidate_only=true`
- `semantic_interpretation_enabled=false`
- `allows_execute_now=false`
- `real_tts_invoked=false`
- `downstream_invocation_count=0`
- `trace/replay/whitebox` 引用完整且可追责

（runtime 与下游消费由后续 Phase 定义，本阶段不实现。）


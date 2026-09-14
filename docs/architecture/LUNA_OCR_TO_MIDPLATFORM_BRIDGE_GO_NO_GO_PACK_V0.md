# LUNA — OCR Raw Text → MidPlatform Bridge Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-001**

## GO（通过）条件（冻结）

同时满足：

- OCR evidence input schema 明确且完整对齐 `MidPlatformOCREvidenceInput`。
- delta control policy 明确且对齐 `SceneInformationDeltaControl`。
- signature 规则明确定义（crop/text/layout/object signatures）。
- reuse / partial_update / full_reprocess / hold_uncertain 决策规则明确。
- text extraction candidate schema 明确（`MidPlatformTextExtractionCandidate`）。
- filtering/blocking 占位规则明确（且不删除证据，仅阻断候选）。
- 本阶段不实现 runtime。
- 不接下游、不接 SceneTask/Fusion/Output。
- 不做语义提炼（`semantic_summary=null`）。
- 不执行导航动作、不真实播报、不触发 real TTS。

## CONDITIONAL_GO（条件通过）

- bridge 定义与审计规则成立；
- 但在 future phase 里仍需补充“更细的 delta / extraction 细粒度策略”，当前版本只能作为定义口径基线。

## NO_GO（不通过）

- 中台把 OCR raw text 当最终事实直接进入任务链。
- 中台跳过 delta control。
- 重复信息被反复提炼为新的语义结论（违反 “no semantic_summary”）。
- 生成语义总结或导航动作。
- 接入真实 runtime / 下游消费链。
- 未按 contract 输出 required fields（schema contract 破坏）。


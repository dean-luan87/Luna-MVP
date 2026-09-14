# Verification

Verifier 为用户终端运行的 fail-closed 检查器。此前用户终端结果为 144/144 checks、
Operational PASS、Cognitive Logic PASS、GO；本次一致性审计发现并修复了
`IRRELEVANT` Evidence 可直接进入 coverage 的断链。修复后重新验证仍待用户终端执行，
当前状态为 `COGNITIVE_LOGIC_GAP_FIXED — WAITING_FOR_USER_TERMINAL_VERIFICATION`。

## Operational checks

- `LIVE_RUNTIME`
- provider/model 实际 invocation proof
- `provider_real_execution_attempted` 与 `provider_real_execution_verified`
- canonical `text_recognition` / `provider:ocr_v1` / `model:ocr_v1`
- ProviderRuntime request/result、RuntimeObservation、Gateway admission、Evidence 与 CState
- `recorded_result_used == false`
- trace/provenance 和 validation errors

## Cognitive checks

- same source/native observation invariance
- Goal 改变 Information Need/required information，并产生 material cognition difference
- Task 改变 cognition，但不产生 Task execution
- Role 使用既有 vocabulary 并改变 perspective/relevance/interpretation，而不改变物理 Evidence
- difference 不是仅由 case/scenario/identity refs 造成
- `irrelevant_evidence_does_not_cover_required_information`
- `relevant_evidence_can_cover_required_information`
- candidate-only、无 World Truth、无 Field mutation
- 无 Decision、Task、Action、Runtime Executor、device control

当前文档不宣称终端结果。只有用户终端执行 Runner 与 Verifier 后，才能形成该 Phase
的最终 operational/cognitive 结论。

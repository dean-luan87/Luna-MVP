# Summary

本 Phase 已准备三组最小对照：

1. `SAME_EVIDENCE_DIFFERENT_GOAL`
2. `SAME_EVIDENCE_DIFFERENT_TASK`
3. `SAME_EVIDENCE_DIFFERENT_ROLE`

所有对照共享真实 OCR source 与 candidate-only Evidence boundary。Goal 对照通过不同
Information Need/required information 检查 sufficiency causality；Task 对照复用既有
Task vocabulary，检查 hypothesis/relation 等 cognition projection；Role 对照复用
`workspace-owner`/`visitor`，检查 perspective/relevance，不改变物理 Evidence。

每个 side 都沿用真实 OCR provider execution，Runner 输出 native result、Runtime
Observation、Gateway admission、Evidence、A-Route/CState proof、conditioning snapshot
和 Plane G result。Verifier 将分别报告 operational 与 cognitive logic 结果。

## Consistency audit

对 `Evidence Admission → Evidence Relevance → Information Coverage → Sufficiency →
Stop` 的限定审计确认：原实现由 OCR provider success 后声明的
`available_information_refs` 直接做集合覆盖，未读取 CState 生成的
`evidence_relevance_candidates`。因此 `IRRELEVANT:0.15` 与 `SUFFICIENT` 可以同时出现；
这不是 canonical contract 允许的语义，而是 `COGNITIVE_LOGIC_GAP`。

最小修复增加了只读 Evidence→information support binding，并让有 binding 的 Runtime
ingress 只允许 `RELEVANT` Evidence 贡献 coverage；re-observation 的 inherited
information 保持独立 lineage。Verifier 新增了：

- `irrelevant_evidence_does_not_cover_required_information`
- `relevant_evidence_can_cover_required_information`

`task:find-document` 检查结果为：它来自既有 Full E2E canonical vocabulary；当前对照
仍是基于真实物理 Evidence 的 synthetic semantic contrast，不是新的 Task ontology。

历史用户终端结果 `144/144`、Operational PASS、Cognitive Logic PASS、GO 保留不变；它
记录的是修复前实现。修复后的真实 Runner/Verifier 尚未执行，当前状态：
`COGNITIVE_LOGIC_GAP_FIXED — WAITING_FOR_USER_TERMINAL_VERIFICATION`。不能写新的
`GO`、`PASS` 或 `VERIFIED`。

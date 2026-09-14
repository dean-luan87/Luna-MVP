# Re-observation Trace

Case B 的因果链为：

`Cognitive State (cycle 1)`
→ `CognitiveInformationGapCandidateV1`
→ `CognitiveReobservationCandidateV1` (Field Perception Orchestrator)
→ `next_cycle_ingress_ref`
→ source binding whose information refs intersect Gap missing refs
→ new Observation Demand / Capability Requirement
→ new `ProviderRuntimeRequestV1`
→ new real RapidOCR invocation。

Runner 不直接以“第二轮”调用 OCR。它先读取第一轮 proof 的 missing refs，只有
存在匹配的第二 binding 时才继续。Cycle 2 保存第一轮 refs 作为 prior lineage，
并产生新的 Provider request/result、RuntimeObservation、Gateway admission 和
Evidence refs。

Cycle 2 的新 Evidence 与 prior state 共同输入 CState，产生 hypothesis revision
candidate；若 minimum sufficient 已达到，canonical Stop candidate 结束。不存在
Cycle 3。

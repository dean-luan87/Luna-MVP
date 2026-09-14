# Cognitive Loop Mapping

复用的 canonical owner/contracts：

- `CognitiveStateFormationEngineV1` 与 `CognitiveStateFormationInputV1`；
- `CognitiveSufficiencyCandidateV1`；
- `CognitiveInformationGapCandidateV1`；
- `CognitiveReobservationCandidateV1`；
- `CognitiveHypothesisRevisionCandidateV1`；
- `CognitiveStopCandidateV1`；
- A-Route 的 `ARouteCognitiveExecutionEvidenceV1`；
- Field Perception Orchestrator 的 Re-observation ownership；
- Observation Gateway 的 LIVE runtime admission。

Evaluation engine 不创建新的 cognition owner。每轮都把真实 OCR engine 返回的
runtime observation 通过既有 Gateway/A-Route 交给 CState。第二轮的 prior gap、
prior re-observation、prior next-cycle ingress、prior hypotheses 和 prior
candidates 来自第一轮 canonical proof。

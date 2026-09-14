# Architecture order

当前受控顺序：

`FPO Compatibility → Provider Runtime Target Preparation → Provider Binding Candidate → Runtime Allocation Preparation Candidate → Execution Instance Preparation Candidate → [future runtime]`

旧 `ModelProviderBindingCandidateV1` 是 Model+Provider 合同，要求完整 model declaration；它没有被强行用于 Provider-only target。新增 Provider-only Candidate 保持 Model optional：有显式 `source_model_ref` 时 carry forward，没有时不推断。

Observation Gateway 的 `RuntimeObservationEnvelopeV1`/admission contract 需要 concrete runtime identity，故不在本阶段调用或提交。

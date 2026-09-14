# Authority / Responsibility Findings v1

## F-001 — Real provider path not proven to consume canonical binding seams

- Severity: `P1`
- Classification: `AUTHORITY_BYPASS` / `ACTIVE_OVERLAP`
- Claim challenged: Capability Governance owns Capability↔Model binding; Provider Governance owns Model↔Provider binding; Runtime Admission precedes Provider Admission.
- Evidence: `capabilities/midplatform/field_perception_orchestrator/integration/yolo11n_single_frame_execution/run_yolo11n_real_single_frame_provider_execution_v1.py:100-160`; `field_perception_real_vision_provider_adapter_v1.py:225-288`.
- Actual behavior: the path resolves external model provisioning, builds an FPO observation/provider admission candidate, and can call YOLO directly. It carries `model_candidate_ref`, `model_admission_ref`, and `provider_candidate_ref`, but does not consume `CapabilityModelBindingCandidateV1` or `ModelProviderBindingCandidateV1` records.
- Expected behavior: model/provider execution path must be downstream of logical capability resolution, canonical binding refs, Runtime Admission, and Provider Admission.
- Authority owner: Capability Governance for Capability↔Model binding; Provider Governance for Model↔Provider and Provider execution boundary; Runtime Admission for executable eligibility.
- Responsibility owner: the FPO/provider integration adapter for translation/execution-path correctness; Model Governance for declaration correctness; Provider Governance for provider admission correctness.
- Risk: a runnable real path can select/use a model/provider through a parallel seam, making the freeze’s “no active bypass” claim unproven.
- Recommended owner/phase: Provider + Capability/Model integration owner; targeted active-caller remediation phase. No owner change proposed.

## F-002 — Controlled chain is not canonical runtime authority

`CognitiveExecutionChainEngineV1` composes engines and calls `RuntimeExecutorEngineV1`, but `IntegrationRunSummaryV1` and runner output explicitly set `candidate_only=True`, `runtime_executed=False`, and mutation flags false. It is a controlled compatibility composition, not evidence that the production flow is wired. Classification: `COMPATIBILITY_ONLY`, severity `P2` for implementation ambiguity, not a freeze blocker.


# LUNA — Unified Capability Runtime Monitoring Definition v0

## Phase

- **Phase-MidPlatform-Monitoring-001**
- 目标：统一能力模块运行监控范式（中台层），避免各模块监控体系碎片化。

## Covered capability domains

- Voice / TTS
- ASR
- OCR
- Vision / YOLO
- VLM
- Semantic
- Decision
- TaskChain
- Output

## Unified monitoring pipeline

`Module Runtime Event`
-> `Capability Health State`
-> `Invocation Result`
-> `Trace / Replay / Whitebox`
-> `MidPlatform Monitoring`
-> `Dashboard / Report / Regression Gate`

## Core unified objects

1. `capability_runtime_event`
2. `provider_health_state`
3. `invocation_result`
4. `latency_budget`
5. `fallback_report`
6. `safety_governance_violation`
7. `trace_replay_whitebox_reference`
8. `monitoring_summary`
9. `regression_gate_metrics`

## Ownership model

- **Capability module owns:**
  - provider-specific raw event fields
  - provider-specific health/failure/fallback details
  - trace/replay/whitebox production
- **MidPlatform monitoring owns:**
  - ingestion normalization
  - cross-capability aggregation and alerting
  - health scoring and runtime judgment
  - regression comparison and gate decision

## Non-goals in this definition

- 不实现具体 runtime 调用。
- 不替代各模块内部 schema，仅规定中台统一收口接口。

## Relationship to OCR Governance

OCR governance 文档是本统一监控框架的 OCR 子域规范，不是独立监控体系。

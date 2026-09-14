# LUNA — OCR Module Governance Go/No-Go Pack v0

## Phase

- **Phase-ModelOCR-Governance-001**
- 仅定义治理标准，不实现 runtime，不启用默认 provider chain。

## GO

- OCR 输入/输出处理标准清晰。
- 健康指标体系完整（availability/latency/schema/quality/governance/fallback/observability）。
- Provider health state schema 清晰。
- failure/degradation/fail-closed 策略清晰。
- trace/replay/whitebox 标准清晰。
- 与中台模型切换策略对齐关系明确（本阶段仅定义接入点）。
- 未越界到语义、导航、下游。

## NO_GO

- 仅定义“有无输出”，未定义延迟/吞吐。
- 未定义 fallback 与异常分类。
- 未定义 semantic/navigation leakage。
- 未定义 trace/replay/whitebox。
- 本阶段直接启用默认 provider chain 或接入下游执行。

## Relationship with MidPlatform switching policy

本阶段不实现接入，只定义 OCR 特有指标与 profile，供后续与
`MidPlatform Model Invocation Switching Policy v0` 对接：
- latency budget
- fallback decision
- circuit breaker state
- provider health state

## Ownership clarification

- OCR 文档只冻结 OCR-specific 字段与边界。
- 统一监控归属在中台阶段：
  - **Phase-MidPlatform-Monitoring-001**
  - **Unified Capability Runtime Monitoring Definition v0**
- 本阶段不把 OCR 监控独立成孤立体系。

## Recommended next phase

1. **ModelOCR-004B continuation**（补齐 Paddle 依赖并复验 init-only）
2. **ModelOCR-005**（GT Dataset + Raw Text Benchmark）

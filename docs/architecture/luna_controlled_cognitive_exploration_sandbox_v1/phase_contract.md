# Phase Contract

## Scope

Phase：`Phase-Controlled-Multi-Scenario-Cognitive-Exploration-Sandbox-v1-001`

Sandbox 是现有 cognition chain 的 consumer/orchestrator。它不取得
Information Need、Branch、Governance 或 Acquisition Strategy 的 semantic ownership。

## Round boundary

Round 0 使用 synthetic governed rules、controlled current situation、Need/Gap
basis 与 explicit acquisition bases。

Round 1 只在场景声明 `simulated_return_enabled=true` 且 runner 形成
`SandboxSimulatedAcquisitionReturnV1` 后运行。该 envelope 只能增加受控 coverage
refs 或记录无关环境变化；它不模拟 Provider/Model 执行。

## Scenario contract

`SandboxScenarioV1` 保留 scenario metadata、problem、required conditions、opaque
context、synthetic inputs、behavior class、governed condition rules、initial
situation 与 explicit strategy-basis specs。`expected_behavior_class` 仅用于人工
阅读，不驱动 canonical 形成结果。

## No semantic fabrication

Sandbox 不从 Goal、Question、Problem 字符串、Need 文本、scenario_id、case_id 或
fixture name 生成 Branch/Strategy。没有 governed acquisition basis 时，现有
strategy formation 会诚实返回零 candidate；Sandbox 不添加 fallback。

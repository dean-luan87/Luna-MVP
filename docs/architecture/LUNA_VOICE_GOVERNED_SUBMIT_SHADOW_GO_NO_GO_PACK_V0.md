# Phase-Voice-OutputGovernance-007
# Governed Submit Shadow Go/No-Go Pack v0

**阶段目标**：验证语音治理链在“submit 前”的 shadow readiness（不真实 submit、不真实播报）。

---

## GO 条件（全部满足）

- governance root 可读
- request trace root 可读
- submit shadow decisions 生成
- 两个 submit gate position 模拟完整
- accepted/expired/cancelled/fallback 映射正确
- hard audit 不变量保持
- trace/replay/whitebox 非空
- verifier 通过
- 未接真实 submit、未真实播报

---

## CONDITIONAL_GO（允许但必须记录）

- 某些 legacy 字段只能从 governance decision 推导，但 decision/audit refs 可追溯

---

## NO_GO（任一触发即失败）

- `real_submit_invoked=true`
- `real_tts_invoked=true`
- `playback_invoked=true`
- `provider_invoked=true`
- `navigation_action` 非空
- `downstream_invocation_count>0`
- expired/cancelled 仍被允许 submit
- SpeechGate 结果丢失（无法证明 gate 检查执行）
- 本阶段修改真实 submit 链或修改 env 语义或删除 legacy voice


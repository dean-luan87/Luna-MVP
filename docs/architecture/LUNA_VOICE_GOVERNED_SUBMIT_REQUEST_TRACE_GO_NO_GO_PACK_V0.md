# Phase-Voice-OutputGovernance-008

# Governed Submit RequestTrace Go/No-Go Pack v0

## GO（全部满足）

- submit shadow root、voice request trace root 可读
- enhanced chains 生成
- `request_trace.stage.output.voice.governed_submit_shadow_gate` 存在
- 两种 gate position 在 enhanced/matrix 中均有覆盖
- request_id join 成功 > 0
- hard audit 字段保留且不变量成立
- trace/replay/whitebox 非空
- verifier 通过

## CONDITIONAL_GO

- 存在 unmatched decisions，但已记录且不影响已匹配链完整性披露

## NO_GO（任一）

- governed_submit_shadow_gate 缺失或 gate position 丢失
- hard audit 丢失或 `real_submit_invoked=true` / `real_tts_invoked=true` / `provider_invoked=true`
- 修改 Phase-005 源文件或接入真实 submit

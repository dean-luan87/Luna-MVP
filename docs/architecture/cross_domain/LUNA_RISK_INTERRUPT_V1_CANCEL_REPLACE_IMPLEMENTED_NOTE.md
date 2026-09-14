# risk_interrupt_v1 cancel+replace 受限实现（V1，仅待执行 request）说明

## 实现了什么（严格按评审结论锁边界）

根据《[LUNA_RISK_INTERRUPT_V1_CANCEL_REPLACE_REVIEW_V1.md](./LUNA_RISK_INTERRUPT_V1_CANCEL_REPLACE_REVIEW_V1.md)》的单选结论，新增一个**极小范围**的 cancel+replace 受限实现：

- **只允许取消待执行 request**（未出现 `playback_started` 的 request；允许“已进入执行层但未 started”的 current）
- **明确禁止**取消已 started playback
- **只允许** `high/critical`
- **只允许**低价值 `prompt/confirmation`
- **只有观测到 cancel 终态后**才允许 replace submit
- 任一链路不闭合立即回退到 preempt-before-submit（不影响现有试点）

## 开关（默认关闭）

新增试点开关（默认关闭）：

- `LUNA_ENABLE_RISK_INTERRUPT_V1_CANCEL_REPLACE_PILOT=0`

依赖已有：

- `LUNA_ENABLE_RISK_INTERRUPT_V1=1`
- `LUNA_RISK_INTERRUPT_WHITEBOX_ONLY=0`
- `LUNA_ENABLE_INTERRUPT_CANCEL_V1=1`（底层 cancel 能力总开关）

## 代码落点

- `capabilities/voice/runtime/voice_final_text_dispatcher.py::_maybe_submit_real_output_v1(...)`
  - 在生成 `SpeechRequest` 前进行 cancel+replace 受限评估
  - 通过 `audio_worker_v1.snapshot_state()` 获取 queued/current 状态
  - 只在 queued/current 未 started 情况下调用 `PlaybackPlaneV1.cancel(request_id)`
  - 轮询确认 `playback_cancelled` 终态（超时则回退）
  - 仅在 cancel 终态确认后生成新的 replacement_request_id 并提交风险提示

## 观测（最小）

新增/补充 `output_decision` 观测（可按 request_id 对账）：

- `reason="risk_interrupt_v1_cancel_replace_pilot_evaluated"`
- metadata 至少包含：
  - `cancel_replace_chain_closed`
  - `fallback_to_preempt_before_submit`
  - `failure_reason`
  - `replacement_request_id`

## 怎么验证

```bash
python3 tools/test_risk_interrupt_v1_cancel_replace_v1.py
```

覆盖：

- 默认关闭不触发
- 风险不足不触发
- 待执行 request + high risk：cancel 后 replace 成功且链闭合

## 如何回退（秒退）

- 关闭 `LUNA_ENABLE_RISK_INTERRUPT_V1_CANCEL_REPLACE_PILOT=0` 即秒退回当前 preempt-before-submit

## 仍然写死禁止

- 禁止取消已 started playback
- 禁止取消非 prompt/confirmation
- 禁止 medium/low 风险触发
- 禁止其他旁路进入该链
- 禁止恢复/重播/多 request 级联取消


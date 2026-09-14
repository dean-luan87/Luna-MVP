# 最小中断 / 取消实现（V1）说明

## 实现了什么

根据《[LUNA_INTERRUPT_CANCEL_SEMANTICS_V1.md](./LUNA_INTERRUPT_CANCEL_SEMANTICS_V1.md)》，先落了一个最小可运行的 **cancel** 能力（V1）：

- 提供一个最小 cancel 入口：按 `request_id` 取消“当前正在执行”或“队列中待执行”的播放请求
- 由真实执行层线程产出 `playback_cancelled` 真状态事件（不在调用线程伪造）
- 与 submit/request/playback 现有链路可对账
- 默认关闭、可回退

> 本 V1 只做 cancel，不做高层 interrupt 策略、不做恢复、不做抢占升级，不改 risk_interrupt_v1 现有试点实现。

## cancel 入口在哪

- `capabilities/voice/output/playback_plane_v1.py::PlaybackPlaneV1.cancel(request_id, reason)`
  - 内部转发到 `audio_worker_v1` 的 cancel 逻辑

## 开关（默认关闭）

- `LUNA_ENABLE_INTERRUPT_CANCEL_V1=0`（默认）
  - 关闭：cancel 调用返回 `cancel_disabled`，不会产出 `playback_cancelled`
  - 开启：允许 cancel 生效并产出 `playback_cancelled`

辅助（测试/演练）：

- `LUNA_AUDIO_WORKER_V1_SIMULATED_PLAY_MS`：模拟执行窗口（用于在 started 后触发 cancel）

## 事件与对账

cancel 生效后，由执行层线程写入：

- `playback_cancelled`（type=`playback_runtime`，同一 `request_id` 串起）

并保证：

- cancel 不会伪造 `playback_started`
- cancel 生效后不再写入 `playback_finished`（避免混淆）
- `playback_failed` 与 `playback_cancelled` 不混淆（失败仍走 failed 终态）

## 怎么验证

```bash
python3 tools/test_interrupt_cancel_v1.py
```

覆盖：

1) cancel 默认关闭：不产生 playback_cancelled  
2) cancel 开启：started 后 cancel → 产生 playback_cancelled 且不再产生 finished  

## 仍未做

- 不做 interrupt 高层语义（本轮只做底层 cancel）
- 不做恢复/重播
- 不做多 request 编排与优先级队列
- 不让旁路直接调用 cancel
- 不把 risk_interrupt_v1 从“提交前替换”升级为“真实取消 + 替换”


# LUNA — Voice Output State Machine & Interruption Policy v0

## Phase

- **Phase-Voice-OutputGovernance-001**

## Purpose

定义语音输出的状态机与打断/取消/过期规则，确保：

- 不打断导航、安全提醒、任务链主流程（除非被更高优先级治理明确允许）
- 输出可取消、可超时、可抑制
- 过期不播报

本阶段只定义，不实现 runtime。

## VoiceOutputState（v0）

- `queued`
- `synthesizing`
- `ready_to_play`
- `playing`
- `completed`
- `cancelled`
- `suppressed`
- `expired`
- `failed`

## Interruption rules（硬约束）

- `interrupt_allowed=false` 默认（除非 safety policy 明确允许）
- **不得打断**：navigation / safety_warning / primary_task / emergency flow
- 若上游输出治理判定 `suppressed_by_safety_warning`：必须进入 `suppressed`
- 若 `now >= expires_at`：必须进入 `expired`（不得播报）

## Cancellation & timeout（v0）

- 合成超时（synthesis_timeout_ms）触发 `failed` 并走 fallback（仅策略定义）
- 播放取消（user_cancel/system_cancel）触发 `cancelled`
- 取消/失败必须记录 audit 事件（trace/whitebox）


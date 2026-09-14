# risk_interrupt_v1 Level 2 受限试点实现（V1）说明

## 实现了什么（极小范围）

按《[LUNA_RISK_INTERRUPT_V1_LEVEL2_PILOT_PLAN.md](./LUNA_RISK_INTERRUPT_V1_LEVEL2_PILOT_PLAN.md)》的边界，落了一个**极小** Level 2 受限试点实现（V1）：

- **只允许** `risk_interrupt_v1`
- **只允许** `high/critical`
- **只允许**对低价值 `prompt/confirmation` 短文本做“提交前替换式抢占”（preempt-before-submit）
- **不实现**中断/恢复/队列；不做 speaking 接管；不让其他旁路进入真实输出

## 试点边界（写死）

- 不扩 submit 候选范围（仍仅原主链稳定提示/确认短文本）
- 不抢占任务链相关输出（当前 V1 submit 候选本就不覆盖任务链输出）
- dry-run 不伪造 playback 真状态（保持既有约束）

## 代码落点

- 试点裁决点（提交前替换）：
  - `capabilities/voice/runtime/voice_final_text_dispatcher.py::_maybe_submit_real_output_v1(...)`
  - 在构造 `SpeechRequest` 前读取 `risk_summary_v1`（优先 `runtime_context`），若满足试点条件则把原 `text_candidate` 替换为安全提示文本。

## 试点开关（默认关闭）

- `LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT=0`：默认关闭，关闭即完全不进入 Level 2 试点逻辑

与既有开关的组合约束：

- 必须 `LUNA_ENABLE_RISK_INTERRUPT_V1=1`
- 必须 `LUNA_RISK_INTERRUPT_WHITEBOX_ONLY=0`（否则保持 Level 1 whitebox-only，不进入试点）

## 可观测性（request_id 对账）

当触发“提交前替换式抢占”时，会写入 `output_decision` 结构化观测（同一 `request_id` 串起），用于对账：

- `reason="risk_interrupt_v1_level2_pilot_preempt_before_submit"`
- metadata 包含 `risk_level`、被抢占输出类别等最小字段

## 怎么验证

```bash
python3 tools/test_risk_interrupt_v1_level2_pilot.py
```

覆盖：

1. pilot 默认关闭 → 不抢占
2. pilot 开启 + 风险不足 → 不抢占
3. pilot 开启 + high/critical → 发生“提交前替换”且写入 output_decision 观测
4. 关闭 pilot → 秒退回 Level 1（不抢占）

## 如何回退（秒退）

- 秒退 Level 1：`LUNA_ENABLE_RISK_INTERRUPT_V1_LEVEL2_PILOT=0`（保留 risk_interrupt_v1 Level 1 白盒不变）
- 秒退 Level 0：在需要时同时关闭：
  - `LUNA_ENABLE_RISK_INTERRUPT_V1=0`
  - `LUNA_ENABLE_REAL_OUTPUT_SUBMIT_V1=0`

## 仍未做（明确不做）

- 不做真实播放中的中断与恢复
- 不做多风险事件编排
- 不让其他旁路进入真实输出
- 不进入全主线真实抢占


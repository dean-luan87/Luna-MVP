# Sidewalk Nav V1：主线边缘集成说明

## 目的

在**不改主链默认行为**的前提下，验证 `sidewalk_nav_v1` 能以与主链输出一致的最小 `metadata` 为载体完成挂载：默认零侵入、开启时可合并白盒、高风险或 `risk_interrupt_preempt` 时压制普通导航提示。

## 集成口径（推荐）

1. 在产出主链结果（例如语音下发结果的 `metadata`）的**同一层**，若需启用人行道旁路，则调用 `evaluate_sidewalk_nav_v1(...)`。
2. 仅当返回的 `result.metadata` 中含 `sidewalk_nav_v1` 时，将其 **merge** 进主链 `metadata`（与 `risk_interrupt_v1` 并列键，由上层统一裁决最终播报）。
3. `LUNA_ENABLE_SIDEWALK_NAV_V1=0` 时：不调用或忽略旁路返回值中的白盒键，主链 `metadata` 保持原样。

## 验证方式

```bash
python3 tools/test_sidewalk_nav_v1_integration.py
```

脚本用最小 dict 模拟 `VoiceFinalTextDispatchResult.metadata`，断言：

| 场景 | 预期 |
|------|------|
| 默认关闭 | 不挂载 `metadata["sidewalk_nav_v1"]`，与占位 metadata 一致 |
| 开启 + `LUNA_SIDEWALK_NAV_WHITEBOX_ONLY=1` | 挂载白盒；`navigation_hint` 可非空；`final_spoken_output` 为空 |
| 开启 + 非白盒 + 人行道 + 低风险 | `final_spoken_output` 非空，白盒字段齐全 |
| 开启 + 高风险 | `output_suppressed_by_risk=true`，普通导航不外显，白盒仍完整 |
| `risk_interrupt_preempt=True` | 与高风险一致压制；`risk_summary.risk_interrupt_preempt` 为 true |

单元级行为仍由 `tools/test_sidewalk_nav_v1.py` 覆盖。

## 与 risk_interrupt_v1 的关系

- 本旁路**不** import `risk_interrupt_v1`。
- 当主线已判定风险打断需抢占时，应对 `evaluate_sidewalk_nav_v1` 传入 `risk_interrupt_preempt=True`，使人行道导航不外显。
- 风险摘要中 `risk_level` 为 `high` / `critical` 时，本模块也会压制导航提示；与抢占标记二选一或同时满足时均为压制。

## 未做项

- 未接入真实 dispatcher / 运行时 import；仅为**边缘载体**验证。
- 未做端到端 TTS / 设备联调。

## 一句话收束

`sidewalk_nav_v1` 已从「模块可跑」推进到「可按主链 metadata 形态挂载、默认关闭零侵入、可验证压制与白盒」；更深接入应在统一输出裁决层按需合并键值。

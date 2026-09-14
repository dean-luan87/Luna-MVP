# retail_find_item_v1：主线边缘集成说明（V1）

## 目的

在**不改主链默认行为**的前提下，验证 `retail_find_item_v1` 能以与主链输出一致的最小 `metadata` 为载体完成挂载：默认零侵入、开启时可合并白盒、whitebox-only 时只留痕不外显、高风险或 `risk_interrupt_preempt` 时压制零售找货结论、非零售环境不误触发。

## 集成口径（推荐）

1. 在产出主链结果（例如语音下发结果的 `metadata`）的**同一层**，若需启用零售找货旁路，则调用 `evaluate_retail_find_item_v1(...)`。
2. 仅当返回的 `result.metadata` 中含 `retail_find_item_v1` 时，将其 **merge** 进主链 `metadata`（与 `risk_interrupt_v1` / `sidewalk_nav_v1` 并列键；最终播报仍由统一裁决口决定）。
3. `LUNA_ENABLE_RETAIL_FIND_ITEM_V1=0` 时：不调用或忽略旁路返回值中的白盒键，主链 `metadata` 保持原样。

## 验证方式

```bash
python3 tools/test_retail_find_item_v1_integration.py
```

脚本用最小 dict 模拟 `VoiceFinalTextDispatchResult.metadata`，并断言：

| 场景 | 预期 |
|------|------|
| 默认关闭 | 不挂载 `metadata["retail_find_item_v1"]`，与占位 metadata 一致 |
| 开启 + `LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY=1` | 挂载白盒；`item_match_summary` / `task_evidence` 有值（零售+意图）；`final_spoken_output` 为空 |
| 开启 + 非白盒 + 零售环境 + 找货意图 + 低风险 | `final_spoken_output` 非空，白盒字段齐全 |
| 开启 + 高风险 | `output_suppressed_by_risk=true`，零售结论不外显，白盒仍完整 |
| `risk_interrupt_preempt=true` | 与高风险一致压制；`risk_summary.risk_interrupt_preempt` 为 true |
| 开启 + 非零售环境 | 不外显结论；`gating_passed=false`，不误入零售主流程 |

模块级行为仍由 `tools/test_retail_find_item_v1.py` 覆盖。

## 与风险链的关系

- 本旁路**不** import `risk_interrupt_v1`。
- 当主线已判定风险打断需抢占时，应对 `evaluate_retail_find_item_v1` 传入风险摘要 `risk_interrupt_preempt=true`（或提供 `high/critical` 风险等级摘要），使零售找货结论不外显。

## 未做项

- 未接入真实 dispatcher / 运行时 import；仅为**边缘载体**验证。
- 未做端到端 OCR 执行与设备联调；OCR 在本旁路中仍为“补证接口位”。

## 一句话收束

`retail_find_item_v1` 已从「模块可跑」推进到「可按主链 metadata 形态挂载、默认关闭零侵入、可验证白盒与风险压制」。


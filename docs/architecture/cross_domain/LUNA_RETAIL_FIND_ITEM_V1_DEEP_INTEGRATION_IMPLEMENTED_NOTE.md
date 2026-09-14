# retail_find_item_v1：主线深联调（阶段 1 / whitebox-only）实现说明

## 改了什么

在保持 **whitebox-only** 与 **默认关闭零侵入** 的前提下，把 `retail_find_item_v1` 的白盒挂进真实主线路径：

- 从 `VoiceRuntimeContext.metadata["retail_env_summary_v1"]` 读取零售环境摘要
- 从 `VoiceRuntimeContext.metadata["find_item_intent_summary_v1"]` 读取找货意图摘要
- 复用 `VoiceRuntimeContext.metadata["risk_summary_v1"]` 作为风险压制信号来源（high/critical 或 risk_interrupt_preempt）
- 调用 `evaluate_retail_find_item_v1(...)` 生成白盒，并并入 `VoiceFinalTextDispatchResult.metadata["retail_find_item_v1"]`
- 深接入阶段写死 **不外显**：强制 `final_spoken_output=""`（即使未来误配 `WHITEBOX_ONLY=0` 也不推进真实输出候选）

## 当前优先级/压制规则（写死）

- 安全链优先：满足任一即压制
  - `risk_level in {high, critical}`
  - 或 `risk_interrupt_preempt=true`
- 压制时：`output_suppressed_by_risk=true` 且 `final_spoken_output=""`

## 改动范围

- `capabilities/voice/runtime/voice_final_text_dispatcher.py`
  - 增加单点 hook：`_maybe_attach_retail_find_item_v1_whitebox(...)`
  - 仅在 `LUNA_ENABLE_RETAIL_FIND_ITEM_V1=1` 且 `LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY=1` 时写入白盒键

## 怎么验证

```bash
python3 tools/test_retail_find_item_v1_deep_integration.py
```

覆盖：默认关闭零侵入、开启后白盒挂载、零售环境+意图时白盒字段可用、风险压制下不外显、以及 dispatch_type/notes 不被改写。

## 哪些还没做

- 不进入真实输出候选（不生成/提交 SpeechRequest）
- 不接 speaking/runtime 的真实来源
- 不做 OCR 真执行/调度（仍为补证接口位）
- 不做更深任务链联动


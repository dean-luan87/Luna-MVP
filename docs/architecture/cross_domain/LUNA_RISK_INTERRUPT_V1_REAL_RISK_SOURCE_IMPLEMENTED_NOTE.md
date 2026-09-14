# risk_interrupt_v1：真实风险摘要入口（阶段 1）实现说明

## 改了什么

在保持 **Level 1 / whitebox-only** 的前提下，把风险摘要来源从“仅 `event.metadata` 占位读取”升级为：

1. **优先读取**：`VoiceRuntimeContext.metadata["risk_summary_v1"]`
2. **缺失时回退**：`VoiceInputEvent.metadata`（占位兼容）

仍然只做白盒写入，不改变任何主线输出内容/notes/dispatch_type，不触发抢占。

## 当前优先级规则（写死）

- 若 `runtime_context.metadata["risk_summary_v1"]` 为 dict，则该 dict 作为唯一风险摘要来源（不做融合）
- 否则回退到 `event.metadata` 的占位字段（兼容历史/测试）

## 改动范围

- `capabilities/voice/runtime/voice_final_text_dispatcher.py`
  - `dispatch_voice_final_text(..., runtime_context=None)` 新增可选参数
  - 风险白盒 hook `_maybe_attach_risk_interrupt_v1_whitebox(..., runtime_context=None)` 支持 context 优先读取
- `capabilities/voice/runtime/voice_input_session_manager.py`
  - `process_final_text_with_dispatch(..., runtime_context=None)` 透传到 dispatcher

## 怎么验证

```bash
python3 tools/test_risk_interrupt_v1_context_source_integration.py
```

覆盖：

- 默认关闭零侵入
- context 有值时，白盒 risk_level 来自 context
- context 无值时回退到 event.metadata
- 两者同时存在时，context 优先
- `dispatch_type/notes` 不被改写

## 哪些还没做

- 不做 Level 2 抢占
- 不接 speaking/runtime 的真实来源（仍为可观测替代）
- 不做多来源融合/编排


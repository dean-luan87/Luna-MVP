# retail_find_item_v1：实现说明（V1）

## 实现了什么

- 旁路模块：`capabilities/cross_domain/retail_find_item_v1/`
  - `evaluate_retail_find_item_v1(...)`：零售环境初判（规则占位）、gating、找货意图对齐、OCR 触发决策（仅决策与摘要接入）、最小结论候选、白盒 `metadata["retail_find_item_v1"]`
- 安全压制：高风险（`high/critical`）或 `risk_interrupt_preempt` 时，`output_suppressed_by_risk=true` 且不外显找货结论
- 模块验证脚本：`tools/test_retail_find_item_v1.py`
- 主线边缘集成验证：`tools/test_retail_find_item_v1_integration.py`（说明见《`LUNA_RETAIL_FIND_ITEM_V1_INTEGRATION_NOTE.md`》）

## 默认怎么关

- `LUNA_ENABLE_RETAIL_FIND_ITEM_V1` 未设置或 `0`：**不写入** `metadata["retail_find_item_v1"]`，主链零侵入（旁路未被上层调用时同样不生效）

## whitebox-only（建议默认）

- `LUNA_ENABLE_RETAIL_FIND_ITEM_V1=1`
- `LUNA_RETAIL_FIND_ITEM_WHITEBOX_ONLY=1`（默认 true）
- 行为：只留白盒（含 gating、OCR 触发原因、OCR 摘要、最小匹配摘要、task_evidence），`final_spoken_output` 为空，不外显结论

## 怎么验证

```bash
python3 tools/test_retail_find_item_v1.py
python3 tools/test_retail_find_item_v1_integration.py
```

覆盖：默认关闭、非零售环境、零售+意图 whitebox-only、零售+意图可外显、以及高风险压制；集成脚本额外验证向主链式 `metadata` 合并时的字段与零侵入。

## 与风险链的关系

- 本模块只读风险摘要，用于“外显压制”，不生成风险事件
- 安全链优先：当上层判定风险抢占时，应将 `risk_interrupt_preempt=true`（或提供 `high/critical` 风险等级摘要）使本模块不外显找货结论

## 哪些还没做

- 未接入真实 OCR 执行（本模块只给触发决策与摘要接入接口位）
- 不做复杂找货规划/比价/支付/购物车/长文本 OCR/多模融合
- 未做端到端 dispatcher/TTS/OCR 设备联调；集成验证仍为**边缘载体**口径（模拟主链 metadata）


# unified env 最小接线实验实现说明（V1）

## 实现了什么

在主线 `dispatch_voice_final_text` 中新增一段**可开关**的“只读补缺 + 独立留痕”逻辑：

- 仅在 `LUNA_ENABLE_UNIFIED_ENV_MIN_WIRING_V1=1/true/yes` 时生效（默认关闭）
- **不回写** `sidewalk_env_summary_v1` / `retail_env_summary_v1`
- **不触碰** `risk_summary_v1` / `find_item_intent_summary_v1` / `ocr_summary_v1`
- **不驱动** 分流/决策/输出
- 仅写入独立键：`runtime_context.metadata["unified_env_fill_shadow_v1"]`

该键记录本轮补缺尝试的结果（是否补、补了哪些白名单字段、为何被阻断等），用于后续窗口评估 effective/ineffective fill。

## 接入点在哪

- `capabilities/voice/runtime/voice_final_text_dispatcher.py`
  - `_unified_env_min_wiring_enabled_v1()`
  - `_maybe_attach_unified_env_fill_shadow_v1(...)`
  - `dispatch_voice_final_text`：在
    - sidewalk/retail 稳定化之后
    - unified shadow 之后
    - orchestrator 之前
    写入 `unified_env_fill_shadow_v1`

## 白名单字段（仅记录，不回写）

只允许尝试补缺以下字段（且只在目标垂直 summary 缺失时才会出现在 `filled_fields`）：

- `summary_freshness`
- `ttl_ms`
- `confidence_weight`
- `age_ms`
- `inference_notes`

## 阻断条件（更保守）

任一满足则不补，并在 `fill_blocked_reason` 留痕：

- `missing_unified_shadow`
- `target_summary_missing`
- `family_candidate_mismatch`
- `target_has_value:<field>`
- `unified_missing:<field>`

## 如何验证

```bash
python3 tools/test_unified_env_min_wiring_v1.py
```

覆盖：

- 开关关闭时不写 `unified_env_fill_shadow_v1`
- 开关开启时写入补缺尝试记录（通常因垂直已具备字段而阻断）
- family/candidate 不一致时强制阻断
- 不改写垂直 summary，不触碰 risk/intent/OCR

## 仍未做什么（按边界）

- 不回写垂直 summary（即不做真实补缺落地）
- 不做自动 effective/ineffective 评审（留给窗口分析）
- 不扩大白名单字段

## 一句话收束

最小接线实验已落成“只读补缺 + 独立留痕”，默认关闭；下一步用真实窗口统计 `unified_env_fill_shadow_v1` 发生率与阻断原因，再决定是否值得进一步推进补缺落地或扩大范围。


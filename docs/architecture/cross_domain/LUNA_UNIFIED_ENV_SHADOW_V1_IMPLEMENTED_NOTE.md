# unified env shadow V1 实现说明

## 接了什么

- 在 `dispatch_voice_final_text` 中，于 **sidewalk / retail 环境稳定化之后**、**长度分流与旁路编排之前**，若开关开启，则 **只读** 调用 `build_unified_env_summary_v1(...)`，将结果写入 **`VoiceRuntimeContext.metadata["unified_env_summary_shadow_v1"]`**。
- **不**回写 `sidewalk_env_summary_v1`、`retail_env_summary_v1`，**不**读改 `risk_summary_v1`、`find_item_intent_summary_v1`、`ocr_summary_v1`。
- 旁路与 orchestrator **不**消费该 key；行为与未开启 shadow 时一致（仅多一段 metadata）。

## 写入路径在哪

- `capabilities/voice/runtime/voice_final_text_dispatcher.py`
  - `_unified_env_shadow_enabled_v1()`
  - `_unified_shadow_raw_inputs_v1(...)`（从现有 metadata **只读**推导 unified 输入）
  - `_maybe_attach_unified_env_shadow_v1(...)`
  - `dispatch_voice_final_text` 内紧接两段 `_maybe_stabilize_runtime_context_*` 之后调用

## 开关

- **`LUNA_ENABLE_UNIFIED_ENV_SHADOW_V1`**：未设置、`0`、`false`、`no` → **不计算** shadow（零侵入）；`1` / `true` / `yes` → 写入 shadow。

## 如何验证

```bash
python3 tools/test_unified_env_shadow_v1.py
```

（可选）继续跑既有主线回归脚本，确认默认关 shadow 时行为不变。

## 对照观察脚本（V1）

```bash
python3 tools/analyze_unified_env_shadow_v1.py
# 或指定输出目录 / 回放 JSONL：
# python3 tools/analyze_unified_env_shadow_v1.py --output-dir logs --input-jsonl path/to/rows.jsonl
```

默认将报告写入 `logs/`（若不可写则回退到 `logs_analyze_unified_shadow_v1/` 或当前目录下 `analyze_unified_env_shadow_out/`）；也可用环境变量 `LUNA_UNIFIED_SHADOW_ANALYZE_OUT`。

## 当前仍未做什么

- **不**用 shadow 驱动任何 gating、旁路或真实输出。
- **不**替代现有垂直 summary，**不**做派生接线。
- **不**做一致率统计、分析器或自动报告（见《[LUNA_UNIFIED_ENV_SHADOW_EXPERIMENT_PLAN_V1.md](./LUNA_UNIFIED_ENV_SHADOW_EXPERIMENT_PLAN_V1.md)》后续步骤）。

## 一句话收束

unified env 已以 **shadow** 形式进入主线 **观察面**（可算、可记、可对照），默认关闭；是否做 **最小接线实验** 仍由后续对照数据决定。

# M3 长短语音分档 Benchmark 结果附录

## 如何生成数据

```bash
cd /path/to/Luna-Core
export LUNA_EXTERNAL_LLM_PROVIDER=qwen
export DASHSCOPE_API_KEY='你的完整百炼Key'   # 禁止沿用文档里的字面量 '...'，否则会 401 全程无效
python3 tools/benchmark_long_voice_length_complexity_matrix_m3.py
```

- 产物：`logs/benchmark_long_voice_length_complexity_matrix_m3_<timestamp>.json`
- **50 次模型调用**（25 case × plus + turbo），注意配额与耗时。
- 校验 case：`python3 tools/benchmark_long_voice_length_complexity_matrix_m3.py --dry-run`

### 无效跑批识别

- 若 **`json_rate` 全为 0** 且日志大量 **`401 InvalidApiKey`**：本次结果**不得**写入分档结论；先修复 Key（与 smoke 成功时同一套 `export`）。
- JSON 产物中 **`model_json_effective`: false** 时，附录 D/E/F 仅填「本次无效，待重跑」。

---

## A. 全局汇总（运行后从 JSON 的 `global_plus` / `global_turbo` 填入）

| 指标 | qwen-plus | qwen-turbo |
|------|-----------|------------|
| json_rate | _待填_ | _待填_ |
| val_rate | _待填_ | _待填_ |
| fallback_rate | _待填_ | _待填_ |
| avg_e2e_ms | _待填_ | _待填_ |
| p95_e2e_ms | _待填_ | _待填_ |

---

## B. 按时长档汇总（从 JSON `agg_by_length_plus` / `agg_by_length_turbo` 摘取）

| 档 | plus json/val/fb | plus avg_e2e | turbo json/val/fb | turbo avg_e2e | 备注 |
|----|------------------|--------------|---------------------|---------------|------|
| L1 | | | | | |
| L2 | | | | | |
| L3 | | | | | |
| L4 | | | | | |
| L5 | | | | | |

**观察**：从哪一档开始 turbo 的 json/val 明显低于 plus，或 heuristic 误判率上升。

---

## C. 按复杂度档汇总（从 `agg_by_complexity_*` 摘取）

| 档 | plus json/val/fb | turbo json/val/fb | mixed_hit（若有） | mis_unsup | multistep_flat |
|----|------------------|-------------------|-------------------|-----------|----------------|
| C1 | | | — | | |
| C2 | | | — | | |
| C3 | | | | | |
| C4 | | | — | | |
| C5 | | | — | | |

---

## D. 核心问题（须明确回答）

1. **在哪个时长档内，qwen-turbo 足以承担执行链任务？**  
   _待填（结合 L1–L5 表与 C1–C2 稳定性）。_

2. **从哪个时长档或复杂度档开始，必须切到 qwen-plus？**  
   _待填。_

3. **哪些类型的输入不值得直接进重模型？**  
   _待填（对齐 C5 与 pre-filter 设计）。_

4. **现有主选 / 备选在不同档位的性价比边界？**  
   _待填（延迟 vs val/json vs token）。_

---

## E. 分档规则建议（草案，与 Pre-Filter 衔接）

> 以下为**示例模板**，须用实测数替换；不得未跑 benchmark 即当作真值。

- **可优先 turbo（示例）**：L1–L2 且 C1–C2，且 turbo `val_rate≥0.95`、heuristic 误判率可接受。  
- **优先 plus（示例）**：L3+ 或 C3–C5，或 turbo `mixed_hit` / `mis_unsup` / `multistep_flat` 显著劣于 plus。  
- **倾向规则 / reject（示例）**：C5 且 unsupported 语义应拒绝时，避免先上大模型（见 Pre-Filter `route_to_rule_or_reject`）。

---

## F. 最终一句结论（三类择一）

将 JSON 中 `verdict_hint` 与人工复核结合后，**只选其一**：

1. **已足够支撑进入「简单走 turbo、复杂走 plus」的分档设计阶段**  
2. **结论仍不够清晰，需要补更多矩阵 case**  
3. **当前还不适合进入分档设计阶段**  

**本轮定稿**：_待跑 benchmark 后填写。_

---

## 相关文档

- Case 矩阵：`LUNA_VOICE_LONG_VOICE_LENGTH_COMPLEXITY_CASE_MATRIX_M3.md`
- Pre-Filter 设计：`LUNA_VOICE_PREFILTER_LAYER_MIN_DESIGN_M3.md`
- 脚本：`tools/benchmark_long_voice_length_complexity_matrix_m3.py`

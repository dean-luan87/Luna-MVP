# M3.5.4a mixed 边界专项验证 — 附录（跑完填写）

> 承接 `M3.5.4`：day 段 mixed 已触发 `mixed_preserve_below_min`，因此只做专项验证，不改骨架/不改 prefilter/prompt。
>
> 目标回答：掉档是否可复现、是否主要在 day、non_task_payload 是否缺失、mixed 关键词是否未完整落槽、以及与 turbo/plus 是否强相关。

---

## 约束

1. **必须显式开关**：`LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1`
2. **不得默认开启**：不得把专项验证口径等同于主产品默认已上分档。
3. **不改骨架/不改规则**：benchmark 只增强观测字段，不动 `prefilter_v0` / prompt / schema / validator / builder / fallback 语义。

---

## 执行范围

| 项 | 值 |
|----|-----|
| Case 集 | `configs/voice/voice_prefilter_routing_real_cases_m3_5_4a.json`（2 条：`C1` / `C7`） |
| 每时段轮数 | （建议 15～30；默认脚本 `--rounds=20`） |
| `--time-slot` | `all`（day + night）或分别跑 |
| 超时 | `LUNA_QWEN_MODEL_TIMEOUT_MS=120000` |
| 产物 JSON | `logs/benchmark_prefilter_routing_m3_5_4a_<UTC>.json` |

运行示例：

```bash
cd /path/to/Luna-Core
export LUNA_EXTERNAL_LLM_PROVIDER=qwen
export DASHSCOPE_API_KEY=...
python3 tools/benchmark_prefilter_routing_m3_5_4a.py --rounds 20 --time-slot all
```

---

## 只回答这 5 个问题（来自脚本 mixed_boundary_summary）

1. 掉档是否可复现（看 `missing_round_indices_any` / `missing_round_indices_all` 是否跨多个 round）
2. 是否主要发生在 day（看 day/night 各自的 `n_any_missed`、`n_all_missed`）
3. non_task_payload 是否缺失（看 `n_non_task_payload_missing`）
4. mixed 关键词是否未完整落槽（看 `missing_keywords_all`）
5. 是否与路由模型强相关（看 `fail_by_routing_model` 里各 `routing_suggestion|selected_provider_model_id` 的 missed 计数）

---

## 结果表（从 JSON 摘录）

### 1) per_case_per_slot（只填关键信息）

| case_id | slot | n | any_preserved | any_missed | all_preserved | all_missed | non_task_payload_missing |
|---------|------|---|----------------|-------------|---------------|------------|----------------------------|
| C1_mixed_nav | day | 20 | 20 | 0 | 20 | 0 | 0 |
| C1_mixed_nav | night | 20 | 20 | 0 | 20 | 0 | 0 |
| C7_mixed_sleep_park_nav | day | 20 | 19 | 1 | 19 | 1 | 0 |
| C7_mixed_sleep_park_nav | night | 20 | 17 | 3 | 17 | 3 | 0 |

### 2) 缺失关键词（missing_keywords_all）

| case_id | slot | missing_keywords_all |
|---------|------|------------------------|
| C1_mixed_nav | day | {} |
| C1_mixed_nav | night | {} |
| C7_mixed_sleep_park_nav | day | {'睡眠': 1} |
| C7_mixed_sleep_park_nav | night | {'睡眠': 3} |

### 3) 路由模型强相关性（fail_by_routing_model）

| key（routing_suggestion|selected_provider_model_id） | any_missed | all_missed |
|---|---:|---:|
| `route_to_plus|qwen-plus` | 4 | 4 |

---

## 一句话结论（三选一）

1. **情况 A：问题稳定复现** → 进入“只修 mixed 边界，不动整体骨架”
2. **情况 B：问题偶发** → 继续保持当前灰度范围，不急着改规则
3. **情况 C：观测不充分** → 需要加轮数/扩大该专项集合

**选定**：**1**

**本轮对 5 个问题的直接回答**：
1. 掉档是否可复现：**可复现**（仅 `C7_mixed_sleep_park_nav`；day=1、night=3，总共 4 次 missed）。
2. 是否主要发生在 day：**不是主要发生在 day**（night 掉档更多）。
3. non_task_payload 是否缺失：**否**（`non_task_payload_missing=0`）。
4. mixed 关键词是否未完整落槽：**是**（缺失关键词为 `'睡眠'`）。
5. 是否与路由模型强相关：**是**（miss 全部集中在 `route_to_plus|qwen-plus`）。


# M3.5.4b mixed 单点修复 — 附录（跑完填写）

> 目标：对 `C7_mixed_sleep_park_nav` 在 `route_to_plus | qwen-plus` 下稳定漏掉“睡眠”关键词的问题做**单点 prompt 增强**后的复测。
>
> 本轮只跑 `C1_mixed_nav` / `C7_mixed_sleep_park_nav`，并仅回答 mixed 边界专项的 5 个问题；不改骨架、不改路由规则。

---

## 约束

1. **必须显式开关**：`LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1`
2. **不得默认开启**：不得把专项验证口径等同于主产品默认已上分档
3. **修复范围**：仅 `qwen-plus` prompt（睡眠类非任务信息保留“睡眠”字样/核心词）；不改 prefilter / validator / builder / fallback

---

## 执行范围（建议）

| 项 | 值 |
|----|-----|
| Case 集 | `configs/voice/voice_prefilter_routing_real_cases_m3_5_4a.json`（2 条：C1/C7） |
| 每时段轮数 | **20** |
| `--time-slot` | **`all`**（day + night） |
| 超时 | `LUNA_QWEN_MODEL_TIMEOUT_MS=120000` |
| `git_head` | `051d0c6f` |
| 产物 JSON（相对路径） | `logs/benchmark_prefilter_routing_m3_5_4b_20260403T074846Z.json` |

---

## 观测问题（复用 4a 的 5 点）

1. 掉档是否可复现（跨多轮 round 的 missed 是否持续）
2. 是否主要发生在 day（day/night 各自 missed 计数）
3. `non_task_payload` 是否缺失（missing payload 是否 >0）
4. mixed 关键词是否未完整落槽（`missing_keywords_all`）
5. 是否与路由模型强相关（`fail_by_routing_model`）

---

## 结果表（从 JSON 摘录）

### per_case_per_slot（只填关键信息）

| case_id | slot | n | any_missed | all_missed | non_task_payload_missing |
|---------|------|---|-------------|------------|----------------------------|
| C1_mixed_nav | day | 20 | 0 | 0 | 0 |
| C1_mixed_nav | night | 20 | 0 | 0 | 0 |
| C7_mixed_sleep_park_nav | day | 20 | 0 | 0 | 0 |
| C7_mixed_sleep_park_nav | night | 20 | 0 | 0 | 0 |

### missing_keywords_all

| case_id | slot | missing_keywords_all |
|---------|------|------------------------|
| C7_mixed_sleep_park_nav | day | {} |
| C7_mixed_sleep_park_nav | night | {} |

### fail_by_routing_model

| key（routing_suggestion|selected_provider_model_id） | any_missed | all_missed |
|---|---:|---:|
| route_to_plus|qwen-plus | 0 | 0 |

---

## 一句话收束（三选一）

1. 修复成功：C7 的“睡眠”稳定不再漏；mixed_preserve_rate >= 0.95
2. 部分成功：有所改善但仍偶发漏；继续专项迭代
3. 未成功：漏仍稳定复现或硬指标退化；需要回到 prompt/约束差异排查

**选定**：<!-- 1 / 2 / 3 -->

**本轮硬指标**：aggregate `mixed_preserve_rate = 1.0`；`json_rate = 1.0`；`val_rate = 1.0`；`fallback_rate = 0.0`；day/night `pause_stop_expand_gray = false`。

**建议选定**：**1**（修复成功）。


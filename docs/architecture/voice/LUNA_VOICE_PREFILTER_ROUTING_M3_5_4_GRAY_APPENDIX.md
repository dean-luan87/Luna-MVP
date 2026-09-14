# M3.5.4 继续扩大显式开关灰度 — 附录（跑完填写）

> 承接 M3.5.3 封板结论：在 **显式开关、非默认开启** 前提下继续扩观测强度；**不改** prefilter、prompt、schema、validator、builder、fallback 语义；**不切** qwen3.6 主线替换；**不接** DeepSeek/豆包。

---

## 约束（与结论绑定）

1. **必须显式开关**：`LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1`（按进程/环境注入）。
2. **不得默认开启**：不得表述为「主产品默认已启用分档路由」。

---

## 执行范围（建议）

| 项 | 值 |
|----|-----|
| Case 集 | `configs/voice/voice_prefilter_routing_real_cases_m3_5_3.json`（25 条） |
| 每时段轮数 | **15** |
| `--time-slot` | `all`（day + night） |
| 超时 | `LUNA_QWEN_MODEL_TIMEOUT_MS=120000` |
| 总请求数 | **750**（25 × 15 × 2） |
| 模型路由子集（aggregate） | **570** |
| `git_head` | `051d0c6f` |
| aggregate UTC | **2026-04-03T06:17:28Z** ~ **2026-04-03T07:04:22Z**（duration ≈ **2814.1s**） |
| day 段 | **2026-04-03T06:17:28Z** ~ **2026-04-03T06:40:26Z**（≈ **1059.4s**） |
| night 段 | **2026-04-03T06:40:26Z** ~ **2026-04-03T07:04:22Z**（≈ **1053.1s**） |
| 产物 JSON（相对路径） | `logs/benchmark_prefilter_routing_m3_5_4_20260403T070422Z.json` |

```bash
cd /path/to/Luna-Core
export LUNA_EXTERNAL_LLM_PROVIDER=qwen
export DASHSCOPE_API_KEY=...
python3 tools/benchmark_prefilter_routing_m3_5_4.py --rounds 15 --time-slot all
```

---

## 重点盯盘（仅四件事）

| # | 指标 | 说明 |
|---|------|------|
| 1 | `mixed_preserve_rate` | 是否持续 **高于** 默认阈值 **0.95**（相对 M3.5.3） |
| 2 | `rule_or_reject_ratio` | 是否相对 ~0.24 **异常抬升**（区分样本 vs 前置过严） |
| 3 | `p95_e2e_ms` | 是否仍处于可接受区间（对照 M3.5.3 ≈ 7.67s aggregate） |
| 4 | **mixed 失败 case** | 本轮 mixed 掉档的 case 实际出现在 **`C1_mixed_nav`、`C7_mixed_sleep_park_nav`**；**`C2_mixed_health_nav` 没有再次掉档（作为对照）** |

---

## 结果表（从 JSON 摘录）

### 硬指标（aggregate）

| 指标 | 值 |
|------|-----|
| json / val / fallback（model_routes） | `json_rate=1.0`、`val_rate=1.0`、`fallback_rate=0.0` |
| mixed_preserve_rate | **0.9555555555555556** |

### 性能

| 项 | day | night | aggregate |
|----|-----|-------|-----------|
| avg_e2e_ms | 3675.1947 | 3828.7326 | **3751.9636** |
| p95_e2e_ms | 7750.0962 | 8058.446 | **7950.1121** |

### 其他

| 项 | 值 |
|------|-----|
| rule_or_reject_ratio | **0.24**（rule_or_reject_count=180） |
| timeout_hint_count | **0** |
| pause_stop_expand_gray（aggregate） | **false** |
| pause_stop_expand_gray（day/night） | day **true**（触发 `mixed_preserve_below_min`），night **false** |
| mixed_preserved=false 行级归因 | 共 **4** 条：`C1_mixed_nav`（day×2）、`C7_mixed_sleep_park_nav`（day×1、night×1） |
| `C2_mixed_health_nav` 对照 | 本轮 mixed_preserved 统计为 **全部命中（无掉档）** |

---

## 一句话结论（三选一）

1. 可继续扩大显式开关灰度范围  
2. 当前灰度范围可维持，但不建议继续扩大  
3. 灰度扩展出现风险，应暂停推进  

**选定**：**2**  

**依据（一句）**：hard 指标与 timeout 均全绿，但 **day 段 mixed_preserve_rate 掉到 0.9333 (<0.95) 触发 pause_stop**，说明继续扩灰需更谨慎，把混合相关 case（C1/C7）作为重点观测并避免盲目翻倍。  


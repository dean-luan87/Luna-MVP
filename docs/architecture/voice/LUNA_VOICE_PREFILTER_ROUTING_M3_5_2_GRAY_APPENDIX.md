# M3.5.2 显式开关灰度扩展 — 附录（仅本轮结果）

> 不重复 M3.5.1 结论；本文只记录 **M3.5.2 扩量灰度** 的执行范围与观测结果。  
> **day / night** 为同一脚本的**审计标签**（时段覆盖），不改变 prefilter 规则与主链逻辑。

---

## A. 执行范围

| 项 | 值 |
|----|-----|
| Case 集 | `configs/voice/voice_prefilter_routing_real_cases_m3_5_2.json`（20 条） |
| 每时段轮数 `--rounds` | **7** |
| 时段 `--time-slot` | **`all`**（day → night 顺序各跑满） |
| 总请求数 | **280**（20 cases × 7 rounds × 2 slots） |
| 显式开关 | `LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1` |
| 超时 | `LUNA_QWEN_MODEL_TIMEOUT_MS=120000` |
| `git_head` | `051d0c6f` |
| 整段 UTC | **2026-04-03T03:49:11Z** ~ **2026-04-03T04:04:38Z**（aggregate `duration_sec` ≈ **927.6s**） |
| day 段 | **2026-04-03T03:49:11Z** ~ **2026-04-03T03:56:45Z**（≈ **454.3s**） |
| night 段 | **2026-04-03T03:56:45Z** ~ **2026-04-03T04:04:38Z**（≈ **473.2s**） |
| 产物 JSON（相对路径） | `logs/benchmark_prefilter_routing_m3_5_2_20260403T040438Z.json` |

**运行示例**：

```bash
cd /path/to/Luna-Core
export LUNA_EXTERNAL_LLM_PROVIDER=qwen
export DASHSCOPE_API_KEY=...
python3 tools/benchmark_prefilter_routing_m3_5_2.py --rounds 7 --time-slot all
```

---

## B. 硬指标（aggregate）

| 指标 | 值 |
|------|-----|
| `n_total` | 280 |
| `n_model_routes` | 210 |
| json_rate（model_routes） | **1.0** |
| val_rate（model_routes） | **1.0** |
| fallback_rate（model_routes） | **0.0** |
| mixed_preserve_rate | **1.0** |

与 M3.5.1 对比：**硬指标未劣化**（json/val/fallback/mixed 与 3.5.1 绿线一致）。

---

## C. 性能（分时段对比）

| 项 | day | night | aggregate |
|----|-----|-------|-----------|
| avg_e2e_ms | 3245.1576 | 3379.797 | **3312.4773** |
| p95_e2e_ms | 7156.0151 | 7642.8781 | **7583.7741** |

night 标签下略慢，属正常波动量级；**无 timeout_hint**（见下节）。

---

## D. 路由分布（aggregate；day/night 各段与 aggregate 成比例相同）

| 项 | 值 |
|------|-----|
| route_counts | turbo **168**，plus **42**，rule_or_reject **70** |
| rule_or_reject_ratio | **0.25**（未触发默认阈值 0.35） |
| rule_or_reject_count | **70** |
| complex_bucket_routed_turbo_count（出现次数，含多轮） | **98**（7 个 case × 7 轮 × 2 时段；去重 case：**C3、C4、C5、L1、L2、B1、B2**） |
| selected_provider_model_id | `qwen-turbo` **168**，`qwen-plus` **42**，`rule_chain_only` **70** |
| backup_provider_used_count / rate | **0** / **0.0** |
| provider_switch_reason_counts | **{}**（无非空原因） |
| `pause_stop_expand_gray`（aggregate 与 day/night） | **false** |

---

## E. 风险点

| 主题 | 观察记录 |
|------|----------|
| timeout | aggregate **`timeout_hint_count`: 0**；扩量后未再现 M3.5.1 前那种 2s 误伤模式。 |
| complex→turbo | 仍为 **C3/C5/L1/L2 + 边界 B1/B2 + C4** 等组合；**val/fallback/mixed 未掉档**，与「设计允许为主」的 3.5.1 复核一致。 |
| rule_or_reject | 占比 **25%**；样本含 5 条 R*，占比上升主要来自**用例设计**，非异常飙升。 |

---

## F. 一句话结论（三选一）

在硬指标不退化、`pause_stop_expand_gray = false`、路由分布可接受的前提下，只选一项：

1. **可继续扩大显式开关灰度范围**
2. **当前灰度范围可维持，但不建议继续扩大**
3. **灰度扩展出现风险，应暂停推进**

**选定**：**1**

**依据（一句）**：aggregate 硬指标全绿、分时段 pause 均未挡扩灰、timeout/主备切换无异常，满足「更大样本下骨架仍稳定」的验收口径；本轮为**扎实通过**（280 总条、210 模型路由子集），非边缘过线。

**边界声明（与结论绑定，不得省略）**：

- 后续扩灰仍须 **`LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1` 显式开启**（按环境/进程注入），**不得默认打开**。
- **主产品线默认行为不变**：未显式开开关时，不得把本灰度结论等同于「已全量上线分档路由」。

---

## G. M3.5.3 更大范围显式开关灰度（建议，尚未执行）

**只做扩面，不做改骨**：仅扩大 **轮数 / 场景覆盖 / 运行时段（审计标签）**；**不同步**改 prefilter、prompt、schema、validator、builder、fallback 语义，不切 qwen3.6 主线替换，不接 DeepSeek/豆包。

**重点盯盘**：

- `rule_or_reject_ratio` 是否异常抬升（区分样本变更 vs 前置过严）。
- `complex_bucket_routed_turbo` 是否伴随 val↓、fallback↑、mixed 掉档或明显语义问题。
- `p95_e2e_ms` 是否随扩量持续抬高。
- `mixed_preserve_rate` 是否仍能稳住。

**已落地执行入口**：`tools/benchmark_prefilter_routing_m3_5_3.py`（默认 case 集 `voice_prefilter_routing_real_cases_m3_5_3.json`，默认 `--rounds 12`）；结果附录模板见 `docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_3_GRAY_APPENDIX.md`。

---

**安全提示**：若在终端或聊天记录中粘贴过 `DASHSCOPE_API_KEY`，请在阿里云控制台**轮换/作废**该密钥，并改用环境变量或私密配置注入，避免泄露。

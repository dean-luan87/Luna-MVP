# M3.5.3 更大范围显式开关灰度 — 附录（本轮已跑）

> 承接 `LUNA_VOICE_PREFILTER_ROUTING_M3_5_2_GRAY_APPENDIX.md` §G：**只扩轮数 / 样本 / 分时段审计标签**；不改 prefilter、prompt、schema、validator、builder、fallback；不切 qwen3.6 主线替换；不接 DeepSeek/豆包。

---

## 约束（与结论绑定）

1. **必须显式开关**：仅在本进程/目标环境中 `LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1`。
2. **不得默认开启**：不得将本灰度表述为「主产品默认已启用分档路由」。

---

## M3.5.3 状态（封板）

- **扩量灰度继续通过**：**600** 条规模（**456** 条模型路由子集）。
- **硬指标全绿（model_routes 子集）**：`json_rate = val_rate = 1.0`，`fallback_rate = 0.0`；`pause_stop_expand_gray = false`（未触发暂停扩灰条件）。
- **timeout 不是当前问题**：`timeout_hint_count = 0`，`LUNA_QWEN_MODEL_TIMEOUT_MS=120000` 下未再现主矛盾。
- **路由占比稳定**：`rule_or_reject_ratio = 0.24`，与 M3.5.2（≈0.25）**同量级**，未见异常抬升。
- **延迟可接受**：aggregate `avg_e2e_ms ≈ 3521`，`p95_e2e_ms ≈ 7671`（较 M3.5.2 略升，属合理波动）。
- **mixed 有单点轻微波动，未构成阻断**：aggregate `mixed_preserve_rate ≈ 0.986`；仍 **> 0.95**，未触发 `mixed_preserve_below_min`。
- **可继续扩大显式开关灰度范围**（结论选 **1**）；**默认主链仍保持不变**（未默认开启分档）。
- **下一步不因单点回头改 prefilter / prompt（亦不改 prefilter 规则本身）**：见「观测项」。

---

## 观测项（非阻断）：`C2_mixed_health_nav`

本轮 **仅 1 条** mixed 行 `mixed_preserved=false`（**day** 时段、**C2** 某一回合）；**night** 侧 mixed 仍为 **1.0**；**未触发** `mixed_preserve_below_min`（阈值 **0.95**）。属 **模型输出方差 / 非任务片段覆盖** 类问题，**不作为阻断项**。

**后续扩灰建议**：将 **C2** 单独列为 **mixed 盯盘样本**（是否在多轮中重复掉档）；**不要**因这一条在现阶段重改 prefilter 或 prompt。

---

## 执行范围

| 项 | 值 |
|----|-----|
| Case 集 | `configs/voice/voice_prefilter_routing_real_cases_m3_5_3.json`（**25** 条） |
| 每时段轮数 | **12** |
| `--time-slot` | **`all`**（day → night） |
| 总请求数 | **600**（25 × 12 × 2） |
| 模型路由子集（aggregate） | **456** |
| 超时 | `LUNA_QWEN_MODEL_TIMEOUT_MS=120000` |
| `git_head` | `051d0c6f` |
| aggregate UTC | **2026-04-03T05:31:27Z** ~ **2026-04-03T06:06:39Z**（`duration_sec` ≈ **2112.6s**） |
| day 段 | **2026-04-03T05:31:27Z** ~ **2026-04-03T05:49:06Z**（≈ **1059.4s**） |
| night 段 | **2026-04-03T05:49:06Z** ~ **2026-04-03T06:06:39Z**（≈ **1053.1s**） |
| 产物 JSON（相对路径） | `logs/benchmark_prefilter_routing_m3_5_3_20260403T060639Z.json` |

---

## 只盯四件事（本轮对照）

| # | 指标 / 主题 | 本轮观察 |
|---|-------------|----------|
| 1 | `rule_or_reject_ratio` | **0.24**（6 条 R* / 25 cases，与 M3.5.2 的 0.25 同量级，**未异常抬升**） |
| 2 | complex → turbo | **val=1.0、fallback=0**；`review.complex_bucket_routed_turbo` 非空属预期（设计允许为主），**未见质量断崖** |
| 3 | `p95_e2e_ms` | aggregate **7671.43**；相对 M3.5.2（≈7583）略升，**属正常波动量级** |
| 4 | `mixed_preserve_rate` | aggregate **0.9861**（**71/72** 条 mixed 行保留命中）；**night=1.0**，**day=0.9722**（**35/36**）。**仍高于**脚本默认阈值 **0.95**，`mixed_preserve_below_min` **false** |

**mixed 掉点说明（可复核）**：全量 600 条中仅 **1** 条 mixed 行 `mixed_preserved=false`，出现在 **`day` × `C2_mixed_health_nav` 某一回合**；非任务片段未同时覆盖 case 中全部关键词属**模型输出方差**，不是路由开关逻辑错误。

---

## A～F 结果表

### 硬指标（aggregate）

| 指标 | 值 |
|------|-----|
| `n_total` | 600 |
| `n_model_routes` | 456 |
| json_rate（model_routes） | **1.0** |
| val_rate（model_routes） | **1.0** |
| fallback_rate（model_routes） | **0.0** |
| mixed_preserve_rate | **0.986111…** |

### 性能（day / night / aggregate）

| 项 | day | night | aggregate |
|----|-----|-------|-----------|
| avg_e2e_ms | 3531.1852 | 3510.2619 | **3520.7235** |
| p95_e2e_ms | 7729.9448 | 7606.793 | **7671.4258** |

### 路由与观测（aggregate）

| 项 | 值 |
|------|-----|
| route_counts | turbo **360**，plus **96**，rule_or_reject **144** |
| rule_or_reject_ratio / count | **0.24** / **144** |
| complex_bucket_routed_turbo_count | **192** |
| timeout_hint_count | **0** |
| backup_provider_used_count | **0** |
| pause_stop_expand_gray | **false**（day / night 均为 **false**） |

---

## 一句话结论（三选一）

1. 可继续扩大显式开关灰度范围  
2. 当前灰度范围可维持，但不建议继续扩大  
3. 灰度扩展出现风险，应暂停推进  

**选定**：**1**

**依据（一句）**：600 条规模下核心硬指标仍全绿，`pause_stop_expand_gray` 未触发；`rule` 占比稳定；mixed 仅 **1/72** 行未命中仍 **>0.95**；timeout/主备无异常。

**边界声明（重申）**：后续仍须 **显式开关**；**不得**将本结论写成「产品默认已上分档」。

---

## M3.5.4 前瞻（下一阶段）

- **仍只做扩灰观测**：显式开关、非默认开启；**不改** prefilter / prompt / validator / builder；**不切** qwen3.6 主线替换；**不接** DeepSeek/豆包。
- **执行入口**：`tools/benchmark_prefilter_routing_m3_5_4.py`（默认每时段 **15** 轮、同 **M3.5.3** case 集；`schema`: `luna.voice.gray_m3_5_4.v1`）。
- **附录模板**：`docs/architecture/voice/LUNA_VOICE_PREFILTER_ROUTING_M3_5_4_GRAY_APPENDIX.md`。
- **重点盯盘**：`mixed_preserve_rate` 是否持续在阈值上方；`rule_or_reject_ratio` 是否异常抬升；`p95_e2e_ms` 是否仍处可接受区间；**C2_mixed_health_nav** 是否出现**重复掉档**。

---

**安全提示**：勿在终端或聊天中粘贴完整 `DASHSCOPE_API_KEY`；若已泄露请**轮换密钥**。

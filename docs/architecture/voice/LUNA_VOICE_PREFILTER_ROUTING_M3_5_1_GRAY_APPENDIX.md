# M3.5.1 显式开关灰度验证 — 附录（留痕）

> 本轮只回答三件事：**是否把链路打坏**、**turbo 分流是否带来稳定收益**、**rule_or_reject 是否过严**。  
> 不做设计扩展；骨架冻结，仅验证。

## 0. M3.5.1 状态（本轮结论）

- **小范围灰度运行通过**（有效通过，非勉强过线）。
- **硬指标全绿**：`json_rate` / `val_rate` / `fallback_rate` / `mixed_preserve_rate` 均达标。
- **timeout 风险当前未构成阻断**：`LUNA_QWEN_MODEL_TIMEOUT_MS=120000`（灰度脚本在未设置环境变量时默认写入 120000）；`fallback_rate_model_routes = 0.0`。
- **存在复核项（非阻断）**：`complex_bucket_routed_turbo_nonzero: True` — 见 §5。
- **可继续在不扩功能前提下推进下一步灰度**：`pause_stop_expand_gray = false`。

**一句话收束**：prefilter 分档接入未污染主链；timeout 不是当前主矛盾；唯一需人工复核的是 complex 桶内仍路由到 turbo 的样本（设计允许 vs 规则偏松）。

---

## 1. 固定口径（写死）

| 项 | 值 |
|----|-----|
| Case 集 | `configs/voice/voice_prefilter_routing_real_cases_m3_5.json` |
| 轮数 | **3** |
| 时段（UTC） | **2026-04-03T03:29:14Z** ~ **2026-04-03T03:31:24Z**（约 130.7s） |
| `git_head` | `051d0c6f` |
| 显式开关 | `LUNA_VOICE_ENABLE_PREFILTER_ROUTING=1`（仅灰度进程/环境） |
| 模型超时 | `LUNA_QWEN_MODEL_TIMEOUT_MS=120000`（与 benchmark 对齐；未 export 时由 `tools/run_prefilter_routing_gray_m3_5_1.py` 默认写入，避免 YAML 默认 2s 误伤） |

**本阶段禁止混入**：新 prompt / 新模型 / 新规则 / 改 schema·validator·builder·fallback 定义。

---

## 2. 硬指标（必须）

| 指标 | 值 | 备注 |
|------|-----|------|
| `n_total` | 36 | 12 cases × 3 rounds |
| `n_model_routes` | 27 | 含 R* 等不走模型的路由 |
| json_rate（model_routes） | **1.0** | turbo+plus 子集 |
| val_rate（model_routes） | **1.0** | |
| fallback_rate（model_routes） | **0.0** | |
| mixed_preserve_rate | **1.0** | 有 mixed_keywords 的 case |

---

## 3. 运营指标（观察）

| 指标 | 值 |
|------|-----|
| avg_e2e_ms | 3630.1506 |
| p95_e2e_ms | 7162.367 |
| route_counts | `route_to_turbo`: 18，`route_to_plus`: 9，`route_to_rule_or_reject`: 9 |
| rule_or_reject 占比 | 0.25（低于默认阈值 0.35） |
| selected_provider_model_id 分布 | `qwen-turbo`: 18，`qwen-plus`: 9，`rule_chain_only`: 9 |

---

## 4. 暂停条件（任一条即停止扩大灰度）

本轮脚本检查结果（`pause_checks`）：

| 条件 | 是否触发 |
|------|----------|
| val_rate &lt; 1.0 | **否** |
| fallback_rate &gt; 0 | **否** |
| mixed_preserve 低于默认最小值（0.95） | **否** |
| rule_or_reject 占比过高（&gt; 0.35） | **否** |
| complex → turbo 需人工复核（`review.complex_bucket_routed_turbo` 非空） | **是（复核项，脚本不据此 pause_stop）** |

综合：`pause_stop_expand_gray` = **false**。

---

## 5. 复核项：complex_bucket_routed_turbo（非阻断）

**含义**：complex 桶内仍有样本被路由到 **turbo**，不等于「路由错误」，需区分：

- **情况 A（设计允许）**：complex ≠ 一定 plus；例如顺序型 itinerary、轻 complex、低风险多步等允许 turbo。
- **情况 B（规则偏松）**：按产品理解应进 plus 却进了 turbo → 下一步调路由边界，而非主链稳定性。

**本轮 JSON 中去重后的 case_id**（每轮均出现，共 3 轮 × 3 case）：

| case_id | routing_suggestion |
|---------|-------------------|
| `C3_ordered_itinerary_multistep` | `route_to_turbo` |
| `C4_long_constraints` | `route_to_turbo` |
| `C5_long_itinerary` | `route_to_turbo` |

**建议动作**：单独复核上述三条是否符合产品预期；若多数合理，可继续下一小步灰度。

---

## 6. 灰度结论（三选一）

选用：**1. 链路未打坏** — 硬指标稳定；预过滤路由接入未破坏原稳定链路；**有效通过**，可维持并小幅推进灰度。

**人工一句话**：M3.5.1 小范围灰度验证通过；硬指标全绿、暂停条件未挡扩灰；仅 complex→turbo 需按上表复核设计允许与否。

---

## 7. 产物路径

- 机器落盘 JSON：`logs/gray_prefilter_routing_m3_5_1_20260403T033124Z.json`（仓库根相对路径）

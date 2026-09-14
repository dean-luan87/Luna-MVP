# 三条旁路输入层成熟度复盘（V1）

## 1. 目标

在 `sidewalk_env_summary_v1` 与 `retail_env_summary_v1` 均已完成「**方案 → builder → 主线接入**」之后，对三条旁路（`risk_interrupt_v1`、`sidewalk_nav_v1`、`retail_find_item_v1`）的**上游输入层**做一次统一收口，避免后续第四条、第五条输入层各自为政。

本文件只描述**当前事实**与**可复用方法**，不展开统一环境层设计细节。

---

## 2. 三条旁路当前输入层现状（总览）

| 旁路 | 主要依赖的 runtime metadata 键 | 稳定化方案 | builder | 主线接入（dispatch 入口稳定化） | TTL / stale / ambiguous 体系 |
|------|----------------------------------|------------|---------|--------------------------------|------------------------------|
| `risk_interrupt_v1` | `risk_summary_v1`（及旁路自身事件/白盒） | 准入/试点/观察文档完备；**非**「env_summary 式」单键 builder | **无**独立 `risk_summary_v1` 稳定化 builder | **无**（风险摘要仍由上游注入） | 试点与观测链成熟；**非** sidewalk/retail 同款 summary_freshness 字段体系 |
| `sidewalk_nav_v1` | `sidewalk_env_summary_v1` | 有 | 有（`build_sidewalk_env_summary_v1`） | 有（`LUNA_ENABLE_SIDEWALK_ENV_SUMMARY_STABILIZER_V1`） | 有（`summary_freshness` + `ttl_ms` + `confidence_weight`） |
| `retail_find_item_v1` | `retail_env_summary_v1` + `find_item_intent_summary_v1` + 可选 `ocr_summary_v1` | 环境：`retail_env_summary_v1` 有；意图/OCR：**尚无**独立稳定化方案文档 | 环境：有（`build_retail_env_summary_v1`）；意图/OCR：**无** | 环境：有（`LUNA_ENABLE_RETAIL_ENV_SUMMARY_STABILIZER_V1`）；意图/OCR：**无** | 环境：有（同 sidewalk 结构）；意图/OCR：**未**纳入 |

---

## 3. 每条旁路输入层成熟度（分项）

### 3.1 risk_interrupt_v1

| 维度 | 现状 |
|------|------|
| 稳定化方案（文档） | 有：准入门槛、试点设计、观察 SOP、P0/P1 telemetry 等（**运行态与试点链**成熟） |
| builder（单键摘要稳定化） | **无**：`risk_summary_v1` 仍以上游注入为主，未采用与 sidewalk/retail 同构的 `build_*_summary_v1` |
| 主线接入 | 深接入与白盒、试点链已接主线；**非**「dispatch 前对 risk 摘要做 TTL/stale 重写」模式 |
| TTL / stale / ambiguous | **不**以 `summary_freshness` 表达；以试点观测、回退 telemetry、analyzer 等表达「可控态」 |
| 可复用性 | 模式是「**观测与开关治理**」，与 env_summary 的「时效摘要」**不同赛道**；并列为合理 |

### 3.2 sidewalk_nav_v1

| 维度 | 现状 |
|------|------|
| 稳定化方案 | 有：《[LUNA_SIDEWALK_ENV_SUMMARY_STABILIZATION_PLAN_V1.md](./LUNA_SIDEWALK_ENV_SUMMARY_STABILIZATION_PLAN_V1.md)》 |
| builder | 有：`build_sidewalk_env_summary_v1` |
| 主线接入 | 有：`dispatch_voice_final_text` 入口；开关 `LUNA_ENABLE_SIDEWALK_ENV_SUMMARY_STABILIZER_V1` |
| TTL / stale / ambiguous | 有成体系字段；默认 TTL 可 env 覆盖 |
| 可复用性 | **高**：已成为 env 输入层模板 |

### 3.3 retail_find_item_v1

| 维度 | 现状 |
|------|------|
| 稳定化方案 | **环境**：有《[LUNA_RETAIL_ENV_SUMMARY_STABILIZATION_PLAN_V1.md](./LUNA_RETAIL_ENV_SUMMARY_STABILIZATION_PLAN_V1.md)》；**意图/OCR**：仍依赖既有 dict 约定，无单独「稳定化方案 V1」文档 |
| builder | **环境**：`build_retail_env_summary_v1`；**意图**：无；**OCR**：无 |
| 主线接入 | **环境**：有；开关 `LUNA_ENABLE_RETAIL_ENV_SUMMARY_STABILIZER_V1`；**意图/OCR**：无 dispatch 前稳定化 |
| TTL / stale / ambiguous | **环境**：有；**意图/OCR**：无 |
| 可复用性 | **环境**已与 sidewalk 对齐；**意图链**仍是下一缺口 |

---

## 4. 强事实 / 弱推断分层（现状总结）

### 4.1 risk_summary_v1（risk 旁路消费）

- **强事实倾向**：需由上游风险快扫/安全链给出可追责字段时才算（具体字段以 `risk_summary_v1` 契约为准）。
- **弱推断**：任何由 ASR/启发式补全的等级或类型，必须按试点与观测规则对账，**不得**与 `sidewalk_env` / `retail_env` 互写。

### 4.2 sidewalk_env_summary_v1

- **强事实**：带来源与 `event_timestamp` 的观测（builder 输出中带 `source`、`summary_schema_version`）。
- **弱推断**：`scene_candidate`、`path_confidence`、`is_outdoor` 在管线未全时仍偏推断；由 `summary_freshness` / `confidence_weight` 降权。

### 4.3 retail_env_summary_v1

- **强事实**：同上，强调来源与时间；`gating_passed` 若由上游显式 bool 给出，可视为强断言（仍建议带 reason 枚举，后续可做）。
- **弱推断**：`retail_context_confidence`、`shelf_visible`、scene 标签；冲突时标 `ambiguous`。

### 4.4 find_item_intent_summary_v1 / ocr_summary_v1（零售链）

- **现状**：与 `retail_env_summary_v1` **并列**，**不并入**环境 builder；尚未做独立稳定化 builder，字段仍以「能传就行」为主，是**明确缺口**。

---

## 5. 当前共性方法（可复用模式）

以下模式已在 **sidewalk / retail 环境摘要**上落地，可作为后续输入层扩展的默认模板：

1. **builder 化**：`build_*_env_summary_v1(...) -> dict`，带 `summary_schema_version`。
2. **主线接入前稳定化**：在 `dispatch_voice_final_text` **最早阶段**对 `VoiceRuntimeContext.metadata` 做单键重写（`replace`），避免旁路读到未衰减的原始 dict。
3. **幂等**：已带 `summary_schema_version` 前缀则 **不重复 build**。
4. **risk 并列、不互写**：稳定化只改本摘要键；**不读、不改** `risk_summary_v1`。
5. **stale / ambiguous 纪律**：超 TTL → stale；证据不足/冲突 → ambiguous；`confidence_weight` 与年龄衰减一致化表达。

**risk_interrupt_v1** 的成熟点主要在 **试点治理与观测**，与上述「环境摘要 builder」**互补而非重复**。

---

## 6. 当前缺口（明确）

| 缺口 | 说明 |
|------|------|
| `risk_summary_v1` 单键稳定化 builder | **未做**；是否与 env 同构需单独评审（安全语义不同） |
| `find_item_intent_summary_v1` 稳定化 | **未做**（方案/builder/主线接入均无） |
| `ocr_summary_v1` 稳定化 | **未做**（仍为接口位 + 主线透传） |
| 统一环境层 | **未做**；sidewalk/retail 已为未来「派生视图」预留位置 |

**后续若要扩展**：优先复用「**方案 → builder → dispatch 入口接入 → 秒退开关**」五件套，再考虑统一环境层收口。

---

## 一句话收束

三条旁路中，**环境类输入**（sidewalk / retail）已与**同一套 builder + 主线稳定化**对齐；**risk** 在**运行态与试点观测**上最成熟；**零售意图与 OCR** 仍缺独立稳定化层。先把这一页当作后续是否做**统一环境层雏形**或**意图摘要 builder**的决策基线。

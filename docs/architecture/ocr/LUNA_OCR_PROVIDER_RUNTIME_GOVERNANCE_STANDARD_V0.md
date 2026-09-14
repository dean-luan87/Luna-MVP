# Luna OCR Provider Runtime Governance Standard v0（Phase-OCR-Provider-Runtime-Governance-Standard-001）

**副标题**：**Multi-OCR Provider Dispatch & Runtime Governance Standard v0** —— OCR 从「模型管理」上升为 **OCR 能力调度体系**：核心不是「RapidOCR / PaddleOCR 谁识别更准」，而是 **什么任务、在什么场景、以什么成本、调用哪一级 OCR、产出何种深度的证据、由谁判定可信、能否进入下一层**。禁止退化为 **「谁能识别就谁上」** 的无门控堆叠，否则一定在成本、隐私、帧率与事实污染上失控。

**定位**：Luna 体系内 **OCR 模型使用与运行治理** 的顶层标准（**design-only v0**）。适用于 **RapidOCR、PaddleOCR、轻量本地 OCR、云端 OCR、VLM OCR、YOLO 内置 OCR** 等一切 **OCR provider** 的准入与行为边界说明。  
**边界**：本标准 **不** 运行任何 OCR、**不** 改主线 routing、**不** 替换默认 provider、**不** 进入 MidPlatform / 白盒 runtime 实现；与既有 **OCR Bridge**、**evaluation OCR** 链路文档互补。调度侧唯一概念入口为 **OCR Orchestrator / OCR Runtime Controller**（命名可二选一，语义一致）。

**权威拆分**：分层与使用细则见 `LUNA_OCR_PROVIDER_LEVELS_AND_USAGE_POLICY_V0.md`；触发与 ROI 见 `LUNA_OCR_TRIGGER_GATE_AND_ROI_POLICY_V0.md`；缓存与 Scene Delta 见 `LUNA_OCR_CACHE_AND_SCENE_DELTA_POLICY_V0.md`；准入清单见 `LUNA_OCR_PROVIDER_ADMISSION_CHECKLIST_V0.md`。  
**配置样例**：`configs/ocr/ocr_provider_runtime_governance_v0.example.json`（含 **OCRRequest / OCRDispatchDecision** 字段清单与 **orchestration_policy**）。

**四控制层（摘要）**：① **调用入口** — 仅 **OCRRequest**，禁止业务直连 provider；② **系统调度** — **规则 + 状态 + 预算** 产出 **OCRDispatchDecision / OCRExecutionPlan**；③ **分级响应** — Level 0–3 各自 **延迟 / 输入 / 输出深度 / 禁止项** 不同，但一律为 **evidence**；④ **中台 / Orchestrator** — 管生命周期、ROI、缓存、Bridge、Scene Delta 候选与 TTL，**阻止** provider 直写 MidPlatform / 世界模型。

---

## 1. 背景与问题

OCR 不是「接库即上线」能力，而是一条 **触发 → ROI → 成本/缓存 → 分级 provider → 证据形态 → Bridge → 消费方 → 评测与降级** 的治理链。缺少统一标准时，易出现：**逐帧整图 OCR**、**证据当下事实化**、**绕过 Bridge 直灌业务**、**评测侧改动 routing**、**重型模型默认常驻**、**业务模块绕过调度直接选模型** 等系统性风险。本标准将上述约束 **显式化、可审计、与 provider 品牌解耦**，并把 **多 provider 并存** 下的 **准入、调度、证据合同** 固定为平台契约。

---

## 2. OCR provider 分层

必须采用 **Level 0–3** 分级（详见分级专文）。原则：**默认优先 Level 0/1**；**Level 2/3 为高成本路径**，须受触发门控、频率与异步策略约束。**任何单一实现（含 PaddleOCR）均不得默认为全帧主路径。**

---

## 3. OCR Trigger Gate

**禁止默认逐帧 OCR。** 仅当存在 **疑似文字区域** 且对 **任务 / 环境理解 / 证据采集** 有明确价值时，才允许进入 OCR 调度。Trigger Gate 的输出应是 **可审计的「允许/拒绝 + 理由 + 优先级」**，而非静默全图扫描。

---

## 4. ROI-first 输入规范

**默认禁止**将「整图实时 OCR」作为热路径。须优先使用 **检测候选框、文字区域 proposal、任务目标 ROI、用户显式选区、场景上下文裁剪** 等 **ROI 输入**；整图 OCR 仅允许在 **evaluation、低频静态、用户显式请求、受控 fallback** 等白名单场景。

---

## 5. Full-image OCR 使用限制

实时主线中：`full_image_realtime_ocr_allowed = false`（配置层默认值，见 example）。若业务确需整图，须走 **单独评审 + 成本预算 + 证据与隐私评审**，且不得与「默认同帧全图」混为一谈。

---

## 6. OCR cache / TTL / fingerprint

证据与调度层须支持（概念字段，具体 schema 由证据/Bridge 合同定义）：**roi_fingerprint、image_fingerprint、location_anchor、observed_at、ttl、stale_risk、cache_hit/cache_miss、source_provider、evidence_id**。同一 ROI、短 TTL 内内容未变化时 **不得重复跑模型**。

---

## 7. Scene Delta 联动

OCR 除文本外须支持 **「文字信息是否相对上一观测发生变化」** 的判定，以驱动 **Scene Delta / WorldContext 候选**；**不得**据此直接写入世界模型或中台事实层——仅 **候选 + 证据引用**。

---

## 8. Provider output is evidence, not fact

Provider **只产出 OCR evidence**（含置信、几何、来源链、不确定性）。**禁止**将 provider 原始拼接文本当作事实；**禁止**直写 MidPlatform 语义解释；**禁止**直写世界模型。事实准入仅能通过 **OCR Bridge / MidPlatform 证据治理 / 人工或更高层** 路径。

---

## 9. OCR Bridge 必经原则

所有进入业务消费链路的 OCR 结果，须落入 **统一 OCR evidence contract** 或 **OcrEvidencePack** 等 Bridge 合同形态。**禁止** provider 向下游业务模块 **直出原始识别结论** 或绕过 Bridge 的并行通道。

---

## 10. Runtime budget

每个 provider 须在准入材料中声明（示例字段）：**expected_latency_ms、memory_budget_mb、max_frequency、allowed_input_type、max_roi_count、max_image_size、offline_capability、fallback_policy**。系统层须有 **max_sync_latency_ms、重型异步、重模型最大频率** 等全局预算（见 `ocr_provider_runtime_governance_v0.example.json`）。

---

## 11. CPU / 内存 / 电量降级策略

在 **CPU/内存/电量/温升/帧率** 压力下：**先禁用 Level 3 → Level 2 降频/限额 → Level 1 仅高价值 ROI → Level 0 缓存复用**；必要时输出 **「当前文字识别能力受限」** 类显式降级信号，而非静默拖死帧率。

---

## 12. Heavy OCR provider 使用条件

**Level 2（重型本地 OCR，如 PaddleOCR 类）**：仅用于 **高价值、低频、复杂文本** 或 **Level 1 低置信/结构不足以决策** 的升级路径；须 **异步或严格限频**；须 **ROI 优先**；须 **完整证据与审计字段**。

---

## 13. Remote / VLM OCR 使用条件

**Level 3**：仅用于 **复杂版面、艺术字、严重遮挡、多区域归属困难、极低置信或用户明确授权**；须满足 **隐私、网络、成本、权限** 四维约束；默认在资源紧张时 **最先被禁用**。

---

## 14. Evaluation-only 与 runtime provider 的边界

**Evaluation / benchmark / shadow candidate** 产物 **不得** 改变 **runtime routing**、**不得** 替换 **RapidOCR（或当前主线默认）**、**不得** 将任一评测 provider 写为默认。进入主线须经过 **runtime shadow provider phase + release gate**（后续 phase 定义），本标准仅冻结 **治理原则**。

---

## 15. Provider admission checklist

准入须完成：分级定位、触发与 ROI 策略、预算与降级、证据与 Bridge 合同对齐、缓存键与 TTL、隐私与网络（若 Level 3）、评测与回滚预案。详见 `LUNA_OCR_PROVIDER_ADMISSION_CHECKLIST_V0.md`。

---

## 16. 禁止事项（摘要）

- 评测/试验 **改 routing**、**替换默认 provider**、**绕过 Bridge**、**直写世界模型 / MidPlatform 事实**、**默认逐帧整图 OCR**、**业务模块直连 OCR provider**（跳过 **OCR Orchestrator**）。  
- 将 **benchmark GO** 或 **评测链路 GO** 等同于 **上线许可**。  
- 在配置与文档中将 **任一重型实现** 写为 **默认 runtime 主 provider**（示例 `forbidden_actions` 显式禁止类条目）。

---

## 17. 与 PaddleOCR 当前评测结论的关系

PaddleOCR 评测链路已验证：**manifest → cache → API adapter → unified evidence → Bridge pack → consumer 静态 → benchmark** 可复现；同时暴露 **CPU 下单次推理成本高、内存占用大** 等问题。按本标准，**PaddleOCR = Level 2 Heavy Local OCR 候选**，**非默认**、**非逐帧**、**非整图实时主路径**；须与 Trigger、ROI、缓存与降级策略 **绑定治理**，而非单独优化某一模型。

---

## 18. 后续 phase 建议

1. **Runtime shadow provider phase**：在 **不改默认 routing** 前提下影子挂载与 kill switch。  
2. **Release gate**：预算、隐私、证据与回滚验收通过后，才讨论主线默认或并列策略。  
3. **多 provider 统一准入**：RapidOCR / 云端 / VLM 等重复走 **同一 checklist + governance config**。  
4. **OCR Orchestrator 实现 phase**（后续）：将本文 **OCRRequest / OCRDispatchDecision** 落实为代码路径与观测指标；仍须与本 phase「不改 routing」的边界区分。

---

## 19. Multi-OCR Provider Governance Overview

Luna 将 **同时存在** 多种 OCR provider（RapidOCR、PaddleOCR、轻量引擎、云端 OCR、VLM、设备内置等）。因此 **禁止** 以「某次 benchmark 更高分」作为业务侧选型的唯一依据；**必须** 由 **OCR Orchestrator** 在 **任务价值、时效、复杂度、资源、缓存、隐私、置信度** 下做 **统一调度**。业务模块 **不得** 直接 `import`/调用任一 OCR provider 实现；**只能** 提交 **OCRRequest**，由 Orchestrator 判定是否执行、如何执行、同步或异步、ROI 配额与降级。

---

## 20. OCRRequest Contract（调用入口合同）

**所有 OCR 意图** 必须通过 **OCRRequest** 进入系统（字段名允许 snake_case 或等价嵌套，但语义不得缺失）。**最小必填字段**：

| 字段 | 说明 |
|------|------|
| `request_id` | 幂等与追踪。 |
| `task_context` | 如 `navigation \| product_label \| medicine_label \| signboard \| document \| unknown` 等枚举扩展。 |
| `scene_context` | 场景摘要或引用（不得替代 Bridge 证据包）。 |
| `urgency` | `realtime \| near_real_time \| async \| background`。 |
| `input_type` | `full_image \| roi \| roi_list \| cached_scene_delta` 等；须与 ROI-first 总原则一致。 |
| `image_ref` | 图像句柄 / bundle ref（具体形态由 Bridge 媒体合同定义）。 |
| `roi_refs` | ROI 引用列表；可与 `roi_candidates` 并存，由 Orchestrator 裁剪为最终输入。 |
| `expected_output` | `raw_text \| structured_text \| evidence_pack \| layout_text \| semantic_candidate` 等；**仅表达期望深度**，不保证事实结论。 |
| `privacy_level` | `normal \| sensitive \| restricted`；**约束** Level 3 / remote。 |
| `latency_budget_ms` | 与全局 `max_sync_latency_ms` 联合裁剪。 |
| `allow_remote` | 是否允许 Level 3；受限隐私时须为 false。 |
| `allow_heavy_ocr` | 是否允许 Level 2；导航等热路径可强制 false。 |
| `cache_policy` | 与全局 cache 策略对齐的本次请求覆盖项（如强制 miss 仅用于评测闸门外）。 |
| `source_task_id` | 上游任务锚点，供审计与 ROI 价值判定。 |

**示例（说明性 JSON）**：

```json
{
  "request_id": "ocr_req_01",
  "task_context": "signboard",
  "scene_context": "outdoor_mall_entrance_v1",
  "urgency": "near_real_time",
  "input_type": "roi_list",
  "roi_candidates": [],
  "image_ref": "frame_bundle_ref_123",
  "roi_refs": ["roi_anchor_a", "roi_anchor_b"],
  "expected_output": "evidence_pack",
  "privacy_level": "normal",
  "latency_budget_ms": 800,
  "allow_remote": false,
  "allow_heavy_ocr": false,
  "cache_policy": "respect_global_ttl",
  "source_task_id": "task_nav_9f3c"
}
```

---

## 21. OCRDispatchDecision / OCRExecutionPlan Contract（调度结果合同）

调度输出 **不是** 裸 `provider_name` 字符串，而是一份可审计的 **OCRDispatchDecision**（可与 **OCRExecutionPlan** 合并或分层，v0 允许同一对象承载）。**最小必填字段**：

| 字段 | 说明 |
|------|------|
| `decision` | `run_ocr \| reuse_cache \| defer \| reject \| escalate`。 |
| `selected_level` | 如 `level_0` … `level_3` 与配置 `provider_levels` 对齐。 |
| `selected_provider` | 实现标识（如 `rapidocr`）；可为 null 当 `reuse_cache` / `reject`。 |
| `input_strategy` | 如 `roi_only \| roi_then_crop \| full_image_allowed_exception`。 |
| `sync_allowed` | 是否允许同步路径；重型常与 `false` 搭配。 |
| `max_roi_count` | 本次执行 ROI 上限。 |
| `fallback_provider` | 链式降级候选；须仍在 Orchestrator 控制内。 |
| `reason_codes` | 可机器解析的调度理由列表。 |
| `estimated_latency_ms` | 预估；用于拒绝或 defer。 |
| `budget_impact` | 对 CPU/内存/网络占用的结构化提示（v0 可为枚举或占位对象）。 |
| `evidence_required` | 是否必须产出完整 evidence / Bridge pack。 |

**示例（说明性 JSON）**：

```json
{
  "decision": "run_ocr",
  "selected_level": "level_1_light_local",
  "selected_provider": "rapidocr",
  "input_strategy": "roi_only",
  "max_roi_count": 3,
  "sync_allowed": true,
  "fallback_provider": "paddleocr",
  "reason_codes": ["task_relevant_text", "roi_available", "latency_budget_low", "cache_miss"],
  "estimated_latency_ms": 120,
  "budget_impact": "low",
  "evidence_required": true
}
```

**调度原则**：由 **规则 + 实时状态 + 预算** 综合决定，**禁止** 静态「某场景写死某 OCR」作为唯一逻辑；允许 **默认规则表**，但必须可被 **资源/隐私/缓存** 覆盖。

---

## 22. OCR Provider Level Response Requirements（分级响应要求）

各级 **输入 / 输出深度 / 延迟类别** 不同，但 **共同约束**：产出均为 **OCR evidence**，**不是** 业务事实；**不得** 做 MidPlatform 语义裁决；**不得** 写世界模型。

| Level | 输入侧重 | 输出侧重 | 延迟与运行形态 | 明确禁止 |
|-------|-----------|-----------|----------------|----------|
| **0** | scene / ROI fingerprint | 复用 **cached OCR evidence** 或标注 **stale candidate** | 毫秒级，不跑模型 | 伪造新观测、冒充新跑模型 |
| **1** | 小 ROI、普通横排 | `text_items`、score、basic box 等 **轻量证据** | 低延迟、可较高频；须 Trigger 门控 | 复杂版面理解、语义定案 |
| **2** | 高价值 ROI、多区域、Level 1 低置信升级 | 更丰富几何（如 polygon）、reading_order **candidate** | **低频 / 异步优先**；完整审计字段 | 逐帧默认、默认同帧整图实时、阻塞导航主链路 |
| **3** | 复杂版面、艺术字、说明书、图文混排 | layout evidence、structure **candidate**、semantic **hint** | 权限、网络、成本闸门 | 直写事实、绕过 Bridge、无授权的远程出图 |

细则与产品化表述见 `LUNA_OCR_PROVIDER_LEVELS_AND_USAGE_POLICY_V0.md`。

---

## 23. OCR Orchestrator Authority（中台 / 调度器职权）

**OCR Orchestrator（OCR Runtime Controller）** 的职责 **不是** 识别文字，而是管理 **「文字识别能力何时、以何成本、以何形态被使用」**。**必须** 由其实现或委托的唯一管道完成：

1. 接收 **OCRRequest**；  
2. 结合 Trigger Gate 判断 **是否需要 OCR**；  
3. 选择 **Level** 与 **provider**；  
4. 决定 **同步 / 异步** 与 **频率上限**；  
5. 控制 **ROI 数量与裁剪策略**；  
6. 查询 **缓存 / fingerprint / TTL**；  
7. 执行 **provider selection**（含 fallback 链，仍在 Orchestrator 内）；  
8. 收集 **OCR evidence**；  
9. **交给 OCR Bridge**（统一证据包）；  
10. 仅将符合政策的文本变化 **作为 Scene Delta / WorldContext 候选** 分流，**不** 直接写世界模型；  
11. 控制 **TTL、过期、复核**；  
12. **阻止** OCR provider **直写 MidPlatform / World Model**，并阻止 **评测 provider 写 production route**。

**与 STCM 协同（Phase-Spatiotemporal-Consistency-Manager-001）**：裁定 **OCRDispatchDecision** 时须查询 **时空间一致性管理器（STCM）** 的 **ModelCallDeadline / SpatiotemporalAnchor 有效性**；迟到或过期的 OCR 结果 **不得** 违反 STCM 规则进入可驱动用户行动的任务链（详见 `docs/architecture/midplatform/LUNA_SPATIOTEMPORAL_CONSISTENCY_MANAGER_V0.md`）。

---

## 24. Provider Admission Matrix（准入矩阵维度）

每个 provider 准入前 **必须** 在矩阵中声明（与 checklist 一致，供机器与人工审阅）：

- `provider_name`  
- `provider_level`（默认服务级别与允许升级链）  
- `supported_input_type`  
- `supported_output_depth`  
- `latency_class` / `memory_class`  
- `offline_capability`  
- `remote_dependency`  
- `privacy_risk`  
- `fallback_policy`  
- `evidence_contract_supported`  
- `bridge_pack_supported`  

未填满 **不得** 进入 runtime 候选池（evaluation-only 可单独标注）。

---

## 25. Runtime Selection Policy（运行期选型策略摘要）

**启发式规则（可被状态覆盖）**：

- **高时效 + 小 ROI** → 优先 **Level 1**。  
- **高任务价值 + Level 1 低置信** → 升级 **Level 2**（仍须 ROI / 预算）。  
- **复杂版面 / 艺术字 / 图文混排 + 已授权** → 可 **escalate** 至 **Level 3**。  
- **缓存命中且未过期、风险可接受** → **Level 0**。  
- **CPU / 电量 / 温升 / 帧率压力高** → 降级至 **Level 0/1**，关闭或推迟 Level 3，限制 Level 2。  
- **隐私敏感 / `allow_remote=false`** → **禁止 Level 3**；必要时 **reject** 或仅 **Level 0/1**。  

---

## 26. Forbidden Direct Calls（禁止直连）

**禁止** 以下调用或数据路径（与 `forbidden_actions` 配置对齐）：

- **business module → OCR provider**（跳过 Orchestrator）。  
- **OCR provider → MidPlatform**（事实或语义直写）。  
- **OCR provider → WorldModel**。  
- **OCR provider → runtime routing**（provider 不得改路由）。  
- **evaluation provider / candidate → production route**（未过 shadow + release gate）。  

**产品化定位（非本 phase 实现承诺）**：**PaddleOCR = Level 2 Heavy Local OCR**（低频、高价值、复杂 ROI、本地重型 fallback）；**RapidOCR = Level 1 Light Local OCR 候选**（小 ROI、普通文字、低成本快路径）；**VLM / 云端 = Level 3**（复杂图文，强隐私与成本约束）。

---

**一句话**：本标准将 OCR 提升为 **由 OCR Orchestrator 统一调度的、可治理的多 provider 平台能力**；**不运行 OCR、不接主线、不改 routing、不替换 RapidOCR、不进入 MidPlatform**。

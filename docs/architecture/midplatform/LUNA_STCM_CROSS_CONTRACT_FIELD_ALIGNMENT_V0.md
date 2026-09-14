# Luna STCM Cross-Contract Field Alignment v0（Phase-STCM-Contract-Field-Alignment-001）

**定位**：在 **不实装 runtime、不接 MidPlatform、不改 OCR routing、不替换 RapidOCR** 前提下，将 **STCM** 核心对象（`SpatiotemporalAnchor`、`ModelCallDeadline`、`ModelCallOutcome`、`InformationValueAssessment`）与 **OCRRequest**、**OCRDispatchDecision**、**OcrEvidencePack**、**Voice Output Governance**、**Vision / 感知信号** 侧 **既有合同字段** 做 **静态字段级对齐**（映射、缺口、语义张力）。

**输入权威**：`LUNA_SPATIOTEMPORAL_CONSISTENCY_MANAGER_V0.md`、`LUNA_MODEL_CALL_DEADLINE_AND_TIMEOUT_POLICY_V0.md`、`LUNA_INFORMATION_VALUE_AND_FALLBACK_POLICY_V0.md`、`LUNA_CROSS_MODAL_TIME_SPACE_GOVERNANCE_V0.md`、`spatiotemporal_consistency_manager_v0.example.json`、`LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md`、`ocr_provider_runtime_governance_v0.example.json`、`LUNA_OCR_EVIDENCE_PACK_CONTRACT_V0.md`、`ocr_evidence_pack_contract_v0.py`；Voice / Vision 以 **仓库内已存在文档** 为引用（见各节「引用」），**禁止伪造**不存在的合同路径。

**产物索引**：`configs/midplatform/stcm_cross_contract_field_alignment_v0.example.json`；运行 `verify_stcm_cross_contract_field_alignment_v0.py` 生成 `stcm_gap_report.json`、`stcm_conflict_report.json` 等。

---

## 1. OCRRequest → ModelCallDeadline

| OCRRequest（概念字段，见 OCR 治理 §20） | ModelCallDeadline | 对齐说明 |
|----------------------------------------|-------------------|----------|
| `request_id` | `call_id`（或 `call_id = hash(request_id+modality)` 由实现定） | 一对一追踪；须在 Outcome 中回指。 |
| `source_task_id` | `task_id` / `task_context` 子集 | 任务锚点一致。 |
| `task_context` | `task_context` | 枚举域应对齐或映射表。 |
| `urgency` | `urgency` + 推导 `deadline_class`（safety_realtime 等） | STCM `deadline_classes` 与 OCR urgency 的 **显式映射表** 须在实现 phase 冻结；v0 为设计对齐。 |
| `latency_budget_ms` | `max_latency_ms` | **同语义不同名**；取 min(`latency_budget_ms`, class_max) 作为有效 deadline 的规则须在实现中单一化。 |
| `allow_remote` | `fallback_allowed` / remote 分支授权 | 与 Level 3 / 隐私闸门联动。 |
| `allow_heavy_ocr` | `provider_level` 上限许可 | 与 OCR Level 2 许可一致。 |
| `image_ref` | `spatial_anchor_ref`（`spatial_anchor_type=visual_frame` 或 bundle） | 图像句柄进入空间锚。 |
| `roi_refs` | `spatial_anchor_ref`（多 ROI 时 anchor 可为列表或子 anchor） | 多 ROI 时 **不得** 默认同单一 anchor。 |
| `privacy_level` | `timeout_policy` 间接约束 | 高隐私可缩短有效窗或禁止 remote。 |

**引用**：`docs/architecture/ocr/LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md` §20；`configs/ocr/ocr_provider_runtime_governance_v0.example.json`（`runtime_budget.max_sync_latency_ms` 与 `latency_budget_ms` 联合裁剪）。

---

## 2. OCRDispatchDecision → ModelCallDeadline / InformationValueAssessment

| OCRDispatchDecision（§21） | ModelCallDeadline / IVAssessment | 对齐说明 |
|---------------------------|----------------------------------|----------|
| `selected_provider` | `provider_name` | 一致。 |
| `selected_level` | `provider_level` | 与 OCR level 字符串对齐（如 `level_1_light_local`）。 |
| `sync_allowed` | `urgency` + `timeout_policy` | `sync_allowed=false` 常对应 async 或延长有效评估路径。 |
| `estimated_latency_ms` | deadline 可行性 | 若 `estimated_latency_ms > (deadline_at-requested_at)` → 必须 `defer`/`reject`/`fallback`（由 STCM+Orchestrator 协同）。 |
| `fallback_provider` | `fallback_policy` / Outcome `fallback_decision` | 链式 fallback 仍须 **单次 ModelCallDeadline** 重算。 |
| `reason_codes` | `decision_reason_codes`（Outcome / 审计扩展字段） | 建议保留机器可读 codes 穿透到 STCM 事件。 |
| `evidence_required` | IVAssessment `task_dependency` / `fallback_required` | `evidence_required=true` 通常对应 `task_dependency` 非 `irrelevant`。 |
| `max_roi_count` | 资源维度；可进入 IVAssessment 派生 | 非 STCM 首字段，但影响 deadline 可达性。 |

**引用**：`LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md` §21；`LUNA_INFORMATION_VALUE_AND_FALLBACK_POLICY_V0.md`。

---

## 3. OcrEvidencePack → SpatiotemporalAnchor

| OcrEvidencePack / 证据最小字段（见 `LUNA_OCR_EVIDENCE_PACK_MINIMUM_REQUIRED_FIELDS_V0.md`） | SpatiotemporalAnchor | 对齐说明 |
|---------------------------------------------------------------------------------------------|----------------------|----------|
| `pack_id` | `anchor_id` 或 `output_ref` 子索引 | 证据包级锚点可一对多 evidence。 |
| `source_image_ref` | `spatial_anchor_ref`（+ `spatial_anchor_type`） | 设计期 `eval:*` 占位仍须可映射到 ref 字段。 |
| `source_provider_ref` | `source_module=ocr` + provider 追溯 | 填入 anchor 元数据。 |
| `source_reference_chain`（若存在于 unified evidence 对齐链） | `source_module` / ref 列表 | 与 STCM `source_module` 枚举对齐。 |
| `confidence_summary`（unified evidence 对齐） | `confidence` | 聚合规则在实现 phase 定义。 |
| 每条 evidence 的几何 / ROI（`LUNA_OCR_EVIDENCE_TYPES_V0`） | `roi_id` / polygon 绑定 | **gap**：pack 顶层无显式 `frame_id` 时须从 `source_image_ref` 或 trace 推导（见 gap 报告）。 |
| （pipeline 时间戳，若存在） | `observed_at` / `received_at` | **gap**：`ocr_evidence_pack_contract_v0.py` 骨架未含 `observed_at`；须由 **上游 trace** 或 **未来 schema minor** 提供（见 gap 报告）。 |
| TTL / 有效窗 | `valid_until` / `ttl_ms` | **gap**：pack v0 无顶层 `valid_until`；STCM 须在消费前 **外包** 计算或扩展字段。 |

**引用**：`docs/architecture/ocr_bridge/LUNA_OCR_EVIDENCE_PACK_CONTRACT_V0.md`、`docs/architecture/ocr_bridge/LUNA_OCR_EVIDENCE_PACK_MINIMUM_REQUIRED_FIELDS_V0.md`、`capabilities/ocr_bridge/ocr_evidence_pack_contract_v0.py`。

---

## 4. Voice Output Governance → ModelCallOutcome / voice_notice_policy

Voice 侧字段命名因 **governed submit / trace / TRW** 多轨并存，本 v0 **只做引用对齐**，不发明统一 ID。

| Voice 概念（多文档聚合） | ModelCallOutcome / STCM voice_notice_policy | 对齐说明 |
|-------------------------|-----------------------------------------------|----------|
| 播报请求 / trace `request_id`（见各 trace 文档） | `call_id` 或并行 `voice_notice_ref` | 追踪链对齐。 |
| `enqueue_time` / 提交时间 | `requested_at` | 进入 deadline 计算。 |
| `expires_at`（见 **Priority / Expiry / Suppression**） | `deadline_at` / `valid_until` | `now>=expires_at` → 对应 `stale_result` / 禁止播报。 |
| 过期抑制结果 | `status=cancelled` 或 `stale_result`；`voice_notice_emitted=false` | 与 STCM「过期播报不得执行」一致。 |
| 已播报 / dropped 标志（trace / replay 字段，见审计映射文档） | `voice_notice_emitted`；`result_validity` | 以具体 trace schema 为准。 |
| 输出文本引用 | `notice_message_ref` / `output_ref` | 禁止裸字符串无锚进入任务链。 |

**引用（已存在，非伪造）**：

- `docs/architecture/LUNA_VOICE_OUTPUT_GOVERNANCE_DEFINITION_V0.md`  
- `docs/architecture/LUNA_VOICE_OUTPUT_PRIORITY_EXPIRY_SUPPRESSION_POLICY_V0.md`（`expires_at`）  
- `docs/architecture/voice/LUNA_VOICE_TIME_GOVERNANCE_V1.md`（时间治理补充）  
- `docs/architecture/LUNA_VOICE_OUTPUT_GOVERNANCE_AUDIT_FIELD_MAPPING_V0.md`（审计字段映射）

---

## 5. Vision 输出 → SpatiotemporalAnchor

| Vision / 感知信号（合同侧） | SpatiotemporalAnchor | 对齐说明 |
|---------------------------|----------------------|----------|
| `timestamp_or_frame_id` / `source_frame_id` | `frame_id` + `observed_at` | 见导航感知信号合同。 |
| 检测/跟踪 id | `spatial_anchor_ref` + `spatial_anchor_type=visual_frame` | 与 STCM cross-modal §Vision 一致。 |
| 风险结果 TTL | `valid_until` | 强实时须短 TTL。 |
| 动态目标漂移 | `drift_risk` | 启发式或跟踪协方差进入 STCM。 |

**引用（已存在）**：

- `docs/architecture/LUNA_NAVIGATION_PERCEPTION_SIGNAL_CONTRACT_V0.md`  
- `docs/architecture/LUNA_YOLO_TO_PERCEPTION_SIGNAL_ADAPTER_MAPPING_V0.md`  

---

## 与 OCR Orchestrator / STCM 的协同结论（长期保留）

1. **OCR Provider Runtime Governance**：选 provider、**OCRRequest**、**OCRDispatchDecision**、Bridge 证据链。  
2. **STCM**：deadline、时空有效性、超时处置、语音与任务链准入。  
3. **OCR Orchestrator** 必须 **同时查询 STCM**（已在 OCR 治理主文 §23 提示）。

---

**一句话**：本文件把 STCM 从「孤立架构叙述」拉到 **与 OCR / Evidence / Voice / Vision 可核对字段** 的静态对齐面；实现与 runtime 仍属后续 phase。

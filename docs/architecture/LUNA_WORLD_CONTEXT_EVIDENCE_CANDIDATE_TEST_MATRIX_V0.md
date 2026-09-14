# LUNA — WorldContextEvidence Candidate Skeleton Test Matrix v0

## Phase

- **Phase-WorldModel-ContextEvidence-002**

## Goal

验证离线候选骨架满足：

- 合同字段必备项（observed_at / observed_where / trust / lifecycle / world_model_policy）
- governance 全禁止边界不回退
- commercial / world_change 路由可触发且不会进入 primary task decision
- trace / replay / whitebox 可观测输出非空

## Test matrix（Verifier gates A–V）

### A. Input readable（输出根可读）

- `output_root` 存在

### B. Required files present

- summary / candidates / commercial / world_change / trust_lifecycle / trace/replay/whitebox / notes 全部存在

### C. Candidate schema minimal valid

对每条 `WorldContextEvidenceCandidate`：

- top-level 必备字段存在
- `candidate_only=true`
- `observed_at.timestamp_ms` 存在
- `observed_where.spatial_anchor_type` 存在
- trust 必备字段存在（`trust_score` / `cross_validation_status`）
- lifecycle 必备字段存在（`evidence_status` / `ttl_policy` / `requires_revalidation` / `last_seen_at` / `seen_count`）
- world_model_policy 必备字段存在（`write_policy` / `task_planning_impact` / `shareable_to_hive` / `requires_user_confirmation`）
- governance 必备字段存在且“全禁止”

### D. observed_at present

- 全体候选有 `observed_at.timestamp_ms`

### E. observed_where present

- 全体候选有 `observed_where.spatial_anchor_type`

### F. source_attribution / world_model_policy present

- `world_model_policy` 为 dict

### G. source_evidence_refs present

- `source_evidence_refs` 为 list

### H. trust fields present

- `trust` 为 dict

### I. lifecycle fields present

- `lifecycle` 为 dict

### J. governance present

- `governance` 为 dict

### K. commercial activity short_ttl / revalidation / not primary decision

对每条 `CommercialActivityEvidenceCandidate`：

- `expiry_policy=short_ttl`
- `requires_revalidation=true`
- `allowed_for_primary_task_decision=false`
- `navigation_action=null`

### L. expired maps to requires_revalidation

- 若存在 `expired_candidate`，则其 `requires_revalidation=true`

### M. content_replaced maps to world_change_event candidate（当输入覆盖时）

- `world_change_event_candidates` 的 `change_type` 集合包含 `content_replaced`（或 world_change_event 为空时跳过）

### N. content_removed maps to world_change_event candidate（当输入覆盖时）

- `world_change_event_candidates` 的 `change_type` 集合包含 `content_removed`（或 world_change_event 为空时跳过）

### O. duplicate does not create persistent fact

- 对 `candidate/uncertain_candidate` 不允许出现“持久写入策略”（本阶段只允许 no_write / low_priority_candidate / scene_local_candidate）

### P. uncertain does not create persistent fact

- 同 O（uncertain_candidate 必须保持 no_write 倾向）

### Q–U. Governance boundaries（强制）

- `world_model_write_invoked=false`
- `hive_upload_invoked=false`
- `navigation_action=null`
- `real_tts_invoked=false`
- `recommendation_invoked=false`

### V. trace/replay/whitebox present and non-empty

- 三个 jsonl 行数均 > 0

---

## Phase-WorldModel-ContextEvidence-003 — Alignment gates（W–AF）

- **W**：`observed_where_source` 存在且非空
- **X**：`source_reference_chain` 存在且至少 1 项
- **Y**：当 `source_ref_integrity_status in {partial, broken}` 时，`missing_source_refs` 必须非空
- **Z**：不伪造 GPS（`observed_where.geo_location.lat/lng` 必须为 null）
- **AA**：SceneDelta 输入时必须继承 `spatiotemporal_anchor_ref`
- **AB**：`source_modalities` 只允许真实感知模态（ocr/yolo/map/gps/visual_symbol/user_feedback）
- **AC**：`source_layers` 存在且非空
- **AD**：`source_ref_integrity_status` 存在（complete/partial/broken）
- **AE**：`source_evidence_refs` 为空则 NO_GO（hard gate）
- **AF**：unknown anchor 强制 `requires_revalidation=true`


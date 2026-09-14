# Luna 评测 — Scene Delta Write Candidate from Vision GO / NO_GO Pack v0

**Verifier**：`tools/evaluation/midplatform/verify_scene_delta_write_candidate_from_vision_ingest_stub_v0.py`  
**Phase**：`Phase-MidPlatform-Scene-Delta-Write-Candidate-From-Vision-Ingest-Stub-001`

## GO

- **`scene_delta_write_candidate_from_vision.json`** 存在；`schema_version=scene_delta_write_candidate_from_vision_v0`。  
- `candidate_scope=write_candidate_only`；`write_allowed=false`；`requires_gate_approval=true`。  
- `evidence_count > 0`；`provider=vision_stub`，`provider_level=stub`；summary 计数与 `evidence_items` 一致。  
- 每条 item：`source_frame_id` 非空；`roi_id` 或 `unit_id` 非空；`synthetic=true`；`stub_provider=true`；`fact_status=not_fact`；无 **confirmed_fact / confirmed_object** 语义。  
- `forbidden_actions` 六键齐全且为 **true**；gate **`gate_status=not_evaluated`**、`gate_required=true`。  
- audit：`scene_delta_write_candidate_generated=true`；禁止写入 / 禁止模型 / 禁止解释与导航、`database_write_invoked`、`external_bus_invoked` 均为 **false**。

## CONDITIONAL_GO

- 无 **NO_GO** blockers，但存在 **soft_notes**（例如 `source_chain_summary` 较弱、矩阵行数与 count 轻微不一致等）。

## NO_GO

- **写入** Scene Delta / MidPlatform fact / WorldModel；调用 **AI / 导航 / 真实视觉**；`write_allowed=true` 或 **`gate_status=approved`**；候选中出现 **confirmed** 语义或禁止顶层键。  
- **audit** 或关键产物缺失。

## 一句话

本 smoke **只**生成 Vision 来源的 **Scene Delta write candidate** JSON；**不**落库、**不**写 Scene Delta、**不**做 AI 解释。

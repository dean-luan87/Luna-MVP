# Luna — Confirmed Text Evidence Memory Governance Contract v1

**Phase**：`Confirmed-Text-Evidence-Memory-Governance-Contract-v1-001`  
**性质**：contract only；定义中台与 Memory Governance 边界，不调用真实 Memory

## 用户长期原则（冻结）

1. 中台确认后的文字必须留存  
2. 中台不能轻易删除  
3. delete / update / merge / conflict / TTL / 隐私 → **Memory Governance**  
4. 中台仅 **append / read / call / reference**  
5. 中台禁止 delete、禁止 update/overwrite 原始记忆  
6. 修正仅 append correction / supersession / conflict candidate  
7. 过期 ≠ 丢弃；可路由至世界/环境/画像/情感长期候选  

## 核心产物

- `confirmed_text_evidence_schema_v1` — confirmed / candidate / expired 等状态 + source_chain / anchors  
- `confirmed_text_memory_append_request_schema_v1` — `operation=append_only`  
- `midplatform_memory_permission_policy_v1` — delete/update/overwrite forbidden  
- correction / supersession / conflict / stale routing / privacy / responsibility boundary  
- Memory Governance handoff candidate（later only）

## 决策

**Final**：`READY_FOR_MEMORY_GOVERNANCE_HANDOFF_DRYRUN_LATER`  
**不写**：Memory / WorldModel / SceneDelta / fact

## 前置（软件主线）

- OCR Activation Governance  
- Static Reading 链（TSC / ISRC / RRD）  
- WorldModel Unresolved Slot Contract  
- Hardware Adapter Stub（已冻结，`STUB_READY_SOFTWARE_BOUNDARY_CLOSED`）

## 实现

- `capabilities/midplatform/confirmed_text_evidence_memory_governance_contract_v1.py`  
- `tools/evaluation/midplatform/run_confirmed_text_evidence_memory_governance_contract_v1.py`  
- `tools/evaluation/midplatform/verify_confirmed_text_evidence_memory_governance_contract_v1.py`

## 建议下一 phase

- **Confirmed-Text-Evidence-Memory-Handoff-DryRun-v1**（推荐）  
- `OCRRequest-Gated-Submission-from-StaticReading-v1`  
- `WorldModel-Lookup-for-Reading-DryRun-v1`

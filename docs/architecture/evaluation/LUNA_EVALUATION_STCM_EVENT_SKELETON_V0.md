# LUNA Evaluation — STCM Event Skeleton v0（Phase-STCM-Event-Skeleton-001）

## 前置状态

- **Spatiotemporal-Consistency-Manager-001** = GO  
- **STCM-Contract-Field-Alignment-001** = GO  
- **OCR-Provider-Runtime-Governance-Standard-001** = GO  
- **Alignment verifier 产物根目录（示例）**：`/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/stcm_cross_contract_field_alignment_v0`

## 定位

定义 **STCM 事件骨架与 trace contract**，使 OCR / Vision / Voice / Map / Memory 的 **模型调用、deadline、timeout、fallback、stale result、voice notice** 可被 **统一记录、回放、审计**（设计层）。**不**运行模型、**不**接 runtime、**不**改 routing、**不**实装 MidPlatform、**不**写世界模型。

## 权威正文

- 事件骨架与 trace：`docs/architecture/midplatform/LUNA_STCM_EVENT_SKELETON_AND_TRACE_CONTRACT_V0.md`  
- 事件类型注册表：`docs/architecture/midplatform/LUNA_STCM_EVENT_TYPE_REGISTRY_V0.md`  
- 机器可读样例：`configs/midplatform/stcm_event_type_registry_v0.example.json`

## 工具

```text
python3 tools/evaluation/midplatform/verify_stcm_event_skeleton_v0.py \
  --repo-root <ABS_Luna-Core> \
  [--output-root <ABS_OUT>]
```

默认 **`--output-root`**：`<repo-root>/_eval_out/stcm_event_skeleton_v0`。

## 产物

- `stcm_event_skeleton_summary.json`  
- `stcm_event_type_matrix.json`  
- `stcm_event_required_fields_matrix.json`  
- `stcm_event_gap_report.json`  
- `stcm_event_skeleton_verifier_report.json`

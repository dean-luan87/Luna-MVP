# Luna — Static Readable Region Discovery Runtime DryRun v1

**Phase**：`Static-Readable-Region-Discovery-Runtime-DryRun-v1-001`  
**性质**：17 条 ranked source area → readable region candidates（非 detected region、非 bbox）

## 链路

```
ISRC Runtime (17 ranked source areas)
  → RRD Runtime DryRun
  → readable region candidates + classification + filtering
  → user view guidance + static capture handoff + OCRRequest future gate
  → READY_FOR_STATIC_CAPTURE_HANDOFF_LATER
```

## 边界

- `bbox_candidate_unknown_by_default=true`
- `readability_status_unknown_by_default=true`
- 不 camera / detector / OCR / OCRRequest / fact / WorldModel

## 前置

[LUNA_STATIC_READING_INFORMATION_SOURCE_LOCALIZATION_RUNTIME_DRYRUN_V1.md](./LUNA_STATIC_READING_INFORMATION_SOURCE_LOCALIZATION_RUNTIME_DRYRUN_V1.md)

## 实现

- `capabilities/midplatform/static_readable_region_discovery_runtime_dryrun_v1.py`  
- `tools/evaluation/midplatform/run_static_readable_region_discovery_runtime_dryrun_v1.py`  
- `tools/evaluation/midplatform/verify_static_readable_region_discovery_runtime_dryrun_v1.py`

## 评测

[LUNA_EVALUATION_STATIC_READABLE_REGION_DISCOVERY_RUNTIME_DRYRUN_V1.md](../evaluation/LUNA_EVALUATION_STATIC_READABLE_REGION_DISCOVERY_RUNTIME_DRYRUN_V1.md)

## 建议下一 phase

- [LUNA_HARDWARE_CAMERA_CONTROL_CONTRACT_V1.md](./LUNA_HARDWARE_CAMERA_CONTROL_CONTRACT_V1.md)（已实现）
- `Assisted-Static-Reading-GuardedTrial-v1`

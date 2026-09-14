# Luna — WorldModel Lookup for Reading Framework v1

**Phase**：`WorldModel-Lookup-for-Reading-Framework-v1-001`  
**性质**：Framework / contract / policy only；**不**调用 WorldModel runtime

## 升级方向

从 `readable region → OCR` 升级为：

`task/scene + WorldModel hint + unresolved slot + memory reference → information source candidate → readable region → static capture/OCR gate`

## 定义内容

- Lookup request / response candidate schema（schema only）
- Source priority（live observation 优先；不可直接触发 OCR）
- Unresolved slot / memory / confirmed text link policy
- ISRC / RRD handoff policy（policy only，不执行）
- Fallback 与 candidate classification
- Future dry-run entrypoint → **WorldModel-Lookup-for-Reading-DryRun-v1**

## 边界

- `worldmodel_runtime_available=false`
- 不写 WorldModel / Memory / fact
- OCR 主线仍 `closed_for_governance`

## 实现

- `capabilities/midplatform/worldmodel_lookup_for_reading_framework_v1.py`
- `tools/evaluation/midplatform/run_worldmodel_lookup_for_reading_framework_v1.py`
- `tools/evaluation/midplatform/verify_worldmodel_lookup_for_reading_framework_v1.py`

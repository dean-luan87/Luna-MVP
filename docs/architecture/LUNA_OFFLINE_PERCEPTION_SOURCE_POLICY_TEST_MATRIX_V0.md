# LUNA — Offline Perception Source Policy Test Matrix v0 (Phase-EngineeringFlow-002)

## 目的
矩阵化验证 source policy selection 与回退逻辑、审计字段与边界约束是否成立。

## 覆盖用例（A–J 对齐）
### A 正常条件下选择 yolo_shadow
- 预期：source_selected=yolo_shadow，fallback_used=false

### B disable_yolo=true 回退 baseline
- 预期：source_selected=baseline_mock，fallback_used=true，fallback_reason=disable_yolo_true

### C controlled_live_stream=true 回退 baseline
- 预期：source_selected=baseline_mock，fallback_used=true

### D evidence_type 非 phone_local 回退 baseline
- 预期：source_selected=baseline_mock，fallback_used=true

### E pending_real_sidewalk_run=false 回退 baseline
- 预期：source_selected=baseline_mock，fallback_used=true

### F manifest 缺失回退 baseline
- 预期：source_selected=baseline_mock，fallback_used=true，fallback_reason=manifest_missing

### G pinned readiness fail 回退 baseline
- 预期：source_selected=baseline_mock，fallback_used=true

### H YOLO source 输出 schema 不完整时 fallback
- 预期：PerceptionEval 对 YOLO path 的合同校验失败时，fallback baseline/mock（且不伪成功）

### I forbidden output 被阻断
- 预期：YOLO path 若触发 forbidden scan，则被阻断并 fallback（adapter 侧既有能力，EF-002 不改 adapter）

### J audit fields 完整
- 预期：summary 与 per-sample 均包含 source_policy_id/source_selected/fallback_used/fallback_reason 等审计字段

## 本阶段实际验证方式（v0）
- policy/manifest 选择逻辑：`tools/verify_offline_perception_source_policy_v0.py`
- PerceptionEval 接入后的审计字段与两条路径（YOLO vs fallback）：通过运行 `tools/evaluate_option_a_phone_local_perception_v0.py`（仅 PerceptionEval，不进入下游）


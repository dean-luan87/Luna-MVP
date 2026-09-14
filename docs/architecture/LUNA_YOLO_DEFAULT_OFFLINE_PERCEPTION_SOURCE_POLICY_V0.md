# LUNA — YOLO Default Offline Perception Source Policy v0 (Phase-ModelPerception-012)

## 目的
将“后续 Option A / phone_local / offline evaluation 默认使用 YOLO shadow perception（而非 baseline/mock）”固化为**策略**，并明确：
- 适用范围（offline only）
- 选择条件（何时默认用 YOLO）
- 必须回退 baseline/mock 的条件
- 必须禁用 YOLO 的条件
- 必须保留 disable / fallback / rollback-to-baseline
- 必须记录审计字段，保证可复现
- 明确禁止把 offline default 误解为 runtime default

## 严格边界（硬约束）
- **default offline source ≠ runtime default source**
- **default offline source ≠ controlled_live source**
- **default offline source ≠ production source**
- **default offline source ≠ execution authority**
- YOLO 仍是 shadow perception candidate source（candidate-only）
- YOLO 输出仍必须经过 SceneContext gates（治理要求，不得绕过）
- baseline/mock 必须保留 rollback
- disable switch 必须保留
- pending_real_sidewalk_run 仍不得关闭（必须保持 true）
- 记录 torch.hub 风险为 soft follow-up（后续需 pinned weights/deps）

## Policy identity
- **source_policy_id**: `yolo_default_offline_perception_source_v0`
- **policy_version**: `v0`

## Allowed scope（适用范围）
仅当满足全部条件时，策略允许“默认选择 YOLO shadow”：
- offline_evaluation=true
- option_scope=OptionA
- evidence_type=phone_local_controlled_capture
- controlled_live_stream=false
- pending_real_sidewalk_run=true
- 评测链路为离线工具链（非 runtime）

## Non-goals（明确非目标）
- 不允许把该策略解释为 runtime 启用 YOLO
- 不允许把该策略解释为真实导航能力验证
- 不允许把 detection_count 解释为可执行避障
- 不允许把 class-based risk candidate 解释为 collision risk
- 不允许把 object detection 解释为 depth/passability confirmed
- 不允许把 YOLO 替代 baseline 解释为 OCR/dynamic/depth 能力具备


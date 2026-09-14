# Document Surface Detector — Iteration v2 Planning v1

## 路线裁决

**Option A 不再作为唯一路线。** 保留为 `baseline_candidate`（低成本、依赖轻、治理已验证），但**不足以**解决叠放分离、高遮挡、贴附 surface mask、纹理假阳性。

**Option B 引入为 `segmentation_candidate_route`。** 规划阶段仅定义候选路线与 admission 约束；**不指定 active 模型、不下载、不执行、不训练**。

## A/B 关系

- **并行 candidate routes**，非竞争替代、非 silent fallback、非 teacher、非 VLM、非 fact source
- Model Manager 输出 `route_candidate`，不是 execution decision
- A/B 冲突 → `validation_review`，**不按 confidence 自动覆盖**

## 下一阶段

`OptionB-Candidate-Route-DryRun-v1-001` — 重新走 admission + controlled execution 门。

## 明确禁止

runtime activation · OCR per surface · production registry · Option B 执行 · 模型下载

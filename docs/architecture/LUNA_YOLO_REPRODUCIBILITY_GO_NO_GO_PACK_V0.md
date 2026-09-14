# LUNA — YOLO Reproducibility Go/No-Go Pack v0 (Phase-ModelPerception-013)

## Decision
### Result
**GO**

## What this phase achieves (definition-only)
冻结“可复现”所需的三件事：
1. **manifest schema**：`yolo_model_manifest.json` 必须记录权重路径/hash/依赖版本/平台/验证状态
2. **model load policy**：pinned_local 为长期默认；torch.hub 仅 dev/smoke 且标风险；失败必 fallback baseline/mock
3. **readiness check policy**：明确必检项（manifest/sha/import/version/dry-run/one-frame/forbidden scan/工件写入/fallback/disable）

## Hard boundaries (re-affirmed)
- 不新增 runtime
- 不改 YOLO adapter
- 不重跑评测链
- 不扩 Option A
- 不进入 controlled_live_stream / full controlled trial
- 不执行导航动作、不真实播报
- pinning 策略不得绕过 disable/fallback/rollback

## Hard blockers
- `[]`

## Soft follow-ups
- 实现阶段需要选择 manifest 文件落点与本地权重交付方式（但不能变成 runtime 默认路径）。
- 需要定义 dependency pinning 的具体载体（requirements/lockfile/conda env 等）—留到实现阶段落地。

## Recommended next phase (do not auto-enter)
- **Phase-ModelPerception-014：Pinned YOLO Weights Readiness Implementation v0**


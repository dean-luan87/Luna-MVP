# LUNA — YOLO Model Readiness GO/NO-GO Pack v0 (Phase-ModelPerception-014)

## Scope
本 pack 只覆盖 Phase-ModelPerception-014：manifest + readiness check（依赖/权重/hash/dry-run/smoke）。
不触达 runtime、不触达下游链路（SceneTask/Fusion/Output）、不修改 YOLO shadow adapter 安全边界。

## Artifacts
- manifest: `configs/models/yolo/yolo_model_manifest_v0.json`
- readiness tool output: `logs/yolo_model_readiness_001_20260427_1622.json`
- result matrix: `docs/architecture/LUNA_YOLO_MODEL_READINESS_RESULT_MATRIX_V0.md`
- implementation note: `docs/architecture/LUNA_PINNED_YOLO_WEIGHTS_READINESS_IMPLEMENTATION_V0.md`

## Decision
**CONDITIONAL_GO**

### Why
- 依赖检查：pass
- dry-run：pass
- one-frame smoke：pass
- 但当前 weights_source=**torch_hub_dev**，manifest 标注 **reproducibility_risk=true**
- pinned_local weights 尚未就绪（pinned_local_ready=false）

## Hard blockers（本阶段）
- none（readiness tool 可运行、可出报告、smoke 通过）

## Soft follow-ups（下一阶段候选输入）
- 推进 pinned_local 权重落地（可控权重文件 + sha256 固化）
- 消除 torch.hub 的自动依赖更新不确定性（本次日志出现 `pip: command not found` 的 AutoUpdate 尝试）

## Recommended next phase
- Phase-ModelPerception-015：Pinned Local YOLO Weights Hardening v0（仅在你显式批准后进入）

## Boundary attestations
- 默认路径未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- YOLO default 仍只限 offline evaluation
- 本阶段只实现 YOLO readiness，不改变 runtime 安全边界


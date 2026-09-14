# LUNA — Pinned YOLO Weights GO/NO-GO Pack v0 (Phase-ModelPerception-015)

## Scope
仅覆盖 pinned_local 权重 hardening 与 readiness（依赖/sha256/dry-run/smoke）。
不触达 runtime，不触达下游链路，不修改 YOLO shadow adapter 安全边界。

## Artifacts
- pinned_local manifest: `configs/models/yolo/yolo_model_manifest_v0.json`
- pinned_local readiness report: `logs/yolo_model_readiness_pinned_001_20260427_1646.json`
- hardening note: `docs/architecture/LUNA_PINNED_LOCAL_YOLO_WEIGHTS_HARDENING_V0.md`
- result matrix: `docs/architecture/LUNA_PINNED_YOLO_READINESS_RESULT_MATRIX_V0.md`

## Decision
**GO**

### Evidence summary
- weights_source=pinned_local：yes
- weights_path exists：pass
- sha256 matches：pass
- dependency readiness：pass
- dry-run：pass
- one-frame smoke：pass
- pinned_local_ready：true
- fallback/disable：未移除（本阶段未改动相关策略/代码路径）
- safety boundary：未改动 YOLO shadow adapter

## Hard blockers
- none

## Soft follow-ups
- 建议在后续阶段将 torch.hub AutoUpdate 行为进一步隔离/显式治理（本阶段虽走 `source=local`，但依旧看到 AutoUpdate 尝试日志）

## Recommended next phase
- 若你显式批准，可进入后续“offline 默认源”治理层面的更新（不在本阶段自动推进）

## Boundary attestations
- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled_live_stream
- 未扩 Option A
- 未执行导航动作
- 未真实播报
- YOLO default 仍只限 offline evaluation
- 本阶段只做 pinned local weights hardening，不改变 runtime 安全边界


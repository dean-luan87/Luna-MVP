# LUNA — Pinned Local YOLO Weights Hardening v0 (Phase-ModelPerception-015)

## 目标（本阶段唯一目标）
把 YOLO 从 `torch_hub_dev` 固化为 **`pinned_local` 权重路径**，并通过 readiness（依赖/sha256/dry-run/one-frame smoke）。

## 严格边界（确认）
- pinned_local 只影响 **offline evaluation**
- 不接入真实 runtime
- 不进入 SceneTask/Fusion/Output
- 不改 YOLO shadow adapter 安全边界
- 不移除 baseline/mock fallback
- 不移除 disable_yolo
- 不关闭 pending_real_sidewalk_run
- 不执行导航动作、不真实播报
- pinned_local 失败只允许 fallback，不允许强行继续

## 权重落点（推荐）
- 目录：`models/yolo/`
- 文件：`models/yolo/yolov5n.pt`
- 说明：权重文件不入 git（仓库 `.gitignore` 已忽略 `*.pt`），manifest 仅记录路径与 hash/size。

## 产物
- 权重准备工具：`tools/prepare_pinned_yolo_weights_v0.py`
- readiness 工具更新：`tools/check_yolo_model_readiness_v0.py`（支持 pinned_local 加载 + `--require-pinned-local`）
- manifest 更新：`configs/models/yolo/yolo_model_manifest_v0.json`
- readiness report（本次）：`logs/yolo_model_readiness_pinned_001_20260427_1646.json`

## 本次 pinned_local metadata（来自 manifest / report）
- weights_path：`models/yolo/yolov5n.pt`
- weights_sha256：`4f180cf23ba0717ada0badd6c685026d73d48f184d00fc159c2641284b2ac0a3`
- weights_file_size_bytes：`4062133`
- readiness：
  - dependency：pass
  - weights_integrity：pass
  - dry-run：pass
  - one-frame smoke：pass
  - pinned_local_ready：true


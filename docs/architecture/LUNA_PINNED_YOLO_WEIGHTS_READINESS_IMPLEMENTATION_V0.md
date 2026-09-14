# LUNA — Pinned YOLO Weights Readiness Implementation v0 (Phase-ModelPerception-014)

## 本阶段实现范围（最小落地）
仅实现“pinned weights / dependency readiness”最小能力：
- 生成/更新 `yolo_model_manifest_v0.json`
- 运行 readiness check：依赖 import/version、（若有）本地权重存在与 sha256、dry-run、one-frame smoke
- 输出 readiness report JSON
- 若 pinned_local 不可用，明确降级为 torch_hub_dev（dev/smoke only）或最终回退 baseline/mock

## 严格边界（确认）
- 不改 YOLO shadow adapter 的安全边界
- 不进入 SceneTask/Fusion/Output
- 不进入真实 runtime / TTS / 动作
- readiness fail 不等于系统失败：只能 fallback

## 产物与路径
- manifest：
  - `configs/models/yolo/yolo_model_manifest_v0.json`
- manifest build tool：
  - `tools/build_yolo_model_manifest_v0.py`
- readiness tool：
  - `tools/check_yolo_model_readiness_v0.py`
- readiness report（本次运行）：
  - `logs/yolo_model_readiness_001_20260427_1622.json`

## 本次 readiness 结果摘要（来自 readiness report）
- weights_source: `torch_hub_dev`
- dependency_readiness_status: pass
- model_dry_run_status: pass
- one_frame_smoke_status: pass
- pinned_local_ready: false
- torch_hub_dev_ready: true
- fallback_required: false（但 **reproducibility_risk=true**）

## 重要观察（工程风险）
- torch.hub 路径在加载过程中尝试自动更新依赖（日志显示 `pip: command not found`），尽管最终 init/smoke 成功，但这进一步证明：
  - torch.hub 不可作为长期默认加载路径
  - 必须推进 pinned_local weights + 可控依赖 pinning


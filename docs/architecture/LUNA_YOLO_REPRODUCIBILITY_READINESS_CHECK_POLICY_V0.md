# LUNA — YOLO Reproducibility Readiness Check Policy v0 (Phase-ModelPerception-013)

## 目的
定义“离线默认源=YOLO”在运行任何离线评测前必须通过的 readiness check。
readiness check 的目标是：**可复现**与**可回退**，而不是更强能力。

## 输入
- `yolo_model_manifest.json`
- pinned weights 文件（若 weights_source=pinned_local）
- 当前 Python 环境依赖版本（import + version）

## 必检项（v0，全部必须记录）
### Manifest & weights integrity
- manifest exists
- manifest schema 完整（字段齐全）
- weights_path exists（pinned_local 时必须）
- weights_sha256 matches（pinned_local 时必须）
- weights_file_size_bytes 记录且与实际一致（best-effort）

### Dependency readiness
- required dependencies importable：
  - torch / torchvision / cv2 / numpy / pandas / seaborn / PIL
- 依赖版本记录完整（写入审计字段）
- python_version 记录

### Model load / inference dry-run
- model load dry-run 成功（不触发任何执行权）
- one-frame inference smoke 成功（单帧；离线；candidate-only）
- output schema sanity（输出结构可解析）

### Governance / safety checks
- forbidden output scan pass（禁止语义=0）
- candidate-only invariant 可验证（allows_execute_now 必须为 false）
- replay/whitebox/trace 可写（用于审计；若不可写则必须 fallback）
- fallback path available（baseline/mock）
- disable switch available（disable_yolo=true 可强制回退）

### Evidence boundary invariants (offline)
- controlled_live_stream=false
- pending_real_sidewalk_run=true（不得关闭）

## Readiness结果与动作
readiness check 输出至少包含：
- dependency_readiness_status: pass|fail + details
- weights_integrity_status: pass|fail + details
- model_dry_run_status: pass|fail + details
- smoke_inference_status: pass|fail + details
- governance_scan_status: pass|fail + details
- reproducibility_risk: true|false（torch_hub_dev 必须 true）

动作规则：
- 任一 fail => **必须 fallback baseline/mock**（记录 fallback_reason）
- pass 且 weights_source=pinned_local => 允许选择 YOLO 作为离线默认源
- pass 且 weights_source=torch_hub_dev => 仅允许 dev/smoke（不得作为长期默认）


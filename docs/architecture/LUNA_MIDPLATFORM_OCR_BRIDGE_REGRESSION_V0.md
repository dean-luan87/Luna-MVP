# LUNA — MidPlatform OCR Bridge Regression v0

## Phase

- **Phase-ModelOCR-MidPlatform-Bridge-003**

## Purpose

对 Bridge-002 / Bridge-002-Fix 的离线 skeleton 进行**只读回归验收**，以便收口到 `closed_v0`：

- 读取多个既有 `output_root`（不重跑上游，不改产物）
- 聚合输出回归矩阵、边界摘要、trace/replay/whitebox 摘要
- 以 verifier 形式冻结“硬门槛不允许波动项”

## Non-governance boundaries（写死）

- 不接真实 runtime / 真实中台
- 不接 SceneTask/Fusion/Output
- 不做最终语义提炼（`semantic_summary=null`）
- 不生成/不执行导航动作（`navigation_action=null`）
- 不真实播报
- 不写入真实世界模型
- 不接推荐系统

## Regression inputs（只读 roots）

本阶段回归输入为多个 Bridge-002/002-Fix 的 `output_root` 目录（示例）：

- `logs/midplatform_ocr_bridge_002_20260429_174131`（sample_matrix）
- `logs/midplatform_ocr_bridge_002_fix_yolo_20260429_174428`（yolo_ocr_bridge_root）
- `logs/midplatform_ocr_bridge_002_fix_yolo_expand_20260429_174444`（yolo_ocr_bridge_root expansion）
- `logs/midplatform_ocr_bridge_002_fix_yolo_002_20260429_174525`（yolo_ocr_bridge_002 root）
- `logs/midplatform_ocr_bridge_002_fix_ocr_20260429_174540`（ocr_benchmark_root）

## Tools（新增）

### 1) Regression runner（聚合器）

`tools/run_midplatform_ocr_bridge_regression_v0.py`

作用：

- 只读多个 `output_root`
- 生成聚合 summary / matrix / boundary / trace-replay-whitebox summary

示例：

```bash
python3 tools/run_midplatform_ocr_bridge_regression_v0.py \
  --roots \
    logs/midplatform_ocr_bridge_002_20260429_174131 \
    logs/midplatform_ocr_bridge_002_fix_yolo_20260429_174428 \
    logs/midplatform_ocr_bridge_002_fix_yolo_expand_20260429_174444 \
    logs/midplatform_ocr_bridge_002_fix_yolo_002_20260429_174525 \
    logs/midplatform_ocr_bridge_002_fix_ocr_20260429_174540 \
  --output-root logs/midplatform_ocr_bridge_regression_003_<timestamp>
```

输出（写入 `--output-root`）：

- `midplatform_ocr_bridge_regression_summary.json`
- `midplatform_ocr_bridge_regression_matrix.json`
- `midplatform_ocr_bridge_input_root_matrix.json`
- `midplatform_ocr_bridge_candidate_matrix.json`
- `midplatform_ocr_bridge_boundary_summary.json`
- `midplatform_ocr_bridge_trace_replay_whitebox_summary.json`
- `regression_notes.md`

### 2) Regression verifier（聚合验收器）

`tools/verify_midplatform_ocr_bridge_regression_v0.py`

作用：对 regression runner 的输出进行 A–T 验收，产出 `verification_result.json`。

## Acceptance checklist（本阶段硬门槛）

必须满足：

- roots 可读
- 每个 root required output files 齐全
- 每个 root 的原 verifier 为 GO（或等价检查通过）
- evidence/delta/filter/candidate 文件存在
- trace/replay/whitebox 非空
- `semantic_summary=null` / `navigation_action=null`
- `allows_execute_now=false` / `real_tts_invoked=false` / `downstream_invocation_count=0`
- blocked evidence retained（`retained_evidence_ref` 不得缺失）
- 不发生 taskchain execution

允许波动：

- candidate 数量
- world/ambient candidate 数量
- raw text 内容
- relevance 分布
- delta_decision 分布

不允许波动：

- 任意 `semantic_summary` 非 null
- 任意 `navigation_action` 非 null
- 任意 TTS invoked / downstream invocation
- 任意真实世界模型写入
- trace/replay/whitebox 缺失
- blocked evidence 缺失 `retained_evidence_ref`


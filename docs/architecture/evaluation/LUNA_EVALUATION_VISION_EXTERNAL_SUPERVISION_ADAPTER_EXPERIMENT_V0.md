# Luna 评测 — Vision 外部 Supervision 适配实验 v0

**Phase**：`Phase-Vision-External-Supervision-Adapter-Experiment-001`  
**Verifier**：`tools/evaluation/vision/verify_external_supervision_adapter_experiment_v0.py`

## CLI

**参数别名**：`--frame-ingest-root` 等价于 `--video-ingest-root`；`--experiment-root` 等价于 verifier 的 `--smoke-root`。

若系统 Python 的 `pip` 无法写入用户 `site-packages`，可在仓库根创建独立 venv（例如 `.venv_supervision_exp`），在 venv 内执行 `pip install supervision`，再用 **该 venv 的 `python`** 运行 runner / verifier（与系统 `python3` 是否已装库解耦）。

```bash
python3 tools/evaluation/vision/run_external_supervision_adapter_experiment_v0.py \
  --repo-root /Users/luanlei/Desktop/Luna-Workspace-Min \
  --frame-ingest-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/video_frame_minimal_ingest_smoke_v0 \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/external_supervision_adapter_experiment_smoke_v0_after_install
```

## 产物（`--output-root`）

| 文件 | 说明 |
|------|------|
| `external_supervision_adapter_experiment_summary.json` | 汇总：`supervision_installed`、缺口报告、`roi_items_count` 等 |
| `external_supervision_availability_probe.json` | import 探测与能力标志 |
| `external_supervision_synthetic_detections.json` | 合成检测列表 |
| `vision_roi_proposal_candidate.json` | `vision_roi_proposal_candidate_v0` |
| `external_supervision_feature_matrix.json` | 特性矩阵（Detections / polygon / tracker 线索） |
| `external_supervision_audit_report.json` | 实验 audit |
| `external_supervision_adapter_notes.md` | 短说明 |
| `external_supervision_adapter_verifier_report.json` | verifier 输出 |

## Verifier

```bash
python3 tools/evaluation/vision/verify_external_supervision_adapter_experiment_v0.py \
  --experiment-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/external_supervision_adapter_experiment_smoke_v0_after_install
```

首次 `import supervision` 可能触发 Matplotlib 字体缓存构建，终端可能出现 cache 相关告警；不改变本实验 **不接主线 / 不调 YOLO** 的 audit 语义。

GO / CONDITIONAL_GO / NO_GO：`LUNA_EVALUATION_VISION_EXTERNAL_SUPERVISION_ADAPTER_EXPERIMENT_GO_NO_GO_PACK_V0.md`。

## 架构边界

见：`../vision/LUNA_VISION_EXTERNAL_SUPERVISION_ADAPTER_EXPERIMENT_V0.md` 与 `../vision/LUNA_VISION_MAINLINE_PHASE_ORDER_AND_INPUT_GATE_V0.md`。

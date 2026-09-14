# LUNA YOLO Stage-1 10-Frame Dry-run Execution v0

**Phase**：Phase-Mainline-GuardedTrial-005

---

## 1. 范围（允许 / 禁止）

**允许**：本地离线视频最多 10 帧、调用 YOLO detector、写 detection 结果、schema 校验、latency、abort/rollback、`post_trial_report`、本地 TRW（trace / replay / whitebox）与 RequestTrace stage 影子字段。

**禁止**：摄像头 index / 实时流、`rtsp`/`http(s)` URL、README 等占位扩展名、OCR / MidPlatform / SceneTask-Fusion-Output、导航动作、播报与真实 TTS、Qwen、世界模型写入、蜂巢上传、推荐策略改动、默认 provider / env 语义篡改。

---

## 2. 入口代码与 CLI

| 产物 | 路径 |
|------|------|
| 执行内核 | `capabilities/guarded_trial/yolo_stage1_10_frame_executor_v0.py` |
| 一键 dry-run | `tools/run_yolo_stage1_10_frame_dry_run_v0.py` |
| 验收 verifier | `tools/verify_yolo_stage1_10_frame_dry_run_v0.py` |

```bash
python3 tools/run_yolo_stage1_10_frame_dry_run_v0.py \
  --approval-root logs/yolo_stage1_10_frame_approval_gate_004_<UTC> \
  --input-video /path/to/offline_test_video.mp4 \
  --output-root logs/yolo_stage1_10_frame_dry_run_execution_005_<UTC>
```

---

## 3. 与 Phase-004 的关系

- **004**：冻结权重/manifest/detector entry/runbook/hard_audit，**不**执行 detector、**不**开视频推理窗口。
- **005**：在 **真实离线视频** + **权重文件存在** 前提下，窄窗口执行最多 **10** 帧推理并落盘验收材料。

---

## 4. Abort / rollback（概要）

触发 abort 的典型条件：输入视频非法、camera/stream 形态、连续 detector 异常 ≥ 2、`schema_invalid_count > 0`、权重缺失导致无法初始化 detector、hard_audit 侧效应字段异常（由 verifier 复核）。

rollback 建议仍以环境变量门控与人工复核为主；详见 `yolo_stage1_10_frame_abort_rollback_report.json`。

---

## 5. 输出目录约定

默认：`logs/yolo_stage1_10_frame_dry_run_execution_005_<UTC>/`（可与 004 gate 报告交叉引用）。

---
phase: Phase-RealSceneReplay-001
title: Recorded Sidewalk Video Evidence Replay Go/No-Go Pack v0
status: PACK
version: v0
last_updated: 2026-04-24
scope: recorded_video_replay_only
side_effects_released_default: false
---

## 0. 本 pack 的边界

本 pack 只汇总 Recorded Sidewalk Video Evidence Replay v0 的交付物与验证结果。

写死：

- recorded video replay **不能**替代 controlled live
- recorded video replay **不能**把 `pending_real_sidewalk_run` 置为 false
- recorded video replay **不能**标记为 `controlled_live`

## 1. 交付物（路径）

- Definition：`docs/architecture/LUNA_RECORDED_SIDEWALK_VIDEO_REPLAY_DEFINITION_V0.md`
- Archive Contract：`docs/architecture/LUNA_RECORDED_SIDEWALK_VIDEO_ARCHIVE_CONTRACT_V0.md`
- Runner：`tools/run_recorded_sidewalk_video_archive_v0.py`
- Validator：`tools/validate_recorded_sidewalk_video_archive_v0.py`

## 2. 本次实际运行（事实记录）

### 2.1 输入视频

- video_path：`/Users/luanlei/Desktop/Luna-Core/test_video_complex_6m42s.mp4`
- openCV read：可打开，可读首帧，fps≈29.99，frame_count≈12048

### 2.2 生成的 recorded_video_replay archive_root

- archive_root：`logs/recorded_sidewalk_replay_001_20260424_142351`
- run_id：`replay_452a260ef9`
- sampled_frame_count：200（frame_step=30，max_sampled_frames=200）

### 2.3 边界字段（必须成立）

在 `run_evidence.json` 中：

- evidence_type = `recorded_video_replay`
- controlled_live = false
- pending_real_sidewalk_run = true
- input_source = `recorded_video`

## 3. Validator 结果（recorded_video_replay validator）

对 `logs/recorded_sidewalk_replay_001_20260424_142351` 运行：

- `python3 tools/validate_recorded_sidewalk_video_archive_v0.py --archive_root logs/recorded_sidewalk_replay_001_20260424_142351`

结果：

- recommendation = **go**
- hard_blockers = []
- soft_followups = []
- missing_files = []
- hash_mismatches = []

## 4. go / conditional_go / no_go 判定

### 4.1 判定：GO

满足：

- 视频可读
- required_files 全部生成
- manifest hash 校验通过
- evidence_type=recorded_video_replay（未冒充 controlled_live）
- controlled_live=false 且 pending_real_sidewalk_run=true
- 安全断言全部 true
- validator 输出 go

### 4.2 hard blockers

无（以 recorded_video_replay 口径）。

### 4.3 soft follow-ups

无（v0 最小要求已满足）。

## 5. recommended next phase（按两段路线）

进入：

- **Phase-DeviceEnv-004：Phone Web Camera Controlled Live Adapter Definition v0**

目标：手机浏览器摄像头作为真实 controlled live input，Mac 作为接收/归档/validator 端。

## 6. 明确声明（边界重申）

- 默认路径仍未开启
- 未进入 full controlled trial
- 未扩大真实 side effects 面
- 未执行 controlled live run
- recorded video replay 不能替代 pending_real_sidewalk_run


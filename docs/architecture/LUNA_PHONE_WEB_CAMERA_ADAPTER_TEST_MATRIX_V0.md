---
phase: Phase-DeviceEnv-004
title: Phone Web Camera Adapter Test Matrix v0
status: TEST_MATRIX_FROZEN
version: v0
last_updated: 2026-04-24
scope: definition_only
---

## 0. 目标

定义 Phone/Web controlled live adapter 后续实现阶段（DeviceEnv-005）的测试矩阵。

本阶段只写矩阵，不实现测试代码，不执行真实 run。

## 1. 测试矩阵（v0）

### A. phone_camera_permission_granted_case

- **setup**：手机浏览器允许摄像头权限
- **expect**：capture ready；UI 显示 started/running；不开始上传直到 Mac start session

### B. phone_camera_permission_denied_case

- **setup**：拒绝摄像头权限
- **expect**：明确失败；不产生 archive；不上传任何帧

### C. start_session_success_case

- **setup**：Mac 调用 start session，参数齐全（Option A + entry_token + timebox）
- **expect**：返回 session_id/upload_url/archive_root；allowed=true

### D. upload_without_session_case

- **setup**：未 start session 直接上传帧
- **expect**：rejected；trace 记录拒绝；不写入 archive_root（或写拒绝事件到独立审计日志）

### E. upload_frame_success_case

- **setup**：running 状态上传若干帧
- **expect**：accepted=true；trace/replay 写入 frame events；rate limit 未触发

### F. upload_after_stop_case

- **setup**：stop session 后继续上传帧
- **expect**：rejected；stop 后不得写入任何 frame

### G. upload_after_abort_case

- **setup**：abort session 后继续上传帧
- **expect**：rejected；archive_preserved=true；post_run_summary ready

### H. session_timeout_case

- **setup**：timebox 超时
- **expect**：自动 stop/abort 或拒绝后续帧；trace/summary 记录超时；validator 可运行

### I. archive_required_files_case

- **setup**：正常 stop 完成一次短 run
- **expect**：required_files complete；risk_events none_observed 也必须存在

### J. manifest_hash_case

- **setup**：生成 manifest
- **expect**：hash 校验 pass（missing_files=0, hash_mismatch=0）

### K. safety_assertion_case

- **setup**：正常 run
- **expect**：三断言 true；candidate-only；allows_execute_now=false；default_path_disabled=true

### L. phone_network_drop_case

- **setup**：运行中网络断开/重连
- **expect**：记录 drop；可选择 abort/stop；不得静默继续；risk_events/post_run_summary 记录

### M. rate_limit_case

- **setup**：上传过快（超过上限）
- **expect**：限流生效（rejected + reason_codes）；系统不崩溃

### N. privacy_boundary_case

- **setup**：人工标记进入隐私敏感区或合规风险出现
- **expect**：必须 abort；停止接收帧；保全 archive；risk_events 记录


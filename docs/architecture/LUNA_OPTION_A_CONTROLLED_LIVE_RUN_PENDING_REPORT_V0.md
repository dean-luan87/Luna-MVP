# Phase-RealSceneRun-001 — Option A Controlled Live Evidence Collection Actual Run v0（PENDING 报告）

**结论**：`pending_real_device_run=true`  
**原因**：当前 Cursor/本工作区环境无法接入真实设备摄像头/传感器输入与对应运行时链路，无法生成“非 fixture 的真实 controlled live evidence archive”。  
**硬声明**：本报告不生成任何伪装成真实 controlled live evidence 的 `archive_root`，不以 fixture 冒充真实 run。  

---

## 1) 当前状态（写死）

- 工具链就绪：是（Fix-001 evidence contract + manifest + notes/risk template + validator 已成立）
- Option A 范围锁定：是（仅人行道短距离观察）
- 真实 controlled live evidence：未产生
- 是否允许扩场景：否
- 是否允许进入 full controlled trial：否
- 是否允许开放用户测试：否

---

## 2) missing_real_device_reason

- `no_real_device_camera_input_available_in_workspace`
- `no_on_device_runtime_execution_environment_available`

---

## 3) required_manual_steps（必须由人工在真实设备/受控环境执行）

### A. 设备与人员
- 准备目标设备或近似目标设备（可运行导航链路并能落盘文件）
- 现场必须到位并可记录：
  - operator
  - safety observer
  - record owner

### B. 环境与范围（仅 Option A）
- 白天、低人流、平整人行道、短距离
- 禁止：复杂路口/高密人流/夜间雨天/长距离/隐私敏感区域/未授权拍摄

### C. 显式入口与 timebox
- 生成 `entry_token`
- 显式进入 `controlled_live_input_mode` 并落盘 `mode_entry_event`
- 配置 timebox（单次/连续/单日上限）
- 配置 abort triggers（operator 与 observer 均可中止）

### D. 归档产出（archive_root 必须包含 required_files）
在一次真实 run 结束后，生成一个 `archive_root` 目录，至少包含：
- `run_evidence.json`
- `archive_manifest.json`
- `trace.jsonl`
- `replay.jsonl`
- `whitebox.jsonl`
- `model_candidate_trace.jsonl`
- `output_candidate_trace.jsonl`
- `operator_notes.md`（或 json）
- `risk_events.jsonl`（无风险也必须有 `none_observed` 记录）
- `post_run_summary.md`（或 json）

### E. 本地校验（必须）
把 `archive_root` 拷贝到本仓库（或可访问路径）后运行：

```bash
python3 tools/validate_controlled_live_evidence_collection_execution_v0.py --archive_root "<archive_root>"
```

输出为 `go` 才允许进入 Review-003。

---

## 4) 明确声明（写死）

- 默认路径仍未开启  
- 未进入 full controlled trial  
- 未扩大真实 side effects 面  
- 未扩 Option A  
- 未开放真实用户测试  
- 本报告仅说明 pending，不代表完成真实 controlled live run  


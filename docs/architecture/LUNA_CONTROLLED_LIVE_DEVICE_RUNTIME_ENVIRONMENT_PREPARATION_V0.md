# Phase-DeviceEnv-001 — Controlled Live Device Runtime Environment Preparation v0（设备/运行环境准备冻结）

**阶段名**：Phase-DeviceEnv-001  
**性质**：为 Option A controlled live evidence collection 准备真实设备与运行环境；不执行真实 run；不生成伪 evidence。  

---

## 0) 明确声明（硬边界，写死）

- 不是 controlled live run  
- 不是 Review-003  
- 不是 full controlled trial  
- 不开放真实用户测试  
- 不扩场景（仅 Option A）  
- 不生成/伪造 controlled live evidence  

---

## 1) 需要解决的 pending 原因（来自 RealSceneRun-001）

- `no_real_device_camera_input_available_in_workspace`
- `no_on_device_runtime_execution_environment_available`

本阶段目标：把这两项从 “不可用” 变成 “可用/可验证”。

---

## 2) 推荐的真实输入源（最小可行）

仅允许用于 Option A（人行道短距离观察）的 controlled live 输入源之一：
- **优先**：目标手机/可穿戴设备的实时摄像头（现场受控）
- **备选**：笔记本外接摄像头（仅用于“真实 live 输入链路”验证；仍需现场受控与隐私检查）
- **禁止**：用 replay/fixture 冒充 controlled live

---

## 3) 运行环境在哪里执行（最小可行）

三选一（按现实条件选择其一即可）：
- **设备端执行**：在手机/边缘设备本地跑采集与归档（推荐）
- **笔记本执行**：笔记本直接运行链路与采集（若摄像头来自笔记本）
- **设备采集 + 笔记本归档/校验**：设备侧产出文件 → 拷贝到本仓库 → 运行 validator（常用）

写死要求：无论在哪执行，最终必须得到一个真实 `archive_root` 目录（含 required_files），并能在本仓库运行 validator 校验通过。

---

## 4) 需要哪些权限（最小集合）

- 摄像头访问权限（OS 级）
- 本地文件写权限（能写入 archive_root）
- 时间戳与系统时钟访问（用于 start/end/duration）

禁止：
- 任何默认后台常驻/无人监督运行权限扩大
- 任何执行权/副作用放权

---

## 5) 需要哪些启动脚本（最小集合）

本仓库提供的脚本模板（仅做准备与提示，不生成伪证据）：
- `scripts/prepare_option_a_controlled_live_archive_root_v0.sh <archive_root_path>`
- `scripts/run_option_a_controlled_live_capture_v0.sh ...`（DeviceEnv-001 将新增；必须参数齐全，缺参直接失败）

---

## 6) 需要哪些日志目录

建议结构（真实 run 时使用）：
- `runs/controlled_live/option_a/<run_id>/` 作为 `archive_root`

注意：本阶段不创建伪造 evidence 文件；只定义目录规范与写权限检查。

---

## 7) 如何生成真实 archive_root（必须满足 Fix-001 contract）

真实 run 结束后，`archive_root` 必须至少包含（required_files）：
- `run_evidence.json`
- `trace.jsonl`
- `replay.jsonl`
- `whitebox.jsonl`
- `model_candidate_trace.jsonl`
- `output_candidate_trace.jsonl`
- `operator_notes.md`（或 json）
- `risk_events.jsonl`（无风险也必须 none_observed）
- `post_run_summary.md`（或 json）
- `archive_manifest.json`（sha256 校验通过）

并且 `run_evidence.json` 必须满足：
- explicit entry 落盘（entry_token + mode_entry_event_present=true + started/ended=true）
- 三条安全断言为 true（no execute/no default-on/no side effects expansion）

---

## 8) 如何运行 validator（写死）

在本仓库验证真实 archive_root：

```bash
python3 tools/validate_controlled_live_evidence_collection_execution_v0.py --archive_root "<archive_root>"
```

输出 `go` 才允许进入 Review-003。

---

## 9) 人工操作步骤（最小流程）

1. 设备与人员到位（operator + safety observer + record owner）
2. 选定受控环境（白天、低人流、非隐私敏感区域）
3. 配置 timebox 与 abort 方法
4. 启动 controlled live capture（显式 entry + started）
5. 短时运行并持续监控（可随时 abort）
6. 停止并归档（ended + required_files 全部落盘）
7. 生成 manifest（sha256）
8. 拷贝/同步到本仓库
9. 运行 validator 并记录结果

---

## 10) 继续 pending 的条件（写死）

任一条件不满足则继续 pending：
- camera_input_available=false
- runtime_environment_available=false
- archive_root_configured=false
- write_permission_ready=false
- validator_available=false
- operator/observer/record_owner 缺失
- privacy_area_checked=false 或 environment_allowed=false


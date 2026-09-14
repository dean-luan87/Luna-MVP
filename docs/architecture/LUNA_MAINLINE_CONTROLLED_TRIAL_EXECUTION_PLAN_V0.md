# LUNA Mainline Controlled Trial Execution Plan v0（Phase-Mainline-GuardedTrial-001）

**Phase**：Phase-Mainline-GuardedTrial-001  
**定位**：定义 **controlled trial** 的总原则、顺序、范围、样本量、验收、abort、rollback、前置检查与复盘材料——**不执行真实 trial**。

**前置**：`runtime_readiness_status=closed_v0`（Phase-Mainline-RuntimeReadiness-006）。

---

## 1. 总原则

- **顺序执行**：YOLO → OCR → Qwen Voice；**禁止并行**开启多条 capability trial。  
- **串行门禁**：前一 Stage **未 GO**，后一 Stage **不得启动**；任一 **NO_GO**，后续 **全部暂停**。  
- **单次活跃**：同一时刻仅允许 **一个** capability trial 处于 active。  
- **全局熔断**：`LUNA_DISABLE_ALL_GUARDED_TRIALS` 必须可 **一键关闭** 全部 trial。  
- **本 Phase**：仅文档与机器可读矩阵；**不**调用真实 detector/OCR provider/Qwen/TTS/playback。

---

## 2. 产出物

- 工具：`tools/run_mainline_controlled_trial_plan_v0.py`、`tools/verify_mainline_controlled_trial_plan_v0.py`  
- 日志目录：`logs/mainline_controlled_trial_plan_001_<UTC>/`（含 `*_summary.json`、`*_matrix.json`、`post_report_schema.json`、`review_notes.md`）

详见各子文档：trial order、YOLO/OCR/Qwen Voice 分计划、precheck/post-report、Go/No-Go Pack。

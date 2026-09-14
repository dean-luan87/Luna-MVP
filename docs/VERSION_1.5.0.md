# Luna-2 V1.5.0 版本说明

**版本号**: 1.5.0  
**发布日期**: 2026-02-14  
**版本类型**: Guardian Discipline Phase 1 冻结

## 版本概述

本版本冻结 **Guardian Discipline Phase 1** 完整工程闭环：退出纪律审计层（仅基于 control_mode）、suite 集成、Gate 红线、真实视频与 6 视频套件测试。

## 核心变更

- **审计工具**：`tools/audit_exit_latency.py`，输入 baseline/candidate replay_output.jsonl，输出 exit_audit_report.json/.md
- **Gate**：exit_latency_p95≤6、exit_latency_max≤12、hysteresis_efficiency≥0.90，否则 GUARDIAN_DISCIPLINE_VIOLATION
- **Suite**：run_sim_suite 自动跑审计，per_episode 含 guardian_discipline 与 exit_audit_path
- **真实视频**：run_video_replay.py、run_video_replay_suite.py（6 视频）

详见 `docs/GUARDIAN_DISCIPLINE_PHASE1.md`、`releases/freeze_record_1.5.0.md`。

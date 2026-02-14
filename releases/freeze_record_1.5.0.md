# Luna-2 工程封版记录 v1.5.0

**封版日期**：2026-02-14  
**版本号**：1.5.0  
**封版级别**：Guardian Discipline Phase 1 冻结  
**状态**：✅ 已封版

---

## 一、封版范围

本版本冻结 **Guardian Discipline Phase 1** 完整工程闭环：

- **退出纪律审计层**：`tools/audit_exit_latency.py`（仅基于 control_mode，与 A3 risk 数值解耦）
- **Suite 集成**：`tools/run_sim_suite.py` 自动跑审计，per_episode 含 guardian_discipline、exit_audit_path
- **Gate 红线**：`simulation/logic/gate.py`（exit_latency_p95≤6、max≤12、hysteresis_efficiency≥0.90，否则 FAIL）
- **文档**：`docs/GUARDIAN_DISCIPLINE_PHASE1.md`
- **测试**：`tools/test_guardian_discipline.py`、最小测试用例（baseline_test*.jsonl / candidate_test.jsonl）、6 视频套件 `tools/run_video_replay_suite.py`

---

## 二、封版前验证

| 项目 | 结果 | 说明 |
|------|------|------|
| Guardian 单元/门禁测试 | ✅ 通过 | `python3 tools/test_guardian_discipline.py` 及 `--suite` |
| 最小测试用例 | ✅ 通过 | exit_latency、hysteresis_efficiency、baseline_no_entry 口径正确 |
| 6 视频放大测试 | ✅ 6/6 PASS | `python3 tools/run_video_replay_suite.py --config patches/d1_conservative.json --max-frames 600` |

---

## 三、本版本包含的变更要点

- 新增 `tools/audit_exit_latency.py`：baseline/candidate replay 审计，输出 exit_audit_report.json/.md
- `run_sim_suite.py`：集成审计、per_episode 写入 guardian_discipline 与证据链路径
- `simulation/logic/gate.py`：Guardian Discipline 红线（GUARDIAN_DISCIPLINE_VIOLATION、WARN_BASELINE_NO_ENTRY_EVENTS）
- 新增 `tools/run_video_replay.py`：真实视频 → trace → episode → recompute → 审计
- 新增 `tools/run_video_replay_suite.py`：6 测试视频批量跑审计
- 新增 `tools/test_guardian_discipline.py`：审计 + Gate 回归测试
- 文档：`docs/GUARDIAN_DISCIPLINE_PHASE1.md`，最小测试用例与真实视频命令

---

## 四、封版后约定

- Guardian Discipline Phase 1 红线阈值（P95≤6、max≤12、efficiency≥0.90）已冻结，后续调整须在版本说明中引用本记录。
- 6 视频套件为视频侧回归入口；新增测试视频可扩展 `run_video_replay_suite.py` 的 VIDEO_LIST 或使用 `--videos`。

---

## 五、Git 标签

```bash
git tag -a v1.5.0 -m "Luna-2 v1.5.0 - Guardian Discipline Phase 1 冻结"
```

**封版记录文件**：`releases/freeze_record_1.5.0.md`

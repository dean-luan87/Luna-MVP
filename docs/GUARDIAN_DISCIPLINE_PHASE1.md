# Guardian Discipline Phase 1

退出纪律审计层：评估 B 型（安全优先）配置在 stress_v2 / sim_suite 上是否存在**粘滞型 Goodhart**。与 A3 内部 risk 数值完全解耦，**仅基于行为（control_mode）审计**。

## 口径

- **数据来源**：仅使用 `decision.control_mode`，不使用任何 `risk_raw`、threshold 等数值。
- **风险态**：`control_mode ∈ {CAUTION, GUARDED}`。
- **事件**：从非 risk_state 切入 risk_state，直到再次回到非 risk_state，记为一个 event。
  - `entry_seq`：进入 risk_state 的第一帧 seq。
  - `exit_seq`：退出 risk_state 的第一帧 seq（该帧已不在 risk_state）。
  - `dwell_frames`：事件持续帧数 = `exit_seq - entry_seq`。
- **缺失处理**：行内缺少 `decision` 或 `control_mode` 时，视为 `"NONE"`（非风险态）。

## baseline_no_entry 单列原因

- 若 candidate 存在某 event，但在 baseline 中找不到与之 entry 对齐（|entry diff|≤5）的 baseline event，则归类为 **baseline_no_entry**。
- 这些事件可能是 candidate「更敏感」而 baseline「漏检」，不宜直接并入 hysteresis_efficiency 分母（否则会惩罚更保守的 candidate）。
- 因此单独输出 `baseline_no_entry_count` 与 top-k 列表，Phase 1 仅做 **WARN**，不做硬 FAIL。

## 匹配逻辑

- 按 **baseline 事件为锚点**，对每个 baseline event 在 candidate 中找 **entry 最近邻**且 **|entry_seq diff| ≤ 5** 的 candidate event 做一对一匹配。
- 若 baseline 有 event 但无匹配 candidate event → `missing_candidate_event`。
- 若 candidate 有 event 但无匹配 baseline event → `baseline_no_entry`。

## 指标

| 指标 | 含义 |
|------|------|
| exit_latency_frames | 单事件：candidate_exit_seq - baseline_exit_seq（可负，表示 candidate 更早退出） |
| exit_latency_p50/p95/max | 所有 matched 事件的 exit_latency 分位数与最大值 |
| hysteresis_efficiency | sum(overlap) / sum(\|C\|)，其中 C 为 candidate 事件覆盖的 seq 集合，B 为 baseline，overlap = \|C ∩ B\| |
| baseline_no_entry_count | 无 baseline 对齐的 candidate 事件数（仅 WARN） |

## 输出结构

- **exit_audit_report.json**：含 `summary`、`events_matched`、`events_baseline_no_entry`、`top_offenders`（exit_latency / baseline_no_entry）。
- **exit_audit_report.md**：表格形式的 Summary + Top-3 offenders。

路径在 suite 中均使用 `Path(...).resolve()` 写入，保证证据链可复现。

## Gate 红线（Phase 1 冻结）

| 条件 | 结果 |
|------|------|
| exit_latency_p95 > 6 | FAIL，reason: GUARDIAN_DISCIPLINE_VIOLATION |
| exit_latency_max > 12 | FAIL，reason: GUARDIAN_DISCIPLINE_VIOLATION |
| hysteresis_efficiency < 0.90 | FAIL，reason: GUARDIAN_DISCIPLINE_VIOLATION |
| baseline_no_entry_count > 0 | 仅 WARN_BASELINE_NO_ENTRY_EVENTS，不 FAIL |

## 复现命令

**单条手工审计：**  
（请把下面两处路径换成你本机的 baseline / candidate 的 `replay_output.jsonl` 实际路径；不要保留尖括号。）

```bash
python3 tools/audit_exit_latency.py --baseline /path/to/baseline/replay_output.jsonl --candidate /path/to/candidate/replay_output.jsonl
```

示例（suite 跑完后用某 episode 的 bundle 路径）：

```bash
python3 tools/audit_exit_latency.py --baseline outputs/v1.1/simulations/slice_EPISODE_6M42S_complexity_rise_10_10_baseline/replay_output.jsonl --candidate outputs/v1.1/simulations/slice_EPISODE_6M42S_complexity_rise_10_10_d1_conservative/replay_output.jsonl
```

**Suite 自动审计（跑完后检查 suite_report.json）：**

```bash
python3 tools/run_sim_suite.py --golden --patch patches/d1_conservative.json
```

验收点：

- `suite_report.json` 中每个 episode 的 `guardian_discipline` 非空（当 baseline/candidate replay 均存在时）。
- `exit_audit_report.json` / `exit_audit_report.md` 位于 candidate bundle 目录。
- Gate 在违反红线时 FAIL，并写入对应 reason。

## 最小测试用例（可控基准，不跑真实 stress_v2）

仓库内已有人工构造的基准对，用于打通 exit_latency / hysteresis_efficiency 口径：

- **baseline_test.jsonl**：两段风险事件 A(seq 2–3, exit 4)、B(seq 6–7, exit 8)。
- **candidate_test.jsonl**：A 延到 exit 5（+1 latency），B 延到 exit 10（+2 latency），且 candidate 多出帧 → efficiency < 1。

**测试 1（正常匹配 + 正 latency + efficiency < 1）：**

```bash
python3 tools/audit_exit_latency.py --baseline baseline_test.jsonl --candidate candidate_test.jsonl
```

预期：`exit_latency_p50=1`、`exit_latency_max=2`、`hysteresis_efficiency ≈ 0.57`、`baseline_no_entry_count=0`；Gate 应 **FAIL**（efficiency < 0.90）。

**测试 2（baseline 无事件，candidate 有 → baseline_no_entry）：**

```bash
python3 tools/audit_exit_latency.py --baseline baseline_test2.jsonl --candidate candidate_test.jsonl
```

预期：`matched_event_count=0`、`baseline_no_entry_count=2`、`hysteresis_efficiency=1.0`（无匹配时不参与分母，不 crash）。

## 真实视频测试（工业口径）

用真实连续场景验证：分叉是否稳定触发、是否长尾粘滞、是否 baseline_no_entry 爆发。

**一条命令（视频 → trace → episode → recompute → 审计）：**

```bash
# 前 20 秒（默认不限制时可用 --max-frames 600）
python3 tools/run_video_replay.py --video path/to/test_video.mp4 --config patches/d1_conservative.json --max-frames 600

# 6m42s 视频的「后 2 分钟」（暗→亮、风险消退类）：先跑全片再只保留最后 3600 条
python3 tools/run_video_replay.py --video test_video_complex_6m42s.mp4 --config patches/d1_conservative.json --last-records 3600
```

`--last-records 3600` = 最后 3600 帧 ≈ 2 分钟@30fps；输出在 `outputs/video_replay_<视频名>/`，审计报告在 candidate bundle 下 `exit_audit_report.json`。

**「障碍消失」怎么定义？**  
工具里不做自动识别，只按**你选的片段**审计。你只要在选视频/片段时心里有数即可：
- **风险消退类**：光照恢复（暗→亮）、人群散开、遮挡移开等，**语义上**“之前有风险、后来没了”的一段。
- 若没有明显“障碍物消失”的镜头，用**暗→亮**这一段当“风险消退”代理即可，重点看这段上的 exit_latency 是否仍健康。

**真实视频下必看的 6 个指标：** exit_latency_p95、exit_latency_max、hysteresis_efficiency、baseline_no_entry_count、**guarded_tail_ratio**（candidate 中 GUARDED 帧占比）、**max_dwell_frames**（单事件最长持续帧数）。

**6 视频放大测试（冻结前验收）：**  
与 `docs/Test_Videos_Inventory.md` 中 6 个测试视频一致，每个视频跑前 600 帧（约 20s），汇总 Guardian Gate 通过情况。全部通过即可冻结本块。

```bash
python3 tools/run_video_replay_suite.py --config patches/d1_conservative.json --max-frames 600
```

输出目录 `outputs/video_replay_suite_6videos/`，内有各视频子目录及 `suite_report.json`（per_video summary + all_passed）。

## Cursor 必盯数据（优先级）

1. exit_latency_p95  
2. hysteresis_efficiency  
3. exit_latency_max  
4. baseline_no_entry_count（先 WARN）  
5. top_offenders（便于定位「幽灵刹车」事件）  
6. per_episode 中 exit_audit_path（证据链）

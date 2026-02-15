# 测试结果总结（2026-02-12）

## 一、测试范围

| 类别 | 内容 |
|------|------|
| **D0.1 Headless A3 Parity** | A3HeadlessAdapter、run_a3_headless_replay、parity 报告、隔离测试、时间注入、empty_patch |
| **Golden / 对抗验证** | promote_to_golden、golden_bucket_report（tags 统计修复）、run_sim_suite、audit_blind_patch_suite |
| **双长视频 A3 Trace** | test_video_complex_6m42s.mp4（6m42s）、test_video_follow_crowd_crossing_6m14s_60fps.mp4（6m14s） |
| **Trace 分析** | analyze_a3_trace 与当前 trace 格式（obs/decision）兼容、缺失归一化为 NONE/0 |

---

## 二、问题与修复

### 2.1 运行 run_video_a3_trace 报错

- **现象**：`ModuleNotFoundError: No module named 'runtime.observation_frame'`，随后 `runtime.observation_builders`。
- **原因**：主项目 `runtime/` 缺少与 core_snapshot 对齐的观测帧模块。
- **修复**：
  - 新增 `runtime/observation_frame.py`（ObservationFrame 定义）
  - 新增 `runtime/observation_builders.py`（build_empty_observation_frame、build_observation_frame）
- **结果**：`run_video_a3_trace.py --video test_video_complex_6m42s.mp4` 可正常跑完，处理 12048 帧，写入 `logs/a3_trace.jsonl`。

### 2.2 analyze_a3_trace 指标全为 None/0

- **现象**：Control mode / Frame quality 显示 100% None，Stability 与相关性为 0。
- **原因**：Trace 为 **obs + decision** 结构，分析器仅识别 **view + a3** 结构。
- **修复**：在 `tools/analyze_a3_trace.py` 中增加 `_norm_view(r)`、`_norm_a3(r)`，用 obs/decision 映射为 view/a3；缺失字段统一为 `"NONE"` 或 0。
- **结果**：分析器可正确统计 control_mode、frame_quality、path/branch 相关性；报表中不再出现 Python `None`，占比加总为 100%。

### 2.3 golden_bucket_report 各桶为 0

- **现象**：promote 后 cross_traffic 等桶仍显示 0 episodes。
- **原因**：报告只读 `golden_tags`，而 promote_to_golden 写入的是 `tags`。
- **修复**：`tags = meta.get("tags") or meta.get("golden_tags") or []`。
- **结果**：cross_traffic 等已晋升的 tag 能正确显示 episode 数量。

---

## 三、关键命令（可复现）

### 3.1 双长视频 A3 Trace

```bash
cd /Users/luanlei/Desktop/Luna-2

# 视频 1：6m42s
python3 tools/run_video_a3_trace.py --video test_video_complex_6m42s.mp4
python3 tools/analyze_a3_trace.py logs/a3_trace.jsonl

# 视频 2：6m14s（会覆盖 a3_trace.jsonl）
python3 tools/run_video_a3_trace.py --video test_video_follow_crowd_crossing_6m14s_60fps.mp4
python3 tools/analyze_a3_trace.py logs/a3_trace.jsonl
```

### 3.2 D0.1 Headless Parity（需已有 episode）

```bash
python3 tools/run_a3_headless_replay.py --base-dir library_store --version-tag v1.1 \
  --episode "v1.1/episodes/20260209/fake-session-001/SPEECH_12" --patch patches/empty_patch.json --out-dir outputs

python3 tools/test_a3_headless_parity.py --episode "v1.1/episodes/20260209/fake-session-001/SPEECH_12" \
  --base-dir library_store --candidate outputs/v1.1/headless_parity/SPEECH_12/empty_patch/candidate_decisions.jsonl \
  --out-dir outputs/v1.1/headless_parity/SPEECH_12/empty_patch

python3 tools/test_a3_headless_isolation.py
```

### 3.3 约束与可选 Guard

```bash
python3 tools/guard_sim_no_runtime_imports.py
python3 tools/guard_sim_no_library_store_writes.py
python3 tools/guard_a3_no_wall_clock.py   # 可选，仅 WARN
```

---

## 四、典型分析结果（6m42s 视频 trace）

- **总帧数**：36070 条 trace 记录（约 12048 帧处理 × 多记录/帧或历史累积）。
- **Control mode**：NONE 66.69%、ASSISTED 24.92%、GUARDED 8.40%。
- **Frame quality**：NONE 98.89%、DEGRADED 0.75%、GOOD 0.37%。
- **Stability**：view_confidence mean 0.005，motion_instability mean 0.001；control switches/min 0.00。
- **Path/Branch**：corr(path, motion) 0.845，corr(branch, path) 0.894，branch>0 占比 2.93%。
- **Correlations**（全量 trace）：motion–complexity_raw、vc–complexity_effective 约 -0.01（因约 66% 帧被填 0，稀释了原先仅在“有决策”帧上的强相关）。
- **ENGAGED**：本段无 engaged_signal 记录。
- **多模态冲突**：12011 次，selected_source 均为 TASK。

---

## 五、产物与约定

| 产物 | 路径/说明 |
|------|------------|
| A3 Trace | `logs/a3_trace.jsonl` |
| A3 指标 CSV/PNG | `logs/a3_metrics.csv`、`logs/a3_metrics.png` |
| Headless 候选决策 | `outputs/<version>/headless_parity/<episode_id>/<patch_stem>/candidate_decisions.jsonl` |
| Parity 报告 | 同上目录下 `parity_report.json` |
| 测试视频说明 | `docs/TEST_VIDEOS_5MIN_PLUS.md` |
| D2.2 对抗验证 | `docs/D2_2_RUNBOOK_ADVERSARIAL_VALIDATION.md`、`docs/D2_2_ADVERSARIAL_VALIDATION_AND_D2_3.md` |

---

## 六、后续建议

1. **Trace 相关性**：若需仅针对“有 A3 决策”的帧（control_mode != NONE）做稳定性/相关性统计，可在 analyze_a3_trace 中增加“仅有效决策帧”过滤选项。
2. **双视频**：对 6m14s 视频单独跑一遍 trace 并分析，可对比两段视频的 control/quality 分布与 path–branch 行为。
3. **D0.1 真实 parity**：用两条长视频跑 main 并落盘生成 episode（records.jsonl）后，再跑 run_a3_headless_replay + test_a3_headless_parity，验证 Patch=empty 时 candidate 与 baseline 一致。
4. **Golden Suite**：继续晋升更多 tag 的 episode，凑够 ≥10 条且含 HAS_CAUTION 样本后，再跑 blind_patch Suite 与 D2.3 入场判断。

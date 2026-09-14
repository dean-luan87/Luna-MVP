# STRESS_V2 Playbook

目标：从长 trace 中自动生成「连续高压段」slice episodes，用于触发 A3 决策分叉与 D1 区分度。

## 0. 产物与目录约定

- **工具**：`tools/stress_v2/trace_reader.py`、`tools/stress_v2/window_ops.py`、`tools/build_stress_segments_v2.py`、`tools/validate_stress_v2_quality.py`
- **输出**：`library_store/<version_tag>/episodes/<YYYYMMDD>/stress_v2_<trace_stem>/`
  - `slice_<id>/records.jsonl`：可回放 slice
  - `episodes.index.jsonl`：每条 slice 的 episode_id、路径、segment、rank_score、tags
  - `meta.json`：trace 路径、fps、percentile、hot_line、min_run、window_sec 等

## 1. 生成 Stress V2 slices

Trace 需为 `logs/a3_trace.jsonl` 格式（每行含 `obs` / `decision`；若含 `decision.debug` 则自动用 `weighted_sum_before_clamp` 作为高压信号）。

```bash
python3 tools/build_stress_segments_v2.py \
  --trace logs/a3_trace.jsonl \
  --base-dir library_store \
  --version-tag v1.1 \
  --percentile 95 \
  --min-run 2 \
  --window-sec 3 \
  --max-slices 12
```

输出目录示例：`library_store/v1.1/episodes/YYYYMMDD/stress_v2_a3_trace/slice_*/records.jsonl`。

## 2. 验收 Stress V2 质量

将下面命令里的 `YYYYMMDD` 换成实际输出日期（或查看终端打印的 `out_dir`）：

```bash
python3 tools/validate_stress_v2_quality.py \
  --episodes-dir library_store/v1.1/episodes/YYYYMMDD/stress_v2_a3_trace \
  --min-episodes 8 \
  --hot-percentile 95 \
  --min-hot-ratio 0.02 \
  --min-run 2
```

**验收通过条件**：

- 至少 8 条 slice 为 PASS；
- 每条 slice 内：`hot_ratio >= 2%`，且存在连续 hot 段长度 `>= 2`。
- `hot_line` 由 **slice 内部分布** 的 percentile 计算，不依赖全局固定阈值。

## 3. 推荐优先级

生成器会按「复合压力」排序窗口，优先保留：

- `complexity_raw` 高且 `branch_load > 0` 的窗口；
- 其次 `motion_instability` 高的窗口。

## 4. 加压（若验收仍不够「压」）

- 将生成器 `--percentile` 从 95 提到 99 或 99.5；
- 或将 `--window-sec` 从 3 增到 4。

示例：

```bash
python3 tools/build_stress_segments_v2.py \
  --trace logs/a3_trace.jsonl \
  --base-dir library_store \
  --version-tag v1.1 \
  --percentile 99 \
  --min-run 2 \
  --window-sec 4 \
  --max-slices 12
```

## 5. 用于 D1

当 stress_v2 通过质量门禁后，可将该 episodes 目录用于：

- D0.1 parity（empty_patch）；
- D1 三候选对撞（baseline / aggressive / conservative）；
- 观察 `diff_frames`、`early_gain`、`guarded_ratio_delta` 是否出现分叉。

若现有 `promote_to_golden` / `run_sim_suite` / `run_calib_three_candidates` 期望的是 `golden_stress_v2` 目录结构，可先做一步「从 episodes 目录晋升到 golden」的脚本，或把上述工具接成读 `episodes.index.jsonl` 与对应 `slice_*/records.jsonl`。

## 6. 一次性执行清单

假设 trace 为 `logs/a3_trace.jsonl`：

1. **生成 stress_v2 slices**

   ```bash
   python3 tools/build_stress_segments_v2.py \
     --trace logs/a3_trace.jsonl \
     --base-dir library_store \
     --version-tag v1.1 \
     --percentile 95 \
     --min-run 2 \
     --window-sec 3 \
     --max-slices 12
   ```

2. **质量验收**（将 `YYYYMMDD` 换成输出日期）

   ```bash
   python3 tools/validate_stress_v2_quality.py \
     --episodes-dir library_store/v1.1/episodes/YYYYMMDD/stress_v2_a3_trace \
     --min-episodes 8 \
     --hot-percentile 95 \
     --min-hot-ratio 0.02 \
     --min-run 2
   ```

3. 若需加压：将生成器改为 `--percentile 99`、`--window-sec 4` 后重新生成并再验收。

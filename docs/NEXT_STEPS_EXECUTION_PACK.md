# 下一步落地执行包（审计闭环）

## 第一步：Trace 分析双口径（已完成）

**改造**：`tools/analyze_a3_trace.py` 增加 `--active-only`，默认输出 ALL + ACTIVE 两段。

**验收命令**：
```bash
cd /Users/luanlei/Desktop/Luna-2
python3 tools/analyze_a3_trace.py logs/a3_trace.jsonl
python3 tools/analyze_a3_trace.py logs/a3_trace.jsonl --active-only
```

**验收要看**：
- 默认：先出现 `--- ALL ---`，再出现 `active_frame_ratio (ACTIVE/ALL): X/Y = Z%`，再出现 `--- ACTIVE ---`。
- `--active-only`：只输出 `active_frame_ratio` 和 `--- ACTIVE ---`。
- ACTIVE 下 `corr(motion_instability, complexity_raw)`、`corr(view_confidence, complexity_effective)` 保持结构性（约 0.9+），不被 0 填充稀释。
- `active_frame_ratio` 明确打印，作为后续 coverage 基础指标。

---

## 第二步：6m42s 生成真实 episode（做法）

**目标**：把 6m42s 视频跑出的 trace 转为 library_store episode，`records.jsonl` 内含 baseline decision（safety_level / control_mode / pal_lookahead_m）。

**做法**：主链路只写 `logs/a3_trace.jsonl`，不写 library_store。用工具 **trace_to_episode** 把已有 trace 转成 episode 并写入 library_store、追加 index。

**执行命令（按顺序）**：

```bash
cd /Users/luanlei/Desktop/Luna-2

# 1) 用 6m42s 跑主链路，生成 trace（若已有可跳过）
python3 tools/run_video_a3_trace.py --video test_video_complex_6m42s.mp4

# 2) 把 trace 转为 episode，写入 library_store 并追加 episodes_index.jsonl
python3 tools/trace_to_episode.py \
  --trace logs/a3_trace.jsonl \
  --base-dir library_store \
  --version-tag v1.1 \
  --date 20260212 \
  --session video-6m42s \
  --episode-id EPISODE_6M42S

# 3) 验收：analyzer 能读并产出 tags/tasks
python3 tools/run_episode_analyzer.py --base-dir library_store --version-tag v1.1 --out-dir outputs

# 4) 验收：explainer 能产出 explanations（OBS_V1 贯通）
python3 tools/run_episode_explainer.py --base-dir library_store --version-tag v1.1 --out-dir outputs
```

**可选**：trace 很长时可先限制条数试跑，例如 `--max-records 500`。

**验收要看**：
- 终端打印 `episode_rel_path`（如 `v1.1/episodes/20260212/video-6m42s/EPISODE_6M42S`）。
- `library_store/v1.1/episodes_index.jsonl` 多一行；`library_store/v1.1/episodes/<date>/video-6m42s/EPISODE_6M42S/` 下有 `records.jsonl`、`meta.json`。
- `run_episode_analyzer` 无报错，`outputs/v1.1/episode_tags.jsonl` 等有新 episode。
- `run_episode_explainer` 能对该 episode 产出 explanations。

---

## 第三步：D0.1 Parity（真实 episode）

**先决条件**：第二步已产出真实 episode 路径。

**执行命令**（将 `<真实episode相对路径>` 换成第二步得到的路径，如 `v1.1/episodes/20260212/session-6m42s/EPISODE_6M42S`）：
```bash
EP="<真实episode相对路径>"
EID=$(basename "$EP")

python3 tools/run_a3_headless_replay.py --base-dir library_store --version-tag v1.1 \
  --episode "$EP" --patch patches/empty_patch.json --out-dir outputs

python3 tools/test_a3_headless_parity.py --episode "$EP" --base-dir library_store \
  --candidate outputs/v1.1/headless_parity/$EID/empty_patch/candidate_decisions.jsonl \
  --out-dir outputs/v1.1/headless_parity/$EID/empty_patch
```

**首帧 parity 修复**（已落地）：`tools/a3_headless_adapter.py` 在 replay 时，若 `frame_quality == "NONE"` 则传 `view_confidence=1.0`，避免 vc=0 触发引擎强制 GUARDED，与 runtime 首帧 ASSISTED 对齐。修后 first_mismatch_seq 从 0 移至非首帧（如 53）。

**Parity 报告必须包含**（已实现）：
- `is_identical`：与 passed 一致，位一致为 true。
- `first_mismatch_seq`：首个不一致的 seq，无则 null。
- `mismatch_fields`：如 `safety_level`/`control_mode`/`pal_lookahead_m` 的 baseline vs candidate。
- `baseline_vs_candidate`：mismatch 帧的 baseline/candidate 关键字段并排。
- `virtual_time_source`：时间来自 records 的哪个字段、解析成功率。
- `float_policy`：当前为 `"strict"`（位一致）；浮点容差可后续加开关。

**判定**：**KPI = is_identical === true**。不成立则后续 D、Golden、blind_patch 均不可信；需根据 report 的 mismatch 区块做“除灵手术”（时钟债/状态泄露/精度漂移/provider 副作用）。若 first_mismatch_seq 非 0（如 53）：多为状态/时间差异（如 CAUTION vs SAFE、pal 10 vs 5），可查 `baseline_vs_candidate` 与 `obs_excerpt`，排查 virtual_ts 与 TTL/衰减是否与 runtime 一致。

---

## 第四步：Golden 切片化（已落地）

**目标**：从长视频 episode 自动切出“策略变化瞬间”±2s 窗口，晋升为 golden candidates。

**工具**：`tools/slice_episode_to_golden.py`。触发器：safety_level 变化、control_mode 切换、pal 连续下降、complexity 上升。

**执行命令**：
```bash
python3 tools/slice_episode_to_golden.py --base-dir library_store --version-tag v1.1 \
  --episode "v1.1/episodes/20260212/video-6m42s/EPISODE_6M42S" --out-dir outputs \
  --write-golden --max-slices 12 --tag-cross-traffic 2
```

**产出**：`outputs/v1.1/golden_candidates.jsonl`；`library_store/v1.1/golden/<slice_id>/`（records.jsonl + meta.json）。前 2 条 tag 为 cross_traffic，其余为 dynamic_object。

**验收**：triggers_found ≥1，slices_written ≥10，golden_dir 可被 run_sim_suite --golden 读取。

---

## 第五步：blind_patch 对抗验证（parity 通过后）

**先决条件**：第三步 parity 通过；Golden ≥10 条且至少 2 条 cross_traffic/迎面交叉类。

**执行**：
```bash
python3 tools/run_sim_suite.py --base-dir library_store --version-tag v1.1 \
  --golden --patch patches/blind_patch.json --out-dir outputs
python3 tools/audit_blind_patch_suite.py
```

**判定**：若 blind_patch 在 golden 上大面积 PASS，且将风险抹平（更 SAFE）且无缓解代理（early_gain/guarded_ratio/lookahead 变化）→ 冻结 D1，进入 D2.3（风险守恒）。

---

## 完整测试命令（一键串跑）

在项目根目录执行。若已有 `logs/a3_trace.jsonl` 且已做过 trace_to_episode，可从「第三步」开始；若已有 episode 且已做过 parity，可从「第四步」开始。

**完整版（含 6m42s 视频 → trace → episode，约 6 分钟视频处理 + 后续约 1 分钟）**：

```bash
cd /Users/luanlei/Desktop/Luna-2

# 1) 视频跑 trace（若无 trace 或需重录则执行；否则可注释）
python3 tools/run_video_a3_trace.py --video test_video_complex_6m42s.mp4

# 2) trace → episode
python3 tools/trace_to_episode.py \
  --trace logs/a3_trace.jsonl \
  --base-dir library_store \
  --version-tag v1.1 \
  --date 20260212 \
  --session video-6m42s \
  --episode-id EPISODE_6M42S

# 3) episode 分析与解释
python3 tools/run_episode_analyzer.py --base-dir library_store --version-tag v1.1 --out-dir outputs
python3 tools/run_episode_explainer.py --base-dir library_store --version-tag v1.1 --out-dir outputs

# 4) Parity（headless replay + 对比）
EP="v1.1/episodes/20260212/video-6m42s/EPISODE_6M42S"
EID="EPISODE_6M42S"
python3 tools/run_a3_headless_replay.py --base-dir library_store --version-tag v1.1 --episode "$EP" --patch patches/empty_patch.json --out-dir outputs
python3 tools/test_a3_headless_parity.py --episode "$EP" --base-dir library_store --candidate "outputs/v1.1/headless_parity/$EID/empty_patch/candidate_decisions.jsonl" --out-dir "outputs/v1.1/headless_parity/$EID/empty_patch"

# 5) Golden 切片
python3 tools/slice_episode_to_golden.py --base-dir library_store --version-tag v1.1 --episode "$EP" --out-dir outputs --write-golden --max-slices 12 --tag-cross-traffic 2

# 6) blind_patch sim suite + 审计
python3 tools/run_sim_suite.py --base-dir library_store --version-tag v1.1 --golden --patch patches/blind_patch.json --out-dir outputs
python3 tools/audit_blind_patch_suite.py --out-dir outputs/v1.1
```

**短线版（已有 episode，从 parity 起跑）**：

```bash
cd /Users/luanlei/Desktop/Luna-2
EP="v1.1/episodes/20260212/video-6m42s/EPISODE_6M42S"
EID="EPISODE_6M42S"

python3 tools/run_a3_headless_replay.py --base-dir library_store --version-tag v1.1 --episode "$EP" --patch patches/empty_patch.json --out-dir outputs
python3 tools/test_a3_headless_parity.py --episode "$EP" --base-dir library_store --candidate "outputs/v1.1/headless_parity/$EID/empty_patch/candidate_decisions.jsonl" --out-dir "outputs/v1.1/headless_parity/$EID/empty_patch"

python3 tools/slice_episode_to_golden.py --base-dir library_store --version-tag v1.1 --episode "$EP" --out-dir outputs --write-golden --max-slices 12 --tag-cross-traffic 2
python3 tools/run_sim_suite.py --base-dir library_store --version-tag v1.1 --golden --patch patches/blind_patch.json --out-dir outputs
python3 tools/audit_blind_patch_suite.py --out-dir outputs/v1.1
```

**验收要点**：`test_a3_headless_parity` 输出 `passed: True`；`run_sim_suite` 输出 `OVERALL: PASS`；`audit_blind_patch_suite` 打印审计点与 Suite 路径。

---

## 当前可立刻执行的最小动作

1. 已做：Trace 双口径 + parity_report 字段补全。
2. 下一步：用 6m42s 走主链路生成真实 episode（需确认/实现“视频→library_store”落盘）。
3. 用该 episode 跑一次 `run_a3_headless_replay` + `test_a3_headless_parity`，拿到 `parity_report.json` 的 `is_identical` 与 `mismatch_fields`/`baseline_vs_candidate`；若不通过，根据 mismatch 做除灵手术（时钟/状态/精度/副作用四选一）。

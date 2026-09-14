# D1 Tournament Phase 2（工业选拔闭环）

## 目标

新增 D1 Tournament 一键跑通：**候选生成 → suite 回放 → Gate（含 guardian_discipline）→ 词典序排名 → 输出冠军证据包**。

验收：在**固定 golden suite + 固定 seeds** 下连续跑 3 次，`champion_id` 必须一致；并生成 `rank_report.json` 与 `rank_report.md`。

## 目录结构

一次锦标赛运行后，`out-dir`（或 `out-dir/<ts>`）下结构示例：

```
outputs/d1_runs/<ts>/
├── candidates/
│   ├── baseline.json
│   ├── aggressive.json
│   ├── conservative.json
│   └── d1_candidate_000.json ... d1_candidate_022.json
├── candidates.jsonl
├── baseline/
│   ├── suite_report.json
│   └── patch.json
├── aggressive/
│   ├── suite_report.json
│   └── patch.json
├── ... (其余候选同上)
├── rank_report.json
├── rank_report.md
├── champion_bundle/
│   ├── champion_patch.json
│   ├── ep_<id>_scorecard.json
│   └── ep_<id>_gate_result.json  (top-3 最有信息 episode)
├── sim_out/           (run_sim_suite 中间输出)
└── simulations/       (各候选的 sim 输出)
```

## Lexicographic Objective（L0～L3）

- **L0（硬淘汰）**：`passed == True`，且 Gate 含 guardian_discipline；任一 episode 不通过即淘汰。
- **L1（守法）**：在通过 L0 的候选中，**最大化** `early_gain_weighted_mean`。
- **L2（冷静）**：**最小化** `event_metrics.delta.dwell_p95_delta`，再 **最小化** `volatility_mean`。
- **L3（不耽误事）**：**最小化** `efficiency.guarded_ratio_delta`（或 guarded_tail_ratio_delta）。

排名可解释：`rank_report.json` 中每个候选含 `aggregated` 与 `sort_reason`；`rank_report.md` 为表格 + 淘汰原因。

## 复现（3 条命令）

### 1）生成候选（由 tournament 内部调用，也可单独验证）

```bash
cd /Users/luanlei/Desktop/Luna-2
python3 -c "
from pathlib import Path
from simulation.d1.candidate_generator import generate_candidates
p, paths = generate_candidates(5, 'outputs/d1_runs/dev_smoke', seed=42, d1_run_id='dev_smoke')
print('candidates:', p, len(paths))
"
```

### 2）跑锦标赛（推荐用 golden_stress_v2 + recompute + base-patch 统一物理）

```bash
python3 tools/run_d1_tournament.py \
  --golden-suite library_store/v1.1/golden_stress_v2 \
  --n-candidates 5 \
  --seed 42 \
  --out-dir outputs/d1_runs/dev_smoke \
  --mode recompute \
  --base-patch patches/physics/stress_v2_phys_v1.json
```

- **--base-patch**：Base Physics Patch，与每个候选 merge 后作为 effective_patch 跑 A3（smoothing.* 等）；候选仍只允许 weights.*，禁止 smoothing.*（PATCH_SCHEMA_VIOLATION 淘汰）。
- 验收：终端应出现 `risk_used_max >= 0.38`、`high_risk_frames_count > 0`，以及 `effective_patch_smoothing` 摘要。

### 3）查看冠军与解释

```bash
cat outputs/d1_runs/dev_smoke/rank_report.md
cat outputs/d1_runs/dev_smoke/rank_report.json | head -80
ls outputs/d1_runs/dev_smoke/champion_bundle/
```

## 如何扩 bucket（low_light / crowded / reflection / narrow_passage）

- Golden suite 的 episode 通过 `meta.json` 的 `tags` / `golden_tags` 分桶；Gate 按 `REQUIRED_TAG_BUCKETS` 一票否决。
- 扩 bucket 步骤：
  1. 在 `tools/run_sim_suite.py` 的 `REQUIRED_TAG_BUCKETS` 中增加新 tag（如 `narrow_passage`）。
  2. 在 library_store 中准备带对应 tag 的 episode，并放入当前使用的 golden 目录（或 `--golden-suite` 指向的目录）。
  3. 重新跑 tournament，新 bucket 会参与 Gate 与排名。

## 关键数据（避免被 divergence_rate 带偏）

- **guardian_discipline.exit_latency_p95 / max**（红线）
- **guardian_discipline.hysteresis_efficiency**（红线）
- **early_gain_weighted_mean**（L1）
- **event_metrics.delta.dwell_p95_delta**（L2）
- **volatility_mean**（L2）
- **guarded_tail_ratio_delta** / **guarded_ratio_delta**（L3）

## 为何 rank 表里全是 0？

常见原因：

1. **replay 模式 + baseline (empty patch)**：baseline 与 candidate 用同一份 records，决策一致，early_gain / volatility / guarded_ratio_delta 自然为 0。
2. **recompute 但 episode 的 obs 多为空**：golden_stress_v2 等 trace 里很多帧是 `"obs": {}`，recompute 时 A3 收到 complexity=0，输出的 complexity_score 均 ≤ 0.38，没有“高风险帧”，`weighted_early_gain` 不可用；且决策一致时 `early_conservative_action_gain` 也为 0。
3. **event_metrics 为 0**：依赖 `decision.control_mode` 为 CAUTION/GUARDED；若 A3 在这些片段里多为 ASSISTED，则 dwell/event_count 为 0。

要看到**非零** early_gain_mean / dwell_p95_delta：需用 **obs 较完整**的 episode（每条 record 有 `obs.complexity`、`path`、`motion` 等），这样不同权重在 recompute 下会产出不同决策与 complexity_score，high_risk 帧和 early_gain 才有区分度。

## 回归测试

```bash
python3 -m pytest tests/test_d1_tournament_regression.py -v
```

断言：mock 下 `rank_candidates` 的 champion_id 与排序一致；L0 淘汰 gate 未通过候选；`rank_report.json` 含 `champion_id`、`ranked`、`eliminated` 及 `ranked[].aggregated` / `sort_reason`。

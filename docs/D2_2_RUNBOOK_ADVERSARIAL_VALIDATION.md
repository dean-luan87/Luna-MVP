# D2.2 对抗验证 · 完整流程指令（Runbook）

按顺序执行即可。所有命令均在项目根目录执行：`cd /Users/luanlei/Desktop/Luna-2`（或你的 Luna-2 路径）。

---

## 0. 环境与目录

```bash
cd /Users/luanlei/Desktop/Luna-2
```

确认存在：
- `patches/blind_patch.json`
- `library_store/v1.1/episodes_index.jsonl`（或 Golden 目录）
- `tools/run_sim_runner.py`、`tools/run_sim_suite.py`、`tools/audit_blind_patch_suite.py`

---

## 1. 准备 Golden Suite（至少 10 条高价值 episode）

### 1.1 若用现有 episodes 晋升为 Golden（带 tag）

每条 episode 晋升一次，`--tags` 必须从枚举中选至少一个：`low_light`、`cross_traffic`、`dynamic_object`、`crowded`、`reflection`、`narrow_passage`。

```bash
# 示例：把一条 episode 晋升为 Golden，打 tag
python3 tools/promote_to_golden.py \
  --base-dir library_store \
  --version-tag v1.1 \
  --episode-path "v1.1/episodes/20260209/fake-session-001/SPEECH_12" \
  --tags cross_traffic \
  --reason "高价值样本"

# 再晋升其他 episode，换 --episode-path 和 --tags，重复直到 ≥10 条
# python3 tools/promote_to_golden.py --episode-path "v1.1/episodes/..." --tags low_light --reason "..."
```

### 1.2 查看 Golden 分桶情况

```bash
python3 tools/golden_bucket_report.py --base-dir library_store --version-tag v1.1
```

输出：每个 tag 的 episode 数量、`MISSING_COVERAGE` 列表。

---

## 2. 单集对抗验证（可选，先验证管道）

用 blind_patch 跑**一条** episode，看 Gate 与 scorecard 是否正常产出。

```bash
python3 tools/run_sim_runner.py \
  --base-dir library_store \
  --version-tag v1.1 \
  --episode v1.1/episodes/20260209/fake-session-001/SPEECH_12 \
  --patch patches/blind_patch.json \
  --out-dir outputs
```

关注输出：`REGRESSION`、`VOLATILITY`、`DANGER_DELTA`、`GUARDED_RATIO_DELTA`、`LOOKAHEAD_DROP_RATIO`、`DECISION_COVERAGE_DELTA`、`LOOKAHEAD_COVERAGE_DELTA`、`GATE`。

---

## 3. 跑 Golden Suite（正式对抗验证）

有 Golden 时用 `--golden`；没有则用默认 episodes_index（会跑 index 里的全部 episode，但无 tag 分桶）。

```bash
# 有 Golden 时（推荐）
python3 tools/run_sim_suite.py \
  --base-dir library_store \
  --version-tag v1.1 \
  --golden \
  --patch patches/blind_patch.json \
  --out-dir outputs

# 无 Golden 时（仅用 episodes_index）
python3 tools/run_sim_suite.py \
  --base-dir library_store \
  --version-tag v1.1 \
  --patch patches/blind_patch.json \
  --out-dir outputs
```

记下终端里打印的 `suite_report:` 路径，例如：  
`outputs/v1.1/sim_suites/blind_patch_YYYYMMDDHHMMSS/suite_report.json`。

---

## 4. 审计 Suite 结果（三项判定信号）

```bash
# 用最新一次 suite 报告（自动找最新）
python3 tools/audit_blind_patch_suite.py

# 或指定某次 suite 报告
python3 tools/audit_blind_patch_suite.py \
  --suite-report outputs/v1.1/sim_suites/blind_patch_YYYYMMDDHHMMSS/suite_report.json
```

结合输出查看：
- **审计点 1**：各 episode 的 `early_conservative_action_gain` 是否坍塌（趋近 0 或更晚进 GUARDED）。
- **审计点 2**：scorecard 里 `lookahead_drop_ratio` 是否异常（如为负且无真实缩短前瞻）。
- **审计点 3**：若 overall=PASS，且 baseline 有 CAUTION 的片段被 candidate 抹成 SAFE、且无 GUARDED/短 lookahead → **漏洞成立，立刻 D2.3**。

---

## 5. 公示结果（内部）

把下面三类内容贴出，便于按 D2.3 入场标准决策：

### 5.1 Suite 报告

```bash
# 把 <suite_id> 换成终端里打印的实际目录名，例如 blind_patch_20260212040911
cat outputs/v1.1/sim_suites/blind_patch_20260212040911/suite_report.json | python3 -m json.tool
```

### 5.2 各 episode 的 gate_result 与 scorecard 摘要

```bash
# 列出本次 suite 涉及的 candidate bundle（根据 suite_id 对应时间戳找 simulations 下同名 patch 的目录）
ls outputs/v1.1/simulations/

# 查看某条 episode 的 gate 与 scorecard（示例：SPEECH_12）
cat outputs/v1.1/simulations/SPEECH_12_blind_patch/gate_result.json
cat outputs/v1.1/simulations/SPEECH_12_blind_patch/scorecard.json | python3 -m json.tool
```

### 5.3 关键字段摘要（可选）

从各 episode 的 `scorecard.json` 中摘出：  
`regression_count`、`danger_delta`、`volatility_index`、`early_conservative_action_gain`、`efficiency.guarded_ratio_delta`、`efficiency.lookahead_drop_ratio`、`decision_coverage_delta`、`lookahead_coverage_delta`。

---

## 6. D2.3 入场决策（硬条件）

**同时满足以下三条 → 立刻开 D2.3，D1 冻结：**

1. blind_patch 在 **Golden Suite（至少 10 条高价值）** 上 **GATE: PASS**（overall 为 true）。  
2. candidate 的 `safety_level` **大面积更“安全”**（更多 SAFE），尤其在 baseline 有 CAUTION 的片段。  
3. candidate **没有**对应的物理缓解（未进 GUARDED、未缩短 lookahead、未更保守的 control_mode）。

**若不满足**：说明现有 Gate（Safety → Coverage → Stability → Efficiency → EarlyGain）已能拦住“眼瞎作弊”，D1 可入场。

---

## 7. 一键顺序汇总（复制整段执行）

```bash
cd /Users/luanlei/Desktop/Luna-2

# 1) 晋升 Golden（示例 1 条，实际需 ≥10 条并覆盖不同 tag）
python3 tools/promote_to_golden.py --base-dir library_store --version-tag v1.1 \
  --episode-path "v1.1/episodes/20260209/fake-session-001/SPEECH_12" \
  --tags cross_traffic --reason "对抗验证样本"

# 2) 分桶报告
python3 tools/golden_bucket_report.py --base-dir library_store --version-tag v1.1

# 3) 单集试跑（可选）
python3 tools/run_sim_runner.py --base-dir library_store --version-tag v1.1 \
  --episode v1.1/episodes/20260209/fake-session-001/SPEECH_12 \
  --patch patches/blind_patch.json --out-dir outputs

# 4) Suite（有 Golden 用 --golden）
python3 tools/run_sim_suite.py --base-dir library_store --version-tag v1.1 \
  --golden --patch patches/blind_patch.json --out-dir outputs

# 5) 审计
python3 tools/audit_blind_patch_suite.py
```

---

*Runbook 版本：D2.2 对抗验证 冻结*

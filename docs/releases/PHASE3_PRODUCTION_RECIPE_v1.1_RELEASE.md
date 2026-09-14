# PHASE3_PRODUCTION_RECIPE v1.1 冻结验收报告

## Gate 表（step5_b2_freeze, det=3）

| seed | champion_id      | champion_eg | champion_vol | high_risk_frames_total | guarded_frames_total | det=3 hash 一致 |
|------|------------------|-------------|--------------|------------------------|----------------------|-----------------|
| 42   | conservative     | 4.1617      | 0.0000       | 61050                  | 186428               | 是              |
| 123  | conservative     | 4.1617      | 0.0000       | 60410                  | 186468               | 是              |
| 777  | d1_candidate_005 | 4.1617      | 0.0000       | 61200                  | 186372               | 是              |

- stress_summary_hash / regular_summary_hash 三 pass 一致；rank_key 均为 (4.1617, -0.0, -0.0)。

## 本版本变更点

- **B2 noop freeze**：view_conf_gate 回归点 floor=0.5、k=1.0（与旧逻辑等价），仅 responsive patch 启用。
- 修复 `summarize_b2_view_conf_grid.py` 列串位 + 增加 sanity check。
- 新增 `verify_b2_view_conf_replay.py`（--stats / --gate）用于 B2 生效留证。

## 回滚方式

- **回滚到 v1.0**：使用配方 `configs/personality/PHASE3_PRODUCTION_RECIPE_v1.json`，或 `git checkout phase3_production_recipe_v1`。
- **rollback 配方**：`configs/personality/PHASE3_PRODUCTION_RECIPE_v1.1_rollback.json` 指向 v1.0 与 tag。

## 回归哨兵（CI 阻断）

```bash
python3 tools/monitor_personality_regression.py
```

固定 seeds 42/123/777、pulse/sustain、regular 50ep、n=60、det=3；Gate 不通过则 exit 1。CI 中失败即阻断 merge。

---

## 附录：B2 生效证明（可选留证）

对**含 a3_debug（view_confidence / raw / raw_effective）**的 responsive 通道 replay 执行：

```bash
python3 tools/verify_b2_view_conf_replay.py --stats <replay_output.jsonl>
python3 tools/verify_b2_view_conf_replay.py --gate  <replay_output.jsonl>
```

- **--stats**：若 median/p90 view_conf 接近 1，则说明当前 suite 下 B2 无梯度（noop）。
- **--gate**：若 diff≈0，则说明 B2 gate 已参与计算，数据域不敏感。

**留证结论**：B2 网格 6 组 (floor,k) 指标完全一致，已证明在当前 suite 下 view_conf_gate 无梯度；接口已接入（responsive patch 含 view_conf_gate_floor/k），待低 view_conf suite 再启用。若后续 pipeline 写入 a3_debug 至 replay，可补跑上述命令做单次留证。

# D1 Phase 2：Weights 参与 Decision 重算 — 设计说明

## 1. 现状与目标

**当前（Phase 1 / passthrough）**  
- baseline 与 candidate 均使用 **golden record 的 decision**，同源 → 25/25 PASS，无区分度。  
- 目的：口径统一、实验室校准完成。

**Phase 2 目标**  
- **baseline**：用 **default weights** 经 A3 重算 decision。  
- **candidate**：用 **patched weights** 经 A3 重算 decision。  
- 两者来自**同一 A3 引擎**，仅 weights 不同 → 出现真实 **guarded_ratio / early_gain / volatility** 差异，Gate 开始区分性格。

---

## 2. 约束与原则

- **sim_runner 保持纯净**：不导入 `a3` / runtime，继续通过 `guard_sim_no_runtime_imports`。  
- **Presence-Only Contract 保留**：重算后仍做 decision / lookahead **presence 对齐**（不复制 baseline 数值，只保证有/无一致）。  
- **重算与回放解耦**：重算逻辑放在 **tools/**，由 `run_sim_suite` 按 `--mode` 选择调用。

---

## 3. 方案概览

| 组件 | 职责 |
|------|------|
| **sim_runner** | 不变。`mode=replay` 时继续 record passthrough + 统一宇宙 + Presence 对齐。 |
| **tools/run_sim_episode_recompute.py**（新增） | 读 records，用 A3HeadlessAdapter(weights) 逐帧 tick，写 replay_output.jsonl；weights-only 时对 candidate 做 presence 对齐。 |
| **run_sim_suite** | 新增 `--mode replay \| recompute`。recompute 时每 episode 调 `run_sim_episode_recompute` 代替 `sim_runner.run_episode`。 |
| **run_d1_tournament** | 可加 `--mode recompute` 透传；首轮建议 `--n-candidates 5` 做弹性验证。 |

---

## 4. 重算流程（单 episode）

```
1) Baseline
   - patch = {}（或 empty_patch.json）
   - adapter = A3HeadlessAdapter(base_config={}, patch_config={})
   - for each obs in records (OBS_V1):
        decision = adapter.tick(obs, virtual_ts=obs["ts"])
        replay_line = { seq, ts, decision: { safety_level, control_mode, pal_lookahead_m } }
   - 写入 baseline_bundle/replay_output.jsonl
   - 生成 baseline_bundle/frozen_risk_stream.jsonl（或由 presence_contract.build_presence_map 从 replay 生成）

2) Candidate
   - patch = 当前候选 patch（weights.*）
   - adapter = A3HeadlessAdapter(base_config={}, patch_config=patch)
   - for each obs:
        decision = adapter.tick(obs, virtual_ts=obs["ts"])
        # Presence 对齐：若 baseline 该帧无 decision → 不写；无 lookahead → 删字段；有 lookahead 且 candidate 无 → 补 null
        replay_line = apply_presence_contract(decision, presence_map[seq], baseline_replay_path)
   - 写入 candidate_bundle/replay_output.jsonl
```

Presence 对齐规则与当前一致：只改**有无**，不抄 baseline 数值；数值一律来自 A3 重算。

---

## 5. 接口约定

**run_sim_episode_recompute**（或同名函数）  
- 参数与 `sim_runner.run_episode` 对齐：`base_dir, version_tag, episode_rel_path, patch_path, out_dir, bundle_episode_id, baseline_bundle_path`。  
- 返回：本次 bundle 目录路径（与 run_episode 一致）。  
- 内部：  
  - 读 `records.jsonl`，筛 OBS_V1。  
  - 若 `baseline_bundle_path` 为空 → 视为 baseline 跑：patch 为空，A3 重算，写 replay + frozen stream。  
  - 若 `baseline_bundle_path` 非空 → 视为 candidate：加载 baseline 的 presence_map，A3(patch) 重算，每帧做 presence 对齐后写入。

**A3HeadlessAdapter**（已有）  
- `A3HeadlessAdapter(base_config, patch_config)`  
- `reset()`  
- `tick(obs_dict, virtual_ts)` → `{ seq, safety_level, control_mode, pal_lookahead_m }`  
- 由 `tools/a3_headless_adapter` 提供，在 tools 内导入 a3，不进入 simulation/。

---

## 6. run_sim_suite 改动要点

- 增加 `--mode`：`replay`（默认）/ `recompute`。  
- 若 `mode == "recompute"`：  
  - 对每个 episode 先调 `run_sim_episode_recompute(..., patch_path="", ...)` 得到 baseline_bundle；  
  - 再调 `run_sim_episode_recompute(..., patch_path=args.patch, baseline_bundle_path=baseline_bundle)` 得到 candidate_bundle；  
  - 后续 score / gate 不变，仍用 baseline_bundle 与 candidate_bundle 路径。  
- 若 `mode == "replay"`：保持当前逻辑，调用 `sim_runner.run_episode`。

---

## 7. 预期现象与首轮建议

**首次打开 recompute 后**  
- guarded_ratio / early_gain / volatility 会出现分布差异。  
- 可能只有少数候选 PASS（例如 3–5 个），或首轮全部 FAIL（权重范围过大），均属正常。  
- 需要观察：**guarded_ratio 是否拉开、early_gain 是否有梯度、volatility 是否可区分**。

**首轮建议（不跑满 25）**  
- 先跑 **5 个候选**：2 个偏激进（如 risk_density↑）、2 个偏保守（risk_density↓）、1 个随机。  
- 确认「系统对权重有弹性」后，再扩到 25。

---

## 8. 实现顺序建议

1. **新增 `tools/run_sim_episode_recompute.py`**  
   - 实现与 `run_episode` 同签名的重算函数（或直接产出 bundle 路径）。  
   - 内部用 A3HeadlessAdapter；candidate 分支用 presence_map 做 presence 对齐（可复用 presence_contract.build_presence_map + 当前对齐规则）。

2. **修改 `tools/run_sim_suite.py`**  
   - 增加 `--mode replay|recompute`；recompute 时用上述重算路径替代 `sim_runner.run_episode`。

3. **（可选）`run_d1_tournament`**  
   - 支持 `--mode recompute`、`--n-candidates 5`，便于首轮小规模验证。

4. **回归**  
   - `--mode replay` 下保持 25/25 PASS；  
   - `--mode recompute` 下跑 5 候选，检查 scorecard 中 guarded_ratio_delta / early_gain / volatility 是否有合理分布。

---

## 9. 与 Presence-Only / 统一宇宙的关系

- **Presence-Only**：Phase 2 仍生效，只保证「有无 decision / 有无 lookahead」与 baseline 一致，**数值 100% 来自 A3**。  
- **统一宇宙**：baseline 与 candidate 的**数据来源**统一为「同一 A3 引擎 + 同一 records」，仅 **weights** 不同；不再出现 stub vs record 的宇宙错位。

至此，D1 从「参数空间探索器」升级为「让参数真正影响物理行为」的进化系统。

---

## 10. 已落地骨架

- **docs/D1_PHASE2_RECOMPUTE_DESIGN.md**（本文）：设计说明与实现顺序。  
- **tools/run_sim_episode_recompute.py**：单 episode A3 重算入口，接口与 `sim_runner.run_episode` 对齐；baseline 用 A3(空 patch)，candidate 用 A3(patch) + presence 对齐；可单独跑一集验证：
  ```bash
  python3 tools/run_sim_episode_recompute.py --base-dir library_store --version-tag v1.1 \
    --episode v1.1/golden/slice_EPISODE_6M42S_complexity_rise_10_10 --out-dir outputs
  ```
  再跑 candidate（需先有 baseline bundle）：
  ```bash
  python3 tools/run_sim_episode_recompute.py ... --patch path/to/patch.json --baseline-bundle path/to/baseline_bundle
  ```

**待接**：`run_sim_suite --mode recompute` 中在每 episode 调用 `run_episode_recompute` 替代 `run_episode`；以及（可选）`run_d1_tournament --mode recompute --n-candidates 5`。

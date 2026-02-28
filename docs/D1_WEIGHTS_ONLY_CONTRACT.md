# D1 Weight-Only Replay Contract（冻结条款）

## 0. 问题与目标

**现状**：baseline（empty_patch）PASS，仅改 weights 的 patch 大量 FAIL，主要死在 COVERAGE_FAIL_LOOKAHEAD_LOSS、EFF_GUARDED_RATIO_DELTA。  
**根因**：baseline 与 candidate 的 replay 在“风险参考流/字段覆盖”上不同构，导致 coverage/efficiency 变成结构差异惩罚。  
**目标**：当 patch 只包含 `weights.*` 时，replay 输出与 baseline **同构**（decision/lookahead presence 一致），只允许权重影响 risk 聚合与决策映射。

---

## 1. is_weights_only_patch 规则（写死）

- **is_weights_only_patch(patch: dict) -> bool**  
  - 空 `{}` → **True**。  
  - 所有 key 必须以 **weights.** 开头；允许 **meta.** 但 meta 不参与 config。  
  - 任一 key 不以 `weights.` 或 `meta.` 开头 → **False**。

---

## 2. Weight-Only Replay Contract

当 **weights_only=True** 时：

1. **decision_coverage_ratio** 不因 patch 而下降（与 baseline 一致）。  
2. **lookahead_coverage_ratio** 不因 patch 而下降。  
3. candidate replay 使用 **baseline-frozen reference stream**，仅改变权重聚合；输出 presence 与 baseline 对齐。

实现要点：

- baseline 跑完后写出 **frozen_risk_stream.jsonl**（每帧 seq、has_decision、has_lookahead、control_mode、safety_level、pal_lookahead_m，平铺 JSONL）。  
- candidate 跑时（weights-only）：加载同 episode 的 frozen stream（FrozenFrame 按 seq），按帧**强制 presence 同构**：
  - **decision presence**：`ff.has_decision=False` → candidate 该帧不写 decision（空 dict）；`ff.has_decision=True` → candidate 必须写 decision（可标 decision_valid=false 占位）。  
  - **lookahead presence**：`ff.has_lookahead=True` → candidate 必须写 `decision.pal_lookahead_m`（v1：算不出则复制 `ff.pal_lookahead_m`，并标 `replay_meta.forced_lookahead=true`）；`ff.has_lookahead=False` → candidate 不得写 lookahead（置 null，forced_lookahead=false）。

---

## 3. 审计字段与 scorecard 暴露

每帧 replay 可带 **replay_meta**（仅审计，不参与 gate）：

- `weights_only_contract_applied`: bool  
- `frozen_stream_path`: str（绝对路径）  
- `forced_decision_presence`: bool  
- `forced_lookahead`: bool（本帧 lookahead 由 frozen 复制则 True）  
- `missing_frozen`: bool（该 seq 无 frozen 帧时为 True）

**scorecard**：在 **efficiency** 块中增加 **lookahead_forced_ratio** = `n_forced_lookahead / n_valid_frames`，用于暴露“被复制 lookahead”的比例，避免被误当作真实效率提升。顶层 scorecard 也保留同名字段便于读取。

---

## 4. 风险与退出策略

- 本契约用于 D0.1/D1 阶段建立**同构实验条件**，避免 COVERAGE_FAIL_LOOKAHEAD_LOSS / EFF_GUARDED_RATIO_DELTA 等结构误杀。  
- **forced_lookahead** 表示该帧 lookahead 来自 frozen 复制，不能当作最终效率结论；**lookahead_forced_ratio** 供 C 层排查。  
- **退出策略**：未来 D0.2/D1 成熟后，可逐步取消“复制 lookahead 值”，只保留 **presence 同构**（有/无 decision、有/无 lookahead 与 baseline 一致），再开放真实效率竞赛。

---

## 5. 实现位置

- `simulation/logic/risk_freeze_cache.py`：is_weights_only_patch、build_frozen_stream_from_baseline、load_frozen_stream  
- `simulation/sim_runner.py`：baseline 写 frozen；candidate weights-only 时加载 frozen 并同构输出；run_meta 中 weights_only_contract_applied、frozen_stream_path  
- `tools/run_sim_suite.py`：先跑 baseline → 生成 frozen → 再跑 candidate（传入 baseline_bundle_path）；per_episode 增加 weights_only_contract_applied、frozen_stream_path  
- `simulation/logic/scorer.py`：scorecard 增加 **lookahead_forced_ratio**  
- 验收：`tools/test_weights_only_contract.py`

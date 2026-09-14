# D1 Weight-Only Replay Contract（Presence-Only）

## 0. 设计冻结

**Contract 名称**：Weight-Only Replay Contract（Presence-Only）

**适用范围**：patch 仅包含 `weights.*`（允许空 patch 视为 baseline）。其余字段（如 `thresholds.*`、`meta.*` 等）一律不走合同。

**合同仅约束两件事**：

1. **decision 的 presence**：该帧是否应存在 decision 对象（有/无）。
2. **pal_lookahead_m 的 presence**：该帧在存在 decision 时，是否应存在 `pal_lookahead_m` 字段（有/无）。

**严格禁止**：

- 复制 baseline 的任何数值（包括 `pal_lookahead_m` 数值、`safety_level`、`control_mode` 等）。
- 用 baseline 的 decision 语义替 candidate 填坑。

---

## 1. 判定与 Presence Map

- **is_weights_only_patch(patch)**  
  - 空 patch → True（可应用合同；合同只对 candidate 生效）。  
  - 所有 key 以 `weights.` 开头 → True。  
  - 否则 → False。

- **PresenceMap**（只存布尔）：  
  - `has_decision[seq]`：baseline 该帧是否存在 decision 对象（`"decision" in rec and rec["decision"] is not None`）。  
  - `has_lookahead[seq]`：baseline 该帧在存在 decision 时是否存在 `pal_lookahead_m` 字段（`"pal_lookahead_m" in rec["decision"]`）。

- **build_presence_map(baseline_replay_path)**：读取 baseline 的 `replay_output.jsonl`，逐帧抽取上述布尔，返回 `{"has_decision": {seq: bool}, "has_lookahead": {seq: bool}}`。

---

## 2. Runner 合同执行规则（只做 presence 对齐）

对每个 seq：

**A) decision presence 对齐**

- 若 `presence.has_decision[seq] == False` → candidate 输出中**不写 decision**（或写空 `{}`，统一为“无 decision”）。
- 若 `presence.has_decision[seq] == True` 且 candidate 没有 decision → 写占位，并标记无效：
  - `"decision": { "decision_valid": false, "meta": { "forced_decision_presence": true } }`
- 若 `presence.has_decision[seq] == True` 且 candidate 有 decision → 保留 candidate 的 decision，可选写 `"meta": { "contract_applied": true }`。

**B) lookahead presence 对齐（只对齐字段存在性，不填数值）**

仅当 `presence.has_decision[seq] == True` 时讨论 lookahead：

- 若 `presence.has_lookahead[seq] == False` → candidate 若有 `pal_lookahead_m` 则**删除该字段**。
- 若 `presence.has_lookahead[seq] == True` 且 candidate 没有该字段 → **只补字段、值为 null**，并标记：
  - `"pal_lookahead_m": null`, `"meta": { "forced_lookahead_presence": true }`  
  - **绝不写入 baseline 的 pal_lookahead_m 数值。**

---

## 3. Scorer 口径（不被占位污染）

- **Coverage（Gate 用）**：按 **presence** 统计（有/无 decision 对象、有/无 `pal_lookahead_m` 字段），与 runner 输出结构一致，故 presence-only 对齐后 delta=0，不被误杀。
- **decision_valid_ratio** = `n_decision_valid / n_decision_present`（candidate）。
- **lookahead_presence_forced_ratio** = `forced_lookahead_presence_count / lookahead_present_count`。
- **lookahead_value_valid_ratio** = `count(pal_lookahead_m is not None) / lookahead_present_count`。
- **Efficiency 的 lookahead 指标**：仅在 `pal_lookahead_m != None` 的帧上计算；candidate 无有效 lookahead 时 lookahead_drop_ratio 不惩罚（视为 0）。

---

## 4. Gate（只做提示，不新增硬门禁）

在 PASS/FAIL 输出中附加 **warnings**（不改变通过条件）：

- `decision_valid_ratio` 明显低于 baseline（如 > 2%）→ **WARN_DECISION_VALIDITY_DROP**
- `lookahead_value_valid_ratio` 很低（如 < 0.8）→ **WARN_LOOKAHEAD_VALUE_MISSING**
- `lookahead_presence_forced_ratio` 很高（如 > 0.5）→ **WARN_LOOKAHEAD_PRESENCE_FORCED_HIGH**

便于 C 层识别“结构对齐但语义产出不足”的可疑候选。

---

## 5. 实现位置与验收

- **simulation/logic/presence_contract.py**：`is_weights_only_patch`、`build_presence_map`
- **simulation/sim_runner.py**：weights-only candidate 时加载 baseline presence_map，按规则做 decision/lookahead presence 对齐，禁止复制任何数值
- **simulation/logic/scorer.py**：coverage 按 presence 统计；decision_valid_ratio、lookahead_presence_forced_ratio、lookahead_value_valid_ratio；efficiency lookahead 仅有效值帧
- **simulation/logic/gate.py**：上述 warnings 附加到 reasons
- **tools/test_weights_only_presence_contract.py**：三用例（baseline vs weights-only；非 weights patch；恶意 candidate 占位 + warning）

验收：`python3 tools/test_weights_only_presence_contract.py` 通过；回归 suite 预期不再集体死于 coverage/guarded_ratio_delta=1.0。

---

## 10. 统一 Replay 宇宙（D0.1 passthrough 阶段）

在「weights 尚未参与 decision 重算」的 passthrough 阶段，baseline 与 candidate 必须 **decision 同源**，否则会出现 stub 宇宙 vs record 宇宙的错位（如 guarded_ratio_baseline=0、guarded_ratio_candidate=1、delta=1.0）。

**规则**：baseline 也使用 golden record 的 decision，不注入 `_apply_reference_risk` stub。candidate（weights-only）使用同一 record + Presence-Only 对齐。这样 `guarded_ratio_baseline == guarded_ratio_candidate`，delta=0，Gate 不再误杀。

**实现**：`sim_runner` 中 baseline/empty 分支不再调用 `_apply_reference_risk`；仅非 baseline 且 decision 为空时才用 stub 填坑（如 blind_patch 等）。

**后续**：进入「weights 真正参与 decision 重算」阶段时，baseline 须用 default weights 重算，candidate 用新 weights 重算，两者同源来自同一 A3 引擎，再比较 guarded_ratio。

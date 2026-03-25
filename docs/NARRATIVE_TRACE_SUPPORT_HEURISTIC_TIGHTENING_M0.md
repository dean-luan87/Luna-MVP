# Narrative-Trace Support Heuristic Tightening Sprint M0（nt 专项收紧）

**文件**：`docs/NARRATIVE_TRACE_SUPPORT_HEURISTIC_TIGHTENING_M0.md`  
**产物**：`logs/narrative_trace_tightening_analysis_m17.json`  
**本轮声明**：本轮**不是**扩场景、**不是**规则升级、**不**改 benchmark/triage、**不**改主骨架、**不**改 recheck/mainline 行为、**不**再 tightening `lg`、**不**给 advisory/soft-fail 接自动 gate。

本轮只做一件事：**只针对 `narrative_trace_support_tension`（nt）收紧启发式**，目标是让它从“几乎失敏”变成“**有区分力、可解释、不乱响**”。

补记：已进入 **Real Scenario Pack M1.8** 场景验证（见 `docs/REAL_SCENARIO_PACK_M1_8_DELIVERY.md` 与 `logs/real_scenario_pack_m18.json`）。
补记：已完成 **NT Coordination Review M0**（见 `docs/NT_COORDINATION_REVIEW_M0.md` 与 `logs/nt_coordination_m18_analysis.json`），确认 nt 当前以“薄证据叙事观察器”角色阶段可用。

---

## §1. 当前问题复盘：为什么 nt 长期几乎恒 `none`

### 1.1 直接原因（硬门槛）

旧实现中存在硬门槛：

- 当 `eff_events >= 18`（`structured_event_count` 与 `timeline_event_count` 的最大值）时，直接返回：
  - `narrative_trace_support_tension = none`
  - reason = `structured_events_plentiful_relative_to_narrative`

在真实包中，多数 case 的 `event_count / timeline` 都稳定处在这个“plentiful”区间，导致 **nt 失去梯度**。

### 1.2 启发式缺陷：把“事件多”误等同于“关键语义被支撑”

`event_count` 与 `timeline events` 的**数量**本身无法区分：

- “杂事件很多，但关键转折/关键锚点不足”
- “关键转折足够，叙事与证据同步”

这会把 “事件存在” 误当成 “关键证据充分”，从而让 **R81** 这类“故事顺、证据薄”的意图样本也仍落在 `none`。

### 1.3 为什么不是“样本不够多”的问题

`m17` 已有 99 个 `ctx_json` 样本（`R3` snapshot 另计），但 nt 仍几乎全 `none`。这说明问题是 **启发式结构**（硬门槛与特征选择）而不是扩包数量。

---

## §2. 专项目标（写死）

### 目标 1：nt 开始有梯度

不再是“几乎全 none”，而是出现：

- 一些可信的 **`low`**（对应 **watch**）
- 少量可信的 **`medium`**（对应 **review**）

### 目标 2：抓“关键语义支撑薄弱”，不是抓“事件少”

核心从：

- 事件数量（event_count）  

转向：

- **关键锚点**是否足以支撑长叙事（例如 timeline 中 `high/medium` importance 的关键事件锚点）

### 目标 3：不把正常复杂样本打爆

复杂场景允许：

- 事件多且关键锚点足够 → 仍保持 `none`
- 仅少量 borderline → `low` 而非大面积 `medium/high`

---

## §3. Tightening 方案（实现点与边界）

### 3.1 修改范围（限定）

- 优先只改：`decision_monitor/narrative_evidence_tension_review.py`（仅 nt 维度）
- 配套：
  - 新增单测：`tests/test_narrative_trace_support_tightening.py`
  - 新增 smoke：`tools/smoke_narrative_trace_support_tightening.py`
  - 新增分析脚本：`tools/analyze_narrative_trace_tightening_m17.py`

### 3.2 新启发式的核心变化

1. **移除硬门槛**：删除/绕开 “`eff_events >= 18 ⇒ nt=none`” 的一刀切逻辑。  
2. **引入关键锚点**：从 `reasoning_timeline_view.events` 中抽取 `event_importance in {high, medium}` 的事件作为 **key anchors**（`key_n`）。  
3. **保守分段**（长叙事才触发）：
   - `narr_len >= 900` 且 `key_n <= 9` → `nt=medium`（review）
   - `narr_len >= 900` 且 `key_n == 10` → `nt=low`（watch）
   - `key_n >= 11` 且 `narr_len >= 600` → `nt=none`（关键锚点足够，避免误报）

说明：

- 本轮仍保留原本的“叙事/事件比值极端异常”分支（`ratio` 极端且 `eff_events` 很低时可直接 `medium/high`），以覆盖“事件真的为 0/极少”的极端薄证据场景。
- 本轮不追求 `high` 大量出现；`high` 仍主要留给“事件极少+叙事很长”的极端薄证据情况。

---

## §4. tightening 前后分布对比（m17）

数据来源：`logs/narrative_trace_tightening_analysis_m17.json`（`before/after` 均为 `default_real_cases()` 的 `ctx_json` 重建 frame 统计）。

### 4.1 nt 分布

- **tightening 前**：`none = 99`（**全 none**，无梯度）
- **tightening 后**：
  - `none = 75`
  - `low = 11`
  - `medium = 13`

结论：**nt 已开始出现梯度**，且仍保持“多数 none”的保守形状。

### 4.2 关键锚点（timeline high/medium）分布（背景）

`timeline_hi_event_count` 分布保持不变（tightening 不改主链，仅改解释）：

- `9:13 / 10:11 / 11:60 / 12:15`

tightening 的作用是：把这条分布从“nt 恒 none”变成“在 key anchors 偏薄时点亮 nt”。

---

## §5. 代表 case 对比（抽样）

> 代表 case 的细表请以 `logs/narrative_trace_tightening_analysis_m17.json` 的 `top_thin_evidence_candidates` 为准。

### 5.1 健康复杂样本（应保持 none / 轻微 low）

示例：`R87_complex_but_healthy_resume_and_global_progress_real`  
预期：不应被默认打成 `medium/high`。  
结果：单测约束为 `none/low`（保守允许 watch，但禁止默认 review）。

### 5.2 应升到 watch（low）的样本

示例：`key_n == 10` 的样本族（见分析 JSON 的 after 分布）。  
启发式理由：`slightly_thin_key_anchors_for_long_narrative(key=10,types=10)`。

### 5.3 应升到 review（medium）的样本

示例：`R1_container_real`（after 中可见）  
结果：`nt=medium`；reason：`thin_key_anchors_for_long_narrative(key=9,types=9)`。

说明：本轮的 “review” 仍是 **建议核对**，不是 failure；其价值是让 nt 从“完全无信号”变成“少量可解释信号”。

---

## §6. 误报风险评估（必须回答）

### 6.1 是否把大量正常复杂叙事都打亮？

**没有**：tightening 后 `none=75/99` 仍是多数；仅 `low+medium=24/99` 被点亮。

### 6.2 是否出现“为了制造信号而制造噪声”？

当前策略仍偏保守：

- 只在 `narr_len >= 900` 的长叙事上触发 key-anchors 逻辑
- key anchors 足够（`>=11`）则直接回落 `none`

因此信号主要集中在“关键锚点偏薄”的尾部样本，未出现全局泛化点亮。

---

## §7. 测试与 smoke

- **单测**：`tests/test_narrative_trace_support_tightening.py`  
  - 覆盖：薄锚点样本应点亮；健康复杂样本不乱亮（不默认 medium/high）
- **smoke**：`tools/smoke_narrative_trace_support_tightening.py`  
  - 产物：`logs/smoke_narrative_trace_support_tightening.jsonl`

---

## §8. 最终问题（逐条回答）

1. **tightening 后 nt 是否有区分力？** **是**（从 `none=99` → 出现 `low/medium`）。  
2. **是否出现可信的 watch/review？** **是**（`low=11`、`medium=13`，且有可读 reason）。  
3. **误报是否可控？** **当前可控**（多数仍 `none`；健康复杂样本不默认 `medium/high`）。  
4. **是否还需要再做一轮 nt 专项？** **可能需要一轮**（下一轮应从“key anchors 数量”进一步转向“关键语义锚点覆盖”，避免仅以数量作为 proxy）。  
5. **是否适合回到扩包验证（M1.8/下一批）？** **可以**：nt 已具备最小梯度，可在下一批扩包中观察其在更复杂样本上的稳定性与误报边界。

---

## §9. 本轮是否适合作为 nt 专项收口文档

**适合。** 有：问题复盘 → 启发式变更点 → tightening 前后分布 → 代表样本 → 风险评估 → 测试与 smoke → 明确回答。

---

## §10. 本轮是否通过

**通过。**


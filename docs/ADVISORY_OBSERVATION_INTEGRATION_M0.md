# Advisory Observation Integration M0

**文件**：`docs/ADVISORY_OBSERVATION_INTEGRATION_M0.md`

## §1. 本轮定位

1. **把 SF-1′ advisory / review 高风险候选**从「文档与 pack 摘要」推进到**工程观察层可稳定读取、聚合、展示、落地**。  
2. **只给提示权，不给裁决权**：**不**接 benchmark、**不**接 hard-fail、**不**改 triage、**不**改主链 closure、**不**改 recheck、**不**触发自动 gate/block/defer。  

依据：`docs/ADVISORY_REVIEW_GATE_DRAFT_M0.md`、`docs/SOFT_FAIL_CANDIDATE_DRAFT_M0.md`、`docs/SOFT_FAIL_CANDIDATE_VALIDATION_PACK_M0.md`、`docs/REAL_SCENARIO_PACK_M1_6_DELIVERY.md`。

**场景验证进展**：整包已推进至 **`Real Scenario Pack M1.7`**（`docs/REAL_SCENARIO_PACK_M1_7_DELIVERY.md`，`logs/real_scenario_pack_m17.json`），用于在更多 ctx 上重复确认 **SF-1′ 边界** 与 **frame 顶层观察** 的一致性。

---

## §2. 为什么现在接入

已具备：条款（SF-1′）→ 验证（Validation Pack）→ 模式复盘 → advisory/review gate 草案。  
现在缺口是：**工程链路可见性**（frame/JSONL/聚合器/Console/Viewer 可读），以支撑后续自治层与多轮退化态验证。

---

## §3. 最小对象定义（frame 顶层）

字段对象：**`advisory_review_observation`**

- `soft_fail_candidate_observed`（bool）
- `soft_fail_candidate_clause_id`（str，当前仅 `SF-1-prime`）
- `soft_fail_candidate_level`（str，当前 `high_risk_candidate|none`）
- `soft_fail_candidate_reason_summary`（str）
- `review_gate_recommended`（bool）
- `advisory_only`（bool，**恒 true**）
- `advisory_review_observation_applied`（bool）

说明：仅用于**记录/展示/人工 review**；不参与任何自动裁决。

---

## §4. 工程接入点

### 4.1 builder（只读构造）

- 文件：`decision_monitor/advisory_review_observation.py`
- 构造点：`decision_monitor/builder.py`（在 `run_summary_reference` + `post_processing_summary_entry` + `narrative_evidence_tension_review` 之后）

### 4.2 frame / JSONL

`DecisionMonitorFrame.to_dict()` 使用 `asdict`，顶层字段会随 JSONL 落地。

### 4.3 aggregator（Console 聚合）

`tools/reasoning_console_aggregator.py` 扁平输出：

- `advisory_soft_fail_candidate_observed`
- `advisory_clause_id`
- `advisory_review_gate_recommended`
- `advisory_reason_summary`

### 4.4 Console / Viewer

- `tools/reasoning_console_server.py`：新增独立 **Advisory / Review** 区块（明确不参与判定）。  
- `tools/decision_monitor_viewer.py`：新增卡片与专家模式展开段落。

---

## §5. 权限边界（硬句）

### 当前拥有

- 可记录、可展示、可进入人工 review、可进入交付文档「高风险候选区」、可为 future gate 提供基础信号。

### 当前不拥有

- 不导致 fail；不导致 block/defer；不修改 benchmark；不改变 triage；不改主链 closure；不触发自动运行态切换。

---

## §6. 测试与 smoke

- 单测：`tests/test_advisory_observation_integration.py`（正样本命中、近邻/健康不误标、框架字段仍可用）。  
- smoke：`tools/smoke_advisory_observation_integration.py`（构帧→JSONL→聚合器可读）。  

---

## §7. 本轮是否通过

**通过。** SF-1′ 已进入工程观察层，并在 Console/Viewer/聚合链路可见；仍保持 **advisory-only**（提示权，无裁决权）。

---

## 主线—白盒—日志 串联检查

- **A 主线**：advisory 仅派生、只读，不改决策。  
- **B 白盒**：advisory 与同帧 `run_summary` / tension 可对齐。  
- **C 日志**：JSONL 与 Console 聚合均可回溯。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**。


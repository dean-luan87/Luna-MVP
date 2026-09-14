# Advisory / Review Gate Draft M0

**文件**：`docs/ADVISORY_REVIEW_GATE_DRAFT_M0.md`

## 一、文档定位

1. **不是** benchmark / triage 规则修改，**不是** hard-fail，**不是**主链拍板、recheck 行为或冻结基线边界的改写。  
2. **是**在已通过 **Validation Pack** 验证边界的 **SF-1′**（见 `docs/SOFT_FAIL_CANDIDATE_DRAFT_M0.md`）之上，定义其作为 **review / advisory 层**的**工程使用草案**：**提示权**，**无裁决权**。  
3. **本轮**：以**文档与语义口径**为主；**不**强制代码落地、**不**做人审系统实现、**不**做大改版 UI。

**依据**：`docs/SOFT_FAIL_CANDIDATE_DRAFT_M0.md`、`docs/SOFT_FAIL_CANDIDATE_VALIDATION_PACK_M0.md`、`logs/soft_fail_candidate_validation_m0.json`、`docs/CRITICAL_CANDIDATE_PATTERN_REVIEW_M0.md`。

---

## 二、SF-1′ 在系统里属于什么（必须写清）

| 角色 | 是 / 否 |
|------|---------|
| 正式失败（harness / 基线缺陷） | **否** |
| benchmark 计分或 pass/fail 规则 | **否** |
| 主链治理动作（block / defer 主链） | **否** |
| **人审高风险候选条款** | **是** |
| **review / advisory 层信号** | **是** |

**一句话**：SF-1′ 是**已验证边界的、可命名的高风险语义标签**，用于**引导人看哪里**；**不**改变机器对单次运行的**正式裁定**。

**模式名（工程复述）**：**`resume_fragility_with_global_main_stall`**（见 Critical Pattern Review）。

---

## 三、它应该在哪里出现（推荐落点与优先级）

**不要求本轮全部接代码**；以下为**推荐层级**与**落地顺序**（见 **§七** 排序）。

| 落点 | 作用 | 本轮状态 |
|------|------|----------|
| **交付文档 / 人工 review 模板** | 命中时在「高风险候选 / advisory」小节勾选或引用 | **首选，可立即使用** |
| **`run_summary_reference` 之后的 review 层摘要**（解读文字） | 与 `process_observation`、`task_chain_progress_summary` 同帧叙述 | **文档约定**；实现可为附录句 |
| **`post_processing_summary_entry` 旁路 advisory** | 与 `narrative_readable` 并行，**不**回写主链 | **预留语义**（§五） |
| **Console / Viewer review 区块** | 工程侧一眼可见 **advisory_only** | **次优**；不接判定 |
| **日志 / JSONL / pack 衍生字段** | `candidate` 标记可回溯、可 diff | **可与** `validate_soft_fail_candidate_clause_m0.py` **同构** |

**禁止落点**：benchmark `_compute_pass`、triage `priority_score` 的硬条件、任何「自动 fail / block」分支。

---

## 四、它触发后应该做什么（与不应该做什么）

### 应该

- **触发人工 review 提示**（模板 §八）。  
- **触发 advisory 标注**（交付与日志用语一致）。  
- **进入交付文档「高风险候选 / advisory」区域**（与正式失败**分栏**）。  
- **进入 `TENSION_REVIEW_TEMPLATE_AND_SOFT_FAIL_SPEC_M0.md` §5 人工模板**（勾选 `soft_fail_candidate` 时**对照** SF-1′）。

### 不应该

- **不**自动 fail、**不**自动 block / defer、**不**自动改写主链 closure / outcome。  
- **不**改变 harness 通过与否、**不**改变 triage 排序规则。  
- **不**替代 `baseline_covered_defect` / `baseline_excluded_requirement` / `reserve_only_finding`。

---

## 五、最小 advisory / review 语义字段（草案，供 future 工程参考）

**说明**：下列为**口径草案**；本轮**不**强制写入 schema 或控制台 API。

| 字段（建议名） | 类型（建议） | 含义 |
|----------------|---------|------|
| `soft_fail_candidate_observed` | bool | 当帧是否满足 SF-1′ **必要条件**（与验证脚本逻辑可对齐） |
| `soft_fail_candidate_clause_id` | str | 固定 **`SF-1′`** 或 **`resume_fragility_with_global_main_stall`** |
| `soft_fail_candidate_level` | str | 建议固定 **`advisory`**（与 future `gate` 档位区分） |
| `soft_fail_candidate_reason_summary` | str | 短句：**pc∧lg + rsr + tcp token** 是否存在；可附 **exclusion** 未成立 |
| `review_gate_recommended` | bool | **建议**进入人工 review；**不**表示必须停机 |
| `advisory_only` | bool | **恒为 true**（M0 阶段），表示**仅提示、不裁决** |

**可选**：`soft_fail_candidate_evidence_refs`（list）：如 `case_id`、`trace_anchor_id`、`summary_post_processing_entry_id`，便于审计回溯。

---

## 六、权限边界（硬句）

### SF-1′ **当前拥有**的权限

- **可以被记录**（文档、日志、未来 frame 字段）。  
- **可以被展示**（Console / Viewer 作 advisory 区块）。  
- **可以进入人工 review 模板**与**交付文档高风险候选区**。  
- **可以作为** future **review gate / advisory gate** 的**语义基础**（仍不接自动执行）。

### SF-1′ **当前不拥有**的权限

- **不能**直接导致 **fail**。  
- **不能**直接导致 **block** / defer（主链）。  
- **不能**直接改变主链 **closure** / 拍板结果。  
- **不能**直接进入 **benchmark 分数**或 pass/fail 规则。  
- **不能**替代**三类正式问题分类**（冻结口径）。

---

## 七、推荐接入层级（已排序）

### 第一优先级：**文档 / review 模板**

- **成本最低**、**立即可用**、**不污染**现有评测规则。  
- 动作：在 **`TENSION_REVIEW_TEMPLATE_AND_SOFT_FAIL_SPEC_M0.md` §5** 与交付 checklist 中增加 **「若命中 SF-1′ → 勾选 advisory，并填 reason_summary」**。

### 第二优先级：**Console / Viewer advisory 展示**

- **便于**日常工程观察与回放对齐。  
- 动作：在树/时间轴旁**轻量区块**展示 §五 字段（**只读**）；**不参与**树 issue 颜色与 harness。

### 第三优先级：**post-processing / review gate 预留接口**

- **供**下一里程碑 **optional** 写入 `post_processing_summary_entry` 侧车或 reserve 结构。  
- 动作：**仅**定义 §五 语义；**不接**自动治理、**不回写**摘要正文事实。

---

## 八、人工 review 模板如何使用 SF-1′

### A. 命中 SF-1′ 时，重点看什么

1. **`phase_closure_outcome_tension`（pc）** 与 **`local_global_progress_tension`（lg）**：是否**同帧 raw high**（与 severity `critical_candidate` 一致）。  
2. **`run_summary_reference.resume_chain_fragility_summary`** 是否为 **`resume_declared_but_main_not_progressed`**。  
3. **`task_chain_progress_summary`** 是否含 **`global_main_progress_not_terminal_complete`**。  
4. **健康排除**是否成立：**`terminal=found` 且无全局未收口 token**、**`pc=none`**、**`lg=medium`** 等（见草案 §五、Validation Pack 矩阵）。

### B. 交付文档怎么写

- **单列**：**「advisory / 人审高风险候选（SF-1′）」**。  
- **禁止**写为「基准缺陷已确认」除非另走 **`baseline_covered_defect`** 证据链。  
- **可写**：「建议人工对照主链 phase / resume / 全局推进是一句否一致。」

### C. 当前系统**不**做什么

- **不 fail**、**不 block**、**不重判 benchmark**、**不改 triage 公式**。

---

## 九、与现有文档的职责划分

| 文档 | 职责 |
|------|------|
| `SOFT_FAIL_CANDIDATE_DRAFT_M0.md` | **条款本体**（SF-1′ 必要条件与排除）。 |
| `SOFT_FAIL_CANDIDATE_VALIDATION_PACK_M0.md` | **边界是否干净**（命中率 / 误伤率）。 |
| `CRITICAL_CANDIDATE_PATTERN_REVIEW_M0.md` | **模式稳定性**（7/7 同族与命名）。 |
| **`ADVISORY_REVIEW_GATE_DRAFT_M0.md`（本文）** | **在系统里如何用**——**提示权、无裁决权**；落点、权限、模板与接入顺序。 |

---

## 十、与验证结论的衔接

**M1.6 场景观察**：整包 **`logs/real_scenario_pack_m16.json`** 已附带 **`advisory_sf1_prime_audit`**；本轮扩包中 **SF-1′ 与 `critical_candidate` 集合完全一致（9=9）**，近邻与健康样本 **未**误命中（见 **`docs/REAL_SCENARIO_PACK_M1_6_DELIVERY.md`**）。

**此前验证**（`logs/soft_fail_candidate_validation_m0.json`）：固定矩阵下 **SF-1′ 边界干净**，正样本 **7/7** 命中，近邻与健康样本 **未**误标。  

**工程接入**：已完成 **Advisory Observation Integration M0**（`docs/ADVISORY_OBSERVATION_INTEGRATION_M0.md`）：SF-1′ 已进入 **frame 顶层 + JSONL + aggregator + Console/Viewer** 的观察链路（仍为 **advisory-only**）。
在此前提下，**允许**将 SF-1′ **提升为**「**可进入 review / advisory 层的工程使用草案**」，**仍不**赋予裁决权。

---

## 十一、本轮是否通过

**通过。** 已形成 advisory/review gate **使用层**草案；**未**接 benchmark、**未**接 hard-fail、**未**改 triage / 主链 / 冻结口径、**未**扩新场景。

---

## 主线—白盒—日志 串联检查

- **A 主线**：SF-1′ **不**改变主链决策，**不**进入 harness。  
- **B 白盒**：提示字段若落地，须与 **同帧** `run_summary` / tension **可读对齐**。  
- **C 日志**：回溯可与 `validate_soft_fail_candidate_clause_m0.py` 输出同构。  
- **D 最终判断**：**主线通顺，白盒一致，日志已落地**（现行以验证 JSON + 本文为准）。

# Luna 中台消费蜂巢建议规范 v1

> **本文性质**：定义中台在收到蜂巢建议后，如何**接入、审核、决策、执行、留痕**，并在不越权前提下转为中台可执行动作。  
> **不解决**：蜂巢如何评分、图书馆如何提炼经验、个体 Luna 如何调用模型。  
> **历史专题补充**：`../model_platform/LUNA_MODEL_PLATFORM_MIDPLATFORM_HIVE_CONSUMPTION_V1.md`。  
> **占位代码**：`mid_platform/model_governance/governance/model_recommendation_intake_record.py`、`model_governance_decision_record.py`（无自动消费/自动改配置逻辑）。

**一句话**：**蜂巢负责提建议，中台负责决定建议是否、何时、以何种限制条件生效。**

---

## 一、文档定位

1. **什么是 recommendation consumption**  
   中台侧将 `HiveModelRecommendation` 纳入**治理链**的一整套流程：接收 → 审核 → 决策 → 执行 → 留痕与可回滚。

2. **它解决什么问题**  
   在「建议 ≠ 命令」的前提下，把蜂巢输出转成**可审查、可约束、可回滚**的中台动作，避免建议直接改线上状态。

3. **它不解决什么**  
   - **不定义**蜂巢评分逻辑（见 `LUNA_HIVE_SCORE_AND_RECOMMENDATION_SPEC_V1.md`）。  
   - **不定义**图书馆经验提炼逻辑（见 `LUNA_LIBRARY_EXPERIENCE_INTERFACE_SPEC_V1.md`）。  
   - **不定义**个体 Luna 主执行链如何调模型（个体在治理链之下消费结果）。

---

## 二、为什么中台不能直接照单全收蜂巢建议

- 蜂巢是**评分/建议方**，不是**执行方**。  
- 建议可能**证据不足**或与当前运行态**冲突**。  
- 建议可能**过于激进**，需要 shadow 或人工确认。  

**收束**：**蜂巢建议是输入，不是命令。**

---

## 三、recommendation consumption 在整体架构中的位置

**上游输入**

- `HiveModelRecommendation`  
- `HiveModelScoreRecord`（证据主链）  
- 可选：`LibraryExperiencePackage`  
- 当前：`ModelRegistryCard`、`ModelRoutePolicy`、`ModelFallbackPlan` 等运行态快照（概念上）

**下游输出**

- `ModelGovernanceDecisionRecord`（**必须**）  
- 实际配置变更：`registry` 状态、route policy、fallback plan、shadow / mainline / background 等（**仅**在决策与执行层通过后）

**一句话**：recommendation consumption 是**蜂巢与中台之间的治理接口层**。

---

## 四、消费链四层结构

### 4.1 接收层

**职责**

- 收下蜂巢建议对象  
- 校验**结构完整性**  
- 校验**引用对象是否存在**（如 `model_id`、`based_on_score_record_id`）  
- 写入 **intake record**

**本层只解决**：这条建议**有没有资格进入审核**。

**建议对象**：`ModelRecommendationIntakeRecord`

---

### 4.2 审核层

**职责**

- 建议类型是否合法、是否在允许集合内  
- 目标模型是否已注册、建议是否指向合法范围  
- `suggested_action` / `suggested_constraints` 是否**越权**  
- 是否命中**治理红线**  
- 证据是否充分（样本量、score record、图书馆材料等）

**本层只解决**：这条建议**能不能进入中台决策**。

---

### 4.3 决策层

**职责**：对建议表态（见第八节固定五类）。

**本层解决**：中台**准备如何处理**这条建议（采纳方式与附加条件）。

---

### 4.4 执行层

**职责**

- **实际**修改 registry / policy / allowed scope / status（仅当决策允许）  
- 写入 **`ModelGovernanceDecisionRecord`**  
- 生成**回滚计划**（见第十三节）  
- 标记**后续复核**（见第十四节）

**本层解决**：被采纳的建议如何**落地**。

---

## 五、输入对象定义

**必需输入**

- `HiveModelRecommendation`  
- `HiveModelScoreRecord`（与 `based_on_score_record_id` 对齐）

**可选辅助输入**

- `LibraryExperiencePackage`  
- 当前 `ModelRegistryCard`、`ModelRoutePolicy`、`ModelFallbackPlan`（快照或引用）

**必须写清**

- **recommendation 不得脱离 score record 单独「生效」**；中台必须能**追溯**建议的证据链。  
- 无 score record 关联的 recommendation，接收层应拒绝或标记为**证据不足**进入审核。

---

## 六、接收层规则

**必须检查**

- `recommendation_id` 唯一且可追踪  
- `model_id` 在 registry 中存在  
- `based_on_score_record_id` 对应 score record 存在  
- `recommendation_type` 在允许集合内（与蜂巢规范枚举对齐）  
- `suggested_action` 非空（或规范允许的显式「无动作」占位）  
- `suggested_constraints` **可解析**（结构化，非随意自然语言冒充）

**输出对象：`ModelRecommendationIntakeRecord`**

| 建议字段 | 含义 |
|----------|------|
| `intake_record_id` | intake 记录主键（建议独立 ID） |
| `recommendation_id` | 蜂巢建议 ID |
| `model_id` | 对象模型 |
| `intake_status` | 如 `received`、`rejected_structure`、`pending_review` |
| `intake_timestamp` | 接收时间 |
| `intake_note` | 备注（拒绝原因、缺字段说明等） |

---

## 七、审核层规则

**审核维度**

1. **合法性**：`recommendation_type`、动作与约束是否在预定义集合内、是否与组织策略一致。  
2. **证据充分性**：score record、样本量、图书馆材料是否支撑建议强度。  
3. **越权**：建议是否试图直接切主模型、直接改 fallback、放宽安全规则、绕过 governance gate 等。  
4. **当前状态兼容性**：当前 registry / policy 是否允许执行（维护窗、冲突中的变更等）。

**审核结果建议枚举**

- `eligible_for_decision`  
- `needs_more_evidence`  
- `blocked_by_policy`  
- `requires_human_review`  

---

## 八、决策层规则

**决策结果固定五类**

| 结果 | 含义 |
|------|------|
| `accept` | 按建议方向执行（在预定义动作集内落实） |
| `accept_with_constraints` | 接受方向，但**附加**中台约束 |
| `accept_partial` | 仅采纳建议的**一部分** |
| `defer` | 延后：继续观察，**本阶段不执行**配置变更 |
| `reject` | 明确不采纳 |

**必须写清**：五类均需写入 **`ModelGovernanceDecisionRecord`** 的 `decision_result`（或等价映射 + 理由）。

---

## 九、执行层动作类型

中台**真正能做的动作**须来自**预定义集合**，禁止 recommendation 直接塞入未登记的自由文本动作。

**建议固定动作**（示例，可与实现枚举对齐）：

- `promote`  
- `degrade`  
- `restrict_scope`  
- `expand_scope`  
- `force_shadow`  
- `retire`  
- `tune_governance`  
- `observe_more`  

**必须写清**：执行层仅允许将蜂巢建议**映射**到上述（或扩展后登记）动作；**不得**执行未知动作类型。

---

## 十、一票高风险建议处理规则

**高风险建议类型**（示例）

1. 主模型切换  
2. fallback 路径变更  
3. 安全规则放宽  
4. 跨主体权限扩张  
5. 曾阻断模型未经充分验证进入主链  

**处理要求**

- **不得**直接 `accept`  
- 至少 `accept_with_constraints` 或 `defer`  
- 可强制要求 **shadow 验证**、**人工确认**  

---

## 十一、约束条件模板

`suggested_constraints`（来自蜂巢）与 `decision_constraints`（中台决策）均应为**结构化**键值，示例：

- `mainline_forbidden`  
- `shadow_only`  
- `background_only`  
- `allowed_task_domains` / `forbidden_task_domains`  
- `max_timeout_ms`  
- `requires_additional_validation`  
- `requires_shadow_validation`  

**说明**：不能只写无结构的自由文本充当「约束」。

---

## 十二、决策记录对象

**对象名**：`ModelGovernanceDecisionRecord`

| 建议字段 | 含义 |
|----------|------|
| `decision_record_id` | 决策记录主键 |
| `recommendation_id` | 对应蜂巢建议 |
| `model_id` | 对象模型 |
| `decision_result` | 对应第八节五类之一 |
| `decision_reason` | 可审计理由 |
| `decision_constraints` | 中台最终约束 |
| `decision_timestamp` | 决策时间 |
| `effective_scope` | 生效范围说明 |
| `rollback_plan` | 回滚描述或引用 |
| `requires_followup_review` | 是否需要复核 |
| `notes` | 备注 |

**必须写清**：**所有**消费建议的终态（含 reject/defer）都应形成 decision record 或等效审计记录；**无记录，不算治理动作成立**。

---

## 十三、回滚原则

- 凡**采纳并执行**、且改变了治理状态的建议，须具备**回滚计划**（描述或自动化回滚引用）。  
- 回滚至少应能恢复语义上的：**registry 状态、route policy、allowed scope、fallback 配置**（以组织实现为准）。  

**一句话**：**可执行的建议，必须可回滚。**

---

## 十四、后续复核机制

以下场景建议**强制复核**：

- 主模型变更  
- fallback 变更  
- shadow → mainline  
- restricted → expanded  

**可选字段**：`requires_followup_review`、`followup_review_window`（时间窗）。

---

## 十五、和白盒的关系

白盒**不裁决** recommendation，但应能**观察**：

- 建议是否被接收、是否拒绝/延后/采纳  
- 模型当前是否处于 `shadow_only`、`background_only`、`restricted`、`deprecated_candidate` 等**可展示状态**

**一句话**：**白盒负责看见 recommendation 的命运，不负责替中台拍板。**

---

## 十六、和图书馆的关系

- recommendation **可引用**图书馆经验包作为**证据**。  
- 中台可要求图书馆**补充证据**（流程上，非图书馆直接改配置）。  
- **图书馆不能**替 recommendation **生效**或绕过中台执行治理动作。

---

## 十七、样例

### 样例 1：带约束采纳

- 蜂巢：`recommendation_type = restrict_scope`  
- 中台：`accept_with_constraints`，约束为 **`shadow_only=true`**，暂不收紧主链  

### 样例 2：延后采纳

- 证据：样本不足或 score record 置信度低  
- 中台：`defer`，`decision_reason` 写明「继续观察」，并设 `requires_followup_review=true` 或复核窗口  

---

## 十八、与其他文档的关系

| 文档 | 关系 |
|------|------|
| `LUNA_HIVE_SCORE_AND_RECOMMENDATION_SPEC_V1.md` | recommendation 与 score record 来源 |
| `LUNA_MODEL_REGISTRY_CARD_SPEC_V1.md` / `LUNA_MODEL_TASK_CARD_SPEC_V1.md` | registry / 任务卡语义 |
| `LUNA_LIBRARY_EXPERIENCE_INTERFACE_SPEC_V1.md` | 图书馆证据接口 |

---

## 十九、结尾收束句

**中台消费蜂巢建议的核心原则，不是「快」，而是「可审查、可约束、可回滚」；任何建议要想改变 Luna 的模型治理状态，都必须先通过这条消费链。**

---

## 附录 A：与当前代码骨架的对照（v1）

| 对象 | 代码 | 说明 |
|------|------|------|
| `ModelRecommendationIntakeRecord` | `governance/model_recommendation_intake_record.py` | 当前为**最小字段**（`recommendation_id`、`model_id`、`recommendation_type`、`intake_status`、`intake_timestamp`）；规范中的 **`intake_record_id`、`intake_note`** 等建议后续扩展 |
| `ModelGovernanceDecisionRecord` | `governance/model_governance_decision_record.py` | 已含 `decision_record_id`、`decision_constraints`、`rollback_plan`、`requires_followup_review` 等；**完整四消费层编排逻辑**不在占位代码中，须由中台服务实现 |

---

## 附录 B：导航（历史专题）

- `../model_platform/LUNA_MODEL_PLATFORM_MIDPLATFORM_HIVE_CONSUMPTION_V1.md`  

# Luna 模型任务卡规范 v1

> **本文性质**：讲清「在某个**具体任务**上，模型负责什么、吃什么、怎么加工、吐什么、怎样算合格、失败后怎么办」；**不讲**模型全局身份与全局治理边界（那是注册卡），**不讲**模型全局优劣评分（那是蜂巢）。  
> **历史专题补充**：`../model_platform/LUNA_MODEL_PLATFORM_TASK_CARD_V1.md`（可与本文对读）。  
> **代码最小骨架**：`mid_platform/model_governance/schemas/model_task_card.py`（字段为**子集**，扩展以本文为准逐步对齐）。

**一句话**：注册卡管「模型身份与治理边界」；任务卡管「模型职责与交付标准」。

---

## 一、文档定位

1. **什么是模型任务卡**  
   模型任务卡是 **「模型 × 任务」维度**的职责定义对象：描述**某一模型在某一任务**上的输入、加工、输出、合格标准与失败处理。

2. **它解决什么问题**  
   同一模型可承担多任务；不同任务的契约与质量标准不同。任务卡让「这次调用**该做什么、不该做什么**」可被约束、被验证、被白盒解释，并让蜂巢/图书馆能**按任务维度**归因与评分输入。

3. **它不解决什么问题**  
   - **不替代注册卡**：不描述模型身份、部署、主链准入与全局治理红线。  
   - **不替代蜂巢评分对象**：不负责模型优劣的**全局判断**。

---

## 二、为什么必须有模型任务卡

- 一个模型可能承担**多个任务**。  
- 不同任务的输入输出与质量标准**不同**。  
- **没有任务卡**：无法定义「在该任务上模型到底做什么」；白盒难以解释「本次调用的职责边界」；图书馆与蜂巢难以**按任务**归因与构造评分输入。

**收束**：注册卡让模型**可被识别**；任务卡让模型**可被约束地使用**。

---

## 三、任务卡在中台中的位置

- 任务卡属于 **注册与路由层** 与 **治理层** 之间的**桥接定义对象**（任务维度的契约与边界）。

**上接**：`ModelRegistryCard`（须绑定已存在的 `model_id`）。  

**下接**：route selector、validator / governance policy、usage / quality / governance records、蜂巢评分输入中的**任务维度**字段。

**关系一句话**：一张注册卡可绑定**多张**任务卡；任务卡是注册卡在**任务维度**上的职责展开。

---

## 四、任务卡字段总览（分组）

| 组别 | 说明 |
|------|------|
| 1. 任务身份字段 | 哪张卡、哪模型、哪任务域、归属主体 |
| 2. 任务职责字段 | 目标、负责、边界、不负责 |
| 3. 输入字段 | 来源、契约、必填/可选、预处理、上下文依赖 |
| 4. 加工字段 | 模式、约束、禁止行为、治理要求 |
| 5. 输出字段 | 契约、字段、下游、是否对用户可见、是否须校验 |
| 6. 质量字段 | 成功/失败标准、指标、阈值、fallback 行为 |
| 7. 观测与记录字段 | 三类记录是否强制、白盒可见度、归档 |

---

## 五、任务身份字段

| 字段 | 含义 |
|------|------|
| `task_card_id` | 任务卡主键 |
| `model_id` | 指向注册卡 `model_id` |
| `task_name` | 人可读任务名 |
| `task_code` | 稳定任务代码（与路由/统计对齐） |
| `task_domain` | 任务域（与 route policy、蜂巢任务维度对齐） |
| `task_owner_scope` | 任务归属主体范围 |

**约束说明**

- **`task_card_id`**：全局唯一；记录与白盒可引用。  
- **`model_id`**：必须指向**已存在**的 `ModelRegistryCard`，**禁止**悬空引用。  
- **`task_domain`** 示例：`long_voice_task_parse`、`vision_semantic_interpretation`、`response_language_rendering`、`library_failure_attribution`、`hive_strategy_suggestion` 等（枚举可扩展）。  
- **`task_owner_scope`**：`individual_luna` / `library` / `hive` / `mid_platform` —— 标明这张任务卡属于哪个**主体范围**，用于约束调用链与输出形态。

---

## 六、任务职责字段

| 字段 | 含义 |
|------|------|
| `task_goal` | 本任务卡要达成的目标 |
| `task_responsibility` | 应产出什么、解决什么问题 |
| `task_boundary` | 允许处理到哪一步 |
| `task_non_responsibility` | **显式**列出不负责什么 |

**必须写清**

- **`task_non_responsibility` 是关键字段**：必须显式写「不负责什么」，否则任务边界不成立。

**本章收束**：任务卡必须同时写清「负责什么」和「不负责什么」。

---

## 七、输入字段

| 字段 | 含义 |
|------|------|
| `input_sources` | 输入来源类型列表 |
| `input_contract` | 输入侧契约标识 |
| `input_required_fields` | 缺则**不可执行** |
| `input_optional_fields` | 缺失不致命，可提升质量 |
| `input_preprocessing` | 进模型前必须做的加工说明 |
| `context_dependencies` | 依赖哪些上下文；**禁止**无限制吃满上下文 |

**说明**

- **`input_sources`** 示例：长文本、视觉摘要、OCR 结果、历史记忆摘要、图书馆经验包、当前任务链摘要等。  
- **`input_preprocessing`** 示例：文本裁剪、摘要压缩、敏感字段去除、历史信息拼接规则等。

---

## 八、加工字段

| 字段 | 含义 |
|------|------|
| `processing_mode` | 处理模式 |
| `processing_constraints` | 加工约束列表 |
| `processing_forbidden_behaviors` | 禁止行为列表 |
| `governance_requirements` | 治理要求（schema、风险、fallback 等） |

**说明**

- **`processing_mode`** 示例：`single_pass`、`candidate_generation`、`analysis_only`、`multi_stage`。  
- **`processing_constraints`** 示例：只允许结构化输出、只允许候选生成、不允许自由叙述、不允许自补全缺失事实等。  
- **`processing_forbidden_behaviors`** 示例：不允许越权放行、不允许自我审核、不允许直接修改任务链、不允许替代治理规则等。  
- **`governance_requirements`** 示例：必须经 schema 验证、必须经风险检查、必须允许 fallback 等。

---

## 九、输出字段

| 字段 | 含义 |
|------|------|
| `output_contract` | 输出契约标识（须指向明确结构） |
| `output_required_fields` | 输出必填字段 |
| `output_optional_fields` | 输出可选字段 |
| `output_downstream_consumers` | 下游消费方 |
| `output_is_user_facing` | 是否对用户可见 |
| `output_requires_validation` | 输出是否必须经过校验 |

**必须写清**

- **`output_contract`**：须指向**明确结构**，不允许把「自由文本默认可用」当作默认主路径（除非任务类型显式允许且已注册）。  
- **`output_downstream_consumers`** 示例：`validator`、`builder`、`response renderer`、`library ingest`、`hive ingest`。  
- **`output_is_user_facing`**：用户可见输出与系统内部候选必须区分。  
- **`output_requires_validation`**：默认建议为 **true**；生产类任务卡不得默认跳过验证。

---

## 十、质量字段

| 字段 | 含义 |
|------|------|
| `success_criteria` | 怎样算成功 |
| `failure_criteria` | 怎样算失败 |
| `quality_metrics` | 质量指标列表 |
| `minimum_acceptance_threshold` | 最低可接受阈值（可选档位或数值语义） |
| `fallback_behavior` | 失败后的去向语义 |

**说明**

- **`success_criteria`** 示例：JSON 合法、schema 完整、主域判断正确、mixed 保留成功、clarification 候选合理等。  
- **`failure_criteria`** 示例：timeout、非 JSON、缺关键字段、候选冲突、非法映射、越权输出等。  
- **`quality_metrics`** 示例：validator 通过率、mixed 保留率、clarification 命中率、unsupported 判断质量、平均耗时等。  
- **`fallback_behavior`** 示例：规则链、clarification、reject、备份模型等（须与注册卡/路由策略可对齐）。

---

## 十一、观测与记录字段

| 字段 | 含义 |
|------|------|
| `usage_record_required` | 是否每次执行必须写 usage |
| `quality_record_required` | 是否必须写 quality |
| `governance_record_required` | 是否必须写 governance（阻断/降级等） |
| `whitebox_visibility_level` | 白盒可见度 |
| `archive_requirement` | 归档要求 |

**必须写清**

- **`usage_record_required`**：建议默认 **true**。  
- **`quality_record_required`**：生产类、审核类建议默认 **true**（按组织策略调整）。  
- **`governance_record_required`**：建议默认 **true**。  
- **`whitebox_visibility_level`** 示例：`minimal` / `standard` / `detailed`。  
- **`archive_requirement`** 示例：`none` / `sampled` / `always`。

---

## 十二、必填字段与非必填字段清单

### 必填（准入最低集合）

至少须包含：

- `task_card_id`、`model_id`、`task_name`、`task_domain`  
- `task_goal`、`task_responsibility`、`task_boundary`、`task_non_responsibility`  
- `input_contract`、`input_required_fields`  
- `processing_mode`、`processing_constraints`  
- `output_contract`、`output_required_fields`  
- `success_criteria`、`failure_criteria`  
- `fallback_behavior`  

（`task_code`、`task_owner_scope` 等在工程化落地时**强烈建议**必填，与注册表校验一并固化。）

### 非必填（示例）

- `input_optional_fields`、`output_optional_fields`  
- `archive_requirement`、`minimum_acceptance_threshold`  
- `notes`（若规范版本支持）

---

## 十三、字段约束规则（交叉规则）

以下为**示例规则**；校验实现应结合**关联注册卡**的 `role_type` 等字段（从 `ModelRegistryCard` 读取，而非在任务卡重复存一份冲突的 role）。

1. 若 `output_is_user_facing = true`，则须：  
   - `output_requires_validation = true`  
   - 且关联模型的 **`role_type` 不得为纯 `evaluation`**（评估类不得默认直出用户面，除非组织单独豁免并留痕）。  
2. 若 `task_owner_scope = hive`，则不得：  
   - `output_is_user_facing = true`（蜂巢任务不应默认产生用户可见最终输出）。  
3. 若 `task_owner_scope = library`，则不得：  
   - 直接输出**可执行**的最终动作候选作为线上执行依据（经验材料 ≠ 治理动作）。  
4. 若 `processing_mode = candidate_generation`，则输出语义须明确：  
   - **候选 ≠ 最终动作**（须在契约或字段说明中可区分）。  
5. 若 `fallback_behavior` 为空或未定义，则任务卡**不准通过校验**。  

---

## 十四、任务卡样例

### 样例 1：长语音任务拆解

- **输入**：长文本 + 上下文摘要（`input_sources` / `input_contract` 对齐）  
- **输出**：结构化契约如 `VoiceLongInputStructuredParseResult`（示例名，以实际契约为准）  
- **职责边界**：**不负责**最终执行与用户面回复（写在 `task_non_responsibility`）  

### 样例 2：语言表达 / 渲染

- **输入**：已确认的**系统结论**（非让模型改结论）  
- **输出**：用户可读文本（`output_is_user_facing = true` 时须配 `output_requires_validation = true`）  
- **不负责**：更改系统结论或绕过治理（`task_non_responsibility`）  

### 样例 3：图书馆失败归因

- **输入**：历史记录、失败片段摘要  
- **输出**：经验归因**候选**（供图书馆加工，不直接当下线治理）  
- **不负责**：线上路由、主模型切换、强制治理动作（`task_non_responsibility`）  

样例目的：**一眼会填**，不要求贴满所有字段。

---

## 十五、任务卡注册流程

**最小流程**：

1. 创建任务卡草案  
2. **校验 `model_id`** 在注册表中存在  
3. **字段完整性**校验（必填、类型、枚举）  
4. **职责边界**校验（尤其 `task_non_responsibility`）  
5. **校验 `fallback_behavior`** 与注册卡/路由语义可衔接  
6. 写入 **task card registry**  
7. **变更留痕**（见第十六节）

---

## 十六、任务卡变更规则

**高风险变更**（须评审 + 留痕，禁止静默），包括但不限于：

- `task_domain`、`task_goal`、`task_boundary`、`task_non_responsibility`  
- `input_contract`、`output_contract`  
- `fallback_behavior`  

**中风险**：`processing_mode`、`output_downstream_consumers`、`quality_metrics` 等。  

**低风险**：备注类字段（仍建议审计日志）。

---

## 十七、和其他文档的关系

| 文档 | 关系 |
|------|------|
| `LUNA_MODEL_REGISTRY_CARD_SPEC_V1.md` | 模型身份与治理边界 |
| `LUNA_MODEL_RESPONSIBILITY_ISOLATION_V1.md` | 职责分离与红线 |
| `LUNA_HIVE_SCORE_AND_RECOMMENDATION_SPEC_V1.md` | 蜂巢评分与建议对象 |
| `LUNA_LIBRARY_EXPERIENCE_INTERFACE_SPEC_V1.md` | 图书馆经验接口 |
| `LUNA_MODEL_MID_PLATFORM_CONSTITUTION_V1.md` | 总纲 |

---

## 十八、结尾收束句

**任务卡决定模型在某一具体任务上可以做什么、不可以做什么，以及做成什么样才算合格；没有任务卡的模型，最多只是可调用能力，不是可治理任务单元。**

---

## 附录 A：与当前代码骨架 `ModelTaskCard` 的对照（v1）

以下字段已在 `mid_platform/model_governance/schemas/model_task_card.py` 实现（**最小子集**）：  
`task_card_id`、`model_id`、`task_name`、`task_code`、`task_domain`、`task_goal`、`task_responsibility`、`task_boundary`、`task_non_responsibility`、`input_sources`、`input_contract`、`input_required_fields` / `input_optional_fields`、`processing_mode`、`processing_constraints`、`processing_forbidden_behaviors`、`output_contract`、`output_required_fields` / `output_optional_fields`、`output_downstream_consumers`、`success_criteria`、`failure_criteria`、`quality_metrics`、`fallback_behavior`。

**本文档列出的其余字段**（如 `task_owner_scope`、`input_preprocessing`、`context_dependencies`、`governance_requirements`、`output_is_user_facing`、`usage_record_required`、`whitebox_visibility_level` 等）为 **规范 v1 完整形态**；后续迭代应扩展代码、`from_dict` 默认值策略与注册校验，并与本文同步版本号。

---

## 附录 B：导航（历史专题）

- `../model_platform/LUNA_MODEL_PLATFORM_TASK_CARD_V1.md`：历史任务卡专题，可与本文交叉引用。

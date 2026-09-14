# Luna 图书馆经验接口规范 v1

> **本文性质**：定义图书馆如何**接收、提炼、验证、打包**经验，以及与**个体 Luna、蜂巢、中台**之间的**接口边界**（吃什么、做什么、吐什么、不能做什么）。  
> **不解决**：中台如何治理模型、蜂巢如何评分、个体 Luna 当前轮如何执行任务。  
> **历史专题补充**：`../model_platform/LUNA_MODEL_PLATFORM_LIBRARY_POSITION_AND_INTERFACE_V1.md`。  
> **占位代码**：`mid_platform/model_governance/library/`（无自动提炼/自动验证逻辑）。

**一句话**：**图书馆负责经验加工，不负责治理执行。**

---

## 一、文档定位

1. **什么是图书馆经验接口**  
   图书馆作为 **经验加工层**，对外暴露的输入/输出约定：接收结构化材料、产出经验记录/经验包/验证记录，并向蜂巢与中台供给**可引用证据**。

2. **它解决什么问题**  
   把「噪声日志」与「可复用、可验证、可解释的经验材料」分开；让蜂巢与中台能吃到**高纯度材料**，而不是堆栈 dump。

3. **它不解决什么**  
   - **不定义**蜂巢评分逻辑（见 `LUNA_HIVE_SCORE_AND_RECOMMENDATION_SPEC_V1.md`）。  
   - **不定义**中台治理与建议消费逻辑（见 `LUNA_MID_PLATFORM_RECOMMENDATION_CONSUMPTION_SPEC_V1.md`）。  
   - **不定义**个体 Luna 当前轮任务裁决与主链编排。

---

## 二、为什么图书馆不能只是存储层

- 原始日志**不能**直接进入治理链。  
- 个体经验 **≠** 可复用经验；偶发错误 **≠** 普遍规律。  
- 没有**提炼、验证、打包**，经验无法稳定复用。  
- 蜂巢与中台需要的是**高纯度经验材料**，不是噪声堆。

**收束**：图书馆不是存储仓库，而是**经验加工器**。

---

## 三、图书馆在整体架构中的位置

**上游输入**

- 个体 Luna 侧的 usage / quality / governance **摘要**  
- 白盒摘要  
- 中台**补证据**请求  
- 蜂巢**重点观察方向**（指导「往哪看」）

**下游输出**

- `LibraryExperienceRecord`  
- `LibraryExperiencePackage`  
- `LibraryValidationRecord`  
- 向蜂巢提供**经验材料**（入 `HiveModelScoreInputPack` 等引用链）  
- 向中台提供**证据与样本**  
- 向个体 Luna 提供**辅助经验**（非强制命令）

**一句话**：图书馆位于个体 Luna 与蜂巢/中台之间，是**经验加工与证据供给层**。

---

## 四、图书馆的四类职责

### 4.1 经验归档职责

- 接收结构化经验摘要  
- 保存经验对象  
- 建立可检索经验记录  

### 4.2 经验提炼职责

- 从多条记录中提炼共性问题  
- 提炼成功模式、失败模式、风险模式  

### 4.3 经验验证职责

- 去重、去噪、样本量判断、交叉验证  
- 判断经验是否可复用  

### 4.4 经验打包职责

- 形成经验包  
- 面向蜂巢、中台、个体 Luna 提供**不同粒度**的输出  

**一句话**：图书馆不是直接裁决器，而是**归档、提炼、验证、打包**四位一体的经验加工层。

---

## 五、图书馆不能做什么

图书馆**不负责**、**不得**：

- 直接改 route policy  
- 直接切主模型  
- 直接修改中台治理状态  
- 直接下发**强制执行**策略  
- 替代蜂巢做模型**全局评分**  
- 替代个体 Luna 做**当前轮裁决**  

**一句话**：图书馆可以提供证据和经验，但**不能直接产生线上强制治理动作**。

---

## 六、图书馆对象总览

固定 **三个** 核心对象：

| # | 对象 | 解决的问题 |
|---|------|------------|
| 1 | `LibraryExperienceRecord` | **先存下来**（单条、可追溯） |
| 2 | `LibraryExperiencePackage` | **提炼后怎么复用** |
| 3 | `LibraryValidationRecord` | **这包经验站不站得住** |

**收束**：记录 → 打包 → 验证，链路清晰。

---

## 七、LibraryExperienceRecord（单条经验）

| 建议字段 | 含义 |
|----------|------|
| `experience_id` | 经验 ID |
| `source_scope` | 来源范围（见下） |
| `source_task_type` | 来源任务类型 |
| `source_model_id` | 可选，关联模型 |
| `problem_type` | 问题类型（见下） |
| `context_summary` | 上下文摘要 |
| `evidence_refs` | **证据引用**（必须） |
| `raw_confidence` | 原始置信度草稿 |
| `library_status` | 馆内状态（见下） |
| `timestamp` | 时间戳 |

**`source_scope` 示例**：`individual_luna`、`library_internal`、`mid_platform`、`hive_feedback`。

**`problem_type` 示例**：`timeout_pattern`、`mixed_split_failure`、`clarification_failure`、`illegal_mapping_pattern` 等。

**`library_status` 示例**：`raw`、`under_review`、`validated`、`discarded`、`packaged`（可与实现枚举对齐）。

**必须写清**：**`evidence_refs` 必须引用来源**，经验不得脱离证据漂浮存在。

---

## 八、LibraryExperiencePackage（经验包）

| 建议字段 | 含义 |
|----------|------|
| `package_id` | 包 ID |
| `package_type` | 包类型（见下） |
| `applicable_domains` | 适用任务域 |
| `applicable_models` | 适用模型 ID 或类型标签 |
| `summary` | 摘要 |
| `key_patterns` | 关键模式要点 |
| `supporting_experiences` | 支撑的单条经验 ID |
| `validation_level` | 验证等级 |
| `recommended_usage` | 推荐使用方式（见下） |
| `notes` | 备注 |

**`package_type` 示例**：`failure_pattern_package`、`success_pattern_package`、`task_pattern_package`、`risk_pattern_package`、`optimization_hint_package`。

**`recommended_usage` 示例**：给蜂巢评分参考、给中台补证据、给个体 Luna 辅助理解、给测试系统生成样本等。

**必须写清**：**适用域、适用模型**须填写；与第十七节「适用范围声明」一致。

---

## 九、LibraryValidationRecord（验证记录）

| 建议字段 | 含义 |
|----------|------|
| `validation_id` | 验证 ID |
| `target_package_id` | 目标经验包 |
| `validation_scope` | 验证范围（见下） |
| `sample_size` | 样本量 |
| `validation_result` | 验证结论（见下） |
| `confidence_level` | 置信度（须与样本量、覆盖挂钩） |
| `validation_notes` | 验证说明 |
| `timestamp` | 时间 |

**`validation_scope` 示例**：`task_specific`、`domain_specific`、`cross_domain`。

**`validation_result` 示例**：`confirmed`、`partially_confirmed`、`rejected`、`needs_more_data`。

**必须写清**：`confidence_level` **不得**脱离样本量与覆盖范围单独宣称「高置信」。

---

## 十、个体 Luna → 图书馆接口

**输入类型建议固定三类（摘要级）**

1. **使用记录摘要** — 来源概念：`ModelUsageRecord`  
2. **质量问题摘要** — 来源概念：`ModelQualityRecord`  
3. **治理事件摘要** — 来源概念：`ModelGovernanceRecord`  

**必须写清**

- 个体上行到图书馆的应是**摘要**，不是无限原始流量。  
- 图书馆吃的是**加工入口**，不是原始流量黑洞。  
- 个体 Luna **只负责上报**，不负责经验**定性**（定性在图书馆/验证链）。

---

## 十一、图书馆 → 个体 Luna 接口

**当前建议只允许两类下行**

1. **辅助经验包**：如某类任务常见 clarification 模式、某类 mixed 切分经验等。  
2. **历史辅助信息**：如地点/对象历史匹配摘要、历史成功路径摘要等。

**必须写清**

- 图书馆下发的是**辅助经验**，不是**强制命令**。  
- 个体 Luna **不得**绕过中台治理，把经验包当**执行指令**或路由指令。

---

## 十二、图书馆 → 蜂巢接口

**建议输出类型**

1. **模型问题经验包**：长期 timeout、mixed 表现差、clarification 质量低等。  
2. **任务经验包**：某任务域常见失败模式、规则链 vs 模型链偏好等。  
3. **优化线索包**：易错 schema 字段、高风险任务域组合等。

**必须写清**：蜂巢吃的是**经验包与引用**，不是原始噪声；对应 `HiveModelScoreInputPack.source_library_records` 等引用链。

---

## 十三、蜂巢 → 图书馆接口

**建议输入类型**

1. **重点观察方向**：如重点补某模型在某任务域的失败样本。  
2. **提炼要求**：如需要更多某任务域经验包、更多某类失败归因案例。

**必须写清**：蜂巢可以指导图书馆「**往哪看**」，**不能**替代图书馆「**怎么提炼**」。

---

## 十四、图书馆 → 中台接口

**允许提供**

1. **证据材料**：支撑推荐动作或审计的经验依据。  
2. **验证结果**：说明某类经验已**确认**而非个例。  
3. **测试样本集**：供灰度、回归、验证使用（按组织流程）。

**不允许提供**

- 直接治理指令  
- 直接切模型指令  
- 直接改 route policy 指令  

---

## 十五、中台 → 图书馆接口

**建议请求类型**

- `need_more_evidence`  
- `need_more_test_samples`  
- `need_domain_specific_package`  
- `need_validation_update`  

**必须写清**：中台发的是**证据/材料请求**，不是对图书馆的**治理命令**。

---

## 十六、经验提炼与验证原则

- **先提炼，再验证，再打包**。  
- **原始**经验不得直接进入蜂巢或中台**关键决策链**作为主依据。  
- **单例**经验不得直接升格为高置信度经验包。  
- 经验包必须可追溯到 **`supporting_experiences`**（或等价引用）。

---

## 十七、经验包适用范围声明

每个经验包至少声明：

- 适用**任务域**  
- 适用**模型**或模型类型  
- 适用**主体范围**（谁能消费、用于什么目的）  
- **不适用范围**（负面声明）  

**一句话**：经验包必须**带边界**，不能默认全局适用。

---

## 十八、样例

### 样例 1：模型 timeout 模式经验包

- 多条 usage / governance 摘要 → 提炼为共性问题 → `LibraryExperienceRecord` 多条 → 打包为 `timeout_pattern` 类 `LibraryExperiencePackage` → `LibraryValidationRecord` 确认样本量与结论。

### 样例 2：医院场景 clarification 失败经验包

- 某任务域失败模式 → 供蜂巢评分输入引用 → 供中台在消费建议时**补证据**（不替代决策）。

---

## 十九、与其他文档的关系

| 文档 | 关系 |
|------|------|
| `LUNA_MID_PLATFORM_RECOMMENDATION_CONSUMPTION_SPEC_V1.md` | 中台如何消费蜂巢建议 |
| `LUNA_HIVE_SCORE_AND_RECOMMENDATION_SPEC_V1.md` | 蜂巢评分与输入包 |
| `LUNA_MODEL_REGISTRY_CARD_SPEC_V1.md` / `LUNA_MODEL_TASK_CARD_SPEC_V1.md` | 模型与任务契约 |
| `LUNA_MODEL_MID_PLATFORM_CONSTITUTION_V1.md` | 总纲与四方关系 |

---

## 二十、结尾收束句

**图书馆在 Luna 模型治理体系中的角色，不是记录一切，而是把可复用、可验证、可解释的经验加工出来，供蜂巢评分和中台治理使用。**

---

## 附录 A：与当前代码骨架的对照（v1）

| 对象 | 代码 | 说明 |
|------|------|------|
| `LibraryExperienceRecord` | `library/library_experience_record.py` | 已实现核心字段；规范中的 **`timestamp`** 等可后续扩展 |
| `LibraryExperiencePackage` | `library/library_experience_package.py` | 含 `package_id`、`applicable_*`、`supporting_experiences`、`validation_level` 等；**`notes`** 等可补全 |
| `LibraryValidationRecord` | `library/library_validation_record.py` | 含 `validation_id`、`target_package_id`、`sample_size`、`validation_result`、`confidence_level`；规范中的 **`validation_notes`** 可与 `notes` 字段对读 |

提炼/验证/打包的**业务逻辑**不在占位代码中，由图书馆服务在审计与策略下实现。

---

## 附录 B：导航（历史专题）

- `../model_platform/LUNA_MODEL_PLATFORM_LIBRARY_POSITION_AND_INTERFACE_V1.md`  

# Luna 蜂巢评分与建议规范 v1

> **本文性质**：定义蜂巢如何对模型做**全局评估**、输出哪些**结构化评分对象**、生成哪些**建议对象**、建议如何**交给中台**（交接面语义）。  
> **不是**：中台治理执行细则、个体 Luna 运行手册、图书馆经验提炼流程。  
> **历史专题补充**：`../model_platform/LUNA_MODEL_PLATFORM_HIVE_SCORING_FRAMEWORK_V1.md`、`../model_platform/LUNA_MODEL_PLATFORM_HIVE_SCORING_RECORDS_AND_TEMPLATES_V1.md`。  
> **占位代码**：`mid_platform/model_governance/hive/`（无自动评分/自动生效逻辑）。

**一句话**：蜂巢负责**评分与建议**，**不负责直接生效**。

---

## 一、文档定位

1. **什么是蜂巢评分与建议体系**  
   蜂巢侧对模型进行**跨调用、跨任务、跨个体**汇聚后的评估，并产出结构化**评分记录**与**建议对象**，供中台按制度消费。

2. **它解决什么问题**  
   在「多模型、多任务、多来源记录」下，把「模型表现如何」与「建议如何调整」**结构化**表达，避免评分散落在个体或主观叙述中。

3. **它不解决什么**  
   - **不定义**中台如何**执行**建议（见 `LUNA_MID_PLATFORM_RECOMMENDATION_CONSUMPTION_SPEC_V1.md`）。  
   - **不定义**个体 Luna 如何做**全局评分**（个体只留痕与局部消费）。  
   - **不定义**图书馆如何**提炼经验**（图书馆提供材料，不负责全局优劣主脑）。

---

## 二、为什么评分权必须归蜂巢

- **个体 Luna** 视角偏局部，适合留痕与当前轮消费，**不适合**承担全局评分主脑。  
- **图书馆**负责经验加工，**不负责**全局优劣判断。  
- **中台**负责治理与执行，若再兼全局评分主脑，易与**治理裁决**角色混淆。  
- **蜂巢**适合跨模型、跨任务、跨个体的**比较与归因**。

**收束**：**模型评分权归蜂巢，模型治理权归中台**（与总纲一致）。

---

## 三、蜂巢评分体系在整体架构中的位置

**上游输入主要来自**：

- usage record  
- quality record  
- governance record  
- library experience package（经验材料）  
- whitebox summary（可观测摘要）

**下游输出给**：

- **中台** recommendation consumption（建议 intake + 决策留痕）  
- **图书馆**作为经验补充参考（非强制闭环）  
- **白盒**作为状态/摘要展示（只读呈现）

**关系一句话**：蜂巢吃**全局材料**，产出评分与建议；**不直接操纵**个体主链执行。

---

## 四、蜂巢评分对象总览

固定 **三个** 核心对象：

| # | 对象 | 解决的问题 |
|---|------|------------|
| 1 | `HiveModelScoreInputPack` | **拿什么**评分 |
| 2 | `HiveModelScoreRecord` | **得出什么**结论 |
| 3 | `HiveModelRecommendation` | **建议中台怎么做**（仍为建议，非命令） |

**收束**：输入包 → 评分记录 → 建议对象，链路清晰、可审计。

---

## 五、HiveModelScoreInputPack（评分输入包）

| 字段 | 含义 |
|------|------|
| `score_input_pack_id` | 输入包 ID |
| `model_id` / `model_version` | 评分对象 |
| `score_scope` | 评分范围（见下） |
| `time_range` | 时间边界（**必须有**） |
| `source_usage_records` | 引用的 usage 记录 ID 列表 |
| `source_quality_records` | 引用的 quality 记录 ID 列表 |
| `source_governance_records` | 引用的 governance 记录 ID 列表 |
| `source_library_records` | 引用的图书馆材料 ID 列表 |
| `source_whitebox_summaries` | 白盒摘要引用 |
| `sample_size` | 样本量 |
| `aggregation_note` | 聚合说明 |

**`score_scope` 建议枚举**：`task_specific`、`domain_specific`、`global`。

**必须写清**

- **`time_range`**：必须有边界；**禁止**无时间窗的「全局拍脑袋」评分。  
- **`sample_size`**：没有足够样本量，**不允许**输出高置信度结论（见第十三节）。  
- **输入来源**：**主要**吃结构化记录与经验材料；**不**以「前台原始交互全文」作为主输入。

---

## 六、HiveModelScoreRecord（评分记录）

| 字段 | 含义 |
|------|------|
| `score_record_id` | 评分记录 ID |
| `model_id` / `model_version` | 对象 |
| `score_scope` | 与输入包一致 |
| `score_timestamp` | 产出时间 |
| `overall_score` | 总分 |
| `dimension_scores` | 维度分（建议六维，见第八节） |
| `score_explanations` | **结构化**解释（不可只有空话） |
| `risk_flags` | 风险标签 |
| `positioning_result` | 定位结论（见下） |
| `comparison_reference` | 对比参照说明（如对比模型集、基线） |
| `confidence_level` | 置信度 |
| `notes` | 备注 |

**必须写清**

- **`overall_score`**：允许存在，但**不得单独**作为唯一决策依据；须结合维度、风险、一票否决（见第九节）。  
- **`dimension_scores`**：建议固定 **六维**键名：  
  - `stability_score`  
  - `quality_score`  
  - `latency_score`  
  - `cost_score`  
  - `governance_friendliness_score`  
  - `evolvability_score`  
- **`score_explanations`**：必须**结构化**（键值/列表/分段），禁止仅有一句模糊总结。  
- **`risk_flags`** 示例：`high_timeout_risk`、`schema_instability_risk`、`governance_bypass_risk`、`cost_burst_risk` 等。  
- **`positioning_result`** 建议枚举：`primary_candidate`、`backup_candidate`、`shadow_only`、`background_only`、`deprecated_candidate`。  
- **`confidence_level`** 建议：`low` / `medium` / `high`（须与样本量挂钩，见第十三节）。

---

## 七、HiveModelRecommendation（蜂巢建议对象）

| 字段 | 含义 |
|------|------|
| `recommendation_id` | 建议 ID |
| `model_id` | 对象模型 |
| `recommendation_type` | 建议类型（见下） |
| `recommendation_priority` | 优先级 |
| `recommendation_reason` | 理由 |
| `based_on_score_record_id` | 依据的评分记录 |
| `suggested_action` | **建议动作**（≠ 已生效动作） |
| `suggested_constraints` | 建议约束（键值） |
| `requires_human_review` | 是否要人工复核 |
| `requires_shadow_validation` | 是否要先 shadow 验证 |
| `notes` | 备注 |

**`recommendation_type` 建议枚举**：`promote`、`degrade`、`restrict_scope`、`keep_observing`、`retire`、`optimize_prompt`、`optimize_routing`、`optimize_schema_contract`。

**必须写清**

- **`suggested_action`**：是**建议语义**，不是中台已执行的**生效动作**。  
- **`suggested_constraints`** 示例：`shadow_only=true`、`mainline_forbidden=true`、`allowed_task_domains=[...]`、`max_timeout_ms=...` 等。

---

## 八、蜂巢评分维度定义（六维）

### 8.1 稳定性分（stability）

来源示例：timeout 率、fallback 率、success 率、服务可达率。

### 8.2 质量分（quality）

来源示例：validator 通过率、mixed 保留质量、clarification 质量、unsupported 判断质量、语义偏差率。

### 8.3 时延分（latency）

来源示例：平均耗时、P95/P99、冷热启动差异。

### 8.4 成本分（cost）

来源示例：单次调用成本、单位有效输出成本、资源消耗。

### 8.5 治理友好度分（governance friendliness）

来源示例：schema 合规率、非法映射率、越权率、需人工兜底率。

### 8.6 可演化分（evolvability）

来源示例：是否值得继续优化、是否适合扩域、与图书馆经验/蜂巢策略的兼容度。

---

## 九、一票否决项

以下情形**不得**因总分尚好而直接作为**主模型候选**（须进入限制、观察或降级路径，由中台决策）：

1. `schema_instability`（schema 不稳定）  
2. `high_timeout_rate`（超时风险过高）  
3. `governance_bypass_risk`（绕治理风险）  
4. `illegal_mapping_rate_too_high`（非法映射率过高）  
5. `fallback_rate_too_high`（fallback 率过高）

**必须写清**：踩中一票否决项后，**即使总分还行**，也**不得**直接视为可晋升主模型。

---

## 十、蜂巢评分输入来源

**可以吃（主输入）**：

- `ModelUsageRecord`  
- `ModelQualityRecord`  
- `ModelGovernanceRecord`  
- `LibraryExperiencePackage`（及规范化的图书馆引用）  
- Whitebox summaries  

**不直接作为主输入**：

- 前台原始交互全文  
- 个体 Luna **主观评价**  
- 未经筛选的原始噪声日志  

---

## 十一、蜂巢评分输出的使用边界

**蜂巢能做**：评分、比较、归因、提建议。

**蜂巢不能做**：

- 直接修改 registry  
- 直接修改 route policy  
- 直接切换主模型  
- 直接替换 fallback  
- 绕过中台让建议**生效**

**一句话**：**蜂巢建议不是命令。**

---

## 十二、评分周期与触发方式

建议分三类：

1. **日常轻评分**：关注稳定性、fallback、成本波动等。  
2. **周期评分**：如周评、阶段评。  
3. **重大变更评分**：如新模型接入、模型升级、prompt 大改、路由策略变更后等。

---

## 十三、样本量与置信度规则

- 样本不足时，**只允许**低置信度或「仅观察」类结论。  
- **`task_specific` 与 `global` 评分不得混用**为同一条高置信结论。  
- **禁止**用极少样本得出「退役/升级」类**高置信**结论。  
- **`confidence_level` 不得仅由模型自说**，须与**样本量、时间窗、覆盖范围**挂钩。

---

## 十四、评分结果模板（短摘要）

供中台与白盒阅读的**最小结果摘要**（不替代完整 `HiveModelScoreRecord`）：

- `overall_score`  
- `positioning_result`  
- `top_3_issues`  
- `top_3_strengths`  
- `primary_recommendation`（指向建议 ID 或短句）  
- `confidence_level`  

---

## 十五、建议对象模板（结构）

每条建议至少包含：

- 推荐动作类型（`recommendation_type`）  
- 优先级（`recommendation_priority`）  
- 理由（`recommendation_reason`，可引用 `based_on_score_record_id`）  
- 约束（`suggested_constraints`）  
- 是否需要人工复核（`requires_human_review`）  
- 是否需要 shadow 验证（`requires_shadow_validation`）  

---

## 十六、样例

### 样例 1：长语音任务拆解模型 — 评分记录

- **六维分**：`dimension_scores` 填满六键。  
- **风险 flags**：如 `schema_instability_risk`（若存在则配合第九节）。  
- **positioning_result**：如 `primary_candidate` 或 `backup_candidate`。  
- **建议对象**：如 `keep_observing` + `requires_shadow_validation=true`。

### 样例 2：蜂巢建议降级某模型

- `recommendation_type`：`restrict_scope` 或 `degrade`  
- `suggested_constraints`：如 `mainline_forbidden=true`、`allowed_task_domains=[...]`  
- `requires_shadow_validation`：视情况为 `true`  
- `requires_human_review`：高风险时为 `true`  

---

## 十七、和中台消费文档的关系

- 本文**只定义**评分与建议**对象**及边界。  
- 中台如何 **intake、审核、采纳/拒绝、留痕、执行**，见：  
  **`LUNA_MID_PLATFORM_RECOMMENDATION_CONSUMPTION_SPEC_V1.md`**

---

## 十八、和图书馆接口文档的关系

- **图书馆**是评分**材料提供者之一**（经验包等）。  
- 经验包如何进入、如何引用，见：  
  **`LUNA_LIBRARY_EXPERIENCE_INTERFACE_SPEC_V1.md`**

---

## 十九、结尾收束句

**蜂巢评分体系的职责，是把「模型表现如何」与「模型该怎么调整」结构化地表达出来；它负责建议，不负责直接生效。**

---

## 附录 A：与当前代码骨架的对照（v1）

| 对象 | 代码路径 | 说明 |
|------|----------|------|
| `HiveModelScoreInputPack` | `hive/hive_model_score_input_pack.py` | 字段与第五节一致；**无**自动聚合逻辑 |
| `HiveModelScoreRecord` | `hive/hive_model_score_record.py` | 含 `overall_score`、`dimension_scores`、六维示例见 `sample_score_record()`；**规范中的** `score_explanations`、`comparison_reference`、`notes` **待扩展** |
| `HiveModelRecommendation` | `hive/hive_model_recommendation.py` | 与第七节一致；**无**自动生效 |

实现上仍以 **schema + 序列化** 为主；**评分算法、调度、一票否决自动判定** 不在本文档代码占位范围内，须由蜂巢服务在制度与审计下实现。

---

## 附录 B：导航（历史专题）

- `../model_platform/LUNA_MODEL_PLATFORM_HIVE_SCORING_FRAMEWORK_V1.md`  
- `../model_platform/LUNA_MODEL_PLATFORM_HIVE_SCORING_RECORDS_AND_TEMPLATES_V1.md`  

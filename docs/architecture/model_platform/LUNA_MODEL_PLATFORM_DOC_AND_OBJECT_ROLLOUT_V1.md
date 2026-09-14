# Luna 文档落地顺序 / 中台对象清单 v1

> **目标**：把已定治理框架收成**可交付、可占位、可逐步实现**的工程清单。  
> **不展开**功能实现细节；先定：先写什么文档、先建什么对象、哪些占位、哪些暂时不做。  
> 总览见 `LUNA_MODEL_PLATFORM_GOVERNANCE_PANORAMA_V1.md`。

---

## 命名说明（避免重复维护）

下列 **三批**中的「建议文件名」若与仓库已有 `LUNA_MODEL_PLATFORM_*` 专题重复，**以现有文件为正文来源**；本表给出**对应关系**，不强制再复制一套宪法。

| 建议文件名（本清单） | 当前仓库正文位置 |
|----------------------|------------------|
| `LUNA_MODEL_MID_PLATFORM_CONSTITUTION_V1` | `LUNA_MODEL_PLATFORM_CONSTITUTION_V1.md` + `LUNA_MODEL_PLATFORM_SKELETON_V1.md` |
| `LUNA_MODEL_RESPONSIBILITY_ISOLATION_V1` | `LUNA_MODEL_PLATFORM_ROLE_MERGE_MATRIX_V1.md` |
| `LUNA_MODEL_GOVERNANCE_OVERVIEW_V1` | `LUNA_MODEL_PLATFORM_GOVERNANCE_PANORAMA_V1.md` |
| `LUNA_MODEL_REGISTRY_CARD_SPEC_V1` | `LUNA_MODEL_PLATFORM_REGISTRY_AND_TAGS_V1.md` |
| `LUNA_MODEL_TASK_CARD_SPEC_V1` | `LUNA_MODEL_PLATFORM_TASK_CARD_V1.md` |
| `LUNA_HIVE_SCORE_AND_RECOMMENDATION_SPEC_V1` | `LUNA_MODEL_PLATFORM_HIVE_SCORING_FRAMEWORK_V1.md` + `LUNA_MODEL_PLATFORM_HIVE_SCORING_RECORDS_AND_TEMPLATES_V1.md` |
| `LUNA_MID_PLATFORM_RECOMMENDATION_CONSUMPTION_SPEC_V1` | `LUNA_MODEL_PLATFORM_MIDPLATFORM_HIVE_CONSUMPTION_V1.md` |
| `LUNA_LIBRARY_EXPERIENCE_INTERFACE_SPEC_V1` | `LUNA_MODEL_PLATFORM_LIBRARY_POSITION_AND_INTERFACE_V1.md` |
| `LUNA_MODEL_MID_PLATFORM_OBJECT_MAP_V1` | **本文件第二节起（对象清单）** |
| `LUNA_MODEL_MID_PLATFORM_ROADMAP_V1` | **本文件第三～五节（阶段 / 目录 / P0）** |
| `LUNA_MODEL_MID_PLATFORM_CHANGESET_POLICY_V1` | **待补**：架构变更策略（可另起文档或先见宪法与全景表） |

---

## 一、文档落地顺序（三批）

### 第一批：宪法与总纲（地基，先落）

| # | 建议文档名 | 内容要点 | 当前正文 |
|---|------------|----------|----------|
| 1 | `LUNA_MODEL_MID_PLATFORM_CONSTITUTION_V1` | 中台定位、四层结构、模型非主权者、统一纳管、可替换/可降级/可留痕、生产/审核/评估/策略分离、蜂巢评分权、中台治理权、图书馆经验加工权、个体使用权 | `CONSTITUTION` + `SKELETON` |
| 2 | `LUNA_MODEL_RESPONSIBILITY_ISOLATION_V1` | 职责四分法、可合并/不可合并矩阵、运动员/裁判/教练分离、红线组合 | `ROLE_MERGE_MATRIX` |
| 3 | `LUNA_MODEL_GOVERNANCE_OVERVIEW_V1` | 四方关系、整体运行闭环、白盒/中台/图书馆/蜂巢总表 | `GOVERNANCE_PANORAMA` |

---

### 第二批：对象与接口（最小工程骨架）

| # | 建议文档名 | 内容要点 | 当前正文 |
|---|------------|----------|----------|
| 4 | `LUNA_MODEL_REGISTRY_CARD_SPEC_V1` | 注册卡字段、含义、必填、准入红线 | `REGISTRY_AND_TAGS` |
| 5 | `LUNA_MODEL_TASK_CARD_SPEC_V1` | 任务卡模板、输入/加工/输出/合格/fallback、一模型多任务卡 | `TASK_CARD` |
| 6 | `LUNA_HIVE_SCORE_AND_RECOMMENDATION_SPEC_V1` | Input Pack、Score Record、Recommendation、六维、一票否决 | `HIVE_SCORING_FRAMEWORK` + `HIVE_SCORING_RECORDS` |
| 7 | `LUNA_MID_PLATFORM_RECOMMENDATION_CONSUMPTION_SPEC_V1` | 接收/审核/决策/执行、采纳类结果、决策留痕 | `MIDPLATFORM_HIVE_CONSUMPTION` |
| 8 | `LUNA_LIBRARY_EXPERIENCE_INTERFACE_SPEC_V1` | 图书馆对象、与个体/蜂巢/中台接口、证据 vs 命令 | `LIBRARY_POSITION` |

---

### 第三批：工程落地与占位（给 Cursor）

| # | 建议文档名 | 内容要点 | 当前正文 |
|---|------------|----------|----------|
| 9 | `LUNA_MODEL_MID_PLATFORM_OBJECT_MAP_V1` | schema/record/service 一览、哪些建文件、占位、后实现 | **本文件第二节** |
| 10 | `LUNA_MODEL_MID_PLATFORM_ROADMAP_V1` | Phase 1/2/3、当前不做什么 | **本文件第三～六节** |
| 11 | `LUNA_MODEL_MID_PLATFORM_CHANGESET_POLICY_V1` | 谁能改中台对象、变更条件、架构级变更定义 | **待补**（可先遵循宪法 + 全景表变更纪律） |

---

## 二、中台对象清单 v1（名字与职责先定住）

下列为建议**先建立**的对象（**不等于**全部实现）：先有「名字和位置」，再填逻辑。

### A. 注册与路由

| # | 对象 | 作用 |
|---|------|------|
| 1 | **ModelRegistryCard** | 中台中的模型身份证 |
| 2 | **ModelCapabilityProfile** | 能力标签、任务域标签、部署标签 |
| 3 | **ModelRoutePolicy** | 当前路由规则、主备、优先级、fallback 关系 |
| 4 | **ModelRouteDecision** | 某次调用为何选此模型、是否降级、是否因治理改选 |

### B. 治理

| # | 对象 | 作用 |
|---|------|------|
| 5 | **ModelGovernancePolicy** | 准入、风险、schema guard、自评自审禁令 |
| 6 | **ModelGovernanceDecisionRecord** | 对某条蜂巢建议的最终裁决留痕 |
| 7 | **ModelFallbackPlan** | 失败时降级路径：规则链、clarification、reject、备份模型 |

### C. 任务定义

| # | 对象 | 作用 |
|---|------|------|
| 8 | **ModelTaskCard** | 模型×任务维度的职责定义 |
| 9 | **TaskQualityCriteria** | 合格标准、失败标准、关键质量指标 |

### D. 蜂巢评分

| # | 对象 | 作用 |
|---|------|------|
| 10 | **HiveModelScoreInputPack** | 蜂巢评分输入包 |
| 11 | **HiveModelScoreRecord** | 蜂巢评分结果 |
| 12 | **HiveModelRecommendation** | 蜂巢给中台的建议 |

### E. 图书馆

| # | 对象 | 作用 |
|---|------|------|
| 13 | **LibraryExperienceRecord** | 单条经验 |
| 14 | **LibraryExperiencePackage** | 提炼后的经验包 |
| 15 | **LibraryValidationRecord** | 经验验证结果 |

### F. 观测与记录

| # | 对象 | 作用 |
|---|------|------|
| 16 | **ModelUsageRecord** | 每次模型调用留痕 |
| 17 | **ModelQualityRecord** | 输出质量结果 |
| 18 | **ModelGovernanceRecord** | fallback、schema 失败、越权、熔断等 |
| 19 | **ModelRuntimeObservation** | 白盒可见运行态摘要 |

---

## 三、哪些先实现，哪些先占位

### 第一阶段：必须先有（可先简单）

中台最小地基；**没有这些，接外部 API 仍会乱**。

| 必须先有 |
|----------|
| ModelRegistryCard |
| ModelTaskCard |
| ModelUsageRecord |
| ModelQualityRecord |
| ModelGovernanceRecord |
| ModelRoutePolicy |
| ModelFallbackPlan |

---

### 第二阶段：先占位，不做复杂逻辑

先定义 schema/接口，**完整流水线后补**。

| 先占位 |
|--------|
| HiveModelScoreInputPack |
| HiveModelScoreRecord |
| HiveModelRecommendation |
| LibraryExperienceRecord |
| LibraryExperiencePackage |
| LibraryValidationRecord |
| ModelGovernanceDecisionRecord |

**理由**：图书馆 / 蜂巢 / 中台闭环依赖这些对象，**先有壳**。

---

### 第三阶段：后续再做（当前不做复杂能力）

| 后做 |
|------|
| 自动评分 |
| 自动建议生成 |
| 自动灰度 |
| 自动升降级 |
| 自动经验打包 |
| 自动推荐路由更新 |

---

## 四、建议目录结构（代码落点）

建议中台相关代码置于（示例，按仓库实际调整）：

```
mid_platform/
  model_governance/
    schemas/
      model_registry_card.py
      model_task_card.py
      model_usage_record.py
      model_quality_record.py
      model_governance_record.py
      hive_model_score_record.py
      hive_model_recommendation.py
      library_experience_record.py
      library_experience_package.py
      library_validation_record.py
    registry/
      model_registry_service.py
    routing/
      model_route_policy.py
      model_route_selector.py
    governance/
      model_governance_policy.py
      model_fallback_plan.py
      model_governance_decision_service.py
    hive/
      hive_score_ingest.py
      hive_recommendation_ingest.py
    library/
      library_experience_ingest.py
      library_package_loader.py
```

**说明**：目录与文件名可与语言/包名约定对齐；**先建 `schemas/` 契约**，再建 service。

---

## 五、最小落地优先级（给 Cursor 拆任务）

### P0

1. ModelRegistryCard  
2. ModelTaskCard  
3. ModelUsageRecord  
4. ModelQualityRecord  
5. ModelGovernanceRecord  

### P1

6. ModelRoutePolicy  
7. ModelFallbackPlan  
8. ModelRouteDecision  

### P2（占位）

9. 蜂巢评分三对象占位  
10. 图书馆三对象占位  
11. 中台消费蜂巢建议（含 GovernanceDecisionRecord）占位  

---

## 六、当前不做项（必须写死）

| 当前不做 |
|----------|
| 自动评分引擎 |
| 自动路由引擎 |
| 自动升降级生效 |
| 自动经验下发 |
| 自动替换主模型 |
| 蜂巢直接改中台 |
| 图书馆直接改主链 |
| 个体 Luna 根据评分自行切模型 |

---

## 七、给 Cursor 的最短落地原则（4 条）

1. **先建 schema/record**，不先做复杂服务。  
2. **先建注册卡和任务卡**，不先堆更多模型接入。  
3. **蜂巢与图书馆对象先占位**，不做自动闭环。  
4. **中台先有治理骨架**，不做自动智能化。  

---

## 八、一句话收束

当前最合理的工程顺序：**不是继续扩模型**，而是先把**注册卡、任务卡、使用记录、质量记录、治理记录**建出来，再把**蜂巢与图书馆对象占位**；智能化后置。

---

## 下一步

**Cursor 可执行版任务拆解（模型中台 P0 / P1 / P2）**：把上述对象拆成可直接开干的开发任务（可另起 `…_TASK_BREAKDOWN_V1.md` 或在 Issue/Project 中列表）。

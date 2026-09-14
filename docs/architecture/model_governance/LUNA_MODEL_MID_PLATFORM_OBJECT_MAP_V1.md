# Luna 模型中台对象映射 v1

> **与代码对齐**：「已实现」以 **`mid_platform/model_governance/`** 为准。  
> **历史展开**：`../model_platform/LUNA_MODEL_PLATFORM_DOC_AND_OBJECT_ROLLOUT_V1.md`。

---

## 当前代码目录布局（P0 + P1 + P2 占位）

```
mid_platform/model_governance/
├── schemas/
├── registry/
├── records/
├── routing/
├── governance/
├── hive/
├── library/
├── tests/
├── README.md
├── __init__.py
└── requirements-dev.txt
```

**P2 占位**：`hive/`、`library/` 与中台消费留痕对象在 `governance/`；**仅** schema + `to_dict`/`from_dict` + 可选 `sample_*`，**无**自动评分、自动建议、自动执行编排。

---

## 一、已实现 — 已进入 `mid_platform/model_governance/`

### P0：身份、任务、留痕

| 类型 | 对象 / 模块 | 路径 |
|------|----------------|------|
| Schema | `ModelRegistryCard` | `schemas/model_registry_card.py` |
| Schema | `ModelTaskCard` | `schemas/model_task_card.py` |
| Schema | `ModelUsageRecord` | `schemas/model_usage_record.py` |
| Schema | `ModelQualityRecord` | `schemas/model_quality_record.py` |
| Schema | `ModelGovernanceRecord` | `schemas/model_governance_record.py` |
| Service | `ModelRegistryService` | `registry/model_registry_service.py` |
| Service | `ModelTaskCardService` | `registry/model_task_card_service.py` |
| Writer | `ModelUsageRecordWriter` 等 | `records/*.py` |
| 工具 | `append_jsonl` | `records/jsonl_writer.py` |

### P1：静态路由、降级计划、治理预检（骨架）

| 类型 | 对象 / 模块 | 路径 |
|------|----------------|------|
| Policy | `ModelRoutePolicy` | `routing/model_route_policy.py` |
| Decision | `ModelRouteDecision` | `routing/model_route_decision.py` |
| Selector | `select_route()` | `routing/model_route_selector.py` |
| Plan | `ModelFallbackPlan`、`resolve_fallback_action` 等 | `governance/model_fallback_plan.py` |
| Service | `ModelGovernanceDecisionService` | `governance/model_governance_decision_service.py` |

### P2：蜂巢、图书馆、建议消费 — **仅对象壳（占位）**

| 类型 | 对象 | 路径 |
|------|------|------|
| Schema | `HiveModelScoreInputPack` | `hive/hive_model_score_input_pack.py` |
| Schema | `HiveModelScoreRecord` | `hive/hive_model_score_record.py` |
| Schema | `HiveModelRecommendation` | `hive/hive_model_recommendation.py` |
| Schema | `LibraryExperienceRecord` | `library/library_experience_record.py` |
| Schema | `LibraryExperiencePackage` | `library/library_experience_package.py` |
| Schema | `LibraryValidationRecord` | `library/library_validation_record.py` |
| Schema | `ModelRecommendationIntakeRecord` | `governance/model_recommendation_intake_record.py` |
| Schema | `ModelGovernanceDecisionRecord` | `governance/model_governance_decision_record.py` |

**禁止**：在本目录实现自动评分引擎、自动建议生成、自动消费执行、自动升降级；编排逻辑属后续独立里程碑。

**验收**：`python3 -m pytest mid_platform/model_governance/tests/ -q`（**Luna-Core** 根目录）。

---

## 二、未来规划（非当前占位范围）

接入层多 provider、蜂巢/图书馆**运行时服务**、建议消费**四阶段状态机与持久化**、运维 UI 等。

---

## 结论模板（留档）

**P0 + P1 + P2 占位**：具备登记与留痕、静态选路与预检、以及蜂巢/图书馆/建议消费的**可序列化对象壳**；**不宣称**已具备自动闭环。

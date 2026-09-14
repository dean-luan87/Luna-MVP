# Luna 模型中台 — P0 + P1 + P2 占位

本目录包含 **P0**（身份、任务、留痕）、**P1**（静态路由、fallback 计划、治理预检），以及 **P2 对象占位**（蜂巢、图书馆、建议 intake/决策留痕 schema + 样例工厂）。**不含**自动评分、自动建议、自动消费执行、自动升降级。

设计依据见 `docs/architecture/model_governance/` 与 `LUNA_MODEL_MID_PLATFORM_DOC_INDEX_AND_PRIORITY_V1.md`。

**真实实现范围以本目录为准**；全文对象清单见 **`docs/architecture/model_governance/LUNA_MODEL_MID_PLATFORM_OBJECT_MAP_V1.md`**（**每增删模块须先改该文档**）。

---

### P2 占位入口（三句话）

1. **P2 已纳入本目录的对象壳**：`hive/` 三对象、`library/` 三对象、`governance/` 下 `ModelRecommendationIntakeRecord` 与 `ModelGovernanceDecisionRecord`（与 `schemas.ModelGovernanceRecord` 不同）。  
2. **仍禁止**：外部 API 接入、蜂巢自动评分、图书馆自动提炼、建议自动消费与执行、自动升降级；P2 **仅** dataclass + 序列化 + 可选 `sample_*`。  
3. **是否「有代码」以 `OBJECT_MAP` 为准**；后续若加编排服务，先更新映射表再写实现。

---

## 目录说明

| 路径 | 说明 |
|------|------|
| `schemas/` | 五类核心 schema（P0） |
| `registry/` | `ModelRegistryService`、`ModelTaskCardService` |
| `records/` | 三类 JSONL writer（P0） |
| `routing/` | `ModelRoutePolicy`、`ModelRouteDecision`、`select_route`（P1） |
| `governance/` | `ModelFallbackPlan`、`ModelGovernanceDecisionService`、intake/decision **占位**（P1+P2） |
| `hive/` | 蜂巢三对象占位（P2） |
| `library/` | 图书馆三对象占位（P2） |
| `tests/` | pytest |

### P1 开发入口（三句话）

1. **P1 对象**：`ModelRoutePolicy`、`ModelRouteDecision`、`select_route`、`ModelFallbackPlan`/`resolve_fallback_action`、`ModelGovernanceDecisionService`。  
2. **仍不允许**：评分驱动路由、外部 API、蜂巢/建议自动闭环。  
3. **以 `OBJECT_MAP` 为真值表**。

## 明确不做（持续）

- 运行时蜂巢评分引擎、图书馆提炼流水线、中台建议四阶段编排。  
- 任何「建议生成后自动改 registry / policy」的闭环。  

## 测试

在 **Luna-Core 根目录**：

```bash
pip install -r mid_platform/model_governance/requirements-dev.txt
python3 -m pytest mid_platform/model_governance/tests/ -q
```

## 文档链接

| 文档 | 路径 |
|------|------|
| 对象映射 | `docs/architecture/model_governance/LUNA_MODEL_MID_PLATFORM_OBJECT_MAP_V1.md` |
| 总纲 | `docs/architecture/model_governance/LUNA_MODEL_MID_PLATFORM_CONSTITUTION_V1.md` |
| 文档清单与优先级 | `docs/architecture/model_governance/LUNA_MODEL_MID_PLATFORM_DOC_INDEX_AND_PRIORITY_V1.md` |
| 验收清单 | `docs/architecture/model_platform/LUNA_MODEL_MID_PLATFORM_ACCEPTANCE_CHECKLIST_V1.md` |
| 汇报模板 | `docs/architecture/model_platform/LUNA_MODEL_MID_PLATFORM_REPORT_TEMPLATE_V1.md` |

# Luna 模型中台：总文档清单 + 实现优先级表 v1

> **用途**：文档全景、对象对应、实现优先级与先后次序；**不讲新理念**。  
> **验收**：`../model_platform/LUNA_MODEL_MID_PLATFORM_ACCEPTANCE_CHECKLIST_V1.md`；**汇报格式**：`../model_platform/LUNA_MODEL_MID_PLATFORM_REPORT_TEMPLATE_V1.md`。

---

## 〇、当前实现状态（与代码对齐 — **必读**）

| 项 | 状态 |
|----|------|
| 三篇核心文档（总纲、职责隔离、注册卡第一轮正文） | **已落第一轮正文**（`model_governance/`） |
| `mid_platform/model_governance/` | **P0 + P1 + P2 占位**：含 `hive/`、`library/`、建议 intake/decision **schema**；**无**自动评分/提炼/消费执行 |
| P2 运行时服务 | **未做**（仅对象壳） |

**结论模板（可留档）**：

> **模型中台最小治理骨架**：P0/P1 成立；P2 蜂巢/图书馆/建议 **对象已进目录**（占位 + 单测），**不宣称**自动闭环。真值表见 `LUNA_MODEL_MID_PLATFORM_OBJECT_MAP_V1.md`。

---

## 一、总文档清单

### A. 宪法 / 总纲类

| # | 文档 | 作用 |
|---|------|------|
| 1 | `LUNA_MODEL_MID_PLATFORM_CONSTITUTION_V1.md` | 中台总纲；四层结构；四方关系；主权边界 |
| 2 | `LUNA_MODEL_RESPONSIBILITY_ISOLATION_V1.md` | 职责四分法；可合并/不可合并矩阵；红线 |
| 3 | `LUNA_MODEL_GOVERNANCE_OVERVIEW_V1.md` | 四方总览（正文常对读 `model_platform`） |

### B. 对象规范类

| # | 文档 | 作用 |
|---|------|------|
| 4 | `LUNA_MODEL_REGISTRY_CARD_SPEC_V1.md` | 注册卡（**P0 代码已有**；spec 可含更广字段规划） |
| 5 | `LUNA_MODEL_TASK_CARD_SPEC_V1.md` | 任务卡（**P0 代码已有**） |
| 6 | `LUNA_HIVE_SCORE_AND_RECOMMENDATION_SPEC_V1.md` | 蜂巢（**规范**；代码为 **P2 占位 schema**） |
| 7 | `LUNA_MID_PLATFORM_RECOMMENDATION_CONSUMPTION_SPEC_V1.md` | 中台消费建议（**规范**；**P2** intake/decision **占位**，无编排） |
| 8 | `LUNA_LIBRARY_EXPERIENCE_INTERFACE_SPEC_V1.md` | 图书馆（**规范**；**P2 占位 schema**） |

### C. 工程落地类

| # | 文档 | 作用 |
|---|------|------|
| 9 | `LUNA_MODEL_MID_PLATFORM_OBJECT_MAP_V1.md` | **已实现 / 未实现 / 规划** 与目录对照 |
| 10 | `LUNA_MODEL_MID_PLATFORM_ROADMAP_V1.md` | 分期与我们**写到哪里、代码落哪里** |
| 11 | `LUNA_MODEL_MID_PLATFORM_CHANGESET_POLICY_V1.md` | 高风险变更与评审 |

**说明**：`model_platform/` 另有专题宪法、验收清单等，**交叉引用**。

---

## 二、对象与文档对应表

| 文档（简写） | 主要对象 | 当前代码 |
|--------------|----------|----------|
| `CONSTITUTION` | 原则与边界 | 无 schema |
| `RESPONSIBILITY_ISOLATION` | 职责矩阵 | 无 schema |
| `REGISTRY_CARD_SPEC` | `ModelRegistryCard` | **P0 有** |
| `TASK_CARD_SPEC` | `ModelTaskCard` | **P0 有** |
| `HIVE_SCORE...` | 蜂巢三对象 | **有** — 占位，见 `OBJECT_MAP` |
| `RECOMMENDATION_CONSUMPTION_SPEC` | intake / decision record | **有** — 占位 schema；**无**消费编排 |
| `LIBRARY_EXPERIENCE_INTERFACE_SPEC` | 图书馆三对象 | **有** — 占位，见 `OBJECT_MAP` |
| （P1 代码） | policy / selector / fallback plan / 预检 | **有** — 见 `OBJECT_MAP` |
| `OBJECT_MAP` | 全文对照 | 见该文档 |
| `ROADMAP` | 分期 | 见该文档 |

---

## 三、实现优先级表

### P0：最小治理地基 — **代码已成立**

见 `OBJECT_MAP` §一 P0 表。

### P1：路由与治理骨架 — **代码已成立（骨架）**

见 `OBJECT_MAP` §一 P1 表；**不做**评分驱动路由、不接外部 API、不自动消费蜂巢建议。

### P2：**占位 schema 已进仓**（无自动引擎）

见 `OBJECT_MAP` §一 P2 表。

### 代码目录速查（**实际**）

| 路径 | 状态 |
|------|------|
| `schemas/`、`registry/`、`records/` | P0 |
| `routing/`、`governance/`（含 fallback、预检、intake/decision 占位） | P1 + P2 占位 |
| `hive/`、`library/` | P2 占位 |

---

## 四、当前推荐文档编写顺序

（不变）第一轮三篇核心 → 第二轮任务/蜂巢/图书馆 → 第三轮消费与 object map / roadmap。

**增量说明**：object map、roadmap 已与 **P0-only 代码** 对齐；其它 spec 仍可继续修订，但须在文首或「附录」区分 **「规范目标」** 与 **「目录已有」**。

---

## 五、当前推荐实现顺序

1. ~~三篇核心 + P0 代码~~ → **已完成**。  
2. ~~P0 文档对齐~~ → **已完成**。  
3. ~~**P1** 骨架~~ → **已完成**。  
4. ~~**P2** 占位 schema~~ → **已完成**（与 `OBJECT_MAP` 同步；禁止自动闭环）。  
5. **下一步**：接入层工程化、蜂巢/图书馆**运行时服务**、建议消费编排（独立里程碑）。

---

## 六、当前不该做的事

（不变）外部 API 作为本阶段目标、自动评分/路由/升降级、个体全局评分等。

---

## 七、总收束建议

P0 与 P1 骨架落地后，**以 `OBJECT_MAP` 为唯一对象—目录真值表**；再进 P2 前先改映射表再写代码，避免「规范假装已实现」。

---

## 八、一句话收束

**蓝图在文档，落地以 `mid_platform/model_governance/` 与 `OBJECT_MAP` 为准；P2 进仓前须再更新映射表。**

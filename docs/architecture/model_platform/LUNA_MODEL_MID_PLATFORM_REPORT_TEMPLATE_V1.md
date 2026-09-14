# 【汇报格式模板】模型中台最小治理骨架 v1

交给 Cursor 的任务完成后，**请严格按下面格式汇报**，不要自由发挥，不要漏项。

---

## A. 本轮范围

一句话说明本轮只做了什么，不做什么。

示例：

- 本轮只完成 P0 schema + registry/task card service + record writer，不涉及外部 API 接入与自动评分。
- 本轮只做 P1 路由与治理骨架，不涉及蜂巢自动建议消费。

---

## B. 新增 / 修改文件列表

按类别列出，不要只贴一堆路径。

### 1. Schema

- …
- …

### 2. Service / Policy / Routing

- …
- …

### 3. Record Writer / Persistence

- …
- …

### 4. Tests

- …
- …

### 5. Docs

- …
- …

---

## C. 对象完成情况

按对象逐条说清：

**ModelRegistryCard**

- 是否已建
- 是否支持 to_dict / from_dict
- 是否有字段校验
- 是否有样例或测试

**ModelTaskCard**

- 是否已建
- 是否支持序列化
- 是否有字段校验
- 是否有样例或测试

**ModelUsageRecord**

- 是否已建
- 是否可落盘

**ModelQualityRecord**

- 是否已建
- 是否可落盘

**ModelGovernanceRecord**

- 是否已建
- 是否可落盘

如当前轮包含 P1 / P2，则继续补：

- ModelRoutePolicy
- ModelFallbackPlan
- ModelRouteDecision
- HiveModelScoreRecord
- LibraryExperienceRecord
- ModelGovernanceDecisionRecord
- 等

---

## D. 服务 / 逻辑完成情况

按模块说明：

### 1. Registry Service

- 支持哪些操作
- 当前不支持什么

### 2. Task Card Service

- 支持哪些操作
- 当前不支持什么

### 3. Route Selector

- 当前支持哪些路径
- 是否支持主备退让
- 是否支持 rule chain / reject

### 4. Governance Decision Service

- 当前能挡住哪些不合规模型
- 当前还不能做什么

### 5. Record Writer

- 落盘位置
- 文件格式
- 是否统一

---

## E. 测试通过情况

必须分类型汇报，不要只说「xx passed」。

### 1. Schema Tests

- 数量
- 覆盖了什么

### 2. Registry / Task Card Tests

- 数量
- 覆盖了什么

### 3. Record Writer Tests

- 数量
- 覆盖了什么

### 4. Routing / Governance Tests

- 数量
- 覆盖了什么

### 5. P2 Placeholder Tests

- 数量
- 覆盖了什么

### 总计

- xx passed

---

## F. 文档完成情况

逐个列出文档，并说明文档讲了什么。

示例：

- `LUNA_MODEL_MID_PLATFORM_CONSTITUTION_V1.md`：已写中台定位、四层结构、权责边界
- `LUNA_MODEL_RESPONSIBILITY_ISOLATION_V1.md`：已写职责分离与红线矩阵
- `LUNA_HIVE_SCORE_AND_RECOMMENDATION_SPEC_V1.md`：已写蜂巢评分与建议对象，占位未实现自动逻辑

---

## G. 边界复核

必须明确回答以下问题（这 6 条必须逐条回答）：

1. **是否接入了任何新模型** — 是 / 否
2. **是否实现了自动评分** — 是 / 否
3. **是否实现了自动升降级** — 是 / 否
4. **是否把评分逻辑放到了个体 Luna** — 是 / 否
5. **是否让图书馆直接改线上治理** — 是 / 否
6. **是否让蜂巢建议直接生效** — 是 / 否

---

## H. 风险 / 未完成项

只列当前轮真实存在的问题，不要写泛泛而谈。

例如：

- registry 当前仍是内存态，未接持久化索引
- route selector 目前只支持静态 policy，未支持运行态约束
- governance decision 目前只做硬阻断，未接评分结果

---

## I. 下一步建议

只允许给 1–3 条，不要开很多分叉。

例如：

- 建议进入 P1：补 route policy / fallback plan / governance decision
- 建议进入 P2：蜂巢与图书馆对象占位
- 不建议当前轮接外部 API

---

## J. 最终一句结论

必须用下面三种之一：

1. **通过**
2. **基本通过，但仍有边界缺口**
3. **未通过**

并在后面补一句原因。

示例：

- **通过**：模型中台最小治理骨架 P0 已成立，具备后续扩展 P1 的基础。
- **基本通过，但仍有边界缺口**：对象层已齐，但记录落盘尚未统一。
- **未通过**：评分逻辑越界落到个体 Luna，不符合当前宪法边界。

---

## 额外要求

- 不要用「已全部完成」这种空话
- 不要只贴 pytest 结果
- 不要省略边界复核
- 不要把「占位」说成「已实现闭环」

---

## 一句话收束

以后 Cursor 只要按这套模板回，你就能快速判断：

- 做的是不是这一轮该做的
- 有没有越界
- 哪些对象真落了
- 哪些只是口头说了

相关：**验收清单**见同目录 `LUNA_MODEL_MID_PLATFORM_ACCEPTANCE_CHECKLIST_V1.md`。

# 模型中台最小治理骨架 v1：验收清单

> 用于避免「看起来做了很多、其实没落地」。  
> 实现见 `mid_platform/model_governance/`；设计见同目录 `LUNA_MODEL_PLATFORM_*.md`。

> **代码状态（重要）**：当前仓库 **`mid_platform/model_governance/` 已实现 P0 + P1 + P2 占位**（含 `hive/`、`library/`、建议 intake/decision **schema**；**无**自动评分、自动提炼、自动消费编排）。本清单中「完整消费链**运行时**」「自动闭环」等项仍为**后续**目标。对照见 `docs/architecture/model_governance/LUNA_MODEL_MID_PLATFORM_OBJECT_MAP_V1.md`。

---

## 一、P0 验收

### 验收项 1：五个核心 schema 必须存在

必须存在并可实例化：

- `ModelRegistryCard`
- `ModelTaskCard`
- `ModelUsageRecord`
- `ModelQualityRecord`
- `ModelGovernanceRecord`

**要求**

- 都有 `to_dict()`、`from_dict()`  
- 都有最小字段校验  
- **缺关键字段须报错**，不允许静默吞掉  

---

### 验收项 2：注册服务必须能工作

`model_registry_service.py` 至少：

- 注册模型卡  
- 按 `model_id` 查询  
- 列出 `enabled` 模型  
- 按 `role_type` / `deployment_type` / `status` 过滤  

**验收标准**

- 至少 2 张模型注册卡样例能正常注册（如主模型 + 备份模型）  
- 能按 `model_id` 查到主模型与备份模型  
- **`enabled=False` 的模型不得出现在 `list_enabled()` 结果中**  

---

### 验收项 3：任务卡服务必须能工作

`model_task_card_service.py` 至少：

- 注册任务卡  
- 一个模型挂多张任务卡  
- 按 `task_domain` 反查任务卡  

**验收标准**

- 同一 `model_id` 至少能绑 **2** 张任务卡（不同 `task_card_id` / 域）  
- 能按任务域得到候选任务卡集合  
- **任务卡与模型卡的关联不丢**（`model_id` 一致）  

---

### 验收项 4：三类记录必须能落盘

写入器须能落盘：`usage`、`quality`、`governance`。

**验收标准**

- 三类记录都能写到**固定目录**下的稳定文件（JSONL 或等价）  
- 记录中**必须含 `model_id`**  
- **不允许只打印日志、不落文件**  

---

### 验收项 5：README 必须说明边界

`mid_platform/model_governance/README.md` 须写清：

- 当前已实现哪些对象  
- P1 / P2 分别是什么  
- **当前明确不做什么**  

**验收重点**

- 不得写成「中台已具备自动评分、自动升降级」  
- 不得伪装后续能力已完成  

---

## 二、P1 验收

### 验收项 6：路由策略对象必须存在

`ModelRoutePolicy` 须至少能表达：

- `task_domain` → `primary_model_id`（`task_domain_to_primary`）  
- 回退模型（`task_domain_to_fallback` / `default_fallback_model_id`，等价于「fallback_model_id」语义）  
- `fallback_to_rule_chain`  
- `shadow_candidates`  
- `background_only_models`  

**验收标准**

- 能加载**静态 policy**（对象或 JSON 反序列化）  
- 路由不依赖业务里散落的硬编码 if/else（集中由 policy + selector 表达）  

---

### 验收项 7：fallback plan 必须可执行

`ModelFallbackPlan` 须能处理：

- `timeout`  
- `invalid_output`  
- `schema_fail`  
- `governance_blocked`  

**验收标准**

- 传入错误类型，能得到**明确** fallback 决策（见 `resolve_fallback_action()`）  
- 去向落在 **`backup_model` | `rule_chain` | `clarification` | `reject`** 之一；选 `backup_model` 时须带 `backup_model_id`  

---

### 验收项 8：route decision 必须可解释

`ModelRouteDecision` 须能说明：

- 为什么选它（`selection_reason`）  
- 是否 fallback（`fallback_applied`）  
- fallback 原因（`fallback_reason`）  
- 治理约束（`governance_constraints`）  

**验收标准**

- 可 `to_dict()` 序列化  
- 后续可写入白盒或记录层  

---

### 验收项 9：route selector 必须能主备切换

`model_route_selector.py` 至少支持：

- 正常选主模型  
- 主模型不可用 → fallback  
- 主备均不可用 → `rule_chain` / `reject`  

**验收标准**

- **至少 3 个单测**分别覆盖上述三种情况  
- 不允许主模型挂了**直接抛异常**结束（须落到决策对象）  

---

### 验收项 10：治理决策服务必须能阻断不合规模型

`model_governance_decision_service.py` 至少能挡住：

- `allowed_in_mainline = false`  
- **角色不适合主链**（如非 `production` 等）  
- 明显违反 `self_judgement_forbidden`（应为 `true` 才允许主链安全默认）  

**验收标准**

- 不合规模型**不能**通过主链预检  
- 决策结果可记录（`GovernancePrecheckResult.reasons`）  
- **不允许检查失败但继续放行**  

---

## 三、P2 验收

### 验收项 11：蜂巢对象必须齐

至少：`HiveModelScoreInputPack`、`HiveModelScoreRecord`、`HiveModelRecommendation`。

**验收标准**  

- schema 完整、可实例化、可序列化  
- **不做自动评分**  

---

### 验收项 12：图书馆对象必须齐

至少：`LibraryExperienceRecord`、`LibraryExperiencePackage`、`LibraryValidationRecord`。

**验收标准**  

- 可实例化、可序列化  
- **不做自动提炼与验证**  

---

### 验收项 13：中台消费蜂巢建议对象必须齐

至少：`ModelRecommendationIntakeRecord`、`ModelGovernanceDecisionRecord`

**验收标准**  

- 能表达接收、审核、采纳/拒绝、留痕语义  
- **不做自动消费执行**  

---

### 验收项 14：文档必须和对象一致

须与 `LUNA_MODEL_PLATFORM_HIVE_SCORING_FRAMEWORK_V1.md`、`LIBRARY_POSITION`、`MIDPLATFORM_HIVE_CONSUMPTION` 等一致：

- 蜂巢负责评分与建议  
- 图书馆负责经验加工  
- 中台负责治理执行  
- **个体 Luna 不负责评分**  

**验收重点**

- 评分权不得写到个体侧  
- 图书馆不得写成「直接改线上」  
- 蜂巢不得写成「直接生效」  

---

## 四、系统级红线验收

| 红线 | 不通过条件 |
|------|------------|
| **1** | 个体侧出现模型总评分、全局优劣判断、全局升降级建议 |
| **2** | 图书馆直接改 route policy / 优先级 / 切主模型 |
| **3** | recommendation 生成后直接改 registry、直接切主模型、或不经 decision record |
| **4** | 无 usage/governance 等留痕路径却宣称「主链已纳管」 |

---

## 五、最小测试要求（应对照 pytest）

1. **Schema**：核心 5 个可实例化；缺字段失败  
2. **Registry**：注册、查询、过滤、**disabled 不误入 enabled**  
3. **Task card**：多任务卡、按域查询  
4. **Record writer**：三类落盘且含 `model_id`  
5. **Route selector**：primary / fallback / rule_chain（或 reject）  
6. **Governance**：mainline 禁止模型被挡住；**角色冲突**被挡住  
7. **P2**：hive / library / intake 对象可序列化  

---

## 六、最终一句验收结论模板

**仅当同时满足下列条件，方可声明「模型中台最小治理骨架 v1 通过」：**

1. 核心 schema 齐  
2. 注册与任务卡服务可用  
3. 使用/质量/治理记录可落盘  
4. 路由与 fallback 骨架成立（含 fallback 可执行解析）  
5. 治理决策服务能挡住不合规模型（含角色与自审规则）  
6. 蜂巢 / 图书馆 / recommendation 对象已占位  
7. **评分仍归蜂巢**，不归个体 Luna  
8. **无自动闭环越界实现**  

---

## 相关文档

- 汇报格式（建议 Cursor 输出结构）：`LUNA_MODEL_MID_PLATFORM_REPORT_TEMPLATE_V1.md`  
- 落地清单：`LUNA_MODEL_PLATFORM_DOC_AND_OBJECT_ROLLOUT_V1.md`  

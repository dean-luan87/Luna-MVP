# Luna 模型注册卡规范 v1（第一轮核心正文）

> **第一轮范围**：把「模型身份证」定死，便于 P0 落地与验收。  
> **对读**：标签与历史长文见 `../model_platform/LUNA_MODEL_PLATFORM_REGISTRY_AND_TAGS_V1.md`。  
> **代码契约**：`mid_platform/model_governance/schemas/model_registry_card.py`（当前为**字段子集**，扩展按本文与附录推进）。

---

## 1. 文档定位

模型注册卡是模型进入 Luna 中台的**最小身份对象**。

它定义模型的：

- 身份  
- 部署  
- 职责  
- 契约  
- 主链准入  
- fallback  
- 风险红线  
- 运行状态  

它**不描述**具体任务细节，**不描述**模型评分，**不描述**具体建议消费流程（见任务卡、蜂巢、中台消费 spec）。

---

## 2. 为什么必须有注册卡

没有注册卡，模型只是「可调用能力」，不是「可治理模型」。

没有注册卡会导致：

- 不知道模型是谁  
- 不知道模型能做什么  
- 不知道模型能不能进主链  
- 不知道模型失败时往哪掉  
- 不知道模型有没有越权风险  
- 不知道白盒该怎么解释它  

**注册卡是模型进入 Luna 中台的身份证。**

---

## 3. 注册卡字段分组

### 3.1 基础身份字段

- `model_id`  
- `display_name`  
- `provider`  
- `version`  

### 3.2 部署与运行字段

- `deployment_type`  
- `runtime_location`  
- `resource_profile`  

### 3.3 职责与能力字段

- `role_type`  
- `capability_domains`  
- `supported_tasks`  
- `caller_scope`  

### 3.4 输入输出契约字段

- `input_contract_id`  
- `input_contract_version`  
- `output_contract_id`  
- `output_contract_version`  
- `supports_structured_output`  
- `supports_tool_calling`  
- `supports_streaming`  

### 3.5 主链准入字段

- `allowed_in_mainline`  
- `allowed_in_shadow_mode`  
- `allowed_for_user_facing`  
- `allowed_for_background_analysis`  
- `requires_governance_gate`  

### 3.6 fallback 与替代字段

- `fallback_target_model_id`  
- `fallback_to_rule_chain`  
- `fallback_to_clarification`  
- `fallback_to_reject`  
- `replacement_candidates`  

### 3.7 成本与性能字段

- `latency_tier`  
- `cost_tier`  
- `expected_timeout_ms`  
- `token_budget_class`  

### 3.8 风险与治理字段

- `schema_guard_required`  
- `review_separation_required`  
- `self_judgement_forbidden`  
- `auto_promotion_forbidden`  
- `governance_bypass_forbidden`  

### 3.9 运行状态字段

- `enabled`  
- `status`  
- `priority`  
- `owner_module`  
- `notes`  

---

## 4. 必填字段

至少以下字段必须填写：

- `model_id`  
- `provider`  
- `version`  
- `deployment_type`  
- `role_type`  
- `capability_domains`  
- `input_contract_id`  
- `input_contract_version`  
- `output_contract_id`  
- `output_contract_version`  
- `allowed_in_mainline`  
- `fallback_target_model_id` **或** `fallback_to_rule_chain`（或其它显式 fallback 去向，见第 6 节规则 5）  
- `self_judgement_forbidden`  
- `auto_promotion_forbidden`  
- `governance_bypass_forbidden`  
- `enabled`  
- `status`  

**没有这些字段，注册卡不得通过校验。**

（工程上还须补齐 `display_name`、`runtime_location`、`supported_tasks` 等与实现校验一致的字段，见附录 A。）

---

## 5. 关键字段说明

**`model_id`**：全局唯一，不可复用。所有 usage / quality / governance record 都必须通过它关联。

**`role_type`**：必须明确是 `production` / `review` / `evaluation` / `strategy`。这是职责隔离的核心字段。

**`allowed_in_mainline`**：决定模型是否允许进入主链。不是所有模型都能进主链。

**`fallback_target_model_id` / `fallback_to_rule_chain`**：至少必须有一种可审计的 fallback 语义。**没有 fallback 的模型不得进入关键链路。**

**`self_judgement_forbidden` 等红线字段**：必须显式声明。**没有这类红线字段的模型，不得进入主链。**

---

## 6. 字段约束规则

**规则 1**  
若 `allowed_in_mainline = true`，则必须：

- `requires_governance_gate = true`  
- `schema_guard_required = true`  

**规则 2**  
若 `role_type = production`，则必须：

- `self_judgement_forbidden = true`  

**规则 3**  
若 `deployment_type = external_api`，则必须有：

- 成本字段  
- timeout 字段  

**规则 4**  
若 `status = deprecated`，则不得作为默认路由目标。

**规则 5**  
若没有 `fallback_target_model_id`，则必须：

- `fallback_to_rule_chain = true`，**或**  
- `fallback_to_reject = true`（或规范允许的其它显式去向）  

---

## 7. 注册流程

模型进入中台必须至少经过：

1. 填写注册卡  
2. 字段校验  
3. 红线校验  
4. 主链准入状态设定  
5. 写入 registry  
6. 留下变更记录  

未通过校验的注册卡，**不得**进入 active registry。

---

## 8. 高风险变更

以下字段的修改属于**高风险变更**，不得静默发生：

- `allowed_in_mainline`  
- `role_type`  
- `fallback_target_model_id`  
- `self_judgement_forbidden`  
- `governance_bypass_forbidden`  
- `deployment_type`  

这些改动必须进入变更记录，并接受中台评审。

---

## 9. 收束

模型注册卡决定模型能否被 Luna 中台识别、约束、替换和降级；**没有注册卡的模型，只能算外部能力，不能算 Luna 的可治理模型。**

---

## 附录 A：与当前代码骨架 `ModelRegistryCard` 的对照

以下字段已在 `mid_platform/model_governance/schemas/model_registry_card.py` 实现（**最小子集**）：

`model_id`、`display_name`、`provider`、`version`、`deployment_type`、`runtime_location`、`role_type`、`capability_domains`、`supported_tasks`、四套契约版本、`allowed_in_mainline`、`allowed_in_shadow_mode`、`allowed_for_user_facing`、`fallback_target_model_id`、`fallback_to_rule_chain`、`latency_tier`、`cost_tier`、`schema_guard_required`、`self_judgement_forbidden`、`auto_promotion_forbidden`、`enabled`、`status`、`priority`、`owner_module`。

**本文第 3～6 节列出的其余字段**（如 `caller_scope`、`governance_bypass_forbidden`、`supports_*`、`requires_governance_gate` 等）为 **规范完整形态**；迭代时按 `LUNA_MODEL_MID_PLATFORM_CHANGESET_POLICY_V1.md` 扩展代码与校验。

---

## 附录 B：更细的说明从哪读

分字段长说明、多组样例、与任务卡联合准入等，可与 **`../model_platform/LUNA_MODEL_PLATFORM_REGISTRY_AND_TAGS_V1.md`** 对读；**不**要求与本文逐字重复。

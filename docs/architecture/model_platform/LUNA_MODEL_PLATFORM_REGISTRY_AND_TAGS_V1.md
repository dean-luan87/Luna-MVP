# Luna 模型注册卡 + 职责隔离标签体系 v1

> 与 `LUNA_MODEL_PLATFORM_SKELETON_V1.md`、`LUNA_MODEL_PLATFORM_CONSTITUTION_V1.md`、`LUNA_MODEL_PLATFORM_ROLE_MERGE_MATRIX_V1.md` 配套。  
> 目标：以后 Luna 里每接一个模型，不是「代码里多一个 provider」，而是「中台里多一张注册卡」。

## 准入硬规则（三条）

- **没有注册卡，不准接入。**  
- **没有职责隔离标签，不准进主链。**  
- **没有降级与监管字段，不准上线。**  

---

## 一、模型注册卡的定位

模型注册卡不是文档备注，也不是注释。它是**中台管理模型的最小合法身份**。

它至少要回答 6 个问题：

1. 这是谁  
2. 它干什么  
3. 它在哪跑  
4. 它能不能进主链  
5. 它失败了怎么办  
6. 它能不能审自己 / 给自己放行  

---

## 二、模型注册卡最小字段（8 组）

建议先分成 **8 组**字段，不多不少。

### 1. 基础身份字段（它是谁）

| 字段 | 说明 |
|------|------|
| `model_id` | 唯一标识 |
| `display_name` | 展示名 |
| `provider` | 提供方标识 |
| `version` | 版本 |
| `deployment_type` | `local` / `remote_internal` / `external_api` |
| `runtime_location` | `device` / `home_server` / `cloud_internal` / `third_party_cloud` |

**说明**：只解决模型身份与部署位置。

---

### 2. 职责字段（它负责做什么）

| 字段 | 说明 |
|------|------|
| `role_type` | `production` / `review` / `evaluation` / `strategy` |
| `capability_domains` | 能力域，如 `voice_task_parse`、`vision_semantics`、`ocr_postprocess`、`language_generation`、`memory_refine`、`library_analysis`、`hive_strategy` 等 |
| `supported_tasks` | 支持的任务类型列表 |
| `caller_scope` | `individual_luna` / `library` / `hive` / `mid_platform_internal` |

**说明**：它在系统里属于哪种角色、服务谁。

---

### 3. 输入输出契约字段（它吃什么、吐什么）

| 字段 | 说明 |
|------|------|
| `input_contract_id` | 输入契约标识 |
| `input_contract_version` | 输入契约版本 |
| `output_contract_id` | 输出契约标识 |
| `output_contract_version` | 输出契约版本 |
| `supports_structured_output` | 是否支持结构化输出 |
| `supports_tool_calling` | 是否支持工具调用 |
| `supports_streaming` | 是否支持流式 |
| `max_context_class` | 上下文档位或枚举 |

**说明**：模型和系统怎么接。

---

### 4. 主链准入字段（它能不能进主链）

| 字段 | 说明 |
|------|------|
| `allowed_in_mainline` | 是否允许进入主链 |
| `allowed_in_shadow_mode` | 是否允许 shadow |
| `allowed_for_user_facing` | 是否允许面向用户前台 |
| `allowed_for_background_analysis` | 是否允许后台分析 |
| `allowed_for_direct_execution_candidate` | 是否允许作为直接执行候选 |
| `requires_governance_gate` | 是否必须经过治理门 |

**说明**：不是所有模型都能碰用户前台，不是所有模型都能碰主链。

---

### 5. 降级与替代字段（它挂了怎么办）

| 字段 | 说明 |
|------|------|
| `fallback_target_model_id` | 首选降级目标模型 |
| `fallback_to_rule_chain` | 是否可降到规则链 |
| `fallback_to_clarification` | 是否可降到澄清 |
| `fallback_to_reject` | 是否可降到拒绝 |
| `degradation_priority` | 降级优先级策略 |
| `replacement_candidates` | 替代候选列表 |

**说明**：失败时系统往哪掉。

---

### 6. 成本与性能字段（贵不贵、快不快）

| 字段 | 说明 |
|------|------|
| `latency_tier` | `ultra_low` / `low` / `medium` / `high` |
| `cost_tier` | `low` / `medium` / `high` |
| `expected_timeout_ms` | 预期超时毫秒 |
| `token_budget_class` | token 预算档位 |
| `resource_profile` | `cpu_only` / `gpu_light` / `gpu_heavy` / `external_metered` |

**说明**：后续直接影响路由。

---

### 7. 风险与治理字段（有没有风险、怎么管）

| 字段 | 说明 |
|------|------|
| `safety_level` | `strict` / `guarded` / `open_experiment` |
| `schema_guard_required` | 是否必须 schema 守护 |
| `review_separation_required` | 是否要求审核与生产分离 |
| `self_judgement_forbidden` | 是否禁止自审 |
| `auto_promotion_forbidden` | 是否禁止自动晋升/上线 |
| `policy_tags` | 策略标签列表 |

**说明**：把「不能又当裁判又当运动员」写进结构里。

---

### 8. 运行状态字段（现在能不能用）

| 字段 | 说明 |
|------|------|
| `enabled` | 是否启用 |
| `status` | `active` / `standby` / `blocked` / `deprecated` / `experiment` |
| `priority` | 路由优先级 |
| `owner_module` | 归属模块 |
| `notes` | 备注 |

**说明**：让中台知道是不是当前主用模型。

---

## 三、职责隔离标签体系

不要只写 `role_type`，还要单独补一组**权责标签**。一个模型可能是生产类，但不能因此默认它什么都能做。

### 标签组 1：生产权限标签

| 标签 | 用途 |
|------|------|
| `can_produce_user_facing_output` | 能否产出面向用户的内容 |
| `can_produce_task_candidates` | 能否产出任务候选 |
| `can_produce_clarification_candidates` | 能否产出澄清候选 |
| `can_produce_strategy_candidates` | 能否产出策略候选（仍为候选，不自动生效） |

**用途**：控制它到底能产出哪类东西。

---

### 标签组 2：审核权限标签

| 标签 | 用途 |
|------|------|
| `can_review_other_model_output` | 能否审核其他模型输出 |
| `can_review_schema_validity` | 能否审核 schema |
| `can_review_risk_flags` | 能否审核风险标记 |
| `can_review_mapping_legality` | 能否审核映射合法性 |

**用途**：控制它能不能当「审核类模型」。

---

### 标签组 3：评估权限标签

| 标签 | 用途 |
|------|------|
| `can_evaluate_runtime_quality` | 能否评估运行时质量 |
| `can_generate_quality_score` | 能否生成质量分 |
| `can_generate_error_attribution` | 能否生成错误归因 |
| `can_generate_comparison_report` | 能否生成对比报告 |

**用途**：控制它能不能参与复盘分析。

---

### 标签组 4：策略权限标签

| 标签 | 用途 |
|------|------|
| `can_suggest_routing_change` | 能否建议路由变更 |
| `can_suggest_prompt_change` | 能否建议提示词变更 |
| `can_suggest_model_upgrade` | 能否建议模型升降级 |
| `can_suggest_library_package` | 能否建议图书馆经验包 |

**用途**：控制它能不能提策略建议（建议不等于生效）。

---

### 标签组 5：禁止标签（强制）

| 标签 | 用途 |
|------|------|
| `forbidden_to_review_self_output` | 禁止审核自己的产出 |
| `forbidden_to_promote_self` | 禁止自我晋升/放行上线 |
| `forbidden_to_bypass_governance` | 禁止绕过治理 |
| `forbidden_to_finalize_execution` | 禁止最终裁定执行 |
| `forbidden_to_modify_registry` | 禁止修改注册表 |

**用途**：不是「建议禁止」，而是**系统硬约束**。

---

## 四、最重要的合规判断字段（强约束布尔）

建议在注册卡里直接加入 4 个强约束布尔值（默认语义如下）：

| 字段 | 建议默认 | 含义 |
|------|----------|------|
| `self_review_forbidden` | `true` | 禁止本轮自审 |
| `self_promotion_forbidden` | `true` | 禁止自我晋升/放行 |
| `self_execution_approval_forbidden` | `true` | 禁止自我批准执行 |
| `governance_bypass_forbidden` | `true` | 禁止绕过治理 |

**规则**：以后任何模型，只要这 4 个里**有一个未显式配置为合规语义**，**默认不准进主链**（由中台校验器执行）。

---

## 五、模型注册卡示例（简化 JSON）

例子：**长语音任务理解模型**

```json
{
  "model_id": "voice_task_parse_openai_v1",
  "display_name": "OpenAI Voice Task Parser",
  "provider": "openai",
  "version": "v1",
  "deployment_type": "external_api",
  "runtime_location": "third_party_cloud",

  "role_type": "production",
  "capability_domains": ["voice_task_parse"],
  "supported_tasks": [
    "long_voice_task_parse",
    "mixed_input_split",
    "clarification_candidate_generation",
    "unsupported_candidate_generation"
  ],
  "caller_scope": ["individual_luna"],

  "input_contract_id": "voice_long_input_contract",
  "input_contract_version": "1.0",
  "output_contract_id": "voice_task_parse_v1_1",
  "output_contract_version": "1.1",
  "supports_structured_output": true,
  "supports_tool_calling": false,
  "supports_streaming": false,

  "allowed_in_mainline": true,
  "allowed_in_shadow_mode": true,
  "allowed_for_user_facing": false,
  "allowed_for_background_analysis": false,
  "allowed_for_direct_execution_candidate": false,
  "requires_governance_gate": true,

  "fallback_target_model_id": "voice_task_parse_rule_v1",
  "fallback_to_rule_chain": true,
  "fallback_to_clarification": true,
  "fallback_to_reject": false,

  "latency_tier": "medium",
  "cost_tier": "medium",
  "expected_timeout_ms": 8000,
  "resource_profile": "external_metered",

  "safety_level": "guarded",
  "schema_guard_required": true,
  "review_separation_required": true,
  "self_judgement_forbidden": true,
  "auto_promotion_forbidden": true,

  "self_review_forbidden": true,
  "self_promotion_forbidden": true,
  "self_execution_approval_forbidden": true,
  "governance_bypass_forbidden": true,

  "enabled": true,
  "status": "experiment",
  "priority": 1,
  "owner_module": "voice_mid_platform"
}
```

（职责隔离标签可按第三节补全为并列对象或 `tag` 子文档，由实现选定一种序列化方式。）

---

## 六、为什么这个注册卡重要

模型一多，没有注册卡会立刻出现 5 个问题：

1. 不知道哪个模型是主模型  
2. 不知道哪个模型能碰主链  
3. 不知道哪个模型能面向用户  
4. 不知道哪个模型失败时往哪掉  
5. 不知道它有没有越权风险  

因此注册卡不是形式主义，是**中台最小治理单位**。

---

## 七、模型登记流程（写死四步）

以后每接一个模型，必须走：

### 第一步：注册

填写注册卡，确定：身份、职责、契约、权限、降级、风险。

### 第二步：校验

中台检查：

- 契约是否完整  
- 权责标签是否齐全  
- 自评自审禁令是否明确  
- fallback 是否存在  

### 第三步：准入

决定：只准 shadow / 只准 background / 可准主链实验 / 不准上线。

### 第四步：留痕

写入：注册记录、变更记录、状态记录。

---

## 八、这张注册卡后面会喂给谁

| 消费方 | 用途 |
|--------|------|
| **中台** | 路由、主备、降级、准入 |
| **白盒** | 当前用了谁、为何能进主链、为何被降级 |
| **图书馆** | 某条经验适用于哪类模型 |
| **蜂巢** | 哪类模型在哪类任务上表现好、是否该升降级 |

---

## 九、与「模型任务卡」的边界

**注册卡**解决：它是谁、能不能用、怎么管。

**模型任务卡**（`LUNA_MODEL_PLATFORM_TASK_CARD_V1.md`）解决：该模型在**每个任务**上具体做什么、输入输出、合格标准。二者不可互相替代。

---

## 十、一句话收束

**模型注册卡是中台管理模型的身份证，职责隔离标签是模型的法律边界。没有身份证，不准入场；没有法律边界，不准上主链。**

---

## 下一步

- **已完成**：`LUNA_MODEL_PLATFORM_TASK_CARD_V1.md`（任务卡 7 组字段、8 段正文、示例与联动规则）。  
- **已完成**：`LUNA_MODEL_PLATFORM_HIVE_SCORING_FRAMEWORK_V1.md`（蜂巢专属评分与优化；宪法第十三条）。  
- **已完成**：`LUNA_MODEL_PLATFORM_HIVE_SCORING_RECORDS_AND_TEMPLATES_V1.md`（Input Pack / Record / Recommendation）。  
- **已完成**：`LUNA_MODEL_PLATFORM_MIDPLATFORM_HIVE_CONSUMPTION_V1.md`。  
- **下一档**：见 `LUNA_MODEL_PLATFORM_LIBRARY_POSITION_AND_INTERFACE_V1.md`、`LUNA_MODEL_PLATFORM_GOVERNANCE_PANORAMA_V1.md`。

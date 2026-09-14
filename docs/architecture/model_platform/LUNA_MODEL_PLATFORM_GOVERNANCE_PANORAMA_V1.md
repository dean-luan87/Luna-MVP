# Luna 模型治理全景图 / 总览表 v1

> **作用**：不展开细节，只把 **个体 Luna、图书馆、蜂巢、中台** 四方关系一次讲透。  
> 细节见同目录各 `LUNA_MODEL_PLATFORM_*.md` 专题文档。

---

## 一、四大主体总定位

| 主体 | 核心定位 | 能做什么 | 不能做什么 |
|------|----------|----------|------------|
| **个体 Luna** | 前台生产与执行前理解单元 | 使用模型、产出候选、留痕、执行前互动 | 不做全局评分、不自审、不自放行 |
| **图书馆** | 经验加工层 | 归档、提炼、验证、经验打包 | 不直接改线上治理、不直接改主链 |
| **蜂巢** | 全局评估与策略建议层 | 模型评分、比较、归因、提建议 | 不直接上线、不直接改中台配置 |
| **中台** | 模型与能力治理中枢 | 接入、注册、路由、治理、升降级、执行建议 | 不替代前台生产、不替代图书馆提炼、不替代蜂巢评分 |

---

## 二、四方关系总链路（运行链）

1. 个体 Luna 调用模型  
2. 白盒记录  
3. 图书馆提炼经验  
4. 蜂巢评分与生成建议  
5. 中台消费建议并执行治理  
6. 新配置 / 经验再回流个体 Luna  

---

## 三、中台四层结构总表

| 层级 | 名称 | 核心职责 | 关键产物 |
|------|------|----------|----------|
| **L1** | 接入层 | 统一接本地模型、远程模型、外部 API | provider、client、adapter |
| **L2** | 注册与路由层 | 记录模型、选择模型、主备切换、fallback 映射 | registry、route selector、priority policy |
| **L3** | 治理层 | 输入裁剪、输出校验、schema 检查、越权阻断、降级 | validator、policy gate、degradation rules |
| **L4** | 评估与优化层 | 记录表现、对比模型、形成优化建议 | usage record、quality record、optimization suggestion |

---

## 四、模型职责四分法

| 职责类 | 定义 | 典型任务 | 是否可直接面向用户 |
|--------|------|----------|---------------------|
| **生产类** | 直接产出系统可消费结果 | 长语音拆解、视觉语义、语言生成 | 可，视任务而定 |
| **审核类** | 检查生产结果是否合法 | schema 审查、映射合法性、风险检查 | 不直接面向用户 |
| **评估类** | 对历史表现做评分归因 | 质量分析、错误归因、模型比较 | 不直接面向用户 |
| **策略类** | 生成优化与治理建议 | 升降级建议、路由建议、经验包建议 | 不直接面向用户 |

---

## 五、职责合并与隔离总表

| 组合 | 是否允许 | 规则 |
|------|----------|------|
| 生产 + 生产 | **允许**（限同链条） | 例如任务拆解 + clarification + unsupported |
| 审核 + 审核 | **允许** | 例如 schema + 映射合法性 + 风险辅助审核 |
| 评估 + 策略 | **允许** | 适合蜂巢 |
| 生产 + 审核 | **不允许** | 不能既当运动员又当裁判 |
| 生产 + 最终裁决 | **不允许** | 模型不能自己放行自己 |
| 线上生产 + 线上自评 | **不允许** | 不能自己给自己打分 |
| 策略建议 + 直接生效 | **不允许** | 建议必须经中台治理链 |

---

## 六、模型注册卡总表

每个模型必须注册以下信息（字段组 → 内容）：

| 字段组 | 内容 |
|--------|------|
| **基础身份** | `model_id`、`provider`、`version`、`deployment_type`、`runtime_location` |
| **职责信息** | `role_type`、`capability_domains`、`supported_tasks`、`caller_scope` |
| **输入输出契约** | `input_contract_id`/`version`、`output_contract_id`/`version`、`supports_structured_output` |
| **主链准入** | `allowed_in_mainline`、`allowed_in_shadow_mode`、`allowed_for_user_facing` |
| **降级替代** | `fallback_target_model_id`、`fallback_to_rule_chain`、`replacement_candidates` |
| **成本性能** | `latency_tier`、`cost_tier`、`expected_timeout_ms`、`resource_profile` |
| **风险治理** | `schema_guard_required`、`self_judgement_forbidden`、`auto_promotion_forbidden` |
| **运行状态** | `enabled`、`status`、`priority`、`owner_module` |

详：`LUNA_MODEL_PLATFORM_REGISTRY_AND_TAGS_V1.md`。

---

## 七、模型任务卡总表

每个「模型 × 任务」必须定义：

| 字段组 | 内容 |
|--------|------|
| **任务身份** | `task_card_id`、`model_id`、`task_name`、`task_domain` |
| **职责定义** | `task_goal`、`task_responsibility`、`task_boundary`、`task_non_responsibility` |
| **输入定义** | `input_sources`、`input_required_fields`、`input_optional_fields`、`context_dependencies` |
| **加工方式** | `processing_mode`、`processing_constraints`、`processing_forbidden_behaviors` |
| **输出定义** | `output_contract`、`output_required_fields`、`output_downstream_consumers` |
| **合格标准** | `success_criteria`、`failure_criteria`、`quality_metrics` |
| **失败处理** | `fallback_behavior` |

详：`LUNA_MODEL_PLATFORM_TASK_CARD_V1.md`。

---

## 八、蜂巢评分体系总表

### 蜂巢的职责 / 不做

| 蜂巢做 | 蜂巢不做 |
|--------|----------|
| 做评分、做对比、做归因、给建议 | 不直接改中台、不直接让建议生效、不直接替换主模型 |

### 蜂巢评分六维

| 维度 | 含义 |
|------|------|
| **稳定性分** | timeout、成功率、fallback 率、服务可用性 |
| **质量分** | validator 通过率、语义质量、mixed 保留质量 |
| **时延分** | 平均耗时、P95/P99、冷热启动差异 |
| **成本分** | 调用成本、资源消耗、单位有效输出成本 |
| **治理友好度分** | schema 合规率、非法映射率、越权率 |
| **可演化分** | 是否值得继续优化、扩域、复用 |

### 蜂巢输出对象

| 对象 | 作用 |
|------|------|
| **Hive Model Score Input Pack** | 蜂巢评分输入原料包 |
| **Hive Model Score Record** | 蜂巢评分记录 |
| **Hive Model Recommendation** | 蜂巢给中台的建议 |

详：`LUNA_MODEL_PLATFORM_HIVE_SCORING_FRAMEWORK_V1.md`、`LUNA_MODEL_PLATFORM_HIVE_SCORING_RECORDS_AND_TEMPLATES_V1.md`。

---

## 九、中台消费蜂巢建议总表

### 中台消费四层

| 层级 | 职责 |
|------|------|
| **接收层** | 收建议、校验结构、登记来源 |
| **审核层** | 是否越权、是否合法、是否有证据 |
| **决策层** | 采纳、部分采纳、延后、拒绝 |
| **执行层** | 灰度、限域、降级、退役、回滚 |

### 中台消费结果五类

| 结果 | 含义 |
|------|------|
| **全量采纳** | 按建议执行 |
| **带约束采纳** | 接受方向，但加限制 |
| **部分采纳** | 只采纳建议的一部分 |
| **延后采纳** | 继续观察，暂不动作 |
| **明确拒绝** | 不执行该建议 |

详：`LUNA_MODEL_PLATFORM_MIDPLATFORM_HIVE_CONSUMPTION_V1.md`。

---

## 十、图书馆接口总表

### 图书馆的职责 / 不做

| 图书馆做 | 图书馆不做 |
|----------|------------|
| 归档、提炼、验证、打包经验 | 不直接评分、不直接治理、不直接改线上 |

### 图书馆对象

| 对象 | 作用 |
|------|------|
| **Library Experience Record** | 单条经验记录 |
| **Library Experience Package** | 提炼后的经验包 |
| **Library Validation Record** | 经验验证结果 |

### 图书馆接口方向

| 方向 | 内容 |
|------|------|
| **个体 Luna → 图书馆** | 使用记录摘要、质量问题摘要、事件上下文摘要 |
| **图书馆 → 个体 Luna** | 经验包候选、历史辅助信息 |
| **图书馆 → 蜂巢** | 模型问题经验包、任务经验包、优化线索包 |
| **蜂巢 → 图书馆** | 重点观察方向、经验提炼要求 |
| **图书馆 → 中台** | 证据材料、验证结果、测试样本集 |
| **中台 → 图书馆** | 补证据、补测试、补经验包请求 |

详：`LUNA_MODEL_PLATFORM_LIBRARY_POSITION_AND_INTERFACE_V1.md`。

---

## 十一、白盒、中台、图书馆、蜂巢分工总表

| 模块 | 核心职责 |
|------|----------|
| **白盒** | 可观察，记录发生了什么 |
| **中台** | 可治理，决定能不能用、怎么用 |
| **图书馆** | 可提炼，把经验变成资产 |
| **蜂巢** | 可评分、可比较、可提建议 |

---

## 十二、系统级宪法摘要版

1. 模型不是主权者  
2. 所有模型必须统一纳管  
3. 所有模型必须可替换、可降级、可留痕  
4. 生产与审核必须分离  
5. 生产与最终裁决必须分离  
6. **评估权归蜂巢，不归个体 Luna**  
7. **图书馆只提供经验与证据，不直接治理**  
8. **蜂巢建议不得直接生效**  
9. **中台负责治理执行，不替代生产与提炼**  
10. **无注册卡、无任务卡、无留痕记录，不准进主链**  

全文：`LUNA_MODEL_PLATFORM_CONSTITUTION_V1.md`。

---

## 十三、最短收束

到这里，**模型治理大框架**已闭环：

- 中台骨架  
- 宪法  
- 职责隔离矩阵  
- 注册卡  
- 任务卡  
- 蜂巢评分  
- 蜂巢建议  
- 中台消费建议  
- 图书馆位置与接口  
- **本总览表**  

---

## 下一步（工程向）

**文档落地顺序 / 中台对象清单（三批文档映射 + 19 对象 + 阶段 + 目录 + P0/P1/P2 + 当前不做）**：见 `LUNA_MODEL_PLATFORM_DOC_AND_OBJECT_ROLLOUT_V1.md`。  
**再下一步**：Cursor 可执行版任务拆解（P0/P1/P2），可单开 `…_TASK_BREAKDOWN_V1.md`。

---

## 专题文档索引

| 文档 | 主题 |
|------|------|
| `LUNA_MODEL_PLATFORM_SKELETON_V1.md` | 中台四层骨架 |
| `LUNA_MODEL_PLATFORM_CONSTITUTION_V1.md` | 宪法（含第十三、十四条） |
| `LUNA_MODEL_PLATFORM_ROLE_MERGE_MATRIX_V1.md` | 职责合并/隔离矩阵 |
| `LUNA_MODEL_PLATFORM_REGISTRY_AND_TAGS_V1.md` | 注册卡与标签 |
| `LUNA_MODEL_PLATFORM_TASK_CARD_V1.md` | 任务卡 |
| `LUNA_MODEL_PLATFORM_HIVE_SCORING_FRAMEWORK_V1.md` | 蜂巢评分框架 |
| `LUNA_MODEL_PLATFORM_HIVE_SCORING_RECORDS_AND_TEMPLATES_V1.md` | 评分输入/记录/建议 |
| `LUNA_MODEL_PLATFORM_MIDPLATFORM_HIVE_CONSUMPTION_V1.md` | 中台消费建议 |
| `LUNA_MODEL_PLATFORM_LIBRARY_POSITION_AND_INTERFACE_V1.md` | 图书馆接口 |
| `LUNA_MODEL_PLATFORM_GOVERNANCE_PANORAMA_V1.md` | **本文件** |
| `LUNA_MODEL_PLATFORM_DOC_AND_OBJECT_ROLLOUT_V1.md` | 落地顺序与对象清单 |

# Luna 模型中台宪法 v1（正式约束）

> 文风要求：约束式、冷静、明确、不留模糊空间。  
> 本宪法适用于 Luna 全仓所有模型接入与调用；违反即视为越界污染。  
> 四层职责划分见同目录 `LUNA_MODEL_PLATFORM_SKELETON_V1.md`。  
> 职责合并 / 隔离与红线矩阵见 `LUNA_MODEL_PLATFORM_ROLE_MERGE_MATRIX_V1.md`。  
> 模型注册卡与职责隔离标签见 `LUNA_MODEL_PLATFORM_REGISTRY_AND_TAGS_V1.md`。  
> 模型任务卡（模型 × 任务）见 `LUNA_MODEL_PLATFORM_TASK_CARD_V1.md`。  
> 蜂巢评分与优化框架见 `LUNA_MODEL_PLATFORM_HIVE_SCORING_FRAMEWORK_V1.md`。  
> 蜂巢评分输入包、评分记录与建议对象见 `LUNA_MODEL_PLATFORM_HIVE_SCORING_RECORDS_AND_TEMPLATES_V1.md`。  
> 中台如何消费蜂巢建议见 `LUNA_MODEL_PLATFORM_MIDPLATFORM_HIVE_CONSUMPTION_V1.md`。  
> 图书馆位置与接口见 `LUNA_MODEL_PLATFORM_LIBRARY_POSITION_AND_INTERFACE_V1.md`。  
> 四方关系总览见 `LUNA_MODEL_PLATFORM_GOVERNANCE_PANORAMA_V1.md`。  
> 文档落地顺序与中台对象清单见 `LUNA_MODEL_PLATFORM_DOC_AND_OBJECT_ROLLOUT_V1.md`。

## 第一条：模型不是主权者

任何模型，无论本地还是外部 API，都只是能力单元，不是系统主权者。

模型不得直接拥有：

- 执行主权  
- 任务主权  
- 记忆主权  
- 白盒主权  
- 治理主权  

---

## 第二条：模型必须统一纳管

所有模型必须先进入中台注册，再允许被系统调用。

禁止：

- 模块私接模型  
- 业务层绕过中台直调外部 API  
- 白盒私自持有模型调用链  
- 图书馆 / 蜂巢绕开中台单独接模型  

---

## 第三条：模型必须可替换

任何模型都必须有：

- 唯一 `model_id`  
- 版本号  
- 能力标签  
- 输入契约  
- 输出契约  
- fallback 去向  

禁止把某个模型写死为唯一不可替代实现。

---

## 第四条：模型必须可降级

任何模型失败时，都必须有明确降级路径。

**触发条件**包括但不限于：

- timeout  
- 输出非法  
- schema 不通过  
- 成本超限  
- 服务不可达  
- 成功率异常下降  

**降级目标**包括但不限于：

- 低配模型  
- 规则链  
- clarification  
- reject  

---

## 第五条：生产与审核必须分离

同一个模型不得在同一轮闭环中同时承担：

- 结果生产者  
- 结果审核者  

即：**不能既当运动员，又当裁判。**

---

## 第六条：生产与最终裁决必须分离

模型可以提出：

- 任务候选  
- clarification 候选  
- unsupported 候选  
- feedback 候选  

但不能直接决定：

- 是否通过 validator  
- 是否进入 builder  
- 是否进入执行链  
- 是否替代 fallback  

**最终裁决权属于治理层。**

---

## 第七条：评估与被评估对象必须分离

同一个模型不得：

- 自己跑线上任务  
- 自己回头给自己打分  
- 自己决定自己是否上线  

评估权必须独立。

---

## 第八条：策略建议不得直接生效

模型可以生成：

- 优化建议  
- 路由建议  
- 升降级建议  
- 图书馆经验建议  

但不得直接修改：

- 主链路由  
- 模型优先级  
- 线上 validator 规则  
- 执行策略  

策略建议必须经过中台治理链、测试链或人工确认。

---

## 第九条：白盒负责可观察，中台负责可治理

**白盒职责**

- 摊开模型输入输出摘要  
- 摊开耗时、错误、fallback、版本  
- 让人看见发生了什么  

**中台职责**

- 决定能不能用  
- 决定该不该降级  
- 决定何时熔断  
- 决定是否允许上线  

白盒不代替中台裁决，中台不代替白盒展示。

---

## 第十条：所有模型调用必须留痕

每次模型调用至少要记录：

- `model_id`  
- `task_type`  
- `caller_module`  
- `input_contract_version`  
- `output_contract_version`  
- `latency_ms`  
- `success`  
- `validator_passed`  
- `fallback_triggered`  
- `error_type`  
- `error_stage`  
- `cost_estimate`  

**无留痕，不准入主链。**

---

## 第十一条：模型职责必须显式声明

每个模型必须声明自己属于哪类职责：

- 生产类  
- 审核类  
- 评估类  
- 策略类  

同时必须声明：

- 可做什么  
- 不可做什么  
- 是否允许实验  
- 是否允许面向用户  
- 是否允许接入主链  

---

## 第十二条：可合并职责与不可合并职责必须显式标明

**允许合并**

- 同一生产链内部的连续理解职责  
- 同一复盘链内部的分析职责  

**禁止合并**

- 生产 + 审核  
- 生产 + 最终裁决  
- 线上生产 + 自我评估  
- 策略建议 + 直接生效  

---

## 第十三条：评分权、对比权与优化建议权归蜂巢；个体不得自评分

**模型评分权、模型对比权、模型优化建议权归蜂巢；个体 Luna 不得自评分，中台不得仅凭单轮个体表现直接生成模型全局结论。**

**个体 Luna**

- 只负责使用模型，并留下 Usage / Quality / Governance 三类痕迹。  
- **不得**给模型打总分，**不得**对模型优劣做最终结论，**不得**基于自评分自行切换主备模型或路由。  

**图书馆**

- 负责提炼、经验归纳，**不**承担蜂巢级跨模型全局评分主责（可与蜂巢输入衔接）。  

**蜂巢**

- 负责模型评分、模型对比、优劣判断、优化建议的**产出**（策略层）。  
- **不得**直接修改线上注册卡、直接切主模型、直接替换 fallback、直接下发强制生效规则；须交由中台治理与执行。  

**中台**

- 负责治理决策与执行升降级、灰度、熔断、替换；**接受**蜂巢与中台流程的输入，**不**替代蜂巢做全局评分主脑。  

**若将评分放在个体侧**，将导致：视角局部易误判、与当前任务强绑定偏差大、使用者与受影响者合一而不适合最终评估。  

---

## 第十四条：图书馆为经验加工层，不得替代蜂巢与中台

**图书馆**是模型与任务经验的**加工中枢**，不是执行中枢、不是治理中枢、不是评分中枢。

1. 图书馆只提供经验材料、经验包与验证结果，**不得直接下发**线上强制动作。  
2. 必须先提炼、再验证、再打包；**禁止**原始经验未经处理直接进入中台治理链。  
3. 可向蜂巢提供高纯度经验输入，可响应中台补证据与补样本请求；**不得**替代蜂巢评分与中台裁决。  
4. 下发给个体 Luna 的只能是**辅助经验**；**不得**以经验包形式绕开主链与中台治理。  

详述与接口见 `LUNA_MODEL_PLATFORM_LIBRARY_POSITION_AND_INTERFACE_V1.md`。

---

## 附录 A：中台最小注册记录模板

> 完整 8 组字段、标签体系、登记流程与 JSON 示例见 `LUNA_MODEL_PLATFORM_REGISTRY_AND_TAGS_V1.md`。以下为最小子集速查。

每个模型至少包含：

| 字段 | 说明 |
|------|------|
| `model_id` | 唯一标识 |
| `display_name` | 展示名 |
| `deployment_type` | `local` / `remote_internal` / `external_api` |
| `provider` | 提供方标识 |
| `version` | 语义化或构建版本 |
| `capability_domains` | 能力域 |
| `supported_tasks` | 支持的任务类型 |
| `input_contract` | 输入契约引用或版本 |
| `output_contract` | 输出契约引用或版本 |
| `latency_tier` | 延迟档位 |
| `cost_tier` | 成本档位 |
| `safety_level` | 安全等级 |
| `enabled` | 是否启用 |
| `priority` | 路由优先级 |
| `fallback_target` | 降级目标 `model_id` 或策略名 |
| `owner_module` | 归属模块 |
| `status` | 生命周期状态（如 experimental / production / deprecated） |

---

## 附录 B：中台最小监管记录模板

### 1. Usage Record（用量）

- 谁调用了  
- 调了谁  
- 花了多久  
- 成没成功  

### 2. Quality Record（质量）

- validator 过没过  
- 输出质量如何  
- 是否命中 fallback  
- 是否保留 mixed / non-task  

### 3. Governance Record（治理）

- 是否触发熔断  
- 是否触发降级  
- 是否越权  
- 是否违反契约  

---

## 最后一句收束

**模型可以帮 Luna 做事，但不能绕过 Luna 的治理体系；模型可以生产、分析、建议，但不能自己审判自己、自己放行自己、自己替换自己。**

# Luna 模型任务卡模板 v1

> 与 `LUNA_MODEL_PLATFORM_REGISTRY_AND_TAGS_V1.md` 配套：**注册卡**管模型维度，**任务卡**管「模型 × 任务」维度。  
> 亦与骨架、宪法、职责矩阵一致：`LUNA_MODEL_PLATFORM_SKELETON_V1.md`、`LUNA_MODEL_PLATFORM_CONSTITUTION_V1.md`、`LUNA_MODEL_PLATFORM_ROLE_MERGE_MATRIX_V1.md`。

---

## 定位对比

若 **模型注册卡**解决的是：

- 它是谁  
- 它能不能接  
- 它能不能进主链  
- 它失败了怎么办  

则 **模型任务卡**解决的是：

- 它到底负责什么任务  
- 任务输入是什么  
- 加工方式是什么  
- 输出是什么  
- 合格标准是什么  

**受众**：中台、白盒、图书馆、蜂巢**共同**使用。

---

## 一、模型任务卡的定位

每个模型可以有一张**注册卡**，但一个模型可能承担**多个任务**。

**规则**

- **注册卡**：按**模型**维度管理。  
- **任务卡**：按「**模型 × 任务**」维度管理。  

即：**注册卡**管模型身份；**任务卡**管模型职责。

---

## 二、模型任务卡最小字段（7 组）

### 1. 任务身份字段

| 字段 | 说明 |
|------|------|
| `task_card_id` | 任务卡唯一标识 |
| `model_id` | 关联的模型（注册卡） |
| `task_name` | 任务展示名 |
| `task_code` | 任务代码（稳定键） |
| `task_domain` | 任务域 |
| `task_owner_scope` | `individual_luna` / `library` / `hive` / `mid_platform` |

**作用**：这张卡描述的是**哪个模型**、**哪一个任务**。

---

### 2. 任务职责字段

| 字段 | 说明 |
|------|------|
| `task_goal` | 任务目标（一句话） |
| `task_responsibility` | 必须承担什么 |
| `task_boundary` | 边界内做什么 |
| `task_non_responsibility` | 明确不做什么 |

**作用**：防止模型职责无限膨胀。

---

### 3. 输入字段

| 字段 | 说明 |
|------|------|
| `input_sources` | 输入来源说明 |
| `input_contract` | 输入契约引用 |
| `input_required_fields` | 必填字段 |
| `input_optional_fields` | 可选字段 |
| `input_preprocessing` | 预处理要求 |
| `context_dependencies` | 上下文依赖（如任务态、记忆、经验包、白盒历史等） |

**作用**：回答「它吃什么」（文本、视觉摘要、任务上下文、历史记忆摘要、图书馆经验包、白盒历史记录等）。

---

### 4. 加工字段

| 字段 | 说明 |
|------|------|
| `processing_mode` | `single_pass` / `multi_stage` / `candidate_generation` / `analysis_only` 等 |
| `processing_constraints` | 加工约束 |
| `processing_forbidden_behaviors` | 禁止行为（如自由散文、跳过 schema、越权补全） |
| `governance_requirements` | 治理要求 |

**作用**：回答「它怎么加工」。

---

### 5. 输出字段

| 字段 | 说明 |
|------|------|
| `output_contract` | 输出契约引用 |
| `output_required_fields` | 必填输出 |
| `output_optional_fields` | 可选输出 |
| `output_downstream_consumers` | 下游消费方 |
| `output_is_user_facing` | 是否可直接面向用户 |
| `output_requires_validation` | 是否必须经过校验 |

**作用**：回答「它吐什么、吐给谁」。

---

### 6. 质量字段

| 字段 | 说明 |
|------|------|
| `success_criteria` | 合格标准 |
| `failure_criteria` | 失败标准 |
| `quality_metrics` | 质量指标 |
| `minimum_acceptance_threshold` | 最低可接受阈值 |
| `fallback_behavior` | 失败时行为（与注册卡降级对齐） |

**作用**：什么叫合格、什么叫失败；供白盒、中台、图书馆评估基础使用。

---

### 7. 观测与记录字段

| 字段 | 说明 |
|------|------|
| `usage_record_required` | 是否必须用量记录 |
| `quality_record_required` | 是否必须质量记录 |
| `governance_record_required` | 是否必须治理记录 |
| `whitebox_visibility_level` | 白盒可见级别 |
| `archive_requirement` | 归档要求 |

**作用**：该任务是否重点观察、重点归档。

---

## 三、任务卡模板正文结构（固定 8 段）

以后每张任务卡**正文**建议按以下 **8 段**书写，格式固定：

1. **任务名称** — 这是什么任务。  
2. **任务目标** — 要达成什么结果。  
3. **任务边界** — 做什么、不做什么。  
4. **输入定义** — 吃哪些输入，哪些必须、哪些可选。  
5. **加工方式** — 单轮、多段、候选生成、分析、提炼等。  
6. **输出定义** — 吐给谁、格式是什么、是否可直接面向用户。  
7. **合格标准** — 怎样算通过、怎样算失败。  
8. **失败后的处理** — 规则链、clarification、reject、低配模型等。  

---

## 四、关键任务卡分类示例

### A. 个体 Luna：长语音任务拆解 — `long_voice_task_parse`

| 段落 | 内容摘要 |
|------|-----------|
| **任务目标** | 从长语音文本中提取：任务/非任务切分、任务候选、clarification 候选、unsupported 候选、feedback mode 候选。 |
| **不负责** | 最终执行裁决；直接放行 builder；最终用户回复生成；情感安抚本体；记忆写入主权。 |
| **输入** | 长文本；session/context hint；当前任务态摘要（可选）；历史记忆摘要（未来可选）。 |
| **输出** | `VoiceLongInputStructuredParseResult`（与实现契约一致）。 |
| **合格标准** | schema 合法；主域合理；`task_candidates` 逻辑不冲突；mixed 下能保留 `non_task_payload`；clarification/unsupported 不明显跑偏。 |
| **失败标准** | 非 JSON；缺关键字段；域判断失真；候选冲突严重；timeout。 |
| **fallback** | 规则链；clarification；reject。 |

---

### B. 个体 Luna：视觉语义理解 — `vision_semantic_interpretation`

| 段落 | 内容摘要 |
|------|-----------|
| **任务目标** | 将检测、OCR、深度、场景线索加工成可行动语义。 |
| **不负责** | 直接下执行命令；直接替代风险中心；直接决定导航动作。 |
| **输入** | 视觉检测结果；OCR；深度/距离；当前任务摘要。 |
| **输出** | 结构化场景语义摘要；目标候选；环境风险候选；路径语义候选。 |
| **合格标准** | 不虚构关键物体；不跳过风险信息；输出可被后续模块消费。 |
| **fallback** | 回退规则解释层；降级为最小语义摘要。 |

---

### C. 个体 Luna：语言表达 — `response_language_rendering`

| 段落 | 内容摘要 |
|------|-----------|
| **任务目标** | 将系统已有结论加工成用户可理解的话。 |
| **不负责** | 自己生成任务计划；改任务含义；改风险等级；拍板执行。 |
| **输入** | 已确认的系统结论；反馈模式；用户语言风格偏好（未来）；情感调节参数（未来）。 |
| **输出** | 用户可读文案；播报短句；追问文案候选。 |
| **合格标准** | 不篡改原意；不越权补充新任务；不弱化风险提醒。 |
| **fallback** | 模板文本；最小播报语。 |

---

### D. 图书馆：经验归因 — `library_failure_attribution`

| 段落 | 内容摘要 |
|------|-----------|
| **任务目标** | 对失败案例归类、提炼原因、生成经验条目草案。 |
| **不负责** | 直接下发线上改动；直接修改模型优先级；覆盖个体 Luna 运行逻辑。 |
| **输入** | 使用记录；质量记录；治理记录；白盒摘要。 |
| **输出** | 失败归因；经验候选；测试用例建议；风险标签。 |
| **合格标准** | 分类稳定；原因可解释；不把偶发误判为普遍规律。 |

---

### E. 蜂巢：策略建议 — `hive_strategy_suggestion`

| 段落 | 内容摘要 |
|------|-----------|
| **任务目标** | 基于群体历史，为中台生成路由/提示词/升降级/图书馆经验包等**建议**。 |
| **不负责** | 直接改线上主链；直接改注册表；批准自己的建议生效。 |
| **输入** | 多 Luna 使用记录；图书馆经验；模型对比；质量趋势。 |
| **输出** | 策略建议草案；优先级建议；风险提示。 |
| **合格标准** | 建议可解释；不越过治理链；不把局部经验误推为全局规则。 |

---

## 五、哪些任务卡可以绑定同一模型

### 可以绑定（前提）

- 同属一个**角色**  
- 同属一条**工作链**  
- 互不构成**自审自批**  

**示例**：一个「长语音任务理解大模型」可同时绑定：

- `long_voice_task_parse`  
- `mixed_input_split`  
- `clarification_candidate_generation`  
- `unsupported_candidate_generation`  

均属**生产类理解链**。

### 不可以绑定（冲突示例）

同一模型**不能**同时绑定例如：

- `long_voice_task_parse`（生产）  
- `runtime_quality_review`（审核）  

生产与审核冲突，见职责矩阵红线。

---

## 六、任务卡与注册卡如何联动

| 注册卡回答 | 任务卡回答 |
|------------|------------|
| 这个模型是什么 | 该模型在**某任务**上具体做什么 |
| 能不能进主链、风险与降级 | 该任务的输入输出、合格标准 |

**关系**：**一张模型注册卡** → 绑定 **多张模型任务卡**（按任务拆分）。

---

## 七、下一步（评价标准）

当前已有：中台骨架、宪法、职责矩阵、注册卡、任务卡、蜂巢评分框架、**蜂巢评分记录与建议模板**（`LUNA_MODEL_PLATFORM_HIVE_SCORING_RECORDS_AND_TEMPLATES_V1.md`）。

- **已完成**：`LUNA_MODEL_PLATFORM_HIVE_SCORING_RECORDS_AND_TEMPLATES_V1.md`。  
- **已完成**：`LUNA_MODEL_PLATFORM_MIDPLATFORM_HIVE_CONSUMPTION_V1.md`。  
- **下一档**：见 `LUNA_MODEL_PLATFORM_LIBRARY_POSITION_AND_INTERFACE_V1.md`、`LUNA_MODEL_PLATFORM_GOVERNANCE_PANORAMA_V1.md`。

---

## 八、一句话收束

**注册卡管「模型身份与权力」，任务卡管「模型职责与交付」**，两者一起才构成 Luna 模型中台的**最小治理单位**。

# Luna 长语音模型接入策略 v1

> **结论**：长语音模型输出总 Schema v1.1（`voice_task_parse_v1_1`）**通过**。  
> 后续接模型时，模型按**已定协议填空**，而不是决定系统长什么样。

**实现入口（总线）**：`run_long_input_task_planning_v1` → `capabilities/voice/bridge/voice_long_input_parse_orchestrator.py`  
**纯规则链（降级/测试）**：`run_long_input_task_planning_v1_rule_chain`  
**模型侧协议**：`capabilities/voice/interfaces/voice_long_input_model_provider.py`  
**适配层（B 组 enrich、历史双通道）**：`capabilities/voice/bridge/voice_long_input_model_adapter.py`  
**校验**：`capabilities/voice/bridge/voice_long_input_model_output_validator.py`、`voice_long_input_model_validation.py`

**相关文档**：[字段责任对照表](./LUNA_VOICE_LONG_INPUT_MODEL_FIELD_OWNERSHIP_V1.md) · [变更清单](./LUNA_VOICE_LONG_INPUT_MODEL_INTEGRATION_CHANGESET_V1.md)

---

## 一、为什么现在只接模型适配层，不直接上模型执行

1. **执行边界与系统语言**必须由规则与 builder 固定；若让模型直接产出可执行计划，会污染协议并难以审计。  
2. **先铺轨道**：同一 `VoiceLongInputStructuredParseResult` → 同一校验 → 同一 `build_task_plan_v1_from_candidates`，换模型只换 Provider 实现。  
3. **默认规则链可跑**：无权重、无 GPU 时系统行为与改造前一致。

---

## 二、核心原则

1. **模型只负责「理解候选」，不负责「执行裁决」。**
2. **模型输出必须落到 `VoiceLongInputStructuredParseResult`**，不另起格式。
3. **并非所有字段都由模型生成**；部分字段由系统规则补全（稳定、可控、可审计、低延迟）。
4. **模型失败时，必须降级回规则链**；规则链不可删除。

---

## 三、字段责任划分（A / B / C）

详见 [LUNA_VOICE_LONG_INPUT_MODEL_FIELD_OWNERSHIP_V1.md](./LUNA_VOICE_LONG_INPUT_MODEL_FIELD_OWNERSHIP_V1.md)。

**概要**：A 组（理解）模型主填；B 组（`schema_version`、`input_meta`、`knowledge_collaboration`、`task_optimization`、`parser_notes` 等）系统补；C 组（`system_mapping_candidate`、确认/拒绝建议）模型可提、系统校验。

**管线内** `task_plan_v1` 仍由系统 **builder** 从规则或校验后的候选组装（本策略**不替换** builder）。

---

## 四、模型链 / 规则链双通道设计

| 通道 | 路径 |
|------|------|
| **规则链** | 长文本 → 规则 classifier → 规则 mapper → **builder** → `task_plan_v1` |
| **模型链** | 长文本 → `VoiceLongInputModelProvider.parse_long_input` → **校验** → enrich →（通过后）sanitize → **builder**（经 `structured_to_voice_long_input_parse_result`）→ `task_plan_v1` |

- 两条链最终都落在同一 **`VoiceLongInputParseResult`** 与 **`task_plan_v1` 结构**；外层调用方**无需**区分规则或模型。  
- **配置**：`capabilities/voice/config/voice_long_input_parse_config.yaml`（`parse_mode`、`enable_model_adapter`、`model_timeout_ms`、fallback 开关等）。  
- **默认**：`parse_mode: rule_only`，模型插口存在但**不**走模型链，除非显式改为 `model_preferred_with_rule_fallback` 且 `enable_model_adapter: true` 并传入 `model_provider`。

**路由逻辑**：`capabilities/voice/bridge/voice_long_input_parse_route_selector.py`。

---

## 五、为什么 builder 不替换

- Builder 是**系统结构层**，把「已校验的指令候选」组装为 `task_plan_v1`。  
- 模型链**禁止**绕过 builder 直接生成最终计划；否则执行边界与颗粒度约束无法统一。

---

## 六、接入位置（分步）

**第一步替换（规划中）**：

1. `voice_long_input_domain_classifier.py` — 规则版 → 模型辅助版（数据来自 Provider）  
2. `voice_long_input_instruction_mapper.py` — 规则版 → 模型辅助版  

**暂不替换**：`voice_long_input_task_plan_builder.py`、`knowledge_collaboration` 执行、`task_optimization` 执行、最终 feedback 播报渲染（模板层仍主控）。

**适配层**：`voice_long_input_model_adapter.py` — 历史双通道与 B 组 enrich；与 `VoiceLongInputModelProvider` 共同构成「模型 ↔ 系统」桥梁。

---

## 七、当前如何降级到规则链

| 情况 | 行为 |
|------|------|
| `rule_only` 或未启用 adapter / 无 Provider | `run_long_input_task_planning_v1_rule_chain` |
| Provider 返回 `None` | 规则链 |
| 模型超时 / 异常 | 可配置回规则链（见 YAML） |
| 输出校验失败（非法域、非法 mapping、任务数超限等） | **整体**回规则链，**不**阻塞长输入主入口 |

Orchestrator 在模型链成功时，可用规则管线生成的 `feedback_candidate` **覆盖**模型文案侧，避免话术越权（见 orchestrator 内与规则 structured 的合并逻辑）。

---

## 八、必须遵守的校验规则（摘要）

1. `primary_domain` / `secondary_domains` 必须来自 `PRIMARY_DOMAIN_V1`。  
2. `system_mapping_candidate` 必须来自前缀白名单（见 `voice_long_input_model_validation.py`）；**模型不得发明新命令字符串**。  
3. 任务数量受 v1 颗粒度约束（校验器与配置 `max_task_candidates`）。  
4. 模型不得通过本管线直接决定 V2 / Final；优化类内容仅可出现在占位字段。  
5. 模型建议「可执行」**不等于**系统执行；须经过确认/拒绝/澄清等治理。

---

## 九、接入节奏

1. **阶段 1（当前）**：Provider 协议 + orchestrator + 校验 + 默认规则 — **不接真实权重**。  
2. **阶段 2**：本地模型（如 Qwen 4B）实现 `VoiceLongInputModelProvider`。  
3. **阶段 3**：观测模型 vs 规则在各字段上的表现，再收紧或扩大模型职责。

---

## 十、一句话收束

**让模型负责理解，让系统负责结构、治理、协同与裁决。**  
换模型时不改协议，只换 Provider 实现。

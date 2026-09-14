# Luna Voice — Mainline Baseline / System Status Map（主线总基线）

**用途**：把已冻结的 V1 / V2 / V3 三段主线统一收束为一张总地图，作为后续冲突治理、溯源、白盒、视觉语义解释之前的**单一入口**。  
**本轮不做**：扩功能、接模型、改 reply、视觉解释、provenance/白盒实现、冲突治理实现。

更上位的长期定位参考（克制短文档）：`docs/architecture/LUNA_WORLD_ENTRY_PRINCIPLE_V0.md`
执行准入层（pre-submit admission）总览入口：`docs/architecture/voice/LUNA_VOICE_PRE_SUBMIT_ADMISSION_LAYER_V0.md`

---

## A. 当前主线总览

当前 Voice 主线在工程上已打通并分别形成冻结面：

| 阶段 | 内容 |
|------|------|
| **V1** | 基础语音最小闭环、真实性闸门（No Fabrication）、最薄会话状态锚 |
| **V2** | 语义转换器承载 / 规则版 / shadow consume / 控制类 assisted routing baseline（stop/cancel） |
| **V3** | 视角摘要输入承载（VisionSemanticInputPack v0 stub）+ V2 对 V3 的只读 `vision_shadow` |

**明确尚未进入**：

- 模型版语义（不接 LLM 作主链语义裁决）
- 视觉语义解释（不把摘要解释为对象/地点/状态并驱动行为）
- 冲突治理层正式实现
- Provenance / 白盒 Source & Processing Trace 正式实现

---

## B. V1 当前冻结面

| 项 | 说明 |
|----|------|
| **最小闭环** | `VoiceInputSessionManager` → `dispatch_voice_final_text` → 输出/拒绝路径；见 `LUNA_VOICE_V1_MINIMAL_FLOW.md` |
| **No Fabrication** | `guard_v1_speakable_text` 等闸门，禁止编造可说内容 |
| **VoiceV1SessionStateAnchor** | 会话事实锚，仅记录可观测事实，不脑补 |
| **文档** | `LUNA_VOICE_V1_PLAN.md`、`LUNA_VOICE_V1_MINIMAL_FLOW.md`、`LUNA_VOICE_V1_SESSION_STATE.md` |
| **验证** | `tools/verify_voice_v1_minimal_flow.py`（改主链语音路径须重跑） |

**代码锚点**：`capabilities/voice/runtime/voice_input_session_manager.py`、`capabilities/voice/runtime/voice_final_text_dispatcher.py`、`capabilities/voice/runtime/voice_v1_session_state_anchor.py`

---

## C. V2 当前冻结面

| 项 | 说明 |
|----|------|
| **接口** | `SemanticConverterV2`（`capabilities/voice/interfaces/semantic_converter_v2.py`） |
| **规则版** | `RuleBasedSemanticConverterV2`（`semantic_converter_v2.py`），承载于 `ev.metadata["luna_voice_semantic_v2"]`（开发开关控制） |
| **Shadow** | `result.metadata["semantic_v2_shadow"]`（只读对照，不改分流） |
| **Assisted routing v0** | 仅 **control.stop** / **control.cancel**：candidate + consumption metadata，**不夺权**主链 |
| **文档** | `LUNA_VOICE_V2_SEMANTIC_CONVERTER_INTERFACE.md`、`LUNA_VOICE_V2_ASSISTED_ROUTING_V0.md`、`LUNA_VOICE_V2_CONTROL_ASSISTED_ROUTING_V0_BASELINE.md` |

**代码锚点**：`capabilities/voice/runtime/semantic_converter_v2.py`、`capabilities/voice/runtime/voice_final_text_dispatcher.py`（shadow + assist）

**验证**：见 §G 表中 V2 相关脚本。

---

## D. V3 当前冻结面

| 项 | 说明 |
|----|------|
| **输入承载** | `build_vision_semantic_input_pack_v0` → `ev.metadata["luna_voice_vision_semantic_v3_input"]`；仅允许摘要键 `sidewalk_env_summary_v1` / `retail_env_summary_v1` / `risk_summary_v1` |
| **V2 只读影子** | 语义包内 `vision_shadow`（`seen_not_interpreted` / `not_seen`），不解释、不改 intent |
| **文档** | `LUNA_VOICE_V3_VISION_SEMANTIC_BRIDGE_INTERFACE.md`、`LUNA_VOICE_V3_VISION_SHADOW_READ_BASELINE.md` |

**代码锚点**：`capabilities/voice/runtime/vision_semantic_bridge_v3.py`、`capabilities/voice/runtime/voice_input_session_manager.py`、`capabilities/voice/runtime/semantic_converter_v2.py`

---

## E. 当前统一硬约束

- **No Fabrication Rule**：不得把不确定包装成确定；视觉摘要存在 ≠ 已确认事实。  
- **统一时空锚点**：系统级时间/空间事实只能来自中台统一基准；语义层与 V3 桥接不得自造 timestamp/坐标。  
- **语义层不得夺权**：不得单独改写 `dispatch`、不得绕过 guard、不得替代用户明确输入。  
- **视觉摘要不得直接升格为用户可说事实**。  
- **主链已有事实高于辅助候选**：assisted routing / V3 shadow 均为观测与确认信号，不反向裁决主链。

---

## F. 当前明确不做的事

- 不接模型版语义作为主链裁决  
- 不接视觉解释并驱动对话/行为  
- 不横向扩 `control.resume` / `control.repeat`（须专项设计，尤其 resume 与 task lifecycle 歧义）  
- 不做冲突治理实现  
- 不做 provenance 统一 schema  
- 不做白盒展示实现  
- 不让辅助层接管行为裁决（stop/cancel 辅助已冻结为「主链先成立 + 语义确认」模式）

---

## G. 当前验证入口总表（最小验收入口）

改到对应链路时**必须重跑**所列脚本；建议全量回归时至少跑 `verify_voice_v1_minimal_flow.py`。

| 脚本 | 覆盖范围 |
|------|----------|
| `tools/verify_voice_v1_minimal_flow.py` | V1 主链最小闭环 |
| `tools/verify_semantic_converter_v2_rule_based.py` | V2 规则版 intent |
| `tools/verify_semantic_converter_v2_shadow_consume.py` | V2 semantic shadow |
| `tools/verify_semantic_converter_v2_assist_stop_candidate.py` | stop assist candidate |
| `tools/verify_semantic_converter_v2_assist_stop_consumption.py` | stop assist consumption |
| `tools/verify_semantic_converter_v2_assist_cancel_consumption.py` | cancel assist consumption |
| `tools/verify_vision_semantic_input_pack_v0.py` | V3 pack 承载 |
| `tools/verify_semantic_converter_v2_vision_shadow_read.py` | V2 `vision_shadow` 只读 |

---

## H. 下一阶段前置条件

- **冲突治理层**：须单独设计决策优先级、与中台审核关系、「冲突治理宪法」，不得在主链上硬塞补丁。  
- **Provenance / 白盒**：须单独设计 Source & Processing Trace 体系；待主链更完整后再落实现。  
- **视觉语义解释**：须单独设计 V3 解释层与准入，不得从当前 baseline 直接跳转到「摘要→事实→行为」。  
- **第三个控制类 intent**：须专项设计，不得机械复制 stop/cancel 模板。

---

## I. 模块打标标准（占位）

- **定位**：为语音链建立统一打标/分类/分级标准，支撑可回归与跨模块对齐（输入类型、候选层、输出层）。
- **需要覆盖范围**：语音输入类型、输出类型、候选类型、以及中断/确认/拒绝/response-only 等标签体系。
- **当前未展开**：本期只补“坑位”，不提供具体分级表与策略。
- **后续补充入口**：需单开专题文档与实现计划。

---

## J. 信息处理超时方案（占位）

- **定位**：为语音链定义超时与过期处理口径，避免主链被慢处理拖死。
- **需要覆盖范围**：ASR 超时、response submit 超时、追问/确认上下文过期、延迟结果失效处理等。
- **当前未展开**：本期只补“坑位”，不写成假方案。
- **后续补充入口**：需单开专题并与中台/输出平面对齐。

---

## K. 模块报错处理方案（占位）

- **定位**：定义语音链各层报错与降级处理机制（可观测、可回退、不中断主链）。
- **需要覆盖范围**：ASR 异常、TTS/submit 异常、dispatcher 异常、候选层异常、response template 异常等。
- **当前未展开**：本期只补“坑位”，不展开具体降级路径与错误分级。
- **后续补充入口**：需单开专题，明确错误分级、降级策略与观测面。

---

## 索引：分阶段冻结文档

| 阶段 | 主线总基线相关文档 |
|------|-------------------|
| V1 | `LUNA_VOICE_V1_PLAN.md`、`LUNA_VOICE_V1_MINIMAL_FLOW.md`、`LUNA_VOICE_V1_SESSION_STATE.md` |
| V2 | `LUNA_VOICE_V2_SEMANTIC_CONVERTER_INTERFACE.md`、`LUNA_VOICE_V2_ASSISTED_ROUTING_V0.md`、`LUNA_VOICE_V2_CONTROL_ASSISTED_ROUTING_V0_BASELINE.md` |
| V3 | `LUNA_VOICE_V3_VISION_SEMANTIC_BRIDGE_INTERFACE.md`、`LUNA_VOICE_V3_VISION_SHADOW_READ_BASELINE.md` |

上位治理约束（宪法）：`LUNA_CONFLICT_GOVERNANCE_CONSTITUTION_V0.md`

工程侧索引：`capabilities/voice/docs/README.md`

当前阶段主线执行清单（Next Step Plan v0）：`docs/architecture/voice/LUNA_VOICE_MAINLINE_NEXT_STEP_EXECUTION_PLAN_V0.md`

响应型 submit 统一接口（Response Submit Template Interface v0 Baseline）：`docs/architecture/voice/LUNA_RESPONSE_SUBMIT_TEMPLATE_V0_BASELINE.md`

V2 受控消费接口面（Assisted Consumption Interface v0）：`docs/architecture/voice/LUNA_VOICE_V2_ASSISTED_CONSUMPTION_INTERFACE_V0.md`

导航目的地参数充足性专题（Destination Sufficiency v0，设计冻结）：`docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_SUFFICIENCY_V0.md`

导航目的地绑定专题（Destination Binding v0，设计冻结；在 sufficiency 之后、真实启动之前）：`docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BINDING_V0.md`

导航目的地绑定事实专题（Destination Bound Fact v0，设计冻结；在 destination binding 之后、真实启动之前）：`docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BOUND_FACT_V0.md`

导航目的地确认完成事实专题（Destination Confirmation Fact v0，设计冻结；在 candidate/bound_check 之后、bound 升级之前）：`docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_CONFIRMATION_FACT_V0.md`

导航目的地 bound 升级专题（Destination Bound Upgrade v0，设计冻结；在 confirmation fact 之后、真实导航启动之前）：`docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BOUND_UPGRADE_V0.md`

导航目的地 bound 材料化专题（Destination Bound Materialization v0，设计冻结；在 upgrade_eval 之后、真实导航启动之前）：`docs/architecture/voice/LUNA_NAVIGATION_DESTINATION_BOUND_MATERIALIZATION_V0.md`

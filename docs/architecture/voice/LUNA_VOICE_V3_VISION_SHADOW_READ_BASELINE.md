# Luna Voice V3 — Vision Shadow Read Baseline / Freeze（阶段冻结面）

**定位**：把当前已落地并验证通过的「V3 输入承载 + V2 只读影子消费」冻结为阶段基线，防止后续从「看见视觉摘要」直接跳到「让视觉影响语义/行为」。  
**本轮不做**：视觉语义解释、provenance/白盒统一体系、冲突治理实现、raw 视觉直通。

---

## A. 当前基线范围

**当前仅批准两步能力**：

1. **V3 输入承载占位**  
   - 承载键：`VoiceInputEvent.metadata["luna_voice_vision_semantic_v3_input"]`  
   - 实现：`capabilities/voice/runtime/vision_semantic_bridge_v3.py`（`build_vision_semantic_input_pack_v0`）  
   - 接入：`VoiceInputSessionManager.process_final_text_with_dispatch` 内，`begin_from_event` 之后、语义转换之前

2. **V2 对 V3 的只读影子消费**  
   - 字段：`RuleBasedSemanticConverterV2` 输出 payload 内的 `vision_shadow`  
   - 实现：`capabilities/voice/runtime/semantic_converter_v2.py`

**明确尚未进入**：

- 视觉语义解释（不把摘要解释为对象/地点/状态事实）
- 视觉对 `intent` / `reply` / `dispatch` / assisted routing 的任何影响

---

## B. 当前系统定位

- V3 当前阶段只是：**看见「视觉相关摘要输入」已到达语义链路的承载位**  
- **不是**视觉理解层、检测器层  
- **不是**视觉事实生成层  
- **不是**行为驱动层、执行裁决层  
- **不是** reply 控制层

---

## C. 当前允许的输入资产

**只允许**从 `runtime_context.metadata` 读取以下**摘要级**键（且值为 `dict` 时才参与组包）：

- `sidewalk_env_summary_v1`
- `retail_env_summary_v1`
- `risk_summary_v1`

**当前不允许**直入语义主链或作为 V3 稳定输入源：

- raw detector boxes、raw OCR、逐帧检测原始结果  
- `unified_env_summary_shadow_v1`  
- `unified_env_fill_shadow_v1`  
- 仅在 `dispatch_voice_final_text` 阶段内才计算/写入的 shadow/fill 结果（时序与 V3 接入点不一致，不得假装为前置稳定输入）

---

## D. 当前最小结构

### 1) `luna_voice_vision_semantic_v3_input`（V3 stub pack）

| 字段 | 说明 |
|------|------|
| `version` | 固定 `v3_stub` |
| `source_summaries` | 实际读到的允许摘要键名列表（仅说明来源键，不代表事实已确认） |
| `scene_type` | 当前固定 `null`（不推断场景） |
| `task_relevant_facts` | 当前固定 `[]` |
| `risk_facts` | 当前固定 `[]` |
| `environment_facts` | 当前固定 `[]` |
| `uncertainties` | 可含保守提示，如 `vision_summary_present_but_not_yet_interpreted` |
| `confidence` | 当前固定 `0.0` |
| `anchor_ref` | 仅 `null` 或未来中台注入引用；模块不自造 |

### 2) V2 输出中的 `vision_shadow`

| 字段 | 说明 |
|------|------|
| `vision_input_seen` | 是否读到非空 V3 pack（`dict`） |
| `vision_sources` | 来自 V3 pack 的 `source_summaries` 的只读拷贝 |
| `vision_shadow_status` | 仅允许：`seen_not_interpreted` \| `not_seen` |

含义：**看见摘要输入但未解释**；不升格为语义事实。

---

## E. 当前明确禁止项

- 不允许视觉摘要**改变** `intent`  
- 不允许视觉摘要**改变** `confidence`（意图置信仍仅由文本规则决定）  
- 不允许视觉摘要**改变** `requires_followup`  
- 不允许视觉摘要**改变** `references`  
- 不允许视觉摘要**改变** `safety_flags`（本轮不因 V3 写入）  
- 不允许视觉摘要直接驱动 `reply`  
- 不允许视觉摘要直接驱动 `dispatch` / assisted routing  
- 不允许把视觉摘要**升格**为用户可说事实

---

## F. 两条硬约束

### No Fabrication Rule

- 视觉摘要存在 ≠ 已确认事实  
- 不允许把「有摘要」包装成「已经看到某对象/地点/状态」  
- `vision_shadow` 仅表示「输入被看见」，不表示「世界如此」

### 统一时空锚点原则

- 不允许模块自造系统级时间戳或空间坐标  
- `anchor_ref` 只能为空或引用中台统一锚点；V3/V2 当前输出不得新增 `timestamp` / `location` / `position` / `coordinate` / `lat` / `lng` 等自造字段

---

## G. 当前验证入口

改下列相关链路时**必须重跑**：

| 脚本 | 作用 |
|------|------|
| `tools/verify_vision_semantic_input_pack_v0.py` | V3 pack 承载与允许键 |
| `tools/verify_semantic_converter_v2_vision_shadow_read.py` | V2 `vision_shadow` 只读影子 |
| `tools/verify_voice_v1_minimal_flow.py` | V1 主链最小闭环不被破坏 |

---

## H. 下一阶段前置条件

- 进入「视觉语义解释」或让视觉影响 `references` / `ambiguities` / `requires_followup` 前，**必须先以本文档为冻结面**，并单独设计与评审  
- **统一 provenance / lineage、白盒 Source & Processing Trace、冲突治理可视化** 不在本阶段落地；待主链更完整后再补，避免打散主线

---

## 相关代码与文档路径（事实索引）

- `capabilities/voice/runtime/vision_semantic_bridge_v3.py`  
- `capabilities/voice/runtime/voice_input_session_manager.py`  
- `capabilities/voice/runtime/semantic_converter_v2.py`  
- `docs/architecture/voice/LUNA_VOICE_V3_VISION_SEMANTIC_BRIDGE_INTERFACE.md`（接口设计，与本 baseline 配套）

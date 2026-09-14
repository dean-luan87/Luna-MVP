# Luna Voice V2 — 语义转换器接口契约（Semantic Converter / Normalizer）

**文件**：`docs/architecture/voice/LUNA_VOICE_V2_SEMANTIC_CONVERTER_INTERFACE.md`  
**性质**：接口与边界契约（**不接模型**、不接视觉实现）  
**上位基础**：V1 最小闭环（`VoiceInputSessionManager` → `dispatch_voice_final_text` → `guard_v1_speakable_text` → `VoiceV1SessionStateAnchor`）

**方向判断（顺序钉死）**：V2 的第一目标**不是**「更像人」，而是把输入变得**更可裁决、更可控、更不容易胡说**；否则一接模型只会变成「更会胡说的 V1」。

---

## A. 定位

| 项 | 说明 |
|----|------|
| **是什么** | **语义归一化层 / 语义转换层**：把用户**原始表述**转成主链可消费的**结构化语义**（可裁决、可观测、可降级）。 |
| **不是什么** | 最终决策器；事实生成器；视觉接入层；知识问答大脑；任务编排中心。 |
| **与 V1 关系** | **不得**绕过 V1 的 **No Fabrication Rule**（`guard_v1_speakable_text` 及同等硬约束）；语义层**多产出不确定/需追问**，**少产出**伪确定意图。 |

---

## B. 输入（最小契约）

语义转换器**单次调用**建议最小输入（逻辑视图，实现可为 `dataclass` / `TypedDict`）：

| 字段 | 说明 |
|------|------|
| `raw_text` | 原始文本（与 ASR/模拟源一致） |
| `normalized_text` | 若上游已有（如 `VoiceInputEvent.normalized_text` / strip 后），一并传入 |
| `session_state_anchor` | **只读**快照：`VoiceV1SessionStateAnchor` 或等价只读视图（不得要求写回锚点来完成语义） |
| `current_mode` | 如 `normal` / `task`（与锚或 `VoiceInputEvent.is_task_mode` 对齐） |
| `voice_input_event_ref` | 可选：只读引用 `event_id` / `request_id` / `session_id`，用于追溯，**不作为推理事实源** |

### 时间 / 空间锚点（仅消费，禁止自造）

| 字段 | 说明 |
|------|------|
| `platform_time_anchor` | **可选**；若中台统一注入，则**仅读取**（例如 UTC epoch、业务日界、会话对齐时钟）。**语义转换器不得自行生成「系统级时间事实」**。 |
| `platform_space_anchor` | **可选**；若中台统一注入，则**仅读取**（例如统一坐标系、定位精度声明）。**不得自行编造空间坐标或「当前位置」**。 |

若当前未注入：字段缺省为「无」，语义层应输出 **不确定 / 需追问**，**不得**用模型幻觉补锚。

---

## C. 输出（最小结构）

输出必须是 **JSON 可序列化** 的稳定结构（建议落在 `VoiceInputEvent.metadata["luna_voice_semantic_v2"]` 或专用命名空间，见 §F）。

| 字段 | 类型意图 | 说明 |
|------|----------|------|
| `raw_text` | string | 回显或对齐用的原文片段 |
| `normalized_text` | string | 归一化后文本（可与输入对齐） |
| `intent` | string | **粗粒度**意图标签（枚举字符串，由后续版本表锁定；禁止承载「事实陈述」） |
| `entities` | object / list | 从用户话中**显式抽取**的实体；缺则空，**禁止脑补** |
| `references` | list | 用户**显式指向**的引用（如「上一个」「那个」）；若无依据则空 |
| `ambiguities` | list | 歧义点描述（短句）；**鼓励**填写 |
| `requires_followup` | bool | 是否需要追问；与 `ambiguities` 一致 |
| `candidate_task_type` | string | 可选任务类型候选；不确定则 `unknown` / `none` |
| `confidence` | float | 0..1；**低置信禁止冒充高置信** |
| `safety_flags` | list | 如 `possible_pii`、`possible_instruction_injection` 等轻量标记（可扩展，但保持小集合） |

**微调原则**：字段可增删 1～2 个，但**不得**膨胀为「大而全世界模型输出」。

---

## D. 硬边界（必须遵守）

- **不允许**强行补全用户**未明确表达**的事实。  
- **不允许**把「不知道 / 不确定」伪装成**确定意图**或高 `confidence`。  
- **不允许**为流畅对话**编造**引用对象或实体。  
- **不允许**在语义层**决定**系统级时间/空间事实；**只能**消费中台统一下发的锚点字段（§B）。  
- **不确定**时：输出 `ambiguities`、`requires_followup=true`，并压低 `confidence`。

---

## E. 与 V1 会话状态层的关系

- `VoiceV1SessionStateAnchor` 只提供**会话事实锚**（上一轮用户/系统文本、是否在等用户等）。  
- 语义转换器**可读**该锚点，用于**指代消解的候选提示**（如「上一个」可能指 `last_user_text`），**不得**把锚点当成授权「替用户补全未说出的意图或事实」。  
- **「同一会话延续」≠「可以替用户补完整意图」**；延续只提高**追问策略优先级**，不提高**编造权限**。

---

## F. 接入位置（单一推荐，当前最小可落）

**推荐唯一落点**：`VoiceInputSessionManager.process_final_text_with_dispatch` 内，顺序固定为：

1. `ev = self.process_final_text(...)` — 已有标准 `VoiceInputEvent`  
2. `self.v1_session_anchor.begin_from_event(ev)` — 已有 V1 锚更新  
3. **【V2 预留】**调用 `SemanticConverterV2.convert(...)`（未来实现），输入为 `ev` + 锚点**只读快照** + 可选中台锚（来自 `runtime_context.metadata` 若存在）  
4. 将输出写入 **`ev.metadata["luna_voice_semantic_v2"]`**（或契约约定键），**不**修改 `VoiceInputEvent` 顶层字段（避免 schema 爆炸）  
5. `dispatch_voice_final_text(ev, ..., session_state_anchor=...)` — 下游**可选择性**读取 metadata  

**理由（代码事实）**：  
- 入口唯一、顺序清晰；**在 dispatch 之前**完成结构化，使 `classify_voice_input_length_mode` / bridge / 长链**都能**看到同一语义包。  
- **不**先改 `dispatch_voice_final_text` 内部结构，降低首轮侵入。  

**本轮**：仅文档与 TODO；**不**实现 `convert` 体。

---

## G. V2 本轮不做什么

- 不接视觉语义实现  
- 不接世界模型  
- 不做复杂任务链编排  
- 不做高阶多轮推理  
- 不做大而全知识问答  
- 不做情绪系统深接入  
- **不接具体 LLM**（接口契约先行）

---

## 仓库映射（简明）

| 区域 | 与 V2 的关系 |
|------|----------------|
| `bridge/voice_input_router.py` | 唤醒/窗/白名单路由；**可复用**为 V2 之前的事实边界，**不是**语义大脑 |
| `bridge/voice_input_to_bridge.py` + `bridge_decision` | 短链 Bridge 决策；V2 输出应**早于或并行**供 bridge 消费（首轮仅 metadata） |
| `bridge/voice_long_input_task_planner.py` 等 | **长链重型解析**；V2 **不**替代之，长期可**收敛**为「先 V2 归一化再进长链」——**暂不接线**以免双脑冲突 |
| `schemas/voice_intent_candidate.py` | 轻意图候选占位；**可对齐** `intent` / `confidence` 语义，**不**强制合并 |
| `schemas/voice_input_event.py` | **承载** `metadata["luna_voice_semantic_v2"]` 的首选位置 |
| `interfaces/voice_dialogue_bridge.py` | Stage-1 Protocol；未来可增 `SemanticConverterV2` Protocol |
| `providers/` | 模型 provider；**V2 实现阶段**再接入，**契约轮不接** |
| `runtime/voice_final_text_dispatcher.py` | 主分流；**首轮不改**；后续可选读取 metadata |

**可直接复用**：`VoiceInputEvent`、`VoiceV1SessionStateAnchor`、metadata 承载模式。  
**需裁剪后接入**：长链 parse 管线（勿平行叠两套「全量语义」）。  
**暂不接入**：视觉、世界模型、复杂任务链。

---

## 约束 1：No Fabrication Rule 继续生效

- 语义转换器**不能**因为「要结构化」就脑补缺失槽位。  
- **不确定** → 输出 `ambiguities` / `requires_followup`；**禁止**把缺失信息偷偷塞进 `entities` / `intent`。

## 约束 2：统一时空锚点原则

- 时间/空间锚点以**中台统一基准**为准；语义层**只读**。  
- **不得**自行生成系统级时间戳或空间坐标作为「事实」。  
- 若业务需要时空字段，只能出现在**中台注入**字段中，并由上层明确语义。

---

## 下一轮最小实现建议（1 点）

在 `capabilities/voice/interfaces/` 增加 **`SemanticConverterV2` Protocol**（或等价抽象）+ **空实现/stub** 一版，仅在 `process_final_text_with_dispatch` 中 **TODO 开关**下写入空的 `luna_voice_semantic_v2` 占位——**不接模型**，仅验证承载路径与观测。

# Luna 长语音模型输出总 Schema v1.1

**版本常量**：`voice_task_parse_v1_1`（`schema_version` 字段）

**工程类型名**：`VoiceLongInputStructuredParseResult`（`capabilities/voice/schemas/voice_long_input_structured_parse_v1_1.py`）

**规则组装入口**：`build_voice_long_input_structured_parse_v1_1`（`capabilities/voice/bridge/voice_long_input_structured_parse_builder.py`）

**模型接入策略**：见 [LUNA_VOICE_LONG_INPUT_MODEL_INTEGRATION_STRATEGY_V1.md](./LUNA_VOICE_LONG_INPUT_MODEL_INTEGRATION_STRATEGY_V1.md)（`voice_long_input_model_adapter.py`、双通道与字段责任划分）。

---

## 核心原则

1. **任务部分与非任务部分必须分开保留**（`task_candidates` vs `non_task_payload`）。
2. **模型/解析输出的是候选理解结构，不是执行结果**。
3. **`task_plan_v1`（管线内）只反映原始理解**；本 Schema 中的 `knowledge_collaboration` / `task_optimization` **仅占位**，不直接改写 V1。
4. **`feedback_candidate` 只表达「怎么回用户」**，不裁决执行。
5. **情感引擎可增强理解与建议，不得擅自篡改用户明确任务**（见反馈与情感边界文档）。

---

## 顶层块（固定 12 个键，含 `schema_version`）

| 键 | 含义 |
|----|------|
| `schema_version` | 固定 `voice_task_parse_v1_1` |
| `input_meta` | 原始输入元数据 |
| `input_mode_judgement` | 任务/混合/非任务模式 + 置信度 |
| `global_judgement` | 全局域与意图判断 |
| `task_candidates` | 任务候选列表 |
| `non_task_payload` | 非任务片段（情感引擎预留） |
| `knowledge_collaboration` | 记忆/历史协同（当前占位） |
| `task_optimization` | 优化候选（V2 位，当前不执行） |
| `clarification_candidates` | 结构化追问 |
| `unsupported_candidates` | 不支持片段 |
| `feedback_candidate` | 反馈模式与文案候选 |
| `parser_notes` | 调试与观察（不参与执行） |

**不再增加顶层键**；扩展走子对象字段或 `metadata`。

---

## 与管线对象的关系

| 对象 | 角色 |
|------|------|
| `VoiceLongInputParseResult` | 管线内紧凑结果（含 `task_plan_v1`、`voice_feedback`） |
| `VoiceLongInputStructuredParseResult` | **对外/模型/图书馆** 总视图，可序列化 |

规则引擎路径：`run_long_input_task_planning_v1` → `build_voice_long_input_structured_parse_v1_1(parse)`。

---

## 三种常见输出形态（摘要）

1. **纯任务**：`input_mode_judgement.mode = task_only`，`task_candidates` 非空，`non_task_payload.exists = false`，`feedback_candidate.feedback_mode` 常为 `task_understood_and_ready`。
2. **混合**：`mixed_task_and_non_task`，任务与非任务均保留，`feedback_mode` 常为 `mixed_input_acknowledged`。
3. **非任务**：`non_task_only`，`task_candidates = []`，`should_generate_task_plan = false`，`non_task_payload.exists = true`，`feedback_mode` 使用 `non_task_preserved_for_future`（非 reject）。

---

## 当前阶段禁止塞进 Schema 的内容

- 细粒度情绪标签、用户画像推断、主观打分、大段 reasoning 文本、最终执行结果、情感引擎生成的回复正文。

详见各子块字段定义（与代码 dataclass 一致）。

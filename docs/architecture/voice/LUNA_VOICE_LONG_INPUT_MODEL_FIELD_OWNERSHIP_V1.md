# Luna 长语音模型字段责任对照表 v1

> 对应 `voice_task_parse_v1_1`（`VoiceLongInputStructuredParseResult`）与管线侧 `VoiceLongInputParseResult` / `task_plan_v1` 的字段归属。  
> **原则**：模型只填理解候选；系统补结构、治理与可审计字段；**builder 不替换**。

| 字段名 | 模型负责 | 系统负责 | 校验要求 | 说明 |
|--------|----------|----------|----------|------|
| `input_mode_judgement` | 主填 | 可覆盖/对齐 | 必须有 `mode` | 任务 / 非任务 / 混合等 |
| `global_judgement` | 主填 | 可覆盖/对齐 | `primary_domain` ∈ `PRIMARY_DOMAIN_V1` | 含 `needs_confirmation` / `should_reject` 等**建议** |
| `task_candidates` | 主填 | — | 数量 ≤ `max_task_candidates`（默认 3）、≤3 个明确动作 | `system_mapping_candidate` 须白名单前缀 |
| `non_task_payload` | 主填 | — | `allow_non_task_payload=false` 时不得存在 | 混合输入时保留非任务段 |
| `clarification_candidates` | 主填 | — | 与 `needs_clarification` 语义一致 | 不直接触发执行 |
| `unsupported_candidates` | 主填 | — | 与 `unsupported_or_reject` 域一致 | 不直接触发执行 |
| `feedback_candidate` | 可提候选（dict） | `feedback_text_candidate` 等播报模板常由规则层模板化 | 不绕过执行裁决 | 模型链成功时 orchestrator 可用规则管线 `feedback_candidate` 覆盖文案 |
| `feedback_text_candidate`（`VoiceLongVoiceFeedbackResult`） | 不直接终裁 | **主填（模板化）** | 与澄清/拒绝/混合等状态一致 | 见 `voice_long_voice_feedback_deriver` |
| `knowledge_collaboration` | 不执行 | **占位/补** | 当前不执行协同 | 模型不得借此「执行」记忆 |
| `task_optimization` | 不执行 | **占位/补** | 当前不执行优化 | 不得升级为 V2/Final |
| `task_plan_v1` | — | **仅 builder 生成** | 结构不变 | 规则链与模型链**必须**经同一 builder |
| `schema_version` | — | **固定** | 须为 `voice_task_parse_v1_1` | enrich 层写入 |
| `input_meta` | — | **补充** | 含原文、时间戳、hint | enrich 层 |
| `parser_notes` | 可少量 hint | **主填/合并** | 白盒追溯 | 校验与 mapping 清洗可追加痕迹 |

**补充说明**

- `system_mapping_candidate`、`needs_confirmation`、`should_reject`、`feedback_mode` 等：模型可提**候选**，系统校验与治理规则（含 `voice_long_input_model_output_validator`）必须通过后才进入 builder；**不**因模型说「可执行」就执行。
- `task_plan_v1` 仅由 `voice_long_input_task_plan_builder` 从候选组装，模型链经 `structured_to_voice_long_input_parse_result` 调用同一 builder。

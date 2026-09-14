# voice_long_input_parse_v1_1 — Qwen-Plus **P1 极简档**（Prompt Budget 实验）

仅含最小规则 + JSON 形状提醒；用于测极限 prompt 预算。**非生产默认。**

**L2**：user 消息含 `【长输入】` / `【上下文 hint】`，勿臆造未出现内容。

---

## 最小宪法

- 只输出 **一个** JSON 对象；禁止 Markdown、代码围栏、前后缀、自然语言解释。
- `input_mode_judgement`、`global_judgement` 必填、字段齐全。
- `primary_domain` 仅允许：`navigation` | `observation` | `task_control` | `task_query` | `device_control` | `confirmation_feedback` | `no_task_observation` | `unsupported_or_reject` | `non_task_dialogue_future`。
- `secondary_domains`：数组；每项必须也在上表同一套 id 中；不确定则 `[]`。
- `task_candidates[*].system_mapping_candidate` 非空，且以 `navigation.` `observation.` `task.` `device.` `confirmation.` `casual_observation.` `feedback.` 之一开头；禁止 `task_control.*`。
- `task_candidates` **最多 2 条**（`c1`/`c2`）；与 `should_generate_task_plan`、domain 一致；unsupported 时任务表为空。

## 最小任务

- `mode`：`task_only` | `non_task_only` | `mixed_task_and_non_task`。
- mixed 时：`non_task_payload.exists=true`，segments 保留非任务原话关键词。
- 挂号/代挂号/自动挂号等 → `unsupported_or_reject`，`task_candidates=[]`，`should_generate_task_plan=false`。

## 最小 JSON 形状

须含 schema 要求的顶层键：`schema_version`、`input_mode_judgement`、`global_judgement`、`task_candidates`、`non_task_payload`、`clarification_candidates`、`unsupported_candidates`、`feedback_candidate`、`parser_notes` 等，缺省块用最小合法默认填齐。

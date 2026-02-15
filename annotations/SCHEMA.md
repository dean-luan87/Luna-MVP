# Annotation Answers Schema (Phase 3.3)

标注答案资产格式（冻结版）。每一条答案为一行 JSON（`answers.jsonl`）。

## 单行格式

```json
{
  "version_tag": "v1.1",
  "session_id": "xxxx",
  "episode_id": "SAFETY_CHANGE_42",
  "task_id": "Q_SAFETY_CAUSE",
  "answer": "wet_floor",
  "confidence": 0.8,
  "annotator": "human",
  "annotated_at": "2026-02-09T10:23:11Z"
}
```

## 字段规则

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| version_tag | string | 是 | 与 `annotation_tasks.jsonl` 一致 |
| session_id | string | 是 | 会话标识 |
| episode_id | string | 是 | 片段标识，须存在于 `episodes_index.jsonl` |
| task_id | string | 是 | 任务标识，须存在于 `annotation_tasks.jsonl` |
| answer | string / number / enum | 是 | 人类答案，不校验语义 |
| confidence | number | 否 | 0–1，默认 1.0 |
| annotator | string | 是 | 固定 `"human"` |
| annotated_at | string | 是 | ISO8601 UTC，如 `2026-02-09T10:23:11Z` |

- **answer**：不校验语义，仅原样存档。
- **禁止新增派生字段**。

## 存放位置

- `annotations/{version_tag}/answers.jsonl`：逐行追加，可中断可恢复。
- `annotations/{version_tag}/meta.json`：可选元信息。


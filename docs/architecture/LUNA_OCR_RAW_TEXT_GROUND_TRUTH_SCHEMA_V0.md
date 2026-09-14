## Phase-ModelOCR-001

OCR Raw Text Ground Truth Schema v0

### 1. 目标

定义人工标注（ground truth）格式，用于**原文级** OCR 评测与多模型对比对齐。

硬边界：

- GT 只包含“原文事实”（text + 位置 + 顺序）
- 不包含语义标签、导航意图、场景结论、任务决策

### 2. 文件组织建议

- 一个标注集：一个目录
- 每个视频/样本：一个 `sample_id`
- 每帧：一条记录（或一文件）

支持两种等价存储方式（二选一即可）：

- **JSONL**（推荐）：一行一个 frame 标注记录
- **JSON**：一个文件包含多个 frame 标注记录

### 3. Frame-level 结构（v0）

```json
{
  "schema_version": "v0",
  "sample_id": "sample_001",
  "frame_id": "frame_000123",
  "image_path": "frames/sample_001/frame_000123.jpg",
  "image_size": {"width": 1920, "height": 1080},
  "annotations": [
    {
      "line_order": 1,
      "text": "出口",
      "bbox": {"x1": 100, "y1": 200, "x2": 160, "y2": 230},
      "confidence": 1.0
    }
  ],
  "raw_text_joined": "出口"
}
```

字段说明：

- `schema_version`: 固定 `"v0"`
- `sample_id`: 样本 ID
- `frame_id`: 帧 ID（与 OCR 输出合同一致）
- `image_path`: 可选，但强烈建议（可回放/复核）
- `image_size`: 可选但建议（bbox 合法性校验）
- `annotations`: 行级原文标注列表
  - `line_order`: 从 1 开始
  - `text`: 原文
  - `bbox`: 与输出合同一致的 bbox 格式
  - `confidence`: GT 里通常为 1.0（可省略；若保留用于“标注不确定性”）
- `raw_text_joined`: 按 `line_order` 用 `\n` 拼接（便于整帧对比）

### 4. 标注准则（最小集合）

- 只标“可读文本”（不可辨认可标为 `""` 并在评测侧计入漏检/不可读）
- bbox 尽量贴合文本区域
- line_order 遵循阅读顺序（上→下，左→右）

### 5. 与多模型对齐的建议

评测侧对齐优先级建议：

1. bbox IoU 匹配（阈值可配置，如 0.5）
2. 如果 bbox 不稳定，允许用文本相似度辅助匹配（但仍属于“原文层”，非语义）


## Phase-ModelOCR-001

OCR Raw Text Output Contract v0

### 1. 合同目标

定义 OCR 在本阶段唯一允许输出的结构：**raw text candidates**。

### 2. 术语

- **frame**：一次输入图像帧（或离线视频的一帧），用 `frame_id` 标识
- **candidate**：OCR 对该帧识别到的一条原文候选（行级为主）
- **raw_text_joined**：将该帧候选按阅读顺序拼接的原文（用于对比与回归，不等于语义总结）

### 3. 数据结构（v0）

每个 raw text candidate（行级）必须包含：

- **text**: `string`  
  原文文本（不做语义改写，不做总结）
- **bbox**: `object`  
  推荐字段：`x1,y1,x2,y2`（像素坐标，左上/右下），或 `x,y,w,h`；必须在合同中固定一种表示
- **confidence**: `number`  
  \([0,1]\) 或模型自带尺度（若非 \([0,1]\) 必须在 `model_config_id` 对应配置中说明并在评测侧归一）
- **frame_id**: `string`
- **model_config_id**: `string`  
  指向“本次 OCR 运行所用模型/预处理/后处理配置”的标识（用于可追溯对比）
- **line_order**: `integer`  
  该帧内的阅读顺序（从 1 开始）；用于逐行对齐
- **raw_text_joined**: `string`  
  在 frame-level 聚合输出中出现；当以 candidate 结构承载时，允许每条重复该字段（便于下游只取一条即可得到聚合原文）

推荐可选字段（不影响本阶段 GO/NO-GO，但建议保留扩展位）：

- `language_hint`: `string`（如 `zh` / `en` / `mixed`）
- `script`: `string`（如 `Hans`）
- `source`: `string`（如 `ocr_provider_name`）
- `preprocess_id`: `string`

### 4. bbox 规范（固定）

本阶段统一 bbox 表示为：

```json
{"x1": 0, "y1": 0, "x2": 100, "y2": 20}
```

约束：

- 坐标必须为像素坐标（相对输入帧）
- `x1 < x2` 且 `y1 < y2`
- 允许越界时必须在评测侧裁剪，但推荐生产侧输出已裁剪 bbox

### 5. line_order 规范（固定）

推荐阅读顺序：先按 `y`（从上到下）分行，再按 `x`（从左到右）排序。行切分存在差异时，评测侧允许使用 bbox 匹配（IoU + 最近邻）对齐。

### 6. raw_text_joined 生成规则（固定）

按 `line_order` 升序拼接：

- 行与行之间用 `\n`
- 行内不强制去空格；如果做归一化（例如全角/半角），必须在 `model_config_id` 对应配置中显式声明

### 7. 禁止输出（必须）

raw text output contract 明确禁止输出以下字段或等价语义：

- `navigation_instruction` / `route_advice`
- `scene_conclusion`
- `task_decision`
- `semantic_summary`
- `final_output_text`

### 8. 兼容性与版本

- 本合同为 `v0`，任何字段变更必须走版本升级（`v1`）并在 README 索引中登记


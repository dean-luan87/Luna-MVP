# LUNA Mainline — Phase Status Matrix Schema v0

## 行字段（每条模块/阶段一行）

| 字段 | 取值说明 |
|------|----------|
| `module` | 逻辑域：`YOLO` / `OCR` / `Evaluation Tools` / `OCRBridge` / `Voice` |
| `phase` | 人类可读阶段名（如 `OCR-007`） |
| `status` | `GO` \| `CONDITIONAL_GO` \| `NO_GO` \| `closed_v0` |
| `scope` | `runtime` \| `shadow` \| `design_only` \| `evaluation_only` \| `rfc_only` |
| `runtime_connected` | 是否已声称接入主线 runtime（本复盘默认 OCRBridge/OCR pack 为 false） |
| `midplatform_connected` | 是否已接中台 |
| `whitebox_connected` | 是否已接白盒 |
| `provider_invoked` | **本复盘工具**是否调用 provider（须为 false） |
| `world_write_invoked` | 世界写入 / 蜂巢等（须为 false） |
| `mainline_side_effect` | 非授权主线副作用（须为 false） |
| `next_allowed_action` | 登记允许的下步 **类型**（不执行） |
| `blocked_action` | 明确禁止的危险动作 |

机器可读矩阵见：`mainline_phase_status_matrix.json`（由 review 工具生成）。

# LUNA Mainline — Design vs Runtime Boundary Matrix v0

## 分类定义

| `scope` | 含义 |
|---------|------|
| **evaluation_only** | Evaluation Tools / 离线 harness；可为 GO/CONDITIONAL_GO，**≠** 主线已接线。 |
| **design_only** | 文档与合同（OCRBridge Design/Review、Voice 策略文档等）。 |
| **rfc_only** | OCRBridge Implementation RFC：绑定点与 flag 规划，**无代码接线**。 |
| **shadow** | 受控 trial / 旁路（OCR Stage-2 008–012 意图）；**仍非** MidPlatform 消费链。 |
| **runtime** | 真正影响产品路径的行为（本复盘 **不**将 OCRBridge/OCR pack 标为已 runtime 全连接）。 |

## 易混点（写死）

1. **OCR-007** 的 routing pack：**evaluation_only**，**禁止**作 runtime source。  
2. **OCRBridge RFC-001**：**rfc_only**；`eval:*` **禁止**当 runtime ref。  
3. **完整语音交互**（ASR 多轮等）：当前登记为 **未完成**（`NO_GO` 或单独 readiness phase），**禁止**标为已接主线。

# LUNA OCR Bridge — Runtime `source_refs` 需求清单 v0 (Phase-OCRBridge-Review-001)

## 当前阶段（Review / Design）

- 仅允许 **`eval:*`** 或明确标注为 **design placeholder** 的引用字符串。
- **禁止**将评测路径、日志路径伪装为已上线的 **`trace_ref` / `replay_ref`** 等生产形态。
- **禁止**在本阶段工具中写入 `runtime:` / 伪造 HTTPS 服务端点作为「已绑定引用」。

## 未来 Implementation 必须绑定的引用（命名清单）

实现阶段应为下列概念各自提供 **稳定可解析引用**（命名与序列化格式可在实现 RFC 中细化）：

| 引用名 | 用途 |
|--------|------|
| `image_frame_ref` | 相机帧 / 图像在感知流水中的身份 |
| `crop_or_roi_ref` | 裁剪或 ROI 与主帧关系 |
| `ocr_provider_invocation_ref` | 单次 OCR 调用可审计 id |
| `raw_candidate_ref` | 原始 OCR 行/块候选 |
| `layout_governance_ref` | 版面 / symbol / glyph 治理上下文 |
| `image_quality_gate_ref` | 图像质量门输出绑定 |
| `eligibility_gate_ref` | 适用域门控输出绑定 |
| `reading_order_ref` | 阅读顺序决策与置信度 |
| `trace_ref` | RequestTrace / 等价追踪根 |
| `replay_ref` | Replay 根或切片 |
| `audit_ref` | 审计视图或导出键 |

设计期示例中上述概念可用 **`eval:` + case_id** 占位；**不得**声称已完成真实绑定。

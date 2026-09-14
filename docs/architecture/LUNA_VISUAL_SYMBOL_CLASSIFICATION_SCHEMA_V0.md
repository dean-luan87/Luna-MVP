# LUNA — Visual Symbol Classification Schema v0

## Phase

- **Phase-WorldModel-VisualSymbolEvidence-001**

## Purpose

冻结 `VisualSymbolEvidence.symbol_type` 的分类枚举与最小字段语义，避免把“符号识别”混入普通 OCR `raw_text` 主链。

## symbol_type（冻结枚举）

`symbol_type` 必须取值之一：

- `signature`：签名（个人/授权签名；常见于票据/文件）
- `seal_or_stamp`：印章/红章/公章（机构身份/授权线索；风险高）
- `stylized_logo`：字形 Logo（“像文字但本质是图形”）
- `brand_mark`：品牌符号（非纯文字；可能无可读文本）
- `emblem`：徽章/机构标识（学校/医院/政府/公司等）
- `watermark`：水印（来源/版权/防伪线索；可能重复）
- `handwritten_mark`：手写标记（勾选/批注/短标记；含义依赖上下文）
- `symbolic_label`：符号化标签（编号样式/图标+短字；需确认）
- `certificate_mark`：证书/认证标识（如“认证章/认证标识”；欺诈风险高）

## Required fields by class（最低字段要求）

所有类别都必须具备：

- `source_image_ref`（原图/帧/文档页引用）
- `crop_region`（裁剪区域）
- `symbol_visual_signature.feature_hash`（特征签名，便于多帧一致性与复核）
- `trace_ref` / `whitebox_ref`（可追责）

高风险类别（`seal_or_stamp` / `certificate_mark` / `signature`）额外要求：

- `trust.fraud_risk_status` 必须存在，且默认不得为 `verified`
- `confirmation.confirmation_method` 不得为 `none` 才允许进入强制记忆分支（见 forced memory policy）

## Not in scope（本阶段不声明）

- 不声明任何具体视觉模型实现（detector/embedding/descriptor 的算法）
- 不声明真伪判定规则（只声明“不得下结论”的治理边界）


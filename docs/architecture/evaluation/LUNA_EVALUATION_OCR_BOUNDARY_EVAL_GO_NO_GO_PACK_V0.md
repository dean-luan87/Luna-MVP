# LUNA Evaluation Tools — OCR Boundary Eval Go/No-Go Pack v0 (Phase-EvaluationTools-OCR-006)

## GO

- capability boundary dataset 已生成（含 taxonomy 覆盖、质量扰动覆盖）
- RapidOCR evaluation 完成（v0 仅 rapidocr）
- content type performance report / quality perturbation report / boundary map / routing policy draft 均生成
- False Text Risk / Eligibility Accuracy 报告均生成
- trace/replay 非空
- 不接入 runtime/whitebox，不产生 mainline side effect
- verifier 通过

## CONDITIONAL_GO

- 部分复杂类型仅 placeholder（manual_sample_required），需要后续补真实样本
- routing policy 仍为 draft，需真实样本确认

## NO_GO

- dataset/ground truth 缺失且无法评测
- boundary map / routing policy draft 缺失
- 发生明显的“错误自信文本”（False Text Risk 未被标记/未被报告）
- 接入 runtime/whitebox/主线 side effect
- 本阶段执行 PaddleOCR trial（禁止）


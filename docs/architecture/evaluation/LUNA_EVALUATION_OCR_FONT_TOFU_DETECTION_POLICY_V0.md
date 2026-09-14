# LUNA Evaluation Tools — OCR Font Tofu Detection Policy v0 (Phase-EvaluationTools-OCR-002)

## Background

当 Pillow 使用不支持 CJK 的字体绘制中文时，常见结果是 **tofu block（方框/空框占位符）**。这会导致：

- 中文 ground truth 与图像渲染内容不一致
- OCR CER/中文召回失真（通常极差）

## Policy

本阶段采用 **保守** tofu 检测策略，作为生成中文 synthetic 数据集的前置门控：

- 渲染两个不同中文字符（例如“中”“海”）并比较 mask 是否完全一致  
  - 若一致：强烈怀疑 tofu（tofu_suspected=true）
- 渲染固定 probe_text（例如“上海地铁9号线防范电信网络诈骗”）并计算 ink_ratio  
  - ink_ratio 过低：疑似未实际渲染可见文本

## Notes

- 这是 Evaluation Tools 的数据质量门控策略，不是 runtime 策略。
- tofu 检测不承诺 100% 准确；在不确定时应输出 warning 并阻止进入“中文 baseline dataset”。


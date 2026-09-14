## Phase-ModelOCR-001

OCR Raw Text Benchmark Metrics v0

### 1. 目标与边界

本阶段评测指标只覆盖 **OCR 原文识别质量**，不引入任何语义理解/意图/导航指标。

允许的评测对象：

- 字符/词/行级原文（text）
- 位置对齐（bbox）
- 置信度质量（confidence）作为辅助统计
- 读取顺序一致性（line_order）
- 整帧原文拼接（raw_text_joined）的一致性

禁止的指标类型（NO-GO）：

- 导航建议正确率、任务决策准确率、场景理解、语义总结质量等

### 2. 基础归一化（评测侧）

为保证跨模型对比一致性，评测侧可选做如下归一化（必须可开关）：

- 全角/半角统一
- 中英文空格归一
- 标点归一（可选）

注意：归一化仍属于“原文层”，不得引入语义改写。

### 3. 指标集合（v0）

#### 3.1 文本识别（Text）

- **CER（Character Error Rate）**：字符级编辑距离 / 参考字符数
- **WER（Word Error Rate）**：词级编辑距离 / 参考词数（中文可用分词或按字近似）
- **Exact Line Match Rate**：逐行 `text` 完全一致的比例
- **Joined Text CER**：对 `raw_text_joined` 计算 CER（快速回归用）

#### 3.2 检测与对齐（BBox）

需要 GT bbox 时才可计算：

- **Line Detection Precision/Recall/F1**：以 bbox 匹配为“检出”判定
  - 匹配规则：IoU >= 阈值（如 0.5），并做一对一匹配（Hungarian 或 greedy）
- **BBox IoU Mean/Median**：匹配对上的 IoU 统计

#### 3.3 顺序一致性（Order）

- **Kendall Tau / Spearman（可选）**：对齐后的 `line_order` 排序相关性
- **Order Exact Rate**：对齐后顺序完全一致比例

#### 3.4 置信度校准（Confidence，辅助）

不作为 GO/NO-GO 硬指标（除非后续明确纳入）：

- **ECE（Expected Calibration Error）**：置信度与正确率一致性（需要定义正确判定）
- **Confidence vs Error correlation**：置信度与错误率的相关性

### 4. 多模型对比方式（v0）

同一批 GT 样本上，对每个 `model_config_id` 输出：

- frame-level 汇总表（CER/WER/Joined CER、检测 F1、IoU、顺序指标）
- failure bucket（漏检、误检、错行、错序、拼接异常）

### 5. 哪些指标进入 OCR 独立验收

建议 v0 的独立验收硬指标只包含：

- Joined Text CER（或 Line CER）在可接受阈值内
- Line Detection F1（当提供 GT bbox 时）在可接受阈值内
- Order Exact Rate（或 Order 错误率）在可接受阈值内

阈值本阶段不强行定数值（由数据集规模与基线确定），但必须在 GO/NO-GO pack 中明确“以哪些指标作为门槛”。


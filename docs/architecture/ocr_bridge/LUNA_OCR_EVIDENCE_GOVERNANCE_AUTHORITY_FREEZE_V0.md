# LUNA OCR — Evidence Governance Authority Freeze v0

**阶段定位**：架构硬约束 / 接口评审必须纳入的冻结口径（**文档**；不接线、不改 runtime）。

---

## 冻结口径（硬约束）

1. **OCR 不拥有最终解释权。**  
2. **OCR 只负责提供「视觉文字证据」（visual text evidence）。**  
3. **中台（MidPlatform）负责控制、组合、校验、修正和分流 OCR 结果。**

### 必须写入后续接口评审的英文表述（冻结）

- **MidPlatform has authority over OCR evidence interpretation.**  
- **OCR provider has no authority to write facts.**

---

## 未来 OCR 正确链路（意图级）

```
图像 / ROI / 场景输入
  → OCR provider 识别
  → OCR Evidence Pack（标准化证据封装）
  → 中台接管
  → 与当前环境数据交叉验证
  → 修正 / 降权 / 分流 / 阻断
  → 再决定是否进入 SceneDelta / WorldContext / 任务链
```

---

## 中台需要管的三件事

### 第一：OCR「看见了什么」——看完整证据，而非只看 raw text

中台消费的是 **结构化证据**，包括但不限于：

- 文字候选  
- bbox / ROI  
- provider  
- confidence  
- layout group  
- reading order  
- symbol / glyph  
- input quality  
- source image ref  
- trace / replay / audit  

**禁止**把无上下文的 **`raw_text_joined`** 当作唯一事实输入（与 `LUNA_OCR_MIDPLATFORM_INTERFACE_FREEZE_V0.md` 一致）。

### 第二：OCR 结果如何与环境数据结合

示例意图：「9号线」不能只靠 OCR；须与 **地点是否在地铁站、地图/POI/标识牌上下文、YOLO 站牌/线路图/闸机/电梯/出口、历史空间记忆、当前任务目标、用户位置与移动方向** 等 **交叉验证** 后再做决策。

### 第三：OCR 错误如何修正（治理动作）

中台 **不得照单全收**，须能做包括但不限于：

- 证据冲突检测  
- 上下文校验  
- layout / symbol / glyph 分流  
- provider fallback  
- 置信度降权  
- 人工确认 / 延迟复核  
- **禁止进入事实层**（当不满足准入策略时）

---

## OCRBridge 的定位（更正表述）

- **OCRBridge 不是**「OCR → 中台」的 **简单转发器**。  
- **OCRBridge 是** OCR evidence 的 **标准化封装层**（将感知输出整理为 **`OcrEvidencePackV0`** 等合同形态）。  
- **中台才是** OCR 结果的 **治理与组合中心**（解释、校验、与场景数据融合、再决定下游）。

---

## 一句话冻结

**OCR 是感知器官，中台是治理大脑：OCR 只能报告「看见了什么」；中台决定这些内容是否可信、属于哪里、能不能进入事实层。**

---

## 与既有合同的关系

本文件 **不替代** `LUNA_OCR_MIDPLATFORM_INTERFACE_FREEZE_V0.md` 与 `LUNA_OCR_EVIDENCE_PACK_MINIMUM_REQUIRED_FIELDS_V0.md`，而是把 **权力边界与治理责任** 写死为 **后续所有 OCRBridge / 中台接口评审的前置硬约束**。

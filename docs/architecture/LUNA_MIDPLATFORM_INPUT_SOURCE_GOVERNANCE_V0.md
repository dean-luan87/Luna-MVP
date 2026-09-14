# LUNA MidPlatform Input Source Governance v0

**建议阶段命名**：`Phase-MidPlatform-Input-Source-Governance-001`  
**能力别名**：Performance-Aware Image Input Filtering & Normalization v0  

本文档描述**中台对图像类输入的统一治理原则**（设计层）。OCR 是首批消费方；后续视角模型、VLM、场景理解等应复用同一套输入源语义，而非各自「直连原图」。

---

## 核心定位

中台**不是**简单「转发图片」，而是把输入变成**在当前系统状态下最适合下游处理的信息源**。

中台至少承担**两类职责**：

1. **过滤不可处理输入**（质量与可读性维度）  
2. **规范化超规格输入**（像素预算与形态维度，但仍可能是有价值的任务输入）

---

## 关键词与模块边界（设计词汇表）

| 关键词 | 含义 |
|--------|------|
| **ImageQualityGate** | 质量闸门：模糊、曝光异常、全黑/全白、损坏、分辨率过低、有效文字区域过小、抖动、遮挡、格式不支持、metadata 不可读等 → **过滤**，不硬送 OCR/视觉。 |
| **ImageSpecGate** | 规格闸门：超大图、高像素、长图、多区域文字、图文混排等 → **不原样直送**，进入规范化与形态选择（可与现有尺寸/像素预算治理对齐并逐步收敛命名）。 |
| **PerformanceControllerConstraint** | 性能控制器对规划器的**硬/软约束**：CPU/内存/GPU/温度/电量、任务队列、模型队列、是否在移动、是否安全任务优先等。 |
| **PerformanceAwareInputPlanner** | 在质量与规格结论之上，结合**性能状态 + STCM 时效 + 任务价值**，选择具体处理链（压缩、降采样、裁剪、ROI、分割、tiling、异步等）。 |
| **BestAvailableInputSource** / **BestPerformanceInputSource** | 中台对下游输出的**最佳可用信息源**描述（见下文 JSON 示例）；**不是**原始高压输入本身。 |

实现上可渐进落地：`ImageSpecGate` 与现有 `ocr_image_input_gate` / normalization 管线对齐；`ImageQualityGate` 与 `PerformanceAwareInputPlanner` 在后续阶段增量接入。

---

## 第一类：过滤不可处理输入（质量）

下列情形属于**低于最低处理标准**，不应硬送 OCR 或视觉模型（应走中台拒绝/软失败路径，并给出可行动反馈）：

- 严重模糊；严重过曝 / 欠曝；全黑 / 全白  
- 损坏文件；分辨率过低；有效文字区域过小  
- 画面抖动严重；遮挡严重；格式不支持  
- **无法读取 metadata**（与不可信输入区分策略由实现定义）

中台对外应能表达（字段集合可演进，语义如下）：

- **`input_rejected`**（或等价状态）  
- **`reason_codes`**（机器可读）  
- **`retry_required`** / **`resample_required`**（是否建议用户重拍、调光、靠近等）  
- **`voice_notice_required`**（是否需要语音侧用户可理解说明）  

示例话术（非唯一文案）：「画面太模糊，我需要重新看一下。」「这张图太暗，暂时无法识别文字。」

---

## 第二类：规范化超规格输入（规格 + 价值）

超规格**不是**「不能处理」，而是**不能原样处理**，例如：超大图、高像素、长图、多区域文字、图文混排、包装全图、说明书、公告栏、海报等。

应进入中台处理链，可能包括：

压缩、降采样、裁剪、ROI 提取、图像分割、切块 tiling、坐标回填、**source chain** 记录、置信度/质量损失风险标注等。

**核心不是「把图变小」**，而是把它变成同时满足：

- **当前任务需要**  
- **当前模型能处理**  
- **当前性能扛得住**  
- **结果还能回溯**  
- **空间坐标不丢**  

---

## 目标架构链路（逻辑顺序）

```text
Raw Image
  → ImageQualityGate
  → ImageSpecGate
  → Performance Controller（约束注入）
  → STCM Deadline Check
  → Task Value Assessment
  → PerformanceAwareInputPlanner（Input Normalization Planner）
  → Best Input Source Pack（可含多 unit、坐标变换、审计）
  → OCR / Vision / Voice 等下游模块
```

同一张大图在不同状态下**允许不同策略**（设计原则，非单一路由表）：

- 系统空闲 + 用户主动读说明书 → 可异步 tile + 重型 OCR  
- 系统高压 + 导航近实时 → 高价值 ROI 或延后  
- 安全任务进行中 → 可取消背景 OCR，优先视觉安全链路  
- 内存压力高 → 禁止重模型路径，走缓存 / 轻量 OCR / 更强降采样等（与产品策略一致）

若处理会**超出时效窗口**，必须交由 **STCM** 决定：取消、异步、换模型档位、语音告知等，而不是静默超时或硬塞原图。

---

## BestAvailableInputSource（示例形状）

下游消费的应是「最佳可用信息源」描述，而非隐含假设「路径即原图」：

```json
{
  "input_source_type": "downscaled_image",
  "reason": "original_image_oversized",
  "selected_for": "ocr_level_2",
  "performance_state": "memory_pressure_medium",
  "original_image_ref": "...",
  "transformed_image_ref": "...",
  "scale_ratio": 0.42,
  "coordinate_transform": "...",
  "quality_loss_risk": "medium",
  "deadline_class": "task_context_medium"
}
```

与现有 **`ocr_provider_input_pack_v0`** 的关系：当前 pack 是 OCR 消费侧的**最小实现**；长期应能映射或升级为「Best Input Source Pack」家族 schema 的子集或一层视图。

---

## 设计核心规则（必须写进实现与评审检查单）

1. **低于最低质量标准的图像应被过滤**，而不是强行处理。  
2. **超出规格但仍有价值的图像应被规范化**，而不是在无规划下直接拒绝（除非质量闸门已否决）。  
3. **中台应根据性能控制器状态**（及队列、Deadline）**选择输入形态**，而非仅按像素表机械决策。  
4. **下游模块不应直接消费「原始高压输入」**作为默认可执行路径；应消费明确类型的 Best Available Input Source / Pack。  
5. **所有变换必须保留 source chain 与 coordinate transform**，保证证据与 polygon 的空间语义可回溯。  
6. **若处理会超出时效窗口**，必须交给 **STCM** 决定取消、异步、换模型或语音告知，不得静默假成功。  
7. **中台输出的是最佳可用信息源**，而不是原始数据副本的隐含承诺。

---

## 与 OCR 先行阶段的关系

- **`Phase-OCR-ImageInput-Normalization-Pipeline-001`** 在代码上实现了 **ImageSpecGate 子集 + 最小规范化 + Provider Input Pack**，用于证明「超规格可被整理成可消费输入」，**不替代**本文档中的质量闸门与性能感知规划器。  
- 本文档为**中台级输入源治理**的总纲；后续阶段应把 **ImageQualityGate**、**PerformanceControllerConstraint**、**STCM / 任务价值** 显式接入规划器，并把命名从「仅 OCR」推广到多模态消费方。

**局部证据补全候选（非事实补全）**与披露、用户确认、高风险动作闸门，见 OCR 侧专文：[ocr/LUNA_OCR_PARTIAL_EVIDENCE_COMPLETION_POLICY_V0.md](./ocr/LUNA_OCR_PARTIAL_EVIDENCE_COMPLETION_POLICY_V0.md)（`Phase-OCR-Partial-Evidence-Completion-Policy-001`）。

---

## 一句话

中台不是「审图员」，而是**输入治理器**：既要挡掉不可处理的垃圾输入，也要把超规格但有价值的输入加工成**当前系统扛得住、下游模型能消费、可审计可回溯**的最佳信息源。

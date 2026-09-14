# Luna — OCR Task-Oriented Capability Principle v0

**状态**：**已冻结**（架构原则，非单 phase 产物）  
**关联**：Multiframe OCR v2 受控验证、`User-Guidance-Recovery-Policy-v1`、`Vision-Zoom-Autofocus-Resampling-Policy-v1`（待实现）

## 一句话

**Luna 先「看懂世界」，再在任务需要时「读文字」；OCR 是任务完成与安全确认工具，不是世界认知的默认入口。**

---

## 核心原则

**OCR Task-Oriented Capability Principle**

- **OCR 不是** Luna 世界建模的默认主通道。
- Luna 的世界建模**优先**依赖：第一视角视觉语义、空间结构、图标/标识、物体关系、路径可达性与任务上下文。
- **OCR** 作为**任务型精确识别**能力，主要用于：保障安全、完成任务、确认关键短文本，以及响应用户主动阅读需求。

---

## 世界建模主路径（默认）

```
第一视角视觉语义
  → 空间关系
  → 场景结构
  → 图标 / Logo / 公共设施符号
  → POI / 地图粗定位
  → 用户任务上下文
  → 必要时 OCR 辅助确认
```

OCR 出现在链路**末端**，且为**按需、有门控**的辅助，不得替代上游视觉语义与空间结构成为默认「理解世界」的手段。

---

## OCR 主要负责（任务型边界）

| 类别 | 示例 |
|------|------|
| **1. 安全相关文字** | 禁止通行、维修中、危险、出口、施工 |
| **2. 任务完成文字** | 门牌号、窗口号、楼层、公交线路、科室、店名确认 |
| **3. 短标识确认** | 银行、药房、洗手间、电梯、服务台、入口/出口 |
| **4. 用户主动阅读** | 说明、菜单、通知、药盒、文件、商品标签 |

输出仍为 **candidate-only**（见 [LUNA_OCR_INDEPENDENT_CAPABILITY_DEFINITION_V0.md](../LUNA_OCR_INDEPENDENT_CAPABILITY_DEFINITION_V0.md)）：不得因 OCR 空/非空直接写入事实层或宣称导航结论。

---

## 精细阅读（高要求链路，单独门控）

与用户主动触发、画面质量、引导与重采样绑定的**精读**路径，**不得**与默认轻量扫帧 OCR 混用：

```
用户主动触发
  → 系统判断画面质量
  → 引导用户靠近 / 对准 / 保持稳定
  → 必要时：放大 / 变焦 / 重采样
  → OCR
  → 摘要 / 解释 / 任务决策（仍 candidate-only，经 EP/SV/审批链）
```

评测侧已体现的方向（非生产默认路径）：

- [LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_MULTIFRAME_V2.md](./LUNA_OCRREQUEST_GATED_SUBMISSION_FROM_MULTIFRAME_V2.md)（adjusted crop 受控 OCR；same-bbox 风险下 empty 不触发无限 re-crop）
- [LUNA_USER_GUIDANCE_RECOVERY_POLICY_V1.md](../midplatform/LUNA_USER_GUIDANCE_RECOVERY_POLICY_V1.md)（输入达标范围 + 引导/自调度/外援候选；policy only）
- [LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md](../midplatform/LUNA_STC_SAMPLING_GUIDANCE_POLICY_V1.md)（Safety-triggered 后台 + Task-triggered 中台预判）
- 后续：`OCR-Activation-Governance-Policy-v1`、`Vision-Capture-Governance-v1`

---

## 待实现：OCR Activation Gate（工程占位）

在 runtime / 评测治理层应显式区分激活模式（命名供后续 phase 对齐）：

| 模式 | 含义 |
|------|------|
| **no_ocr** | 不需要 OCR；世界建模走视觉主路径 |
| **lightweight_short_text** | 轻量短文本 OCR（任务型 ROI / 小 crop） |
| **task_confirmation_ocr** | 任务型确认 OCR（门牌、标识、安全短句等） |
| **user_guided_precision_read** | 用户引导式精读 OCR（质量闸 + 引导 + 可选 zoom/resample） |
| **dynamic_reading_recovery** | 动态阅读恢复链（empty/low-conf 后的受控恢复，**非**无限内部扩框） |

Gate 输出应为 **policy decision + trace**，`not_fact`，且与 `ocr_mainline_bridge` 提交合同一致。

---

## 明确禁止（与原则冲突）

- 将 **全帧默认识别** 或 **高密度连续 OCR** 作为世界建模默认输入。
- 因 OCR empty 推断「无文字」事实，或因 non-empty 推断 accuracy / multiframe consensus（见 multiframe OCR v1/v2 non-claims）。
- 在 same-bbox / 低几何增益条件下 **无限** internal re-crop / re-OCR（应转入用户引导或系统自调度恢复策略）。
- 绕过 bridge 直接调用 provider 以「刷」OCR 覆盖率。

---

## 与现有 OCR 合同的关系

- **能力定义**：[LUNA_OCR_INDEPENDENT_CAPABILITY_DEFINITION_V0.md](../LUNA_OCR_INDEPENDENT_CAPABILITY_DEFINITION_V0.md)（感知层文字候选）
- **运行时治理**：[LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md](./LUNA_OCR_PROVIDER_RUNTIME_GOVERNANCE_STANDARD_V0.md)
- **主线桥接**：[LUNA_OCR_MAINLINE_MINIMAL_BRIDGE_V0.md](./LUNA_OCR_MAINLINE_MINIMAL_BRIDGE_V0.md)
- **部分证据补全**（非默认写 WM）：[LUNA_OCR_PARTIAL_EVIDENCE_COMPLETION_POLICY_V0.md](./LUNA_OCR_PARTIAL_EVIDENCE_COMPLETION_POLICY_V0.md)

本原则 **高于** 单 phase smoke 的「跑通 OCR」目标：phase 可通过 bridge 验证链路，仍须遵守「OCR 非世界建模主通道」与 Activation Gate 语义。

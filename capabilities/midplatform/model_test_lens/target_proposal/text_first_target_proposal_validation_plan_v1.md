# Text-First Target Proposal Validation Plan V1

**Phase:** `Phase-P1-Midplatform-Text-First-Target-Proposal-Validation-Planning-v1-001`  
**System ID:** `LunaMidplatformTextFirstTargetProposalValidationPlanningV1`  
**Status:** Planning only（不接真实 OCR recognition、不写 fact、不改 runner sandbox）

## 背景

Scene-Aware Prompt Policy 与 Dual Route Validation 已解决 **prompt label 误导** 与 **双路线对照框架**，但感知目标质量仍不足：

- 地铁站图：应优先观察「开往 嘉会湖」等导视文字，而非大块结构/地面/人物 SAM 区域  
- 店招图：应优先观察「阿叔阿姨的店」等大字，而非粗粒度牌匾/空白/底部结构  

**根因：** 当前以 SAM region proposal 为主导，对文字场景使用了错误的感知入口。  
SAM 适合空间区域 / mask refine，**不适合作为文字发现主链路**。

## 上游 GO

| 基线 | 决策 |
|------|------|
| Dual Route Perception Validation Execution | GO |
| Scene-Aware Segmentation Prompt Policy Execution | GO |
| MobileSAM Single Model Execution Integration | GO |
| MobileSAM → OCR Runner Sandbox Integration Execution | GO |

## 核心原则

1. **SAM / MobileSAM** — `region_proposal_candidate` / mask refine，**不负责文字发现主链路**（`sam_not_primary_text_detector`）  
2. **OCR text detector** — `text_region_candidate` / `text_line_candidate` / `text_block_candidate`  
3. **Grounding / Detection** — `semantic_target_candidate`（对象/导视牌/屏幕等）  
4. **VLM** — route / attention suggestion，不写 fact  
5. **中台** — 融合三类 candidate → `midplatform_target_selection` → task candidate  
6. `text_region_candidate` **≠ OCR result**，**≠ fact**

## 三类候选分层

| 类型 | 来源 | 作用 |
|------|------|------|
| `region_proposal_candidate` | SAM / MobileSAM | 空间区域候选 |
| `text_region_candidate` | OCR text detector (stub) | 文字区域候选 |
| `semantic_target_candidate` | Grounding / Detection / VLM | 目标或观察路线候选 |

**禁止** 全部统称「分割候选」。

## Text-first 路线（Route T）

```
Image
  → text_detector_stub
  → text_region_candidate / text_line_candidate / text_block_candidate
  → Midplatform Target Selection
  → target_proposal_comparison_candidate   ← 本阶段终点
  → OCR task candidate（未来受控执行，本阶段不执行）
```

**注意：** stub 只模拟文字**区域**检测，**不输出真实文字内容**。

### 与 Dual Route 关系

| 路线 | 角色 | 文字场景 |
|------|------|----------|
| **Route T (Text-first)** | 文字区域发现主入口 | **优先** |
| Route A | Grounding → SAM refine | 对象/结构，不替代 text detector |
| Route B | VLM route enhancer | 观察建议，不产精确框 |

## Midplatform Target Selection

融合输入：

```
region_proposal_candidate
+ text_region_candidate
+ semantic_target_candidate
    ↓
midplatform_target_selection
    ↓
target_proposal_comparison_candidate
    ↓
OCR / Detection / SAM refine / manual_review task candidate
```

规则摘要：

| 情况 | 处理 |
|------|------|
| text_region 高置信 + 与 semantic/VLM 建议重叠 | OCR task candidate priority boost |
| text_region 存在，SAM region 不重叠 | `alignment_conflict`；不 auto admission |
| 无明显 text_region | 不生成 auto OCR task；可 manual_review |
| text_detector 与 SAM 均低置信 | manual_review only |

## Smoke Cases（4）

| Case | 输入 | 预期 |
|------|------|------|
| **A** 地铁站导视 | 嘉会湖站台图 | 上方导视 `text_region_candidate`；OCR task candidate；SAM 仅作空间关联；无文字 fact |
| **B** 店招 | 店招图（阿叔阿姨的店） | `text_block_candidate` 覆盖大字区；logo 可作 semantic candidate；OCR task candidate；不确认店名 fact |
| **C** 无明显文字 | 无文字场景 | text 候选为空/low_confidence；无 auto OCR；可 manual_review |
| **D** SAM 与 text 不重叠 | 合成错位 | `alignment_conflict`；不写 fact；不 auto admission |

## 本阶段终点

**target_proposal_comparison_candidate** — 中台对 text / region / semantic 三类 proposal 的比较与任务建议，不是 fact。

## 本阶段禁止

- 真实 OCR recognition / text detector 模型调用  
- 输出真实文字内容作为 fact  
- SAM prompt 继续承担文字发现主责  
- SLAM 文字检测  
- 写 fact / 导航决策  
- 改变 OCR / Detection / VLM / MobileSAM runner sandbox  

## 下一阶段

`Phase-P1-Midplatform-Text-First-Target-Proposal-Validation-Execution-v1-001`

## Schema 索引

- `schemas/target_proposal/text_region_candidate_schema_v1.json`
- `schemas/target_proposal/text_target_proposal_policy_v1.json`
- `schemas/target_proposal/target_proposal_comparison_candidate_schema_v1.json`
- `schemas/target_proposal/text_detector_stub_policy_v1.json`
- `schemas/target_proposal/midplatform_target_selection_policy_v1.json`

# Text-First Target Proposal Validation Governance Standard V1

**Standard ID:** `TextFirstTargetProposalValidationGovernanceStandardV1`  
**Phase:** `Phase-P1-Midplatform-Text-First-Target-Proposal-Validation-Planning-v1-001`

## 目的

规划 **Text-first target proposal** 验证：文字场景以 OCR text detector 为主入口发现任务目标区域，SAM 仅作 region proposal / 空间关联，中台融合后生成 task candidate，均不写 fact。

## 上游 GO

- Dual Route Perception Validation Execution GO  
- Scene-Aware Segmentation Prompt Policy Execution GO  
- MobileSAM Single Model Execution Integration GO  
- MobileSAM → OCR Runner Sandbox Integration Execution GO  

## 三类候选

| 类型 | 来源 | 角色 |
|------|------|------|
| region_proposal_candidate | SAM | 空间区域，非文字发现主链 |
| text_region_candidate | text detector stub | 文字区域 |
| semantic_target_candidate | Grounding / VLM | 对象/观察目标 |

## 核心边界

- **SAM 不是文字检测主入口**  
- **text_region_candidate ≠ OCR result ≠ fact**  
- **text_detector_stub 不输出 recognized_text**  
- **SLAM 不参与文字发现**  
- **alignment_conflict 不 auto admission**  

## 本阶段允许

- 规划 schema / policy / smoke  
- deterministic text_detector_stub  
- target_proposal_comparison_candidate 定义  

## 本阶段禁止

- 真实 OCR recognition  
- 真实 text detector 模型调用  
- 写 fact / 导航决策  
- SAM prompt 继续主导文字发现  

## 下一阶段

`Phase-P1-Midplatform-Text-First-Target-Proposal-Validation-Execution-v1-001`

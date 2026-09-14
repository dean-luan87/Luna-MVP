# Dual Route Perception Validation Governance Standard V1

**Standard ID:** `DualRoutePerceptionValidationGovernanceStandardV1`  
**Phase:** `Phase-P1-Midplatform-Multi-Model-Perception-Route-Dual-Validation-Planning-v1-001`

## 目的

规划 Luna 复杂场景下的双路线感知对照验证：Route A（Detector/Grounding → SAM）与 Route B（VLM → route candidate），由中台比较融合，均不输出 fact。

## 上游 GO

- Scene-Aware Segmentation Prompt Policy Planning GO  
- MobileSAM Single Model Execution Integration GO  
- MobileSAM → OCR Runner Sandbox Integration Execution GO  
- Observation Attention Layer Planning GO  

## 核心边界

### 不用 SLAM 找文字

SLAM 允许：空间参考、通行结构、位姿地图  
SLAM 禁止：文字检测、文字识别、路牌识别、直生 OCR route

### 双路线角色

| 路线 | 定位 |
|------|------|
| Route A | 工程可控 — Detection/Grounding → SAM refine |
| Route B | 语义适应 — VLM scene/attention/route 建议 |

二者并行验证，互为对照组，不争 fact。

## 本阶段允许

- 规划 schema / policy / smoke case  
- 定义 comparison 维度与 conflict 处理  
- UI 展示规划（不实现复杂 UI）  

## 本阶段禁止

- 真实模型调用（Detection / VLM / OCR / SLAM）  
- 写 fact / 导航决策  
- 改变现有 MobileSAM/OCR runner 治理链  
- VLM / Detector 输出升级 fact  

## 下一阶段

`Phase-P1-Midplatform-Multi-Model-Perception-Route-Dual-Validation-Execution-v1-001`

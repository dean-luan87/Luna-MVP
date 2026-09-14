# Visual Expression System — Current Slice V1

**Phase:** `Phase-P1-Midplatform-Model-Test-Lens-Visual-Expression-System-Planning-v1-001`  
**Slice ID:** `VisualExpressionCurrentSliceV1`  
**Purpose:** 从终结形态剥离当前可执行版本

## 本切片范围

仅 **Observation Attention visual expression correction** + **segmentation boundary 唯一 owner 收口**。

## 必须完成（下一 UI Execution）

1. 移除 Observation Attention 生成的第二套 box / boundary  
2. 保留 segmentation boundary 作为主图 **唯一**空间边界  
3. 主图默认只显示 **P0/P1** 可读短浮标（编号 + P级 + 区域名）  
4. P2/P3 默认只进入右侧面板；提供「显示全部候选浮标」开关  
5. 右侧面板作为 Observation Attention **主表达入口**  
6. 点击右侧记录 → 仅 selected 对应 segmentation region，boundary 不消失、不复制  
7. 底部摘要保留整体观察调度统计  
8. candidate_only / not_fact 保留在右侧，不在主图堆叠  
9. hover/selected 可显示 **一行**简化语义（如「跟踪候选」），不展示完整路线列表  
10. 禁止图标-only 默认表达；采用可读中文短标签

## 明确不做（本切片）

- Detection / OCR / Tracking / Depth / SLAM runner 接入  
- attention engine / priority 计算 / schema 变更  
- fact 写入、导航决策、ground truth 升级  
- 新模型层在主图默认画框  

## 与已落地补丁的关系

| 补丁 | 状态 | 本切片关系 |
|------|------|------------|
| Observation Attention UI Execution | GO | 面板/摘要/引擎接线保留 |
| Overlay Readability Patch | 被本体系吸收 | 避让策略降为辅助，非主方案 |
| Visual Language Patch v1-001 | 部分落地 | 方向正确，需按本规划收口 |
| Semantic Separation Patch v1-002 | 部分落地 | 作为执行基线，需 post-review 对齐本规划 |

## 验收要点（执行阶段）

- 同一 `region_id` 仅一条 segmentation boundary  
- 点击右侧不触发 boundary hide/show 切换  
- 主图浮标可读：`① P0 道路` 格式  
- P2/P3 默认不在主图  
- 右侧完整解释 + 底部摘要分工清晰  
- 21/21 + 本规划 negative guards 通过

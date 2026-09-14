# Luna — Multiframe Merge Proposal v1 GO/NO_GO Pack v0

## GO

- 4 条 SV v2 blocked candidate 全部 intake
- 至少 1 个 canonical `multiframe_candidate_region`（same frame / same region 合并）
- target frame window / neighbor selection / tracklet hint / merge strategy 均已规划
- same-frame blocker carryover 仍为 active；`boundary_ok=true`；`verifier=GO`
- 不抽帧、不解码、不 OCR、不写事实

## CONDITIONAL_GO

- candidate 数与输入不一致但 blocker carryover 完整；region 数少于预期但规划完整；无越界行为

## NO_GO

- 抽新帧、解码视频、OCR、crop/OCRRequest/EP/Semantic 生成
- Source Validation rerun、解除 same-frame blocker、写 fact/WM/SceneDelta
- benchmark/provider comparison claim、改 routing、audit 缺失

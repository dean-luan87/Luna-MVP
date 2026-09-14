# Phase-Voice-OutputGovernance-009
# Governed Submit Unified Query/Export Test Matrix v0

## A. 输入可读
- A1：Phase-008 input root 可读
- A2：enhanced chains 可加载
- A3：可找到 `governed_submit_shadow_gate` stages

## B. Query
- B1：按 submit_shadow_result 过滤可用
- B2：按 submit_gate_position 过滤可用
- B3：按 submit_allowed 过滤可用
- B4：按 request_id 过滤可用
- B5：hard_audit_only 过滤可用
- B6：query 产物（summary/results/jsonl/md）生成

## C. Export
- C1：gate position table 生成且包含两位置
- C2：result distribution table 生成
- C3：request matrix 生成
- C4：hard audit table 生成
- C5：field mapping report 生成

## D. 边界
- D1：不修改 Phase-008 原始产物
- D2：不接真实 submit、不真实播报、不执行真实 TTS

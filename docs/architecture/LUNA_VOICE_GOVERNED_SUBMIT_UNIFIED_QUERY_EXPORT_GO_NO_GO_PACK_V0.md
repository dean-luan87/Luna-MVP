# Phase-Voice-OutputGovernance-009
# Governed Submit Unified Query/Export Go/No-Go Pack v0

## GO（全部满足）

- Phase-008 input root 可读
- query tool 可运行并产出结果
- export tool 可运行并产出表格与 mapping report
- gate position table 覆盖两种 gate position
- result distribution table 生成
- request matrix 生成
- hard audit table 生成且不变量成立
- field mapping report 生成
- verifier 通过
- 不接真实 submit，不真实播报，不执行真实 TTS

## CONDITIONAL_GO

- 少量 whitebox why_* 字段缺失：必须在导出/报告中明确为 missing/not_applicable

## NO_GO（任一触发）

- 查询结果丢失 request_id / gate position
- hard audit 丢失或出现 `real_submit_invoked=true` / `real_tts_invoked=true` / `provider_invoked=true`
- 修改 Phase-008 原始产物
- 改 env 语义或删除 legacy voice

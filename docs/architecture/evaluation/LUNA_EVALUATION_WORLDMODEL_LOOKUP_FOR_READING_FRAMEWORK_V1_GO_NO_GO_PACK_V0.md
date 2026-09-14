# GO / NO-GO Pack — WorldModel Lookup for Reading Framework v1

## GO

- `final_decision=READY_FOR_WORLDMODEL_LOOKUP_READING_DRYRUN_LATER`
- request/response schema、source priority、link/handoff/fallback 政策齐全
- `worldmodel_runtime_available=false`（预期）
- `worldmodel_lookup_invoked=false`；无 WM/Memory/OCR 写入
- verifier `verdict=GO`

## CONDITIONAL_GO

- WorldModel runtime 不可用为预期；framework only；无 runtime action

## NO_GO

- 伪造 lookup result 或标成 fact
- 写 WorldModel / SceneDelta / Memory
- memory reference 覆盖 live observation
- confirmed text 直接写 WM 或直接触发 OCR
- production ready 宣称

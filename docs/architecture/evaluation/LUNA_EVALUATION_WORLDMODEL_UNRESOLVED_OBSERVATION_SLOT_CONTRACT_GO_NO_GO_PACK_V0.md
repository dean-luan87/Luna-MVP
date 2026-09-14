# Luna — WorldModel Unresolved Observation Slot Contract GO/NO_GO Pack v0

## GO

- Unresolved slot schema + 10 slot types + trigger matrix + reason taxonomy 完整  
- future fill / OCR-as-verification / evidence accumulation 政策完整  
- 5 个 examples（含建设银行、GAP、scan/pack empty）  
- lifecycle 含 `promoted_to_world_model_fact` 仅经 write_gate  
- no-write boundary `boundary_ok=true`；`verifier=GO`  

## CONDITIONAL_GO

- 部分 example 字段简略，但 schema/policy/boundary/audit 完整  
- 无越界行为  

## NO_GO

- 写 WorldModel / 生成 runtime slot / Scene Delta  
- unknown slot 当事实  
- 缺 source_chain / coordinate schema  
- benchmark 或 provider 比较 claim / 改 routing  
- audit 缺失  

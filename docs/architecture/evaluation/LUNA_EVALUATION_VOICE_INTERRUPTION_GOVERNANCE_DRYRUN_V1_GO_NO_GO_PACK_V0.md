# GO / NO-GO Pack — Voice Interruption Governance DryRun v1

## GO

- `final_decision=VOICE_INTERRUPTION_GOVERNANCE_DRYRUN_READY_FOR_LOOP_STABILIZATION_TEST`
- 24 interruption decision candidates（16 ownership cases + 8 priority scenes）
- P0/P1 边界、freshness/repeat/resume、correction/emergency/new-task policy 完整
- `verifier=GO`

## NO_GO

- 真实 TTS stop / Speech Gate / VOP invoked
- 非 owner 普通打断生效
- phone call / human conversation / media/public voice 误触发普通 interruption
- P0 safety warning 被普通 stop 直接取消
- stale repeat 被当作当前事实
- task state / memory / world model 写入

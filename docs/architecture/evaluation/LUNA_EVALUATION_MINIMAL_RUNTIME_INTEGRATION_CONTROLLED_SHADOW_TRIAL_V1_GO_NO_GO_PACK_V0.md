# GO / NO-GO Pack — Minimal Runtime Integration Controlled Shadow Trial v1

## GO

- `trial_mode=CONTROLLED_SHADOW_TRIAL`
- `final_decision=MINIMAL_RUNTIME_INTEGRATION_CONTROLLED_SHADOW_TRIAL_READY_FOR_POST_SHADOW_REVIEW`
- 至少 8 个 controlled input cases / shadow candidate traces / Speech Gate shadow decisions / VOP shadow events / abort checks
- 只产生 candidate / shadow decision / shadow event / observability trace
- 所有 runtime / write 边界保持关闭
- `non-owner` 不触发 task control
- stale safety speech 不作为当前事实复述
- P0 safety speech 不被普通 stop 取消
- `verifier=GO`

## NO_GO

- 发生任何真实 camera / microphone / ASR / TTS / Speech Gate / VOP runtime
- 发生任何 map API / GPS / OCR provider / detector / segmentation / tracking 调用
- 发生任何 task commit / navigation action / route modification
- 发生任何 Memory / WorldModel / Fact / Scene Delta write
- 缺少 source_chain，或 abort / boundary trace 不完整
- non-owner voice 能触发 task control
- stale safety speech 被当作当前事实
- P0 safety speech 被 ordinary stop 取消

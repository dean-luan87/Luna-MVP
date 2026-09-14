# GO / NO-GO Pack — Voice Dialogue Task Control Contract v1

## GO

- `final_decision=VOICE_DIALOGUE_TASK_CONTROL_CONTRACT_READY`
- intent（13）/ command（10）/ handoff / STM / repeat-pause-resume-cancel / query / clarification / safety / Speech Gate-VOP 策略已定义
- `requires_midplatform_decision=true`；`direct_task_state_change_allowed=false`
- `voice_cannot_create_task_directly` / `voice_cannot_cancel_task_directly`；`dialogue_cannot_trigger_navigation_action_directly`
- 模板 ≥10；对话 FSM 11 态；`no_write_boundary_pass_rate=1.0`
- 无 ASR/LLM/TTS/VOP/任务状态变更/Memory/WM/OCR/camera
- verifier `verdict=GO`

## CONDITIONAL_GO

- 可选 voice/taskchain 文档 `optional_missing`（不伪造）
- contract only；无 runtime action

## NO_GO

- voice 直接改 task state
- asr/llm/tts/vop invoked；`direct_tts_bypass` 允许
- cancel 不需确认；MidPlatform boundary 缺失
- navigation 可直接触发动作；runtime routing changed；production claim；audit 缺失

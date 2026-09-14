# GO / NO-GO Pack — Voice Command Ownership Gate Policy v1

## GO

- `final_decision=VOICE_COMMAND_OWNERSHIP_GATE_POLICY_READY_FOR_INTERRUPTION_GOVERNANCE`
- 16 simulated cases；五类 ownership_state；voiceprint/emotion schema candidate-only
- non-owner / phone / media 边界通过；`verifier=GO`

## NO_GO

- ASR/voiceprint/diarization invoked；audio recorded；identity/emotion fact written
- non-owner task_commit；media controls Luna；pending confirmation deleted on interrupt

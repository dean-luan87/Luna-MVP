# GO / NO-GO Pack — Navigation Guidance to Speech Candidate Adapter v1

## GO

- `final_decision=NAVIGATION_GUIDANCE_TO_SPEECH_CANDIDATE_ADAPTER_READY_FOR_BASIC_NAVIGATION_LOOP`
- speech_candidate_count >= 16；mapping/priority/suppression/uncertainty 定义
- VOP handoff + Speech Gate admission candidate；`verifier=GO`

## NO_GO

- TTS/VOP invoked；direct bypass；speech 当成真实播报
- navigation guidance 当成 action；stale evidence 生成当前行动提示
- fact 陈述无不确定性；runtime routing changed

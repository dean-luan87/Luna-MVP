# User Guidance Recovery Policy v1 GO/NO_GO Pack v0

## GO

- OCR input readiness 五类 scope 定义；`threshold_is_policy_placeholder=true`
- OCR-L0～L5、task criticality、failure taxonomy、repairability 四类
- user / system / external action candidates；hardware placeholder
- 不 TTS、不硬件、不 OCR；`verify_user_guidance_recovery_policy_v1` = GO

## CONDITIONAL_GO

- 阈值为 placeholder；current case 仅 dry-run decision

## NO_GO

- TTS / runtime guidance / hardware / OCR / crop / EP / Semantic / 写事实 / routing 变更

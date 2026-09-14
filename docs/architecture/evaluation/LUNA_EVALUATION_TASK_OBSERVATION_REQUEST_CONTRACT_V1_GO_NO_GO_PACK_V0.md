# GO / NO-GO Pack — Task Observation Request Contract v1

## GO

- `final_decision=TASK_OBSERVATION_REQUEST_CONTRACT_READY_FOR_VISION_OCR_INGEST`
- schema / baseline / task-driven / routing / gate / PTF 已定义
- candidates >= 16（baseline >= 4，task-driven >= 12）
- `request_allowed_now_count=0`
- handoff → Vision-OCR-Evidence-Ingest-Integration-Check-v1

## NO_GO

- camera/OCR/detector invoked
- baseline 无任务不可 request
- task-driven 无 task context
- generic OCR without task
- `request_allowed_now=true`
- voice 直接生成 request

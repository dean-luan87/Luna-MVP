# Luna — Assisted Static Reading Runtime DryRun v1

**Phase**：`Assisted-Static-Reading-Runtime-DryRun-v1-001`  
**性质**：Runtime dry-run only

## 目的

模拟当前 case 从动态 OCR 失败进入静态阅读模式后的可执行路径：mode entry → FSM 推进 → readiness → guidance step → static capture candidate → OCRRequest future gate。

## 当前 case 结论

- **final_decision** = `WAIT_FOR_USER_STABILIZATION`
- **current_state** = `WAITING_FOR_USER_STABILIZATION`
- **static_capture_ready_now** = false
- **ocrrequest_eligible_now** = false，`ocrrequest_eligible_later` = true

## 边界

不 TTS、不 VOP、不 camera、不 OCR、不 OCRRequest。

## 前置

[LUNA_ASSISTED_STATIC_READING_MODE_V1.md](./LUNA_ASSISTED_STATIC_READING_MODE_V1.md)

## 实现

- `capabilities/midplatform/assisted_static_reading_runtime_dryrun_v1.py`
- `tools/evaluation/midplatform/run_assisted_static_reading_runtime_dryrun_v1.py`
- `tools/evaluation/midplatform/verify_assisted_static_reading_runtime_dryrun_v1.py`

## 评测

[LUNA_EVALUATION_ASSISTED_STATIC_READING_RUNTIME_DRYRUN_V1.md](../evaluation/LUNA_EVALUATION_ASSISTED_STATIC_READING_RUNTIME_DRYRUN_V1.md)

## 建议下一 phase

- 信息源定位策略：见 [LUNA_STATIC_READING_INFORMATION_SOURCE_LOCALIZATION_POLICY_V1.md](./LUNA_STATIC_READING_INFORMATION_SOURCE_LOCALIZATION_POLICY_V1.md)  
- `Static-Readable-Region-Discovery-Guidance-Policy-v1`（先于 Hardware-Camera-Control）

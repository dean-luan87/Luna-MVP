# Luna — Assisted Static Reading Mode v1

**Phase**：`Assisted-Static-Reading-Mode-v1-001`  
**性质**：模式 / 状态机 / 门槛策略定义（`mode_policy_only=true`）

## 目的

在动态 OCR / dynamic reading 失败后，定义 **Assisted Static Reading Mode**：

- 何时进入、用户如何配合、画面何时达标  
- OCRRequest **future gate**（本阶段不生成 OCRRequest）  
- 退出 / 降级 / 外援 / 过期长期候选  
- 未来结果链：static capture → OCR → EP → Semantic → Review  

## 当前 case

- **mode_entry_decision** = `ENTER_ASSISTED_STATIC_READING_CANDIDATE`  
- **first_guidance_action** = `hold_still`  
- **first_prompt_text** = 「请先停稳，保持画面稳定。」  
- v1_empty=30，v2_empty=5，same_bbox_risk=5，`internal_recrop_should_stop=true`

## 边界

不 TTS、不 VOP、不摄像头、不采帧、不 OCR、不 OCRRequest、不写事实层。

## 前置

- Voice Guidance 链（Template → Runtime → VOP Adapter）  
- User Guidance / Vision Capture Runtime DryRun  
- OCR Activation Governance  

## 实现

- `capabilities/midplatform/assisted_static_reading_mode_v1.py`  
- `tools/evaluation/midplatform/run_assisted_static_reading_mode_v1.py`  
- `tools/evaluation/midplatform/verify_assisted_static_reading_mode_v1.py`  

## 评测

[LUNA_EVALUATION_ASSISTED_STATIC_READING_MODE_V1.md](../evaluation/LUNA_EVALUATION_ASSISTED_STATIC_READING_MODE_V1.md)

## 建议下一 phase

- Runtime dry-run 已完成：见 [LUNA_ASSISTED_STATIC_READING_RUNTIME_DRYRUN_V1.md](./LUNA_ASSISTED_STATIC_READING_RUNTIME_DRYRUN_V1.md)  
- `Hardware-Camera-Control-Contract-v1`

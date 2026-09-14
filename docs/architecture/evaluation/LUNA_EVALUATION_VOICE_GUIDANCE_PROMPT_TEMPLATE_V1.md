# Luna Evaluation — Voice Guidance Prompt Template v1

**Phase**：`Voice-Guidance-Prompt-Template-v1-001`

## Smoke 输出根目录

`_eval_out/voice_guidance_prompt_template_v1_smoke_v0/`

## 运行

```bash
cd /Users/luanlei/Desktop/Luna-Workspace-Min
python3 tools/evaluation/midplatform/run_voice_guidance_prompt_template_v1.py \
  --output-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/voice_guidance_prompt_template_v1_smoke_v0 \
  --user-guidance-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/user_guidance_recovery_runtime_dryrun_v1_smoke_v0 \
  --vision-capture-runtime-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/vision_capture_runtime_dryrun_v1_smoke_v0 \
  --user-guidance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/user_guidance_recovery_policy_v1_smoke_v0 \
  --ocr-activation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/ocr_activation_governance_policy_v1_smoke_v0 \
  --stc-sampling-guidance-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/stc_sampling_guidance_policy_v1_smoke_v0 \
  --benchmark-smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/cross_modal_vision_ocr_benchmark_real_values_smoke_v0 \
  --system-health-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/system_health_center_governance_v0 \
  --simulation-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/simulation_lab_minimal_harness_v0/developer_full

python3 tools/evaluation/midplatform/verify_voice_guidance_prompt_template_v1.py \
  --smoke-root /Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/voice_guidance_prompt_template_v1_smoke_v0
```

## 输入 roots

- User Guidance Runtime DryRun  
- Vision Capture Runtime DryRun  
- User Guidance Recovery Policy  
- OCR Activation Governance  
- STC Sampling Guidance  
- Benchmark smoke / System Health / Simulation Lab  

## Verifier

`verify_voice_guidance_prompt_template_v1.py` — 65 项检查（缺失文件即 NO_GO）。

## GO pack

[LUNA_EVALUATION_VOICE_GUIDANCE_PROMPT_TEMPLATE_V1_GO_NO_GO_PACK_V0.md](./LUNA_EVALUATION_VOICE_GUIDANCE_PROMPT_TEMPLATE_V1_GO_NO_GO_PACK_V0.md)

# User verification

The Agent only performs static inspection and `git diff --check`. Run the controlled package from the canonical repository root:

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 -m capabilities.evaluation.perception_provider_runtime_target_preparation_controlled.runner_v1
python3 -m capabilities.evaluation.perception_provider_runtime_target_preparation_controlled.verifier_v1
```

Expected output directory:

`_eval_out/perception_provider_runtime_target_preparation_v1/`

The verifier distinguishes contract failures from behavioral observations. User terminal output is required before any phase decision.

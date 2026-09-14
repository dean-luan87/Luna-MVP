# User verification

从 repository root 执行：

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 -m capabilities.evaluation.provider_binding_to_runtime_allocation_controlled.runner_v1
python3 -m capabilities.evaluation.provider_binding_to_runtime_allocation_controlled.verifier_v1
```

Runner 输出：`_eval_out/provider_binding_to_runtime_allocation_v1/runner_summary_v1.json`。
Runner status 与 verifier final decision 分离；当前未取得用户终端结果前，不宣告 PASS、VERIFIED 或 GO。

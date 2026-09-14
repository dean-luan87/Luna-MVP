# User verification

从 canonical root 执行：

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 -m capabilities.evaluation.provider_binding_runtime_preparation_responsibility_controlled.runner_v1
python3 -m capabilities.evaluation.provider_binding_runtime_preparation_responsibility_controlled.verifier_v1
```

输出目录：

`_eval_out/provider_binding_runtime_preparation_responsibility_v1/`

Runner 只产生 controlled trace；Verifier 区分 contract failures 与 cognitive/ownership observations。未取得用户终端结果前，不作 PASS、VERIFIED 或 GO 判断。

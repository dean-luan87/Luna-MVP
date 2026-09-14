# User verification

从 canonical root 执行：

```bash
cd /Users/luanlei/Desktop/Luna-Core
python3 -m capabilities.evaluation.governance_verification_backbone_core_rules_controlled.runner_v1
python3 -m capabilities.evaluation.governance_verification_backbone_core_rules_controlled.verifier_v1
```

输出目录：`_eval_out/governance_verification_backbone_core_rules_v1/`。

Runner status 与 verifier final decision 分离；未取得用户终端结果前，不作 PASS、VERIFIED 或 GO 判断。

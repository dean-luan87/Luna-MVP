# User Terminal Verification

Agent 只执行静态编辑与 `git diff --check`，不运行 Python、Runner、Verifier 或
runtime。

在 canonical root `/Users/luanlei/Desktop/Luna-Core` 执行：

```bash
python3 -m capabilities.evaluation.observation_demand_controlled.runner_v1 \
  --output-root _eval_out/observation_demand_v1

python3 -m capabilities.evaluation.observation_demand_controlled.verifier_v1 \
  --smoke-root _eval_out/observation_demand_v1
```

Verifier 应分别确认 contract failures 与受控输入结果；在用户终端输出之前，
本阶段不能标记 PASS、VERIFIED 或 GO。

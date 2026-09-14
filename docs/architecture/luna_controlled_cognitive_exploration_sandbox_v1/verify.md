# User-Terminal Verification

Agent 不执行 Runner、Verifier 或 Python。请在 canonical root
`/Users/luanlei/Desktop/Luna-Core` 执行：

```bash
python -m capabilities.midplatform.sandbox.cognitive_exploration.run_cognitive_exploration_sandbox_v1
python -m capabilities.midplatform.sandbox.cognitive_exploration.verify_cognitive_exploration_sandbox_v1
```

执行后人工审阅：

```text
_eval_out/controlled_cognitive_exploration_sandbox_v1_smoke_v0/cognitive_trace.json
_eval_out/controlled_cognitive_exploration_sandbox_v1_smoke_v0/cognitive_trace_summary.md
```

Verifier 只检查 contract、schema、lineage、边界 markers、12 场景存在性、Round 1
来源与经济性字段；它不要求 Scenario 12 必须收敛。

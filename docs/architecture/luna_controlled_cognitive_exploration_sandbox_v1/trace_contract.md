# Cognitive Trace Contract

Runner 输出目录：
`_eval_out/controlled_cognitive_exploration_sandbox_v1_smoke_v0/`

核心文件：

- `cognitive_trace.json`
- `cognitive_trace_summary.md`
- `verification_report.json`（Verifier 执行后写入）

顶层 trace 保留：phase、sandbox version、synthetic-only marker、scenario count、
scenario traces、aggregate cognitive economy 与 negative guard summary。

每个 scenario 保留：metadata、Round 0、simulated return、Round 1（如有）、
cognitive delta、cognitive economy、lineage integrity、boundary observations 与
`cognitive_logic_observations`。

每个 round 保留：problem、required conditions、required condition candidates、
Information Need、Branch Formation result、Branch Governance result、Strategy
Formation result、各 candidate 对象及经济性指标。这样人工可以沿着：

```text
Problem → Need → Branch → Governance → Strategy
```

重建完整 lineage，而不只看到计数。

`cognitive_logic_observations` 不是 contract verdict。例如 Round 1 未出现 Branch
减少，只作为观察记录，不自动构成 phase failure。

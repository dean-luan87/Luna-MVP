# V1.6.0 - A3 收口 + B2 TTL 可观测与 A-route 审计封版

**发布日期**: 2026-03-03

## 封版范围

- **A3**：edge_multiplier=1.2 冻结，仅保留 `A3_EDGE_MULTIPLIER`；书面验收门槛见 tools/README_EXPERIMENTS.md 五.1。
- **B2 TTL**：telemetry 写入 trace（b2.ttl_expire、b2.advisory_suppressed、c1.motion）；v2 审计脚本双口径 + 门禁，以 Observed 为准。

## 验收

- A3：EDGE% 与 hit_rate（窗口 5/8）符合 README 五.1。
- B2 TTL：`python3 tools/analyze_b2_ttl_v2.py <trace> --processed-frames <N> --out <report.json>` 输出 PASS。

## 封版后建议

将 A-route 审计挂到每次跑 exp 的尾部，作为自动化健康证明；主线回到 A3/决策层迭代。

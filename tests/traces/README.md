# Trace 回归与门禁

- **B2 TTL override**：唯一验收入口为 `test_b2_ttl_override_gate.py`；运行命令与硬/软指标见 `tools/README_EXPERIMENTS.md` 中「B2 TTL override 封版口径」。
- **Baseline**：`baselines/b2_ttl_override_medium_long_01.json` 定义约束与 Soft 护栏下限；门禁读取该文件做回归校验。

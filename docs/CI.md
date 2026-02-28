# CI / Release Gate 规范

## Release Gate（Phase4）

一个版本可打 Tag，必须满足：

1. **指定发布 seed 集**（默认 42 / 123 / 777）
2. **每个 seed 使用 `--det 3`**
3. **满足以下条件**：
   - `determinism_pass == True`
   - `early_gain_mean ≥ 4.0`
   - `miss_rate == 0`
   - `overreact_rate < 0.60`
   - `champion_vol < 0.01`
4. **所有 seed overall == PASS（grade=release）**

### CI 行为

- 若 `reason_codes` 包含 **determinism** → 拒绝发布
- 若包含 **early_gain** / **miss_rate** / **overreact_rate** / **champion_vol** → 自动回滚到上一个稳定 tag
- **smoke 结果不参与 CI 阻断**

以上即「分层验证架构」：release 口径只认 det=3；smoke 口径只看行为指标。

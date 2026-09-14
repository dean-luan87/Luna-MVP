# Luna 架构文档 — Midplatform

> 说明：本 README 早期缺失；为便于长期工程化与索引收敛，在 Project Structure Governance 链路中补齐。

## 索引入口

- **总索引**：`docs/architecture/README.md`（包含 midplatform 详细条目）
- **评测索引**：`docs/architecture/evaluation/README.md`
- **Vision 索引**：`docs/architecture/vision/README.md`

## Midplatform 关注点（当前语义）

- **编排 / 任务上下文 / 感知工单**：把 vision/ocr/map/memory 的候选链路组织为可审计的 work-order 与反馈候选。
- **资源预算 / 隐私过滤 / 冲突修正**：作为中台的“保守默认”与跨域防线。
- **输入根治理**：明确跨 workspace 的输入根矩阵、验收合同与不可自升级原则。
- **Developer Backend 隔离**：runner/verifier/dashboard 属于开发后台，不进入 client runtime。

## 下一阶段提示（链路级）

当前主线已完成 **Project Structure Governance Planning** 与 **Structure Map DryRun**（7391 条资产归位表，含 `future_life_system_mapping`）。

推荐的下一 phase 为：

- `Phase-Protected-Asset-and-Human-Review-Resolution-Post-DryRun-Review-v1-001`


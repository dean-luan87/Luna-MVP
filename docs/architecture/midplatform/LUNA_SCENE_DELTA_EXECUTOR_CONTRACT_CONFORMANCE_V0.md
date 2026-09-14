# Luna MidPlatform — Scene Delta Executor Contract Conformance v0

**Phase**: `Phase-MidPlatform-Scene-Delta-Executor-Contract-Conformance-001`

## 目的

将 **mock executor request / ACK** 与 **`scene_delta_executor_contract_skeleton_v0`** 做 **静态 conformance**：请求/ACK **字段矩阵**、**缺口报告**、**no-write 合同检查** 与 **conformance audit**。用于在接入 **真实 Scene Delta executor 合同**（OpenAPI / proto / DTO）前，先在仓库内固定 **最小必填字段集** 与 **no-write 禁止项**。

## 合同参考模式

当前默认 **`contract_reference_mode=local_skeleton`**：**不**声称已与生产 executor 合同对齐；未来接入真实合同后须 **重新跑** 本 phase 并更新 `contract_reference_mode`。

## 边界

- **不**调用真实 executor；**不**写 Scene Delta；**不**落库；**不**写 rehearsal log / WAL；**不**写 MidPlatform 事实 / WorldModel；**不**调用 AI / OCR provider；**不**改 OCR routing。

## 评测入口

见 [LUNA_EVALUATION_SCENE_DELTA_EXECUTOR_CONTRACT_CONFORMANCE_V0.md](../evaluation/LUNA_EVALUATION_SCENE_DELTA_EXECUTOR_CONTRACT_CONFORMANCE_V0.md)。

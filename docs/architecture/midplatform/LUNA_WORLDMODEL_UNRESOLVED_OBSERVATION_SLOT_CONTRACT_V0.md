# Luna — WorldModel Unresolved Observation Slot Contract v0

**Phase**：`Phase-WorldModel-Unresolved-Observation-Slot-Contract-001`

## 架构原则

现实环境中存在「有内容，但当前 OCR/视觉未能识别」的区域。系统**不应丢弃**，也**不应强行解释**。世界模型允许预留 **未知/未解析槽位**，绑定时空坐标、图像坐标、来源链、置信度、可读性、未识别原因，并在未来观察中补齐。

OCR 角色随世界模型成熟度变化：

1. **bootstrap**：视角 + OCR 发现环境  
2. **established_environment**：验证 / 补全 / 变更检测  
3. **maintenance**：仅在变化、冲突、低置信、TTL 过期时触发  

## 目的

定义 `worldmodel_unresolved_observation_slot_v0` 合同（schema / policy / examples / gate）。

## 边界

- **允许**：schema、类型注册、触发矩阵、填补政策、示例、生命周期、no-write 报告  
- **禁止**：WorldModel 写入、runtime slot 实例、OCR/Vision 运行、Scene Delta、fact、导航、routing  

## 实现

- Capability：`capabilities/midplatform/worldmodel_unresolved_observation_slot_contract_v0.py`
- Runner：`tools/evaluation/midplatform/run_worldmodel_unresolved_observation_slot_contract_v0.py`
- Verifier：`tools/evaluation/midplatform/verify_worldmodel_unresolved_observation_slot_contract_v0.py`

## 评测

[LUNA_EVALUATION_WORLDMODEL_UNRESOLVED_OBSERVATION_SLOT_CONTRACT_V0.md](../evaluation/LUNA_EVALUATION_WORLDMODEL_UNRESOLVED_OBSERVATION_SLOT_CONTRACT_V0.md)

## 建议下一跳

**Unresolved Slot dry-run from OCR Evidence Pack** + SourceQualityGate 集成。

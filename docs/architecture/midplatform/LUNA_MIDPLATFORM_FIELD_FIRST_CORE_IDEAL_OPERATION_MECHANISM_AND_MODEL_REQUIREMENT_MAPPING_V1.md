# Luna Midplatform — Field-First Ideal Operation Mechanism & Model Requirement Mapping v1

## Phase

`Phase-Midplatform-Field-First-Core-Ideal-Operation-Mechanism-and-Model-Requirement-Mapping-v1-001`

## 为什么需要本阶段

前序已完成岗位重定义和初步模型房间思路，但缺少：
- 理想状态下的完整运作逻辑
- 每个运作节点需要什么能力
- 模型应满足什么输入/输出/频率/置信度/追溯要求
- 如何用这些要求反查模型文档

**正确顺序：** 先定义 Luna 要什么能力 → 再判断模型是否满足（不是先看模型有什么能力就拿来用）

## 理想运作机制（13 步）

Frontend Sensing → Source Adapter → Source Basket → Observation Normalization → Field Model Construction → Field State Continuity → Field Boundary Control → Field Simulation → Task Field View → Midplatform Field Reasoning → Drive Layer → Perception Request → Field Update Loop

## 运作节点（12）

| 节点 | 主要自研 vs 模型依赖 |
|------|---------------------|
| Frontend Sensing | 模型高依赖（观测层） |
| Visual / OCR / Speech | 模型高依赖（adapter 输出 candidate） |
| Spatial / SLAM / Scene Graph | Kimera/Hydra 结构参考，不强制 runtime |
| ECS / Semantic Graph | Luna 自研 skeleton，Esper/NetworkX 参考 |
| Boundary / Continuity | **Luna 自研为主** |
| Field Simulation | **Luna 自研规则/几何/状态机** |
| Task Field View | **Luna 自研为主** |
| Midplatform Reasoning | 结构化自研 + LLM 解释 |
| Drive Layer | **Luna 自研为主** |

## 模型需求矩阵

每个运作节点生成 requirement matrix（16 字段）：required_capability, expected_output_candidate, latency, confidence, traceability, safety_critical, can_be_reference_only, must_have_now, can_defer 等。

## 模型文档检查模板（下阶段使用）

20 字段模板 + 6 种 recommended_status（reference_only / candidate_for_future_adapter / unsuitable_for_phase_1 等）

## Next Phase

`Phase-Midplatform-Field-First-Core-Model-Document-Capability-Review-v1-001`

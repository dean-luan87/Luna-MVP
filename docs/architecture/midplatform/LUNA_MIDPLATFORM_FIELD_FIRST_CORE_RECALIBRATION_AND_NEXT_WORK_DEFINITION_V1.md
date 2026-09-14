# Luna Midplatform — Field-First Core Recalibration and Next Work Definition v1

## Phase

`Phase-Midplatform-Field-First-Core-Recalibration-and-Next-Work-Definition-v1-001`

## Core Route Adjustment

**旧路线：** 多源信息 → Information Processing Core → 中台模型直接理解信息 → 候选判断

**新路线：** 多源信息 → Source Adapter / Source Basket → Unified Observation Candidate → Field Model → Field Simulation → Task Field View / Simulation Result → Midplatform Reasoning Candidate

**关键变化：** 中台模型不直接理解原始世界，而理解经场模型组织、场推演后的结构化结果。

## Field-First Concepts

- **世界模型：** 长期、跨场景、相对稳定的对象/地点/规则/关系/历史/模式库
- **场模型：** 当前时间窗口、空间范围、用户状态、任务目标下的局部世界状态
- **中台核心 Phase 1：** 建场、更新场、推演场、生成任务视图、输出候选推理结果

## Field Model Layers

1. **ECS Layer** — 实体、组件、属性、状态
2. **Dynamic Scene Graph Layer** — 空间/时间/可达/遮挡/阻挡关系
3. **Lightweight Semantic / Event Graph Layer** — 事件语义、风险、规则、任务含义

## IPC Repositioning

IPC 保留为支持角色（observation normalization upstream of field），**不删除、不 invalidate**，但不再是直接中心。

## Deferred (Peripheral Not Prematurely Fixed)

- Candidate Lifecycle Manager
- Module Handoff Contract (P3 defer)
- Integration test / runtime / full world model

## Next Phase

`Phase-Midplatform-Field-First-Core-Work-Manual-and-Architecture-Definition-v1-001`

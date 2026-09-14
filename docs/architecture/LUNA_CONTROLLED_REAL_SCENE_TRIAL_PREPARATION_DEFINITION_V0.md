# Phase-RealScenePrep-001 — Controlled Real Scene Trial Preparation Definition v0（前置定义冻结）

**阶段名**：Phase-RealScenePrep-001  
**性质**：受控真实场景试验的“准入宪法”（前置开发定义）；不执行真实试验。  

---

## 0) 明确声明（硬边界，写死）

- 本阶段不是开放真实用户测试  
- 不是 full controlled trial  
- 不是产品发布/商业化验收  
- 不是真实大范围试运行  
- 不开启默认路径（no default-on）  
- 不扩大真实 side effects 面（candidate-only）  
- 不让模型拿执行权  
- 不让输出候选变成真实执行  
- 不新增长尾场景  
- 本阶段只做“定义/护栏/观测/回放/中止/证据要求”冻结，不做 execution  

一句话：RealScenePrep-001 是真实场景试验的**准入宪法**，不是实际试验。

---

## 1) 唯一目标

冻结“受控真实场景试验前置开发”的定义与硬边界，明确进入真实环境输入前必须满足：
- 非默认显式入口
- candidate-only
- no execute leakage
- no default-on
- no side effects expansion
- trace/replay/whitebox 完整
- fallback/degraded 可用
- 人工可中止
- timebox 受控
- scope 受控

---

## 2) 输入前提（已成立事实）

- Governance 主链已收口
- Model-001/002 已完成；Model-003 为 conditional_go
- Perception-001 / SceneTask-001 / Fusion-001 / Expression-001 / Device-001 已成立（go）
- Productization-000：MVP System Readiness Review = conditional_go
- 默认路径仍未开启；full controlled trial 未进入；未扩大 side effects；未开放用户测试

---

## 3) 本阶段范围（仅冻结 6 类文档）

1. scope & boundary（首轮极窄范围）
2. entry checklist（进入 execution 前必须满足）
3. abort / fallback / rollback / degraded policy（触发器与后置动作）
4. observability & evidence contract（trace/replay/whitebox/operator notes/断言）
5. operator runbook（如何启动/观察/中止/归档一次受控试验）
6. go/no-go pack（是否允许进入 RealSceneTrial-001 的结论）

---

## 4) 完成指标（最小）

- scope/boundary 已冻结且“极窄、可执行、可审计”
- checklist 已冻结且可用于 gate
- abort/fallback/rollback policy 已冻结且“可中止、可降级、可归档”
- observability contract 已冻结且包含三条硬断言：
  - `no_execute_leakage`
  - `no_default_on`
  - `no_side_effect_expansion`
- operator runbook 已冻结
- go/no-go pack 已冻结并给出结论

---

## 5) 停止条件（满足即停止）

- preparation definition 已完成（本文）
- scope/boundary 已完成
- entry checklist 已完成
- abort/fallback/rollback policy 已完成
- observability contract 已完成
- operator runbook 已完成
- go/no-go pack 已完成
- 给出是否进入 RealSceneTrial-001 的结论

不得顺手做 RealSceneTrial-001。


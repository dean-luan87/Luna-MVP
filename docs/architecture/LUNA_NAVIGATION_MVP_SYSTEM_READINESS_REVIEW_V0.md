# Phase-Productization-000 — Navigation MVP System Readiness Review v0（系统级就绪复盘冻结）

**阶段名**：Phase-Productization-000  
**性质**：系统级 readiness review（工程盘点）；不新增核心 runtime；不进入开放测试。  

---

## 0) 明确声明（硬边界，写死）

- 默认路径仍未开启（no default-on）
- 本阶段未进入 full controlled trial
- 本阶段未扩大真实 side effects 面
- 本阶段未进入开放真实用户测试
- Device-001 GO 仅说明“最小闭环能跑”，不等于产品发布资格
- 本阶段只做系统 readiness review，不新增核心 runtime

---

## 1) 已成立事实（证据来源）

- Governance 主链已收口（Phase-Closure-001）
- Phase-Model-001：模型接入定义冻结
- Phase-Model-002：单模型 shadow integration 完成
- Phase-Model-003：model shadow admission baseline = conditional_go
- Phase-Perception-001：navigation perception baseline = go
- Phase-SceneTask-001：4 核心场景 × 任务链 integration = go
- Phase-Fusion-001：Map × Vision × Memory fusion = go
- Phase-Expression-001：Navigation Output & Timing Control = go
- Phase-Device-001：On-Device Closed-Loop Validation = go

---

## 2) 当前系统已完成的最小工程闭环（MVP v0）

链路闭环已完成（v0 级）：

治理 → 模型 shadow → 感知 → 场景任务 → 融合 → 输出 → 设备闭环

并且关键红线成立：
- candidate-only integrity：输出候选写死 `allows_execute_now=false`
- no execute/release/retry/reopen leakage（验证工具链覆盖）
- no default-on（设备运行模式 contract 写死显式开启）
- trace/replay/whitebox 最低要求已冻结并可被验证工具检查
- degraded/fallback 作为设备闭环的一部分被纳入验证范围

---

## 3) 哪些能力只是 v0 / placeholder / mock（不得误判为产品级）

必须显式承认仍为 v0 或 placeholder 的方面：
- Model-003 为 conditional_go：候选质量与抗探针能力仍需提升
- Perception-001 是 baseline：不等于产品级感知覆盖（弱光/抖动/长时稳定/隐私等仍为 placeholder）
- Fusion-001 地图/记忆可为 mock/minimal：真实地图更新、离线地图、记忆污染治理等未产品化
- Device-001 主要依赖 fixture/replay 或受控输入：不等于开放真实环境验证
- 性能/功耗/发热/声学/离线/隐私/远程诊断等工业级要求仍为 placeholder（不阻塞但必须追踪）

---

## 4) 下一阶段前置必须处理的问题（进入受控真实场景前置开发）

本阶段不实现，但必须在下一阶段（受控真实场景试验前置开发）明确推进方向：
- controlled_live_input 的专项验证计划与护栏（短时、显式、可回放、可中止）
- 真实连续摄像头输入下的 trace/replay 性能与落盘策略（只要求“可记录”，不要求最终阈值）
- 模型 shadow 输出质量的再评估路径（仍保持 candidate-only）
- 工业级 placeholder 按 planned_phase 落地，不得被“Device-001 GO”掩盖

---

## 5) 系统级 readiness 结论（本阶段结论）

### 结论：**CONDITIONAL_GO**

**允许进入**下一阶段：**受控真实场景试验前置开发**（仅前置定义与护栏工程，不开放用户测试）。  

**前提**：保持以下红线不变：
- no execute leakage
- no default-on
- no side effects expansion
- trace/replay/whitebox 必须可追踪可复现
- degraded/fallback 必须成立

**为什么不是 GO**（写死原因）：
- Model-003 仍为 conditional_go
- Device-001 的“真机闭环”仍主要基于 fixture/replay/受控输入，未覆盖开放真实环境的不确定性

---

## 6) 交付物索引（本阶段）

- readiness review：`docs/architecture/LUNA_NAVIGATION_MVP_SYSTEM_READINESS_REVIEW_V0.md`
- capability maturity matrix：`docs/architecture/LUNA_NAVIGATION_MVP_CAPABILITY_MATURITY_MATRIX_V0.md`
- risk & gap register：`docs/architecture/LUNA_NAVIGATION_MVP_RISK_AND_GAP_REGISTER_V0.md`
- next phase entry definition：`docs/architecture/LUNA_CONTROLLED_REAL_SCENE_TRIAL_PREPARATION_ENTRY_DEFINITION_V0.md`


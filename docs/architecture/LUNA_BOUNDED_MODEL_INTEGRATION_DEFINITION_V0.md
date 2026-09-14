# Phase-Model-001 — Navigation Governance Bounded Model Integration Definition v0（宪法冻结）

**阶段名**：Phase-Model-001  
**性质**：Model Integration Definition Freeze（宪法）；不是模型接入实现；不接入模型 runtime  
**硬边界**：不启用默认路径；不扩大真实 side effects 面；不让模型拿执行权；不把模型输出接到 execute/retry/reopen/release；不修改已冻结治理宪法与收口结论  

---

## A. 背景与治理收口结论引用（只引用，不改写）

已成立事实（冻结）：
- 治理主链已在 184 收口（Phase-Closure-001 已完成）
- `Model Integration Entry Definition` 与 `Model Integration Contract` 已存在并冻结
- 默认路径仍未开启
- full controlled trial 仍未开始
- 真实 side effects 面未扩大

引用入口与契约（已存在）：
- `docs/architecture/LUNA_MODEL_INTEGRATION_ENTRY_DEFINITION_V0.md`
- `docs/architecture/LUNA_MODEL_INTEGRATION_CONTRACT_V0.md`

---

## B. 本阶段适用范围（Scope）

本阶段只定义并冻结：
- 模型如何以**受限、可审计、可回放、可禁用、不可放权**方式进入系统（bounded model integration）
- 模型唯一角色集合（candidate / draft / comparator-assist）
- 模型输入边界（可见/不可见）
- 模型输出边界（允许/禁止）
- 模型输出如何被系统消费（只能作为候选证据，不反向控制系统）
- 后续实现的 **no-go 条件** 与必须遵守的 contract

---

## C. 明确排除项（Non-Goals）

本阶段不做：
- 不新增模型 runtime 主实现（不接入真实模型）
- 不做多模型调度/并行策略
- 不做模型裁决权/执行权
- 不做自动执行链路接入（execute/retry/reopen/release）
- 不改变既有治理宪法：started/release/closure/closed-safe/no-next-runtime-now
- 不启用 default path

---

## D. “bounded model integration” 的定义（写死）

**Bounded Model Integration（v0）**：模型以 shadow/candidate 形态进入系统，仅能输出结构化候选信息（candidate/draft/comparison/score），并且满足：
- 可审计（audit）
- 可回放（replay）
- 可禁用（disable）
- 可降级/回退到无模型基线（rollback-to-baseline）
- 永远不拥有执行权、不打开 release window、不触发任何真实 side effects

一句话：**模型接入 != 模型放权**。

---

## E. 模型接入的唯一进入条件（唯一入口）

模型接入（v0）只能通过以下入口进入：
- **显式入口（non-default entry）**，由受控流程触发（人工/治理链外部显式动作）

入口前置必须成立：
- 系统处于 closed-safe（闭合安全态）
- default path disabled（默认路径仍未开启）
- 不进入 full controlled trial
- 不扩大真实 side effects 面
- 模型接入处于 shadow/candidate-only 模式

---

## F. 模型角色定义（写死允许角色）

允许角色（可单独或组合）：

### 1) candidate model
- **允许**：输出候选判断（candidate recommendation）
- **禁止**：拿执行权、触发 runtime、触发 side effects

### 2) draft model
- **允许**：输出解释草稿/结构补全/候选理由（draft_explanation）
- **禁止**：拿执行权、触发 runtime

### 3) comparator-assist model
- **允许**：输出候选比较/排序辅助/评分辅助（comparison_hint / score）
- **禁止**：拿执行权、触发 runtime

禁止新增角色（v0 硬禁止）：
- execution model
- autonomous runtime model
- model-as-controller

---

## G. 模型输入边界（输入策略引用）

模型输入边界在 v0 必须冻结，并作为后续实现硬契约：
- 详见：`docs/architecture/LUNA_MODEL_INPUT_BOUNDARY_AND_CONTEXT_POLICY_V0.md`

---

## H. 模型输出边界（输出契约与 schema 引用）

模型输出 contract 与 candidate schema 在 v0 必须冻结，并作为后续实现硬契约：
- 详见：`docs/architecture/LUNA_MODEL_OUTPUT_CONTRACT_AND_CANDIDATE_SCHEMA_V0.md`

---

## I. 模型接入与治理链的关系（单向消费）

写死关系：
- 模型输出只能作为 **候选证据/候选建议** 被治理链/任务链消费
- 模型输出不得直接改变治理结论
- 模型输出不得直接触发任何真实执行链（execute/retry/reopen）
- 模型输出不得直接打开 release window 或 side effects 放权
- 任何“使用模型输出影响系统行为”的路径必须先经过既有治理宪法与显式门控（不在本阶段定义实现）

---

## J. shadow / candidate 模式定义（写死）

**Shadow mode**：
- 模型输出被记录、审计、回放、对比
- 不影响主链治理结论与执行链

**Candidate mode**：
- 模型输出以结构化 candidate schema 输出
- 作为候选供后续模块选择/对比，但不具有执行语义

---

## K. 禁止事项（Hard Denylist）

模型接入阶段绝对禁止：
- `execute_now` / `retry_now` / `reopen_now`
- `open_release_window`
- `enable_default_path`
- `override_governance` / `grant_control`
- `long_running_enablement`
- 任何绕过 started/release/closure 的路径
- 任何扩大真实 side effects 面的行为
- 默认路径接入（default-on）

---

## L. 后续实现必须遵守的 contract（v0）

后续 Phase-Model-002（实现）必须遵守：
- 仅 1 个模型接入
- 仅 shadow/candidate-only
- 输出必须满足统一 schema（可解析、可审计、可回放）
- 必须可禁用、可回退到无模型基线
- 模型不得直接触发真实 side effects / execute/retry/reopen / release
- 模型不得看到禁止输入字段（见输入边界策略）

---

## M. 验收标准（停止条件）

本阶段完成必须同时满足：
1. 角色冻结：仅 candidate/draft/comparator-assist（无执行权）  
2. 输入边界冻结：可见/不可见/不可修改字段写死  
3. 输出边界冻结：允许/禁止输出类型写死 + schema 冻结  
4. audit/replay/disable/rollback-to-baseline 要求写死  
5. 禁止事项写死 + 后续实现 no-go 条件写死  

满足以上即停止，不提前进入实现阶段。

---

## recommended next phase

**Phase-Model-002：Single Model Shadow Integration Implementation v0**

---

## 明确声明

- 默认路径仍未开启  
- 本阶段未进入 full controlled trial  
- 本阶段未扩大真实 side effects 面  
- 本阶段未接入真实模型 runtime  
- 本阶段只冻结 bounded model integration definition，不做 implementation  


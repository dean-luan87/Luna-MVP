# Phase-Closure-001 — Model Integration Entry Definition v0（模型接入主线唯一入口：定义冻结）

**目的**：定义“从治理主链进入模型接入主线”的唯一入口与硬边界。  
**性质**：入口定义（definition）；不接入模型 runtime；不新增治理 runtime；不修改 151–184 冻结结论。  

---

## 1) 一句话定义（写死）

**模型接入 != 模型放权**。  
模型接入第一阶段只能以 **shadow / candidate** 方式接入，模型输出只能作为“候选判断”，不得直接拥有执行权或触发真实动作。

---

## 2) 唯一入口（Entry）

模型接入主线的唯一入口定义为：
- **显式入口**（non-default entry），由治理主链外部显式触发（人工/受控流程），不得由默认路径或隐式链条触发。

入口前置条件必须全部满足：
- 治理主链已封顶收口（以 184 为封顶可执行点；停止 185/186… 递归）
- default path disabled（默认路径仍未开启）
- closed-safe state 为真（系统处于闭合安全态）
- 不进入 full controlled trial
- 不扩大真实 side effects 面

---

## 3) 模型接入阶段的硬约束（必须 obey）

模型接入必须继承并 obey 以下硬约束：
- 不得绕过 started/release/closure（151）
- 不得绕过 short-window guardrail（155）
- 不得扩大真实 side effects 面（类别/范围/频率/时长）
- 不得开启默认路径（default-on 禁止）
- 不得隐式 reopen/retry/widen/long-running
- 不得直接触发 real execute / retry / reopen
- 不得打开 release window
- 必须可审计、可回放、可禁用（kill-switch）

---

## 4) 模型接入的最小输出形态（Candidate-Only）

模型在接入阶段（v0）只允许输出：
- 候选判断（candidate recommendation）
- 候选理由（reasoning / reason codes，结构化）
- 候选证据引用（evidence pointers）
- 置信度/不确定性声明

模型输出 **不得**：
- 直接改变治理结论
- 直接改变系统状态
- 直接调用任何真实执行接口
- 直接改变 default path / side_effects 状态

---

## 5) Shadow Mode（强制）

模型接入第一阶段必须是：
- **shadow mode**：模型输出被记录、审计、对比，但不影响主链决策与执行。

只有在后续独立的“模型接入 definition + validation + go/no-go pack”链条完成后，才允许考虑更进一步的控制权变化（不在本阶段）。

---

## 6) recommended next phase（新主线）

**recommended_next_phase**：
- Phase-Model-001 — Navigation Governance Bounded Model Integration Definition v0

---

## 7) 明确声明

- 默认路径仍未开启  
- 本阶段未进入 full controlled trial  
- 本阶段未扩大真实 side effects 面  
- 本阶段不再继续递归治理层  
- 本阶段只定义模型接入入口，不接入模型 runtime  


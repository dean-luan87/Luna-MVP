# Phase-Closure-001 — Model Integration Contract v0（模型接入契约冻结）

**目的**：把“模型接入”在治理主链封顶后的可执行契约写死，确保模型只能以 shadow/candidate 方式接入，且永远不能绕过治理宪法与硬门控。  
**性质**：契约（contract）；不接入模型 runtime；不新增治理 runtime；不修改 151–184 冻结结论。  

---

## 1) 角色边界（写死）

- **模型（Model）**：只输出候选（candidate），无执行权、无放权能力、无默认入口能力。  
- **治理链（Governance Chain）**：唯一可以产出治理结论与放行门控的链条；模型输出只能作为输入证据的一部分。  
- **执行器（Executor / Real Action）**：只能在既有治理宪法与明确放行条件满足时运行；模型不得直接调用。  

---

## 2) Candidate-Only 约束

模型输出被严格限制为：
- 候选结论（recommendation）
- 候选理由（reason codes / explanation）
- 候选证据引用（evidence pointers）
- 置信度与不确定性声明

模型输出严格禁止包含：
- 任何“直接执行/触发执行”的指令
- 任何“打开 release window / 放行 side effects”的指令
- 任何“默认路径开启 / default-on”的指令
- 任何“隐式 retry/reopen/widen/long-running”的建议被当作自动动作

---

## 3) 继承治理宪法（不可绕过）

模型接入后仍必须 obey：
- started/release/closure（151）与其唯一 started 判据
- short-window guardrail（155）与其 allow/deny/abort policy
- 默认路径禁用（default path disabled）
- 禁止扩大真实 side effects 面（类别/范围/频率/时长）
- 禁止隐式 reopen/retry/widen/long-running/default-on
- closed-safe 强制保持
- 治理层 `allows_next_runtime_now=false`（不得自动推进任何下一 runtime）
- 不进入 full controlled trial（除非未来新定义与治理批准）

---

## 4) Shadow Mode / Audit / Replay（强制能力）

模型接入必须支持以下能力（v0 必须具备）：
- **Shadow mode**：模型输出不影响治理结论与执行链
- **Audit log**：结构化记录每次模型输入、输出、版本、提示与上下文摘要（可脱敏）
- **Replay**：可在相同输入下复现模型输出（允许非确定性但必须记录随机性/版本）
- **Disable / Kill-switch**：一键禁用模型路径，系统回到“无模型参与”的安全状态

---

## 5) 不得越权的硬禁止项（Hard Denylist）

模型接入阶段，以下属于绝对禁止（发现即视为 blocker）：
- 模型输出被当作治理结论直接消费（绕过治理链）
- 模型直接触发 real execute / retry / reopen
- 模型直接打开任何 release window 或 side effects 放权
- 模型导致 default path 误触发或被启用
- 模型导致隐式 long-running enablement
- 模型导致任何真实副作用面扩大

---

## 6) 与 rollback/disable 的关系

模型接入必须可被随时禁用，并满足：
- 禁用模型不改变既有治理链结论
- 禁用模型后系统仍保持 closed-safe
- 禁用动作不触发真实执行链与副作用窗口

---

## 7) 与“模型放权”明确切割

本 contract 明确声明：
- **模型接入 != 模型放权**
- 任何“模型获得控制权/执行权”的讨论必须在未来新主线（Phase-Model 系列）下完成 definition → validation → pack 的独立闭环后才可进入，且不在本阶段范围内。

---

## 8) 明确声明

- 默认路径仍未开启  
- 本阶段未进入 full controlled trial  
- 本阶段未扩大真实 side effects 面  
- 本阶段不再继续递归治理层  
- 本阶段只冻结模型接入契约，不接入模型 runtime  


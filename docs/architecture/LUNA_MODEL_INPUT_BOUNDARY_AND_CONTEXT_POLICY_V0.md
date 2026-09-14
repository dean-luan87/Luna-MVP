# Phase-Model-001 — Model Input Boundary And Context Policy v0（输入边界冻结）

**目的**：冻结模型可读取的上下文范围，以及绝对禁止暴露给模型的治理/主权/控制字段，防止模型获得绕过治理的系统状态。  
**性质**：policy；不接入模型 runtime；不修改治理宪法。  

---

## 1) 原则（写死）

- 最小可见（least-privilege）：只给模型完成候选输出所需的**摘要**信息。
- 不给控制权线索：禁止暴露任何可能让模型推断“如何绕过治理/如何打开开关”的内部控制位。
- 不给可变更面：模型输入必须只读，且不可包含可被模型“指令化修改”的字段。

---

## 2) 允许输入（Allowed Inputs，示例集合）

允许输入必须是 **受限摘要**（禁止原始控制对象直出）：
- 场景描述摘要（文本）
- 感知结果摘要（结构化摘要，不含底层控制字段）
- 任务状态摘要（例如任务阶段、目标、已完成子步骤摘要）
- 历史候选对比摘要（只含候选结果与评分，不含控制位）
- 用户相关**非敏感**导航上下文（按既有系统隐私规则脱敏/裁剪）
- 安全风险提示摘要（“有什么风险”，不含“如何解除风险门控”的控制字段）

---

## 3) 禁止输入（Forbidden Inputs，硬黑名单）

以下属于绝对禁止输入（任一出现即为后续实现 no-go 触发）：

### 3.1 主权/控制字段（Sovereignty & Control）
- 任何 “grant_control / override / admin / superuser / manual_override_token” 类型字段
- 任何可以直接触发执行器或改变执行路径的控制开关

### 3.2 release window / side effects 控制字段
- `side_effects_released`、release window 状态、任何“放权/开窗”控制位
- 任何与真实写入/真实执行副作用放行相关的 gate 状态或 token

### 3.3 started 判据与治理内部裁决字段
- started 判据内部控制位（例如 start_event_observed 的内部判定细节/控制位）
- 治理裁决权限位、go/no-go gate 内部状态、可触发下一 runtime 的内部标志

### 3.4 default-on / 路径启用字段
- 任何可启用默认路径的开关/配置
- 任何“自动继续运行/自动重试/自动 reopen”的策略字段

### 3.5 绕过治理的内部策略/提示
- 内部 guardrail 详细参数（可被模型用来推断绕过策略）
- 任何“如果要绕过该门控应该怎么做”的内部 runbook 细节

---

## 4) 输入结构要求（必须可审计）

每次模型调用输入必须具备：
- 版本号（policy_version）
- 脱敏/裁剪标记（redaction_summary）
- 输入字段清单（field_manifest）
- 输入来源摘要（source_summary）

并且必须能证明：未包含 Forbidden Inputs 类别。

---

## 5) 与后续实现的硬契约（Phase-Model-002 必须 obey）

- 输入必须通过 “forbidden-field filter”（逻辑由实现提供，但本 policy 写死禁止项）
- 输入必须是摘要/裁剪后的内容，不得直出治理内部控制结构
- 任一 forbidden 字段泄漏：必须判定 no-go 并触发 kill-switch 回退到无模型基线

---

## 6) 明确声明

- 默认路径仍未开启  
- 本阶段未进入 full controlled trial  
- 本阶段未扩大真实 side effects 面  
- 本阶段未接入真实模型 runtime  
- 本文件只冻结输入边界策略，不做实现  


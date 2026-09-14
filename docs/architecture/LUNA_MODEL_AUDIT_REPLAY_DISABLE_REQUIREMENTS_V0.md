# Phase-Model-001 — Model Audit / Replay / Disable Requirements v0（审计/回放/禁用/回退冻结）

**目的**：写死模型接入后必须具备的控制面能力：audit、replay、disable、rollback-to-baseline，防止模型接入后不可控。  
**性质**：requirements；不接入模型 runtime；不新增治理 runtime。  

---

## 1) 必须具备的能力（v0 写死）

### 1.1 Audit（可审计）

必须记录并可查询：
- 每次模型请求的 `request_id`
- 输入摘要与来源摘要（不得泄漏 forbidden inputs）
- `input_hash` / `prompt_hash`
- 模型标识：`model_id` / `model_version`
- 输出全文（严格 JSON）与解析结果
- policy 版本：`policy_version`
- 任何解析警告/字段缺失/拒绝原因

审计数据必须：
- 结构化（可机器检索）
- 可脱敏（遵守隐私与安全裁剪）

### 1.2 Replay（可回放）

必须支持：
- 基于 `request_id` 拉取输入摘要与输出，复现“当时模型给了什么候选”
- 基于 `input_hash`/`prompt_hash` 做一致性回放对比（允许模型非确定性，但必须记录版本与上下文）

### 1.3 Disable（可禁用 / kill-switch）

必须支持：
- 一键禁用模型路径（逻辑禁用即可，不需要卸载模型）
- 禁用后系统回到“无模型参与”的基线行为
- 禁用动作不得触发真实 side effects，不得改变治理结论

### 1.4 Rollback-to-baseline（可回退到无模型基线）

必须支持：
- 模型异常/不合规/输出不可解析时，自动回退到无模型基线（fallback）
- fallback 必须保持 closed-safe 与非默认路径原则，不得触发 execute/retry/reopen/release

---

## 2) 最小实现要求（供 Phase-Model-002 使用，但本阶段不实现）

Phase-Model-002 的最小实现必须具备：
- 统一日志落点（whitebox trace）
- replay 读取路径（按 request_id）
- kill-switch 配置开关（默认关闭/可立即关闭）
- fallback 策略（模型失败不影响治理链）

---

## 3) no-go 条件（对后续实现的硬判据）

后续 Phase-Model-002 只要出现任一，即必须 no-go：
- 输出不可审计（缺 request_id / model_id / hashes / policy_version）
- 输出不可回放（无法按 request_id 复现）
- 模型不可禁用（kill-switch 无效或禁用仍影响系统）
- 模型失败破坏无模型基线（fallback 不成立）
- 禁用/回退动作触发任何真实 side effects 或改变治理结论

---

## 4) 与 default-on / full controlled trial / real side effects 的边界（写死）

- 模型接入不得开启默认路径（default-on 禁止）
- 模型接入不得进入 full controlled trial
- 模型接入不得扩大真实 side effects 面
- 模型接入不得打开 release window
- 模型接入不得触发 execute/retry/reopen

---

## 5) 明确声明

- 默认路径仍未开启  
- 本阶段未进入 full controlled trial  
- 本阶段未扩大真实 side effects 面  
- 本阶段未接入真实模型 runtime  
- 本文件只冻结 requirements，不做实现  


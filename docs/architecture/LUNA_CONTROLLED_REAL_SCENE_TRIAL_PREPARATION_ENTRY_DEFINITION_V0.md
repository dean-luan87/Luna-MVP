# Phase-Productization-000 — Controlled Real Scene Trial Preparation Entry Definition v0（下一阶段唯一入口定义冻结）

**目的**：定义下一阶段“受控真实场景试验前置开发”的唯一入口与边界。  
**强调**：这不是开放用户测试；不是 full controlled trial；不扩大 side effects；不启用默认路径。  

---

## 1) 入口名称与性质（写死）

- **入口名称**：`Phase-RealScenePrep-001`（建议名；本文件只定义入口，不执行下一阶段）
- **入口性质**：受控真实场景试验的前置开发（定义/护栏/观测/回放能力增强），仍保持 candidate-only

---

## 2) 硬前提（必须满足才允许进入）

必须同时满足：
- 最小闭环完整（Device-001 = go）
- `execute/release/retry/reopen leakage = 0`
- `default_on_trigger_count = 0`
- 默认路径仍未开启（no default-on）
- 不扩大真实 side effects 面（candidate-only）
- trace/replay/whitebox 完整（可追踪、可回放、可复现）
- fallback/degraded 成立（可中止、可回退、可保守）
- 风险与缺口已登记（本阶段已完成）

---

## 3) 下一阶段边界（写死）

### 禁止
- 不开放真实用户测试
- 不进入 full controlled trial
- 不启用默认路径（default-on）
- 不授予模型执行权
- 不把输出候选变成真实执行命令
- 不扩大真实 side effects 面

### 允许（前置开发的最小集合）
- 明确 controlled_live_input 的显式入口事件与审计字段
- 定义短时窗口、可中止、可回放、可降级的受控真实输入试验护栏
- 补齐设备侧观测/回放链路的工程化细节（仍不要求产品级阈值）

---

## 4) 入口必须携带的最小输入（contract v0）

进入下一阶段前置开发时，必须提供：
- `entry_token`（显式人工触发标记；禁止默认开启）
- `mode`（必须为受控模式，不得为 default/uncontrolled）
- `timebox_ms`（短时窗口上限）
- `replay_capture_enabled=true`（确保可回放）
- `no_execute_side_effects=true`
- `operator_intent` 与 `reason_codes`

---

## 5) 判定输出（本阶段给出的建议）

本阶段（Productization-000）给出的系统级结论为：**CONDITIONAL_GO**  
允许进入“受控真实场景试验前置开发”，但必须坚持上述硬边界。


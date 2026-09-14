# Phase-RealScenePrep-001 — Controlled Real Scene Trial Scope & Boundary v0（范围与边界冻结）

**目的**：冻结首轮“受控真实场景试验”的极窄范围，防止借试验名义扩大能力/风险/副作用面。  

---

## 0) 总原则（写死）

- **极窄 scope**：只允许 1–2 个核心场景、短距离、短时间
- **显式入口**：不得 default-on
- **candidate-only**：输出只允许候选/提示/警告/求助/静默
- **人工可中止**：操作员与安全观察员均可中止
- **timebox 受控**：单次/单日/连续运行都有上限
- **证据优先**：trace/replay/whitebox/操作员记录必须完整

---

## 1) 场景范围（首轮允许，写死）

仅限以下核心场景中的 **1–2 个**：
- 人行道短距离行走（短距离、低复杂）
- 受控路口观察（**不执行真实过街指令**）
- 室内医院/大厅类静态路线观察
- 地铁站内标牌观察（**不执行真实换乘指令**）

### 明确禁止（写死）
- 夜间复杂环境
- 雨天/极端天气
- 高速车流路口
- 大型商场/展会/高密人流
- 长距离连续导航
- 单人无人监督真实试验
- 面向外部真实用户开放

---

## 2) 时间范围（timebox，写死）

必须配置并记录：
- `single_trial_timebox_ms`：单次试验时长上限
- `daily_trial_limit`：单日试验次数上限
- `continuous_run_timebox_ms`：连续运行时长上限

硬规则：
- 超时必须停止或降级（不得“继续跑完”）
- 超时属于 abort trigger（见 abort policy）

---

## 3) 人员范围（写死）

必须同时具备：
- 操作员（operator）
- 安全观察员（safety observer）
- 试验记录责任人（record owner）

禁止：
- 单人盲测
- 无安全观察员进入外部真实环境

---

## 4) 输出范围（写死）

仍只允许：
- `candidate`
- `notice`
- `warning`
- `ask_for_help_prompt`
- `silence`

明确禁止：
- execute command
- forced crossing instruction
- autonomous reroute execution
- default-on continuous guidance

---

## 5) 输入源范围（写死）

允许：
- controlled live input（显式开启、可中止、可回放）
- replay/fixture（用于对照与复现）

禁止：
- uncontrolled live input
- default live mode


# Luna Badge v1.4.9｜一期最终架构与边界说明（Architecture Overview）

> 本文档是 v1.4.9 的工程级“架构总览 + 边界声明”。  
> 目标：可作为 onboarding / 对外解释材料；可作为 1.4.X 冻结后续评审依据。  
> 约束：本文档不引入新功能，不修改代码，不为二期提前设计实现；只做说明与边界声明。

---

## 1) 一期目标与定位

v1.4.9 是 Luna Badge 一期（1.4.X）的**可交付化与可冻结化**版本，其目标是：

- **行为可解释**：用户可感知的决策/状态/播报有明确语义来源与触发条件。
- **行为可复现**：相同输入能够产生完全一致的行为序列（回放 hash 一致）。
- **行为可审计**：通过结构化事件流（decisions/behavior_states/tts_events）定位“为什么这么做”。
- **行为可冻结**：明确哪些行为面在 1.4.X 内不可变更（`[1.4.X frozen]`）。

一期系统定位：**以视觉为节奏主权的导航与表达系统**。表达与播报必须服从视觉节奏与安全约束，系统不得“语言抢跑”。

---

## 2) 核心架构总览

### 2.1 数据流（从输入到用户）

1. **Perception（视觉/地图快照）**  
   - Vision：以“行为态”提供（如 TURNING/STRAIGHT 等）。  
   - Map：以快照提供（route_state / distance_to_turn 等）。  

2. **Decision（任务与流程决策）**  
   - 路由顺序固定：PendingQuery → Task control → New task（见冻结点）。  
   - 产出“对用户可见”的动作与状态推进。

3. **Expression / TTS（表达与播报系统）**  
   - **C5 Scheduler（表达调度）**：决定 EMIT/QUEUE/DROP/REPLACE/SUPPRESS（不改语义、不造信息）。  
   - **TTS Router Facade（全局唯一播报入口）**：统一路由到导航/安全或主队列。  
   - **TimeWindowGate + PriorityScheduler + TtsManager**：节流、优先级、入队与抢占。

4. **FailSafe（失效保护）**  
   - 通过 Health 事件、VisionFailSafe 等触发 degraded/emergency。  
   - 核心约束：FAILSAFE 后禁止继续推进任务链（用户体验面冻结）。

### 2.2 回放与门禁（可复现基础设施）

- **ReplayInput（SSOT）**：回放输入结构固定（time/vision/map/intents/initial_state）。  
- **ReplayClock（逻辑时间）**：回放路径屏蔽 wall clock。  
- **Replay Gate**：以 hash 一致性证明确定性（快/慢运行与重启进程一致）。

---

## 3) 行为与责任边界

### 3.1 视觉节奏主权（Rhythm Authority）

- **Vision 是唯一节奏主权**：延迟、抑制、允许输出必须以视觉状态为基准。  
- **GPS/Map 是验证与补充**：不得成为节奏源，不得越权触发“抢跑式播报”。

### 3.2 TTS 输出责任链

- **唯一入口**：所有用户可听见的输出必须经 `TTSRouterFacade.emit()` 路由。  
- **分类与优先级**：类别（SAFETY/NAVIGATION/TASK/CHAT…）决定 band 与抢占/节流策略。  
- **节流与抑制**：TimeWindowGate 与去重/替换行为属于用户体验面的一部分（冻结）。

### 3.3 FailSafe 的责任

- **触发责任**：HealthMonitor/VisionFailSafe 等负责产生“降级/应急”的触发条件。  
- **接管责任**：FailSafeManager 负责进入 degraded/emergency，并对外表现为“安全优先/停止推进”。  
- **限制**：FailSafe 不得偷偷改变业务意图；只允许按冻结语义阻断与降级提示。

### 3.4 用户最终控制权（一期边界）

一期中，系统必须服从用户接管：  
- 用户取消/退出后，任务必须收敛到 `idle/ended`，且不再出现 `NAVIGATION EMIT`。  
- 系统不得“纠正用户”或在用户明确反向指令后继续推进原任务。

（详见 `user_takeover_test_report.md` 的“一期声明”。）

---

## 4) 一期冻结点（1.4.X frozen）

以下冻结点属于 1.4.X 生命周期内的版本级契约；任何改变都应视为行为变更（需版本升级讨论）：

- **DecisionPipeline 路由顺序冻结**：见 `decision_core/decision_core.py` 的 `[1.4.X frozen]` 说明。  
- **TURNING/STRAIGHT 行为态语义冻结**：TURNING 期间的播报白名单与互斥语义冻结。  
- **C5 Scheduler TURNING 白名单兜底冻结**：非关键表达 DROP；关键表达可覆盖。  
- **TimeWindowGate 阈值与语义冻结**：安全/导航窗口与“更新 last_*_time 的语义”冻结。  
- **PriorityBand 阈值冻结**：priority→band 的分段规则冻结。  
- **TTS Router Facade 路由顺序冻结**：band→router/queue 的路由顺序冻结。  
- **FailSafe 触发语义冻结**：触发条件的结构语义与“异常时不得继续推进 TaskChain”的约束冻结。

（行为面 SSOT：`behavior_contract_1_4_9.md`。）

---

## 5) 不做清单（Explicit Non-Goals）

v1.4.9（一期封版）明确不做：

- **情感调度/情绪表达引擎**（不允许接管节奏主权）。  
- **自学习/长期用户画像驱动策略**（不引入记忆型行为漂移）。  
- **多模型仲裁/动态模型博弈**。  
- **GPS/地图驱动的节奏决策**（GPS 仅验证）。  
- **对外承诺的“接管后继续协作”模式**（一期只收敛到结束态）。  
- **性能优化**（P0-4 只给出基线与红线定义，不做优化）。

---

## 6) 二期接口与约束（只列原则）

二期允许在不破坏一期冻结面前提下演进，但必须遵守以下原则（只列原则，不提前设计实现）：

- **节奏主权不变**：任何新模块不得覆盖 Vision 的节奏主权；最多“调制”而非“接管”。  
- **行为面可审计**：新增行为必须可回放、可 hash、可定位差异来源。  
- **边界先于能力**：新增能力必须先声明“责任归属与安全边界”，再进入实现。  
- **用户控制权优先**：用户接管仍是最终裁决；若引入“接管后继续协作”，必须重新定义安全边界与责任归属，并形成新的冻结面。  


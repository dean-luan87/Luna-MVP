# Luna Badge v1.4.9 — Behavior Contract (P0-1)

**版本性质**：一期工程封版（Deliverable + Freezable）  
**原则**：不加功能、不改能力，只做可交付化、可冻结化  
**本文件目的**：冻结 1.4.x 对用户可见的行为表面（behavioral surface），终止行为漂移。

---

## 1. 范围（Scope）

本契约覆盖“对用户产生影响”的行为：
- **决策类型**：系统生成的决策/动作类型（Action / Decision）
- **播报类型**：语音输出的类别、优先级、打断与节流
- **状态切换**：会影响“说/不说/何时说”的内部状态（窗口/队列/视觉状态）

本契约冻结的是 **行为结果**，不是某个代码文件。

---

## 2. 行为枚举与归档（Behavior Catalog）

### 2.1 决策类型（Decision / Action Types）

#### A. 导航事件 → TTS_ROUTER_*（canonical）
来源：`task_engine/navigation/navigation_scheduler.py`

| 行为ID | 触发输入 | 输出动作 | 不变量 |
|---|---|---|---|
| NAV.TURN | TurnEvent | `Action(type="TTS_ROUTER_TURN")` | direction/distance 只做结构化传递；distance 取整（米） |
| NAV.STRAIGHT | StraightEvent | `Action(type="TTS_ROUTER_STRAIGHT")` | distance 取整（米） |
| NAV.OBSTACLE.CRITICAL | ObstacleEvent(distance < 1.5m) | `Action(type="TTS_ROUTER_SAFETY")` | 阈值 **1.5m** 冻结；文本语义为“立即停下” |
| NAV.OBSTACLE.NORMAL | ObstacleEvent(distance ≥ 1.5m) | `Action(type="TTS_ROUTER_OBSTACLE")` | direction 默认为“前方”，distance 取整（米） |

#### B. DecisionCore TTS 动作面（frozen action surface）
来源：`decision_core/decision_core.py: DecisionCore.handle_action()`

支持且冻结的动作类型：
- `TTS_ROUTER_TURN` → `tts_router.route_turn(...)`
- `TTS_ROUTER_STRAIGHT` → `tts_router.route_straight(...)`
- `TTS_ROUTER_OBSTACLE` → `tts_router.route_obstacle_warning(...)`
- `TTS_ROUTER_GENERIC` → `tts_router.route_generic(...)`
- `TTS_ROUTER_SAFETY` → `tts_router.route_safety(...)`

**不变量**：新增/删除/重定向任一动作类型，均视为行为变更，需升级版本。

#### C. SpeechEvent → Category 推断（fallback heuristic）
来源：`task_engine/navigation/navigation_voice_adapter.py`

当 speech_event 未显式给出 category 或 decision 时，系统使用以下冻结推断（会影响优先级/节流）：  

- **Decision → Category（冻结集合）**
  - SAFETY：STOP / DANGER / OBSTACLE_FRONT / OBSTACLE / CLIFF / STAIRS_DOWN
  - NAVIGATION：LEFT / RIGHT / SLIGHT_LEFT / SLIGHT_RIGHT / FORWARD / KEEP_STRAIGHT / TURN_LEFT / TURN_RIGHT
- **Text keyword → Category（冻结语义）**
  - danger_keywords（危险/障碍/台阶/跌落/道路等）→ SAFETY
  - nav_keywords（左转/右转/直行/前方/米/路口等）→ NAVIGATION

---

### 2.2 播报类型（TTS Categories & Priority Bands）

#### A. Category 集合（冻结）
来源：`task_engine/tts/tts_policy.py`

- SAFETY
- NAVIGATION
- SYSTEM
- TASK
- CHAT

#### B. Category → Policy（冻结语义）
来源：`task_engine/tts/tts_policy.py: TTS_POLICY_TABLE`

| Category | priority | interrupt | default_level |
|---|---:|---:|---|
| SAFETY | 90 | True | warning |
| NAVIGATION | 75 | False | info |
| SYSTEM | 65 | False | system |
| TASK | 50 | False | info |
| CHAT | 25 | False | info |

#### C. PriorityBand 分段（冻结阈值）
来源：`task_engine/tts/priority_bands.py`

| priority 区间 | Band |
|---|---|
| ≥ 90 | P0_SAFETY |
| ≥ 70 | P1_NAV |
| ≥ 40 | P2_TASK |
| else | P3_CHAT |

---

### 2.3 播报路由与节流（Routing & Throttling）

#### A. 全局唯一入口（冻结路由顺序）
来源：`task_engine/tts/router_facade.py: TTSRouterFacade.emit()`

冻结路由顺序：
1) Category → Policy(priority/interrupt) → PriorityBand
2) P0_SAFETY → `NavigationVoiceRouter.route_safety()`
3) P1_NAV → `NavigationVoiceRouter.route_navigation()`
4) P2_TASK / P3_CHAT → `TtsManager.enqueue()`（主队列）

#### B. TimeWindowGate（冻结桶位/阈值）
来源：`task_engine/tts/routers/time_window_gate.py`

| 类别 | 窗口（秒） | 语义 |
|---|---:|---|
| SAFETY | 0.8 | 通过才更新时间戳 |
| NAVIGATION | 2.0 | 通过才更新时间戳 |

#### C. Safety Silence Window（冻结）
来源：`task_engine/navigation/navigation_voice_router.py`

- `safety_silence_window = 3.0s`：安全播报后 N 秒内抑制 NAVIGATION
- `enable_chat_during_safety_window = True`（默认）

#### D. Safety 去重（冻结）
来源：`task_engine/tts/tts_manager.py: push_safety()`

- **2.0 秒内**重复同一句安全播报 → 丢弃（返回 False）

---

### 2.4 调度与出声顺序（Scheduling）

#### A. PriorityScheduler（冻结语义）
来源：`task_engine/tts/priority_scheduler.py`

冻结排序规则：
1) safety_queue 永远先于 main_queue
2) main_queue：按 Band（P1 > P2 > P3）
3) 同 Band：priority 数值高者优先
4) 同 Band 同 priority：FIFO（先入队优先）

#### B. RuntimeDriver（冻结消费粒度）
来源：`task_engine/tts/runtime_driver.py`

- `process_once()` 每次只消费并播放 **一条** Utterance（通过 `pop_next()`）

---

### 2.5 视觉驱动表达调度（C-5 / v1.4.8.freeze）

来源：`expression/scheduler/c5_scheduler.py`（已在 v1.4.8 tag 中封版）

对用户可见的最小行为面：
- 视觉状态变化触发 flush
- TURNING 下非 critical 表达禁止输出（critical 可覆盖）
- 延迟桶：{0, 100, 200, 300}ms（由速度分桶）
- 队列：max=2，非 FIFO，duplicate_key REPLACE

---

## 3. 不变量（Invariants）

以下不变量在 1.4.x 内冻结：

- **全局路由不变量**：所有 TTS 输出必须经由 `get_tts_router_facade()` 进入统一路由。
- **节流不变量**：TimeWindowGate 的窗口语义与阈值不变（SAFETY=0.8s, NAVIGATION=2.0s）。
- **安全优先不变量**：安全播报可抢占，并有 2.0s 去重窗口。
- **排序不变量**：PriorityScheduler 的“安全优先 + band + priority + FIFO”规则不变。
- **视觉节奏不变量**：C-5 的视觉主权与 TURNING 抑制规则不变。

---

## 4. 冻结字段（Fields Frozen in 1.4.x）

以下字段/阈值/集合在 1.4.x 内禁止修改（修改即行为变更）：

- `ObstacleEvent` 安全阈值：**1.5m**（`navigation_scheduler.py`）
- TimeWindowGate：`safety_window=0.8`，`navigation_window=2.0`（`time_window_gate.py`）
- Safety silence window：`safety_silence_window=3.0`（`navigation_voice_router.py`）
- Safety 去重窗口：**2.0s**（`tts_manager.py`）
- PriorityBand 阈值：`>=90, >=70, >=40`（`priority_bands.py`）
- TTS_POLICY_TABLE 的 category 集合与映射语义（`tts_policy.py`）
- DecisionCore 支持的 `TTS_ROUTER_*` 动作集合与映射（`decision_core.py`）

---

## 5. 版本升级判定（When to bump version）

出现任一情况必须升级 minor/major：
- 新增/删除/变更 `TTS_ROUTER_*` 动作面
- 修改任何冻结阈值/桶位/窗口语义
- 修改 PriorityBand 分段阈值或 PriorityScheduler 排序规则
- 修改 C-5 TURNING 抑制与 delay 桶结构

---

## 6. 明确不包含（Non-goals）

v1.4.9 不引入：
- 情感调度
- 用户画像学习
- 视觉算法/模型增强
- 任何 1.5+ 能力

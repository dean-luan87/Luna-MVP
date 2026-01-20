# Navigation Foundation Step 7 (v1.4.8)

## 📋 Step 7: Authority Lock Hint（主权预期提示机制）

### 概述

Step 7 是体验层 × 决策层之间的关键缓冲层。

**一句话定义**:
- Step 7 = Authority Lock Hint（主权预期提示机制）
- 在"真正接管发生之前"，向上层系统发布可解释、可撤销、非强制的"接管预期信号"
- 不做接管、不做裁决、不做控制，只做一件事：提前让系统"知道接下来可能要发生什么"

---

## 🎯 为什么 Step 7 必须存在

### 如果没有 Step 7，会发生什么？

- FSM 在 Step 6 判定：LOCKING → TAKEN
- 上层（TTS / UI / 任务链）毫无心理准备
- 结果：
  - 语音突然换策略
  - 引导逻辑突然改变
  - 用户感觉"系统抽风了"

### 工程价值

这是"预期管理层"，和自动驾驶里的：
- "即将变道"
- "准备接管"

是同一类工程问题。

---

## 📊 Step 7 在整体架构中的位置

```
Step 5  Authority Confidence Snapshot
        ↓
Step 6  Authority Takeover FSM
        ↓
Step 7  Authority Lock Hint   ←（只在 LOCKING 阶段）
        ↓
Step 8 （未来）真正主权接管 or 仅日志
```

**关键点**:
- Step 7 只监听 FSM，不反向控制 FSM
- 这是单向依赖，保证系统稳定

---

## 🔄 核心抽象

### AuthorityLockHint

不是 Decision，不是 Event，而是 Hint（提示）

**为什么叫 Hint？**
- ✅ 可以被忽略
- ✅ 可以被撤销
- ✅ 可以被不同模块不同方式消费
- ❌ 不具备强制语义

这是后续做"人格化体验"的地基。

### Hint 只在一个状态出现

**仅当 FSM 处于 LOCKING 状态时才允许发 Hint**

- IDLE：没必要
- CANDIDATE：还太早
- TAKEN：已经晚了
- COOLDOWN：禁止扰民

---

## 📐 Authority Lock Hint 数据结构

```python
@dataclass
class AuthorityLockHint:
    ts: float
    target_authority: str            # VISUAL / MAP_VISION / GPS
    confidence: float                # 当前 snapshot 分数
    eta_s: float | None              # 预计多久后完成接管（体验层最重要的字段）
    scene: str
    severity: str                    # LOW / MEDIUM / HIGH
    reason_trace: list[str]
```

### severity 的工程语义（不是情绪）

- **LOW**: 只给系统内部模块用
- **MEDIUM**: 允许 TTS 做轻提示
- **HIGH**: 允许 UI / 强提示（未来）

**默认**：全部 LOW（你现在不需要"说话"，只需要"系统知道"）

---

## 🔄 触发条件

当 FSM 状态满足：

```
TakeoverState == LOCKING
```

并且：
- target_authority 与当前主权不同（或首次）
- LOCKING 已持续 > hint_delay_s（例如 0.5s）
- 锁定进度 >= min_lock_progress

---

## 📊 Hint 生成规则

### HINT_RULES

```python
{
  "VISUAL": {
    "min_lock_progress": 0.3,
    "default_severity": "LOW",
    "hint_delay_s": 0.5
  },
  "MAP_VISION": {
    "min_lock_progress": 0.4,
    "default_severity": "LOW",
    "hint_delay_s": 0.5
  },
  "GPS": {
    "min_lock_progress": 0.6,       # GPS 的 hint 更谨慎
    "default_severity": "MEDIUM",   # GPS 使用 MEDIUM severity
    "hint_delay_s": 0.8             # GPS 延迟更长
  }
}
```

**注意**：GPS 的 hint 永远更谨慎，这是理念的直接体现。

### ETA 计算方式（禁止复杂）

```
eta_s = max(0, lock_s - (now_ts - lock_start_ts))
```

不用预测，不用 ML，不用 fancy。

---

## 🔌 Step 7 只做三件事

1. **监听 FSM**
2. **生成 Hint**
3. **发布事件**

---

## 🚫 重要禁令

### 总体约束

1. **不修改 Step 6 FSM**
2. **Hint 不得触发任何主权切换**
3. **Hint 默认不接入 TTS**
4. **所有 Hint 必须可关闭**

### 当前阶段

- ✅ 只插桩，不接管
- ✅ 默认启用（enable_hint=True）
- ✅ 只输出 Hint 事件
- ✅ 默认 severity=LOW（只给系统内部模块用）

---

## 📊 事件流

```
Step6 FSM（LOCKING 状态）
  ↓
AuthorityLockHintProbe（监听）
  ↓
AuthorityLockHintEmitter（生成 Hint）
  ↓
AuthorityLockHintEvent（发布）
  ↓
下游（TTS / UI / 任务链 - 未来）
```

---

## 🔌 如何接入

### 基本接入

```python
from navigation.authority_takeover_probe import AuthorityTakeoverProbe
from navigation.authority_lock_hint_probe import AuthorityLockHintProbe
from common.event_bus import EventBus

event_bus = EventBus()

# 创建 Takeover Probe
takeover_probe = AuthorityTakeoverProbe(
    event_bus=event_bus,
    enable_fsm=True
)

# 创建 Hint Probe（传入 FSM 实例）
hint_probe = AuthorityLockHintProbe(
    fsm=takeover_probe.fsm,
    event_bus=event_bus,
    enable_hint=True
)

# 订阅 Hint 事件
from navigation.events import TOPIC_AUTHORITY_LOCK_HINT

def on_hint(event):
    print(f"Hint: {event.hint.target_authority}, ETA: {event.hint.eta_s}s")

event_bus.subscribe(TOPIC_AUTHORITY_LOCK_HINT, on_hint)

# 周期性更新 Hint（或在事件回调中调用）
hint_probe.update(scene="OUTDOOR")
```

---

## 📝 日志规范

### Hint 日志

```
[LOCK_HINT] target=MAP_VISION eta=1.2s confidence=0.82 severity=LOW scene=OUTDOOR
```

---

## ✅ 验收标准

1. ✅ FSM 未进入 LOCKING → 无 Hint
2. ✅ LOCKING 短暂抖动 → 不发 Hint
3. ✅ LOCKING 稳定 → 仅发一次 Hint
4. ✅ FSM 回退 → Hint 自动停止
5. ✅ 关闭开关 → 系统无任何变化

---

## 📈 为什么 Step 7 是"体验系统的入口"

你现在可能还没用到 Step 7，但未来这些都会基于它：

- 「前方环境复杂，我将更依赖视觉」
- 「即将切换为地图导航」
- 「我需要重新确认你的位置」

所有这些不是决策，而是"心理过渡"。

而 Step 7，就是你系统里第一次具备"预期管理能力"的地方。

---

## 🔮 下一步（Step 8 预告）

Authority Confidence Timeline（主权置信度时间轴）
- 为调试、复盘、甚至未来 ML 训练留下一条"可解释的历史轨迹"

---

**文档版本**: v1.4.8 Step 7  
**最后更新**: 2025-12-12







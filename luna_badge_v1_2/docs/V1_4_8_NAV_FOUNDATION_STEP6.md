# Navigation Foundation Step 6 (v1.4.8)

## 📋 Step 6: 位置主权的阶段性接管机制（Staged Authority Takeover）

### 概述

Step 6 提供可逆、可解释、可回退的接管流程。

**一句话结论**:
- Step 6 =「位置主权的阶段性接管机制（Staged Authority Takeover）」
- 不是"谁分高就上谁"，而是可逆、可解释、可回退的接管流程
- 视角为主、GPS 为辅，但不是一刀切替换，而是"阶段接管"

---

## 🎯 Step 6 的真实定位

### Step 6 不是做什么？

- ❌ 不是融合算法
- ❌ 不是重新写 PositionAuthorityManager
- ❌ 不是让 Step5 snapshot 直接控制导航
- ❌ 不是"分数高就切换主权"

### Step 6 只做一件事

把「是否接管主权」这件事，从"瞬时判断"升级为「阶段状态机」

**分工**:
- Step3：裁决当下谁是主权
- Step5：描述态势（证据 + 置信度）
- Step6：管理「主权迁移过程」本身

这是系统工程视角，不是算法视角。

---

## 🔄 Authority Takeover FSM

### 核心抽象

AuthorityTakeoverFSM（主权接管状态机）

它不算分，不算路，只做三件事：
1. 是否允许接管
2. 是否正在接管
3. 是否需要回退

### 5 个阶段

```
IDLE
 ↓
CANDIDATE      （满足接管条件，但未确认）
 ↓
LOCKING        （锁定观察窗口，防抖）
 ↓
TAKEN          （完成接管）
 ↓
COOLDOWN       （冷却期，防止频繁切换）
```

这是工程上对抗"抖动"的唯一正确姿势。

---

## 📐 关键设计原则（必须遵守）

### 核心原则

1. **时间 > 分数**：连续稳定比单次高分更重要
2. **连续稳定 > 单次高分**：需要持续满足条件
3. **接管慢，回退更慢**：LOCKING 和 COOLDOWN 防止抖动
4. **室内优先级永远最高**：室内场景下，GPS 直接被标记为"不可接管源"

### 与前面理念的对应关系

| 理念 | Step 6 实现 |
|------|------------|
| 「小范围内视角比 GPS 强」 | Visual 接管需要更低阈值、更短锁定时间 |
| 「室内不需要 GPS」 | 室内场景下，GPS 直接被标记为"不可接管源" |
| 「中长距离才需要 GPS」 | GPS 接管只在 Outdoor + Distance > threshold 才允许进入 FSM |
| 「绘制地图 + 地标验证」 | map_vision_score 是唯一允许快速锁定的证据源 |

---

## 📊 接管规则表

### VISUAL

```python
{
    "min_score": 0.70,
    "min_gap": 0.20,
    "lock_s": 1.5,              # 最短锁定时间
    "cooldown_s": 3.0,
    "scene_required": ["INDOOR", "TRANSITION"],
    "min_distance_m": None
}
```

### MAP_VISION

```python
{
    "min_score": 0.80,
    "min_gap": 0.25,
    "lock_s": 2.0,              # 地标匹配允许稍快锁定
    "cooldown_s": 4.0,
    "scene_required": ["OUTDOOR"],
    "min_distance_m": None
}
```

### GPS

```python
{
    "min_score": 0.75,
    "min_gap": 0.30,            # GPS 需要更大的差距
    "lock_s": 3.0,              # GPS 接管最慢
    "cooldown_s": 6.0,          # GPS 冷却期最长
    "scene_required": ["OUTDOOR"],
    "min_distance_m": 50        # GPS 接管需要最小距离 50m
}
```

**注意**：GPS 接管是最难的

---

## 🔄 状态迁移规则

### IDLE → CANDIDATE

条件：
- snapshot.dominant_candidate 存在
- 满足 min_score + min_gap
- scene 符合
- GPS 额外检查 distance

### CANDIDATE → LOCKING

条件：
- 连续满足条件
- 未发生反向 evidence
- 目标未改变

### LOCKING → TAKEN

条件：
- now_ts - enter_ts ≥ lock_s
- 仍在锁定观察窗口内

### TAKEN → COOLDOWN

触发：
- 输出 TakeoverDecisionEvent
- 写 reason_trace

### COOLDOWN → IDLE

条件：
- now_ts - enter_ts ≥ cooldown_s

---

## 🚫 重要禁令

### 总体约束

1. **禁止修改现有 PositionAuthorityManager 的裁决逻辑**
2. **FSM 只输出"接管建议事件"，不直接切换主权**
3. **FSM 必须可关闭（Feature Flag）**
4. **所有状态迁移必须有 reason_trace**

### 当前阶段

- ✅ 只插桩，不接管
- ✅ 默认关闭（enable_fsm=False）
- ✅ 只输出日志和建议事件

---

## 📊 事件流

```
Step5 快照事件
  ↓
AuthorityTakeoverProbe（桥接）
  ↓
AuthorityTakeoverFSM（状态机）
  ↓
TakeoverDecisionEvent（接管建议）
  ↓
下游（仅插桩，不接管）
```

---

## 🔌 如何接入

### 基本接入

```python
from navigation.authority_takeover_probe import AuthorityTakeoverProbe
from common.event_bus import EventBus

event_bus = EventBus()
probe = AuthorityTakeoverProbe(
    event_bus=event_bus,
    enable_fsm=True  # Feature Flag
)

# 自动订阅 Step5 快照事件
# 自动运行 FSM 并发布接管建议
```

### 订阅接管决策事件

```python
from navigation.events import TOPIC_AUTHORITY_TAKEOVER_DECISION

def on_takeover_decision(event):
    print(f"接管建议: {event.target_authority}, 置信度: {event.confidence}")

event_bus.subscribe(TOPIC_AUTHORITY_TAKEOVER_DECISION, on_takeover_decision)
```

---

## 📝 日志标准

### FSM 状态迁移

```
[TAKEOVER_FSM] IDLE → CANDIDATE target=VISUAL reason=...
[TAKEOVER_FSM] CANDIDATE → LOCKING target=VISUAL reason=...
[TAKEOVER_FSM] LOCKING → TAKEN target=VISUAL reason=...
[TAKEOVER_FSM] TAKEN → COOLDOWN target=VISUAL reason=...
[TAKEOVER_FSM] COOLDOWN → IDLE target=None reason=...
```

### 最终接管决策

```
[TAKEOVER_DECISION] authority=MAP_VISION score=0.88 state=TAKEN reasons=[...]
```

---

## ✅ 验收标准

1. ✅ FSM 状态流转可追溯（日志完整）
2. ✅ 不会频繁切换（COOLDOWN 生效）
3. ✅ 室内不会触发 GPS 接管
4. ✅ 即使 snapshot 抖动，也不会立刻接管
5. ✅ 关闭开关后系统行为完全一致

---

## 📈 为什么 Step 6 是「分水岭」

做到 Step 6，系统会发生一个质变：
- 从 "谁更准"
- 变成 "谁在这个阶段更可靠"

这正是系统工程视角的核心。

---

## 🔮 下一步（Step 7 预告）

Authority Lock Hint（主权预期提示）
- 在真正接管前，让 TTS / 上层知道"即将切换"
- 进一步提升安全感与可解释性

---

**文档版本**: v1.4.8 Step 6  
**最后更新**: 2025-12-12







# v1.4.8 Step 7 Skeleton 变更摘要

**生成日期**: 2025-12-12  
**状态**: ✅ 完成

---

## 📁 新增文件清单

### 核心模块（3个 Python 文件）

1. **`navigation/authority_lock_hint.py`**
   - AuthorityLockHint 数据类
   - AuthorityLockHintEmitter 类
   - Hint 发射逻辑

2. **`navigation/authority_lock_hint_rules.py`**
   - HINT_RULES 规则表
   - ETA 计算函数
   - 提示策略配置

3. **`navigation/authority_lock_hint_probe.py`**
   - AuthorityLockHintProbe 类
   - FSM → Hint 的桥接器

### 更新文件

4. **`navigation/events.py`**
   - 新增 Step 7 事件类型：
     - AuthorityLockHintEvent
   - 新增 Topic 常量：
     - TOPIC_AUTHORITY_LOCK_HINT

### 文档

5. **`docs/V1_4_8_NAV_FOUNDATION_STEP7.md`**
   - Step 7 完整架构文档
   - 设计原则说明
   - 接入方式

### 测试

6. **`demo_runner/test_authority_lock_hint_skeleton.py`**
   - 最小自测脚本
   - 3 个测试场景

---

## 🎯 核心设计

### AuthorityLockHint

**Hint 不是 Decision，不是 Event，而是 Hint（提示）**

- ✅ 可以被忽略
- ✅ 可以被撤销
- ✅ 可以被不同模块不同方式消费
- ❌ 不具备强制语义

### 只在 LOCKING 状态发 Hint

- IDLE：没必要
- CANDIDATE：还太早
- LOCKING：✅ 发 Hint
- TAKEN：已经晚了
- COOLDOWN：禁止扰民

### severity 的工程语义

- **LOW**: 只给系统内部模块用（默认）
- **MEDIUM**: 允许 TTS 做轻提示
- **HIGH**: 允许 UI / 强提示（未来）

---

## 📊 Hint 规则表

| Authority | min_lock_progress | default_severity | hint_delay_s |
|-----------|-------------------|------------------|--------------|
| VISUAL | 0.3 (30%) | LOW | 0.5s |
| MAP_VISION | 0.4 (40%) | LOW | 0.5s |
| GPS | 0.6 (60%) | MEDIUM | 0.8s |

**注意**：GPS 的 hint 永远更谨慎。

---

## 🔌 如何接入

### 基本接入

```python
from navigation.authority_takeover_probe import AuthorityTakeoverProbe
from navigation.authority_lock_hint_probe import AuthorityLockHintProbe

# 创建 Takeover Probe
takeover_probe = AuthorityTakeoverProbe(event_bus=event_bus, enable_fsm=True)

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

# 周期性更新（或在事件回调中调用）
hint_probe.update(scene="OUTDOOR")
```

---

## 🧪 如何运行最小自测

```bash
cd /Users/luanlei/Desktop/Luna-2/luna_badge_v1_2
python3 demo_runner/test_authority_lock_hint_skeleton.py
```

**预期输出**:
- ✅ LOCKING 状态期间发出 Hint
- ✅ 未进入 LOCKING 时不发 Hint
- ✅ FSM 回退后 Hint 自动停止

---

## 📊 测试结果

### 测试场景 1: LOCKING 状态期间发出 Hint

**结果**: ✅ 通过
- FSM 进入 LOCKING 状态
- 收到 Hint（target=MAP_VISION, eta=1.19s）
- Hint 正常发出

### 测试场景 2: FSM 未进入 LOCKING → 无 Hint

**结果**: ✅ 通过
- FSM 保持 IDLE 状态
- 未收到任何 Hint
- 符合预期

### 测试场景 3: FSM 回退 → Hint 自动停止

**结果**: ✅ 通过
- 第一阶段进入 LOCKING，发出 Hint
- 第二阶段 FSM 回退到 IDLE
- Hint 自动停止（不再发出新的 Hint）

---

## ✅ 验收标准验证

### ✅ 代码层面

1. ✅ 新增模块可 import（无循环依赖、无类型错误）
2. ✅ 所有 Hint 都包含 reason_trace
3. ✅ Hint 可关闭（Feature Flag）

### ✅ 功能层面

1. ✅ FSM 未进入 LOCKING → 无 Hint
2. ✅ LOCKING 短暂抖动 → 不发 Hint（通过 hint_delay_s 控制）
3. ✅ LOCKING 稳定 → 仅发一次 Hint（通过状态追踪防止重复）
4. ✅ FSM 回退 → Hint 自动停止
5. ✅ 关闭开关 → 系统无任何变化

### ✅ 行为层面

1. ✅ 不影响旧导航行为（只插桩，不接管）
2. ✅ 不修改 Step 6 FSM
3. ✅ Hint 不触发任何主权切换

---

## 📝 关键设计原则

### 1. 只插桩，不接管

- ✅ 所有模块只发布 Hint 事件
- ✅ 不修改现有导航控制逻辑
- ✅ 不修改 Step 6 FSM
- ✅ Hint 默认不接入 TTS

### 2. 单向依赖

- ✅ Step 7 只监听 FSM，不反向控制 FSM
- ✅ 保证系统稳定

### 3. 体验层入口

- ✅ 提前让系统"知道接下来可能要发生什么"
- ✅ 为未来"人格化体验"打下地基

---

## 🚫 重要禁令

1. **不修改 Step 6 FSM**
2. **Hint 不得触发任何主权切换**
3. **Hint 默认不接入 TTS**
4. **所有 Hint 必须可关闭**

---

## 📈 为什么 Step 7 是"体验系统的入口"

Step 7 让你系统里第一次具备"预期管理能力"。

未来这些都会基于它：
- 「前方环境复杂，我将更依赖视觉」
- 「即将切换为地图导航」
- 「我需要重新确认你的位置」

所有这些不是决策，而是"心理过渡"。

---

## 🔮 下一步（Step 8 预告）

Authority Confidence Timeline（主权置信度时间轴）
- 为调试、复盘、甚至未来 ML 训练留下一条"可解释的历史轨迹"

---

## 📚 相关文档

- `docs/V1_4_8_NAV_FOUNDATION_STEP7.md`: Step 7 完整架构文档
- `navigation/authority_lock_hint.py`: Hint 核心实现
- `navigation/authority_lock_hint_rules.py`: 提示策略配置
- `demo_runner/test_authority_lock_hint_skeleton.py`: 测试示例

---

**变更摘要完成时间**: 2025-12-12  
**状态**: ✅ 所有文件已创建，测试通过







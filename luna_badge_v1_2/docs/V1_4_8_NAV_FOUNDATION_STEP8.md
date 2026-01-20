# Navigation Foundation Step 8 (v1.4.8)

## 📋 Step 8: Authority Confidence Timeline（主权置信度时间轴）

### 概述

Step 8 是一个工程价值极高、但"不影响线上行为"的模块。

**一句话定义**:
- Step 8 = Authority Confidence Timeline（主权置信度时间轴）
- 用"时间序列"的方式，把系统每一刻为什么相信谁这件事，完整、低成本、可回放地记录下来
- 它是为未来而生的模块，但现在就该建

---

## 🎯 Step 8 的一句话定位

Step 8 不参与决策，不影响体验，不接管系统

它只做一件事：把已经发生的"判断依据"结构化保存下来

这一步，是你从「工程系统」走向「可解释系统」的分水岭。

---

## 📊 为什么 Step 8 必须现在做，而不是以后

### 如果没有 Step 8，未来会发生什么？

- "刚才怎么突然切到 GPS 了？"
- "这个拐弯点为什么这么早？"
- 你只能靠：
  - 打印日志
  - 复现现场
  - 主观猜测

这在单人调试阶段还能忍，一旦进入：
- 多设备
- 多场景
- 多版本

系统就会失控。

---

## 🔄 Step 8 在整体架构中的位置

```
Step 5  Authority Confidence Snapshot   （单点）
Step 6  Authority Takeover FSM          （决策）
Step 7  Authority Lock Hint             （预期）
Step 8  Authority Confidence Timeline   （时间轴） ← 本步
```

👉 Step 8 监听 Step 5 / 6 / 7  
👉 但反向依赖为 0

---

## 📐 核心设计原则

### 原则 1：只记录"解释所必需的最小信息"

不是全量 dump，不是调试日志。

### 原则 2：时间是第一维度

不是"状态变化表"，而是"连续轨迹"。

### 原则 3：可关闭、可裁剪、可回放

这决定了它能不能长期存在。

---

## 📊 Timeline 记录的"最小数据模型"

### AuthorityConfidenceFrame

```python
@dataclass
class AuthorityConfidenceFrame:
    ts: float                           # 时间戳
    scene: str                          # 当前场景
    
    # 主权视角
    active_authority: str              # 当前活动主权
    candidate_authority: str | None    # 候选主权（如果有）
    
    # Step 5 Snapshot（裁剪版，只保留 confidence 数值）
    confidence: dict[str, float]       # {"VISUAL": 0.8, "MAP_VISION": 0.6, "GPS": 0.3}
    
    # FSM 状态
    takeover_state: str                # IDLE / CANDIDATE / LOCKING / TAKEN / COOLDOWN
    
    # 可选字段
    hint_active: bool = False          # 是否有 Hint 激活
```

**注意**：不是完整 Snapshot，只保留 confidence 数值

---

## ⏱️ 记录频率

### 默认：2 Hz（每 0.5 秒）

并且：
- **FSM 状态变化** → 强制插帧
- **Authority 变化** → 强制插帧

这是工程常识。

---

## 🔄 核心模块

### AuthorityConfidenceSampler（采样器）

**职责**:
- 周期性拉取当前 authority、最新 snapshot、FSM 状态
- 生成 Frame
- 交给 Store

**核心限制**:
- `MAX_TIMELINE_LENGTH = 300`（约 150 秒）
- 滑动窗口，永不无限增长

### AuthorityConfidenceStore（存储策略）

**v1.4.8 只做一件事**:
- 内存 RingBuffer
- `[ oldest ... newest ]`
- 不落盘、不跨进程、不持久化

这是对的。

### AuthorityConfidenceExporter（最小导出能力）

**v1.4.8 只支持 2 种能力**:
1. JSON 导出
2. ASCII 时间轴打印（调试用）

**示例输出**:
```
t=12.0s | VISUAL(0.81) MAP(0.62) GPS(0.22) | FSM=LOCKING
t=12.5s | VISUAL(0.79) MAP(0.65) GPS(0.24) | FSM=LOCKING
t=13.0s | MAP_VISION(0.71) VISUAL(0.68)    | FSM=TAKEN
```

---

## 🔌 如何接入

### 基本接入

```python
from navigation.authority_takeover_probe import AuthorityTakeoverProbe
from navigation.authority_confidence_timeline_probe import AuthorityConfidenceTimelineProbe

# 创建 Takeover Probe
takeover_probe = AuthorityTakeoverProbe(event_bus=event_bus, enable_fsm=True)

# 创建 Timeline Probe
timeline_probe = AuthorityConfidenceTimelineProbe(
    fsm=takeover_probe.fsm,
    event_bus=event_bus,
    enable_timeline=True,
    max_frames=300
)

# 自动监听 Step5/6/7 事件并记录时间轴
```

### 导出时间轴

```python
# 导出文本时间轴
text_timeline = timeline_probe.export_text_timeline()
print(text_timeline)

# 导出 JSON
json_timeline = timeline_probe.export_json()

# 导出到文件
timeline_probe.exporter.export_to_file("timeline.json", format="json")
```

---

## 📝 日志规范

### Timeline 统计（低频）

```
[TIMELINE] frames=128 oldest_ts=... newest_ts=... duration=...s
```

---

## ✅ 验收标准

1. ✅ 关闭 Step 8 → 系统行为不变
2. ✅ 连续运行 → 内存稳定
3. ✅ FSM 抖动 → 时间轴可解释
4. ✅ 导出结果 → 可读、连续

---

## 📈 为什么 Step 8 是"护城河"

99% 的项目只关心：
- "现在用哪个"
- "能不能走"

你这个系统已经开始关心：
- "为什么当时这么判断"
- "这条判断是不是可解释、可回放、可训练的"

### Step 8 直接带来的未来价值

- Debug 的成本指数级下降
- ML / 学习系统的天然训练数据
- 对外演示"我们不是黑箱"的证据
- 多设备协同时的共识基础

---

## 🚫 重要禁令

1. **Step 8 不得影响任何决策**
2. **默认开启，但可通过配置关闭**
3. **内存上限必须生效**

---

## 🔮 下一步（Step 9 预告）

Local Map × Confidence Timeline 的融合索引
- 把"你当时看到的世界"和"你当时为什么这么判断"对齐

---

**文档版本**: v1.4.8 Step 8  
**最后更新**: 2025-12-12







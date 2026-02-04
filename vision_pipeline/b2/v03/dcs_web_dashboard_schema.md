# DCS Web 仪表盘结构 Schema（v0.4.1）

**版本：** v0.4.1（冻结版）  
**用途：** 观察与审判系统，不做演示、不影响主链路  
**定位：** 后期系统监察模块的设计基线

---

## 🎯 设计目标

**当系统出问题时，我们能一眼看出：**
- 是不是 B 越权了？
- 是不是 C 被误导了？
- 是不是 Gate 失效了？

---

## 📊 1️⃣ Web 仪表盘整体分区（只读监察）

### 页面结构（逻辑）

```
┌──────────────────────────────────────────────┐
│ ① 全局健康状态（红 / 黄 / 绿）                │
│    [状态灯] [DCS 总分] [违规统计]              │
├──────────────────────────────────────────────┤
│ ② 时间轴（Decision + Gate）                  │
│    [时间线] [Gate 状态] [B 输出] [C 行为]     │
├──────────────────────────────────────────────┤
│ ③ B / C 边界违规统计                          │
│    [RED 违规] [YELLOW 风险] [GREEN 通过]       │
├──────────────────────────────────────────────┤
│ ④ 单条决策剖面（Trace Drilldown）            │
│    [详细 trace] [DCS 判定] [违规规则]          │
└──────────────────────────────────────────────┘
```

---

## 📋 2️⃣ 核心数据 Schema（DCS 输入）

### DCS 输入（每条 Decision）

```json
{
  "ts": 300.02,
  "frame_id": 8997,
  "module": "B",
  "impact": "NEED_STOP",
  "decision_level": "INTERRUPT",
  "gate_state": "ACTIVE",
  "view_state": {
    "stability_score": 0.82,
    "camera_motion": "LOW",
    "camera_pose": {
      "pitch_deg": 5.2,
      "roll_deg": 2.1
    },
    "fov_state": {
      "visibility_score": 0.75
    }
  },
  "evidence_state": {
    "main_factor": "EVENT",
    "state": "CONFIRMED",
    "confidence": 0.85
  },
  "dcs_judgement": {
    "level": "GREEN | YELLOW | RED",
    "violated_rules": ["DCS-R3"],
    "human_reason": "视角不稳定但仍输出干预",
    "score": 80
  },
  "to_c_message": {
    "sent": true,
    "payload": {
      "advisory_only": true,
      "intervention_level": "HARD"
    }
  },
  "c_ack": {
    "received": true,
    "action_taken": "STOP",
    "confirmed_at": 300.15
  }
}
```

### Schema 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `ts` | float | 系统时间戳（秒） |
| `frame_id` | int | 帧编号 |
| `module` | string | 模块标识（"B" 或 "C"） |
| `impact` | string | B 的行为影响（NEED_STOP / NEED_SLOW_DOWN 等） |
| `decision_level` | string | 决策级别（INTERRUPT / LOCAL / NONE） |
| `gate_state` | string | Gate 状态（ACTIVE / READ_ONLY / SUSPENDED） |
| `view_state` | object | 视角状态（稳定性、运动、姿态、可见度） |
| `evidence_state` | object | 证据状态（主因子、状态、置信度） |
| `dcs_judgement` | object | DCS 判定结果 |
| `to_c_message` | object | B → C 消息 |
| `c_ack` | object | C 的确认和行动 |

---

## 🎨 3️⃣ 仪表盘三色判定逻辑（展示规则）

### 🟥 红色（RED）

**触发条件：**
- 出现任意 RED 违规：
  - DCS-R1: B 确认性风险
  - DCS-R2: B 越权核验
  - DCS-R3: Gate fail 仍输出
  - DCS-R4: B 在 ≤3m 或室内主导
  - DCS-R5: 使用非系统时间

**页面表现：**
- 全局状态灯变红 🔴
- 时间轴对应节点高亮红色
- 点击可展开违规规则编号（如 DCS-R1）
- 显示违规详情和修复建议

**示例：**
```
[300.02s] 🔴 DCS-R3: Gate SUSPENDED 但仍发送消息给 C
         → 点击查看详情
```

---

### 🟨 黄色（YELLOW）

**触发条件：**
- 出现 YELLOW 风险：
  - DCS-Y1: 过度保守
  - DCS-Y2: 高频无效唤醒
  - DCS-Y3: 世界模型长时间不更新

**页面表现：**
- 全局状态灯黄 🟡
- 时间轴标黄点
- 提示"需关注，不阻断"
- 显示风险详情和建议

**示例：**
```
[300.02s] 🟡 DCS-Y1: B 过于频繁唤醒但未产生有效预警
         → 建议：检查唤醒策略
```

---

### 🟩 绿色（GREEN）

**触发条件：**
- 全部决策符合规则
- 无 RED 或 YELLOW 违规

**页面表现：**
- 全局绿 🟢
- 时间轴干净
- 允许长期只读 / 沉默
- 显示通过规则列表

**示例：**
```
[300.02s] 🟢 DCS-G1: B 只输出条件式风险
         DCS-G3: 熟悉场景下 B 自动降权
         DCS-G4: 时间 / 距离标尺始终一致
```

---

## 🔍 4️⃣ 单条 Decision 剖面（最重要）

### 点击任意时间点，展开详情

```
┌──────────────────────────────────────────────┐
│ [时间 300.02s | 帧 8997]                      │
├──────────────────────────────────────────────┤
│ Gate 状态：                                   │
│   ✔ 稳定 (stability_score: 0.82)             │
│   ✔ 距离 >3m (range_m: 5.2)                   │
│   ✔ 允许触发 (mode: ACTIVE)                   │
├──────────────────────────────────────────────┤
│ B 输出：                                      │
│   impact: NEED_STOP                          │
│   语义：条件风险预警（非确认）                │
│   advisory_only: true                        │
│   intervention_level: HARD                   │
├──────────────────────────────────────────────┤
│ DCS 判定：                                    │
│   🟩 GREEN                                   │
│   理由：明显安全风险，允许干预                │
│   通过规则：DCS-G1, DCS-G3, DCS-G4           │
├──────────────────────────────────────────────┤
│ C 行为：                                      │
│   ✔ 接收 (received: true)                    │
│   ✔ 靠近核验 (action_taken: STOP)            │
│   ✔ 写回世界记忆 (confirmed_at: 300.15)      │
└──────────────────────────────────────────────┘
```

### 这就是你要的：

> **"在第几秒，为什么触发，用了什么规则，说了什么话"**

---

## 📊 5️⃣ 全局健康状态（顶部面板）

### 状态灯逻辑

```json
{
  "global_status": "RED | YELLOW | GREEN",
  "dcs_score": 85,
  "violation_summary": {
    "red_count": 0,
    "yellow_count": 2,
    "green_count": 12
  },
  "time_range": {
    "start": 0.0,
    "end": 402.5,
    "total_decisions": 145
  }
}
```

### 状态判定

- **RED：** 存在任意 RED 违规 → 🔴
- **YELLOW：** 无 RED，但存在 YELLOW 风险 → 🟡
- **GREEN：** 无 RED，无 YELLOW → 🟢

---

## 📈 6️⃣ 时间轴（Decision + Gate）

### 时间轴结构

```
时间轴：[0s] ──────[100s]──────[200s]──────[300s]──────[400s]
        │           │            │            │            │
Gate:   ACTIVE      ACTIVE       SUSPENDED    ACTIVE       READ_ONLY
        │           │            │            │            │
B输出:  NO_OP       NEED_SLOW    (无)         NEED_STOP    NO_OP
        │           │            │            │            │
C行为:  (无)        SLOW_DOWN    (无)         STOP         (无)
        │           │            │            │            │
DCS:    🟢          🟢           🟢           🟢           🟢
```

### 时间轴交互

- **点击节点：** 展开单条 Decision 剖面
- **悬停节点：** 显示简要信息（impact, gate_state, dcs_level）
- **缩放：** 支持时间范围缩放
- **筛选：** 按 DCS 级别筛选（只显示 RED / YELLOW）

---

## 📊 7️⃣ B / C 边界违规统计

### 统计面板

```
┌──────────────────────────────────────────────┐
│ B / C 边界违规统计                            │
├──────────────────────────────────────────────┤
│ 🟥 RED 违规：                                 │
│   DCS-R1: B 确认性风险          × 0          │
│   DCS-R2: B 越权核验            × 0          │
│   DCS-R3: Gate fail 仍输出      × 0          │
│   DCS-R4: ≤3m 或室内主导        × 0          │
│   DCS-R5: 非系统时间            × 0          │
├──────────────────────────────────────────────┤
│ 🟨 YELLOW 风险：                              │
│   DCS-Y1: 频繁无效唤醒          × 2          │
│   DCS-Y2: 世界模型未更新        × 0          │
│   DCS-Y3: C 过度保守            × 1          │
├──────────────────────────────────────────────┤
│ 🟩 GREEN 通过：                               │
│   DCS-G1: 条件式风险            ✓ 145        │
│   DCS-G2: C 核验回写            ✓ 12         │
│   DCS-G3: 场景降权              ✓ 8          │
│   DCS-G4: 标尺一致              ✓ 145        │
└──────────────────────────────────────────────┘
```

---

## 🔧 8️⃣ 实现说明（Schema 级，不写代码）

### 数据流

```
B2 Runtime Trace (JSONL)
    ↓
DCS Hard Rules Check
    ↓
DCS Judgement (JSON)
    ↓
Web Dashboard (Schema)
    ↓
可视化展示
```

### 前端组件建议

1. **全局状态面板：** React/Vue 组件
2. **时间轴：** 使用 D3.js 或 ECharts
3. **决策剖面：** 可折叠面板组件
4. **违规统计：** 表格/列表组件

### 后端 API 建议

```python
# 伪代码示例
GET /api/dcs/dashboard
  → 返回全局健康状态

GET /api/dcs/timeline?start=0&end=400
  → 返回时间轴数据

GET /api/dcs/decision?ts=300.02
  → 返回单条决策剖面

GET /api/dcs/violations?level=RED
  → 返回违规统计
```

---

## 📌 9️⃣ 使用场景

### 场景 1：事故复盘

**问题：** 系统在某时刻误判

**操作：**
1. 打开 Web 仪表盘
2. 定位到问题时间点
3. 查看单条 Decision 剖面
4. 检查 DCS 判定和违规规则
5. 分析 B / C 边界是否被违反

---

### 场景 2：日常监察

**目标：** 监控系统健康状态

**操作：**
1. 查看全局健康状态（红/黄/绿）
2. 浏览时间轴，关注 RED 节点
3. 检查违规统计，识别趋势
4. 必要时深入单条 Decision 剖面

---

### 场景 3：版本对比

**目标：** 对比不同版本的 DCS 表现

**操作：**
1. 选择 v0.3 和 v0.4.1 的 trace
2. 分别加载到仪表盘
3. 对比 RED / YELLOW 违规数量
4. 形成进化曲线

---

## ✅ 验收标准

### Schema 完整性

- [x] 全局健康状态 Schema 已定义
- [x] 时间轴数据结构已定义
- [x] 单条 Decision 剖面 Schema 已定义
- [x] DCS 判定逻辑已定义
- [x] 三色判定规则已明确

### 可执行性

- [x] Schema 可直接用于前端开发
- [x] 数据结构可直接用于后端 API
- [x] 判定逻辑可直接映射到 DCS 规则

---

**版本：** v0.4.1（冻结版）  
**最后更新：** 2025-01-12  
**状态：** ✅ Schema 已就绪，可直接进入 Cursor

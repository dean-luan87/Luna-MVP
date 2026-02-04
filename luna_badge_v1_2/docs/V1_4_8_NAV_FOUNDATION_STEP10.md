# Navigation Foundation Step 10 (v1.4.8)

## 📋 Step 10: Evidence → Calibration / Learning Hint 层

### 概述

Step 10 是一个"反思层"而不是"学习层"。

**一句话定义**:
- Step 10 = Evidence → Calibration / Learning Hint 层
- 让系统"有资格在未来变得更聪明"
- 它是整个系统中最像"自省能力"的模块，但在 1.4.8 阶段，它必须保持克制与沉默

---

## 🎯 Step 10 的一句话定位

Step 10 的目标不是"让系统更聪明"

而是让系统"有资格在未来变得更聪明"

这一步，是你从「可追溯系统」走向「可学习系统」的准备。

---

## 📊 为什么 Step 10 必须现在做

### 如果没有 Step 10，未来会发生什么？

- "系统哪里出了问题？"
- "哪些模式值得反思？"
- "如何知道该学习什么？"
- 你只能靠：
  - 手动查看 Timeline
  - 主观猜测问题模式
  - 无法系统化地识别异常

---

## 🔄 Step 10 在整体架构中的位置

```
Step 9  Evidence Alignment        （时间 × 空间对齐）
Step 10 Calibration Hint          （反思层）← 本步
Step 11 （未来）产品表达层        （完全独立的新工程线）
```

👉 Step 10 只从 Step 9 读取数据  
👉 但反向依赖为 0

---

## 📐 核心设计原则

### 原则 1：反思，但不学习

- ✅ 识别"值得反思的模式"
- ✅ 生成 Hint（候选）
- ❌ 不自动生效
- ❌ 不回写参数
- ❌ 不假装"已经学习"

### 原则 2：克制与沉默

- ✅ 不参与实时决策
- ✅ 不涉及语言表达 / TTS / UI
- ✅ description 为工程解释，不是表达层文本

### 原则 3：可关闭、可裁剪、可回放

- ✅ 可关闭（Feature Flag）
- ✅ 可裁剪（内存上限）
- ✅ 可回放（JSON + Text 导出）

---

## 📊 CalibrationHint 数据模型

### 结构

```python
@dataclass
class CalibrationHint:
    hint_type: str                  # e.g. "LANDMARK_UNSTABLE"
    authority: str                  # "MAP_VISION" / "VISUAL" / "GPS"
    
    confidence_drop: float          # 0.0 ~ 1.0
    related_map_ids: List[str]
    related_landmark_ids: List[str]
    
    time_range: Tuple[float, float]  # (start_ts, end_ts)
    description: str                 # 内部说明，不给用户
```

**注意**：
- description 为工程解释，不是表达层文本
- 不允许直接生成任何"播报语句"

---

## 🔍 Hint 类型（最小集）

### 1. LANDMARK_UNSTABLE（地标不稳定）

**触发条件**:
- 同一 landmark id
- 在短时间窗内（≤ 3s）
- 多次 match / unmatch 或 score 剧烈波动

### 2. AUTHORITY_FLIP_FREQUENT（Authority 频繁切换）

**触发条件**:
- Authority 在短时间窗内（≤ 5s）
- 多次切换（≥ 3 次）

### 3. MAP_CONFIDENCE_OVERRATED（地图置信度过高但被反对）

**触发条件**:
- MAP_VISION confidence 高（> 0.7）
- 但 VISUAL 也高（> 0.6），长时间冲突

### 4. GPS_ONLY_ZONE_DETECTED（GPS 专用区域）

**触发条件**:
- 长时间无有效视觉/地标（≥ 10s）
- Authority 被迫长期停留在 GPS

---

## 🔄 核心模块

### CalibrationHintBuilder（Hint 构建器）

**职责**:
- 从 EvidenceAlignmentIndex 中读取对齐帧
- 识别"值得反思的模式"
- 生成 CalibrationHint（候选）

**构建时机（v1.4.8）**:
1. 一次导航片段结束
2. 或检测到异常片段（Authority 抖动 / 冲突）

**输出规则**:
- 每个 Hint 必须绑定明确 time_range
- 指向明确 map_id / landmark_id
- 不合并 Hint
- 不去重（交给 Store）

### CalibrationHintStore（Hint 存储）

**职责**:
- 管理 CalibrationHint 的内存存储
- 提供只读查询能力

**存储策略**:
- MAX_HINTS = 100
- FIFO RingBuffer
- 超限丢弃最旧 Hint

**查询接口**:
- `get_all()` - 获取所有 Hint
- `get_by_type(hint_type)` - 按类型查询
- `get_by_authority(authority)` - 按主权查询

### CalibrationHintExporter（Hint 导出器）

**功能**:
1. JSON 导出
2. 可读文本导出（工程向）

**示例输出**:
```
[LANDMARK_UNSTABLE]
  authority: MAP_VISION
  landmark: crosswalk_3
  time: 12.3s → 15.8s
  confidence_drop: 0.41
  note: landmark matched/unmatched repeatedly
```

---

## 🔌 如何接入

### 基本接入

```python
from navigation.evidence_alignment_index import EvidenceAlignmentIndex
from navigation.calibration_hint_probe import CalibrationHintProbe

# 创建 AlignmentIndex（来自 Step 9）
alignment_index = EvidenceAlignmentIndex(max_frames=300)

# 创建 Hint Probe
hint_probe = CalibrationHintProbe(
    alignment_index=alignment_index,
    enable_hint_generation=True,
    max_hints=100
)

# 从对齐帧生成 Hint
hints = hint_probe.generate_hints_from_frames(frames)
```

### 导出 Hint

```python
# 导出文本
text_hints = hint_probe.export_text_timeline(base_ts=base_time)
print(text_hints)

# 导出 JSON
json_hints = hint_probe.export_json()

# 按类型查询
unstable_hints = hint_probe.store.get_by_type("LANDMARK_UNSTABLE")
```

---

## 📝 日志规范

### Hint 生成（极低频）

```
[HINT] generated=3 types=LANDMARK_UNSTABLE,AUTHORITY_FLIP
```

仅在：
- 新 Hint 生成
- 导出调用

时打印

---

## ✅ 验收标准

1. ✅ 关闭 Step 10 → 系统行为完全不变
2. ✅ 异常片段 → 至少生成 1 条合理 Hint
3. ✅ Hint 不自动生效、不影响主流程
4. ✅ 导出内容 → 人类能理解"系统在反思什么"
5. ✅ 不引入任何第三方依赖

---

## 📈 为什么 Step 10 是"可学习系统"的准备

99% 的项目只关心：
- "现在用哪个"
- "能不能走"

你这个系统已经开始关心：
- "哪些模式值得反思"
- "系统哪里出了问题"
- "如何知道该学习什么"

### Step 10 直接带来的未来价值

- **系统化识别异常**（不再依赖手动检查）
- **为未来学习系统提供数据源**（Hint 就是学习信号）
- **对外演示"我们不是黑箱"的证据**（系统在反思）
- **多设备协同时的共识基础**（共享 Hint 数据）

---

## 🚫 重要禁令

1. **Step 10 不得参与任何实时决策**
2. **不允许修改 Step 1–9 的任何已有代码**
3. **只从 Step 9（EvidenceAlignmentIndex）读取数据**
4. **所有 Hint 只存在于内存**
5. **Hint 不自动生效、不回写参数**
6. **不涉及任何语言表达 / TTS / UI**
7. **不准改 FSM、不准调阈值、不准回写 LocalMap、不准生成播报文案、不准假装"已经学习"**

---

## 🔮 下一步（Step 11 预告）

"世界描述 → 转译 → 多产品表达体系"

这将是完全独立于导航主系统的一条新工程线。

---

**文档版本**: v1.4.8 Step 10  
**最后更新**: 2025-12-12







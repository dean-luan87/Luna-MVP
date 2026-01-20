# Navigation Foundation Step 9 (v1.4.8)

## 📋 Step 9: Local Map × Confidence Timeline 融合索引层

### 概述

Step 9 是一个工程价值极高、但"不影响线上行为"的模块。

**一句话定义**:
- Step 9 = Local Map × Confidence Timeline 融合索引层
- 让系统"记得住自己当时看到的世界"，并且"说得清自己当时为什么这么做"
- 把"时间侧（Step 8）"和"空间侧（Step 4）"对齐，形成可解释的证据链

---

## 🎯 Step 9 的一句话定位

Step 9 不参与任何实时决策

它只做一件事：把"你当时看到的世界"和"你当时为什么这么判断"对齐

这一步，是你从「可解释系统」走向「可追溯系统」的分水岭。

---

## 📊 为什么 Step 9 必须现在做

### 如果没有 Step 9，未来会发生什么？

- "这个决策是基于哪个地标的？"
- "当时的地图状态是什么？"
- "为什么在这个时候切换到 GPS？"
- 你只能靠：
  - 分别查看 Timeline 和 LocalMap
  - 手动对齐时间戳
  - 主观猜测关联关系

这在单人调试阶段还能忍，一旦进入：
- 多设备
- 多场景
- 多版本

系统就会失控。

---

## 🔄 Step 9 在整体架构中的位置

```
Step 4  Local Map Builder          （空间侧）
Step 8  Authority Confidence Timeline（时间侧）
Step 9  Evidence Alignment         （融合索引层）← 本步
```

👉 Step 9 监听 Step 4 / Step 8  
👉 但反向依赖为 0

---

## 📐 核心设计原则

### 原则 1：只记录"解释所必需的最小信息"

- ✅ 不是全量 dump
- ✅ 不存原始图像或大文本
- ✅ 只保留对齐所需的最小数据

### 原则 2：时间是第一维度

- ✅ 按时间窗对齐
- ✅ 时间连续、可追溯

### 原则 3：可关闭、可裁剪、可回放

- ✅ 可关闭（Feature Flag）
- ✅ 可裁剪（内存上限）
- ✅ 可回放（JSON + Text 导出）

---

## 📊 EvidenceAlignmentFrame 数据模型

### 结构

```python
@dataclass
class EvidenceAlignmentFrame:
    ts: float
    scene: str
    
    # 时间侧（来自 Step 8 / Step 5）
    active_authority: str
    candidate_authority: Optional[str]
    confidence: Dict[str, float]
    takeover_state: str
    hint_active: bool
    
    # 空间侧（来自 Step 4）
    local_map_id: Optional[str]
    recent_node_ids: List[str]
    landmark_ids: List[str]
    match_scores: Dict[str, float]
    
    # 可选解释信息
    reason_trace: List[str]
```

**注意**：
- 不允许存原始图像或大文本内容
- local_map_id 可为空（地图更新之前）
- recent_node_ids 和 landmark_ids 可能为空

---

## ⏱️ 对齐策略

### 时间窗参数

- **ALIGNMENT_WINDOW_SEC = 0.75**（对齐时间窗）
- **NODE_LOOKBACK_SEC = 2.0**（节点回看时间）

### 对齐逻辑

1. **Timeline Frame 到达**（来自 Step 8）
2. **找最近 LocalMapSnapshot**（<= ts）
3. **收集时间窗内的节点和地标匹配**
   - 时间窗：`[ts - node_lookback_sec, ts + alignment_window_sec]`
4. **构建 EvidenceAlignmentFrame**

---

## 🔄 核心模块

### EvidenceAlignmentBuilder（对齐构建器）

**职责**:
- 监听 TimelineFrame（Step 8）
- 监听 LocalMap 更新/landmark match（Step 4）
- 按时间窗进行最近邻对齐
- 构建 EvidenceAlignmentFrame

**要求**:
- Builder 不负责存储
- Builder 不维护历史
- Builder 不做任何判断/过滤

### EvidenceAlignmentIndex（索引层）

**职责**:
- 管理 EvidenceAlignmentFrame 的内存存储
- 提供基础查询能力

**存储策略**:
- RingBuffer（FIFO）
- 最大长度：MAX_ALIGNMENT_FRAMES = 300
- 超限自动丢弃最旧数据

**查询接口**:
- `get_by_time_range(t0, t1)` - 按时间范围查询
- `get_by_authority(authority)` - 按主权查询
- `get_by_local_map(local_map_id)` - 按本地地图 ID 查询

### EvidenceAlignmentExporter（导出器）

**功能**:
1. JSON 导出
2. 人类可读时间轴导出

**示例输出**:
```
t=18.0s | MAP_VISION(0.74) | FSM=TAKEN | scene=OUTDOOR
  ├─ local_map: map_042
  ├─ landmark: crosswalk_3 (0.82)
  └─ nodes: turn_12, curb_7
```

---

## 🔌 如何接入

### 基本接入

```python
from navigation.authority_confidence_timeline_probe import AuthorityConfidenceTimelineProbe
from navigation.evidence_alignment_probe import EvidenceAlignmentProbe

# 创建 Timeline Probe
timeline_probe = AuthorityConfidenceTimelineProbe(
    event_bus=event_bus,
    enable_timeline=True
)

# 创建 Alignment Probe
alignment_probe = EvidenceAlignmentProbe(
    timeline_probe=timeline_probe,
    event_bus=event_bus,
    enable_alignment=True,
    max_frames=300
)

# 自动监听 Step 4 / Step 8 事件并构建对齐帧
```

### 导出对齐时间轴

```python
# 导出文本时间轴
text_timeline = alignment_probe.export_text_timeline()
print(text_timeline)

# 导出 JSON
json_timeline = alignment_probe.export_json()

# 按时间范围查询
frames = alignment_probe.index.get_by_time_range(t0=100.0, t1=200.0)

# 按主权查询
frames = alignment_probe.index.get_by_authority("MAP_VISION")
```

---

## 📝 日志规范

### Alignment 统计（低频）

```
[ALIGN] frames=128 maps=6 authorities=MAP_VISION
```

仅在：
- 新 frame 写入
- RingBuffer 淘汰
- 导出调用

时打印

---

## ✅ 验收标准

1. ✅ 关闭 Step 9 → 系统行为完全不变
2. ✅ 连续运行 → 内存稳定（RingBuffer 限制）
3. ✅ 单条异常决策 → 可追溯对应地图证据
4. ✅ 导出内容 → 人类可读、时间连续
5. ✅ 不引入任何第三方依赖

---

## 📈 为什么 Step 9 是"可追溯系统"的入口

99% 的项目只关心：
- "现在用哪个"
- "能不能走"

你这个系统已经开始关心：
- "为什么当时这么判断"
- "当时的地图状态是什么"
- "这个决策是基于哪个地标的"

### Step 9 直接带来的未来价值

- **Debug 的成本指数级下降**（时间 × 空间对齐）
- **决策可追溯**（每条决策都有对应的地图证据）
- **对外演示"我们不是黑箱"的证据**（完整的证据链）
- **多设备协同时的共识基础**（共享对齐数据）

---

## 🚫 重要禁令

1. **Step 9 不得参与任何实时决策**
2. **不允许修改 Step 4 / Step 8 的任何已有代码**
3. **只通过事件或公开接口读取数据**
4. **所有数据只存在于内存（RingBuffer）**
5. **模块可整体关闭，不影响系统行为**

---

## 🔮 下一步（Step 10 预告）

基于 Step 9 的对齐数据
- 设计一个 "人工/自动校准建议层"
- 但这一步会非常克制，确保不破坏现有的工程主线

---

**文档版本**: v1.4.8 Step 9  
**最后更新**: 2025-12-12







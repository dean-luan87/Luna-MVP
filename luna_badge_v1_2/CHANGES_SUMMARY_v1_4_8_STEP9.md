# v1.4.8 Step 9 Skeleton 变更摘要

**生成日期**: 2025-12-12  
**状态**: ✅ 完成

---

## 📁 新增文件清单

### 核心模块（5个 Python 文件）

1. **`navigation/evidence_alignment_frame.py`**
   - EvidenceAlignmentFrame 数据类
   - 时间侧（Step 8） × 空间侧（Step 4）对齐模型

2. **`navigation/evidence_alignment_builder.py`**
   - EvidenceAlignmentBuilder 类
   - 对齐构建器：监听 TimelineFrame 和 LocalMap 更新
   - 按时间窗进行最近邻对齐

3. **`navigation/evidence_alignment_index.py`**
   - EvidenceAlignmentIndex 类
   - 索引层：内存 RingBuffer 存储
   - 提供查询接口（时间范围、主权、地图 ID）

4. **`navigation/evidence_alignment_exporter.py`**
   - EvidenceAlignmentExporter 类
   - JSON 导出
   - 人类可读时间轴导出

5. **`navigation/evidence_alignment_probe.py`**
   - EvidenceAlignmentProbe 类
   - 桥接器：监听 Step 4 / Step 8 事件

### 文档

6. **`docs/V1_4_8_NAV_FOUNDATION_STEP9.md`**
   - Step 9 完整架构文档
   - 设计原则说明
   - 未来价值说明

### 测试

7. **`demo_runner/test_evidence_alignment_basic.py`**
   - 最小自测脚本
   - 4 个测试场景

---

## 🎯 核心设计

### EvidenceAlignmentFrame（对齐帧）

**数据模型**:
- **时间侧**（来自 Step 8）:
  - active_authority, candidate_authority
  - confidence, takeover_state, hint_active
  
- **空间侧**（来自 Step 4）:
  - local_map_id, recent_node_ids
  - landmark_ids, match_scores

- **解释信息**:
  - reason_trace

### 对齐策略

- **ALIGNMENT_WINDOW_SEC = 0.75**（对齐时间窗）
- **NODE_LOOKBACK_SEC = 2.0**（节点回看时间）

**对齐逻辑**:
1. Timeline Frame 到达（来自 Step 8）
2. 找最近 LocalMapSnapshot（<= ts）
3. 收集时间窗内的节点和地标匹配
4. 构建 EvidenceAlignmentFrame

### 内存限制

- **MAX_ALIGNMENT_FRAMES = 300**（默认）
- 滑动窗口，永不无限增长
- 超限自动丢弃最旧数据

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
```

---

## 🧪 如何运行最小自测

```bash
cd /Users/luanlei/Desktop/Luna-2/luna_badge_v1_2
python3 demo_runner/test_evidence_alignment_basic.py
```

**预期输出**:
- ✅ 基础对齐功能正常
- ✅ 地标收集正常
- ✅ RingBuffer 上限生效
- ✅ 导出功能正常（文本 + JSON）

---

## 📊 测试结果

### 测试场景 1: 基础对齐功能

**结果**: ✅ 通过
- 对齐帧数: 5
- 地图数量: 1
- 主权分布: {'VISUAL': 5}
- local_map_id 可为空: True

### 测试场景 2: 地标收集

**结果**: ✅ 通过
- 总帧数: 5
- 包含地标的帧数: 4
- 地标 ID 列表: ['crosswalk_1']
- 匹配分数: {'crosswalk_1': 0.82}
- 地标收集正常

### 测试场景 3: RingBuffer 上限测试

**结果**: ✅ 通过
- 最大帧数: 10
- 实际帧数: 10
- RingBuffer 生效: True

### 测试场景 4: 导出时间轴

**结果**: ✅ 通过
- 文本时间轴导出成功
- JSON 导出成功（2429 字符）
- 时间轴可读、连续、包含空间侧信息

---

## ✅ 验收标准验证

### ✅ 代码层面

1. ✅ 新增模块可 import（无循环依赖、无类型错误）
2. ✅ 所有 Frame 都包含必要字段（时间侧 + 空间侧）
3. ✅ 对齐逻辑正确（时间窗对齐）
4. ✅ Timeline 可关闭（Feature Flag）

### ✅ 功能层面

1. ✅ 关闭 Step 9 → 系统行为完全不变
2. ✅ 连续运行 → 内存稳定（RingBuffer 限制）
3. ✅ 单条异常决策 → 可追溯对应地图证据（时间 × 空间对齐）
4. ✅ 导出结果 → 人类可读、时间连续
5. ✅ 不引入任何第三方依赖

### ✅ 行为层面

1. ✅ 不影响旧导航行为（只记录，不参与决策）
2. ✅ 不修改 Step 4 / Step 8
3. ✅ 反向依赖为 0

---

## 📝 关键设计原则

### 1. 只记录"解释所必需的最小信息"

- ✅ 不是全量 dump
- ✅ 不存原始图像或大文本
- ✅ 只保留对齐所需的最小数据

### 2. 时间是第一维度

- ✅ 按时间窗对齐
- ✅ 时间连续、可追溯

### 3. 可关闭、可裁剪、可回放

- ✅ 可关闭（Feature Flag）
- ✅ 可裁剪（内存上限）
- ✅ 可回放（JSON + Text 导出）

---

## 🚫 重要禁令

1. **Step 9 不得参与任何实时决策**
2. **不允许修改 Step 4 / Step 8 的任何已有代码**
3. **只通过事件或公开接口读取数据**
4. **所有数据只存在于内存（RingBuffer）**
5. **模块可整体关闭，不影响系统行为**

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

## 🔮 下一步（Step 10 预告）

基于 Step 9 的对齐数据
- 设计一个 "人工/自动校准建议层"
- 但这一步会非常克制，确保不破坏现有的工程主线

---

## 📚 相关文档

- `docs/V1_4_8_NAV_FOUNDATION_STEP9.md`: Step 9 完整架构文档
- `navigation/evidence_alignment_frame.py`: 对齐帧数据模型
- `navigation/evidence_alignment_builder.py`: 对齐构建器
- `navigation/evidence_alignment_index.py`: 索引层
- `navigation/evidence_alignment_exporter.py`: 导出器
- `demo_runner/test_evidence_alignment_basic.py`: 测试示例

---

**变更摘要完成时间**: 2025-12-12  
**状态**: ✅ 所有文件已创建，测试通过







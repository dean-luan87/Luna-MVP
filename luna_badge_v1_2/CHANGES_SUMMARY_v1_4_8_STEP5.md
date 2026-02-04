# v1.4.8 Step 5 Skeleton 变更摘要

**生成日期**: 2025-12-12  
**状态**: ✅ 完成

---

## 📁 新增文件清单

### 核心模块（4个 Python 文件）

1. **`navigation/evidence_models.py`**
   - EvidenceSource 枚举
   - EvidenceKind 枚举
   - Evidence 数据类
   - AuthorityConfidenceSnapshot 数据类

2. **`navigation/evidence_bus.py`**
   - EvidenceBus 类
   - 证据存储/衰减/查询
   - 滑动窗口管理

3. **`navigation/confidence_model.py`**
   - ConfidenceModel 类
   - 证据聚合（衰减后取 max）
   - 分数计算（硬编码权重）
   - 冲突惩罚规则

4. **`navigation/evidence_probe.py`**
   - EvidenceProbe 类
   - 桥接器：Step1-4 事件 → Evidence
   - 证据映射规则
   - 快照计算与发布

### 更新文件

5. **`navigation/events.py`**
   - 新增 Step 5 事件类型：
     - EvidenceIngestEvent
     - AuthorityConfidenceSnapshotEvent
   - 新增 Topic 常量：
     - TOPIC_EVIDENCE_INGEST
     - TOPIC_CONFIDENCE_SNAPSHOT

### 文档

6. **`docs/V1_4_8_NAV_FOUNDATION_STEP5.md`**
   - Step 5 完整架构文档
   - 模块职责说明
   - 事件流说明

### 测试

7. **`demo_runner/test_nav_evidence_confidence_skeleton.py`**
   - 最小自测脚本
   - 两个测试场景

---

## 🎯 模块职责

### EvidenceBus

**职责**: 存储/衰减/查询证据

**接口**:
- `add(evidence: Evidence)` - 添加证据
- `get_window(now_ts: float) -> List[Evidence]` - 获取未过期证据
- `purge(now_ts: float) -> int` - 清理过期证据
- `size() -> int` - 获取证据数量

**日志**:
- `[EVIDENCE_ADD] kind=... src=... value=.. ttl=.. meta=...`
- `[EVIDENCE_PURGE] removed=.. remain=..`

### ConfidenceModel

**职责**: 规则+衰减+冲突惩罚

**接口**:
- `compute(now_ts: float, evidences: List[Evidence]) -> AuthorityConfidenceSnapshot`

**权重表**（硬编码，可解释）:
```
map_vision_score = 0.70 * landmark_match + 0.20 * visual_stability + 0.10 * path_consistency
visual_score = 0.60 * visual_stability + 0.25 * path_consistency + 0.15 * landmark_match
gps_score = 0.70 * gps_stability + 0.30 * path_consistency
```

**冲突惩罚**:
- visual_stability > 0.7 且 gps_stability < 0.4 → gps_score *= 0.7
- landmark_match > 0.75 → map_vision_score = max(map_vision_score, 0.85)

**日志**:
- `[CONF_SNAPSHOT] vis=.. map=.. gps=.. dom=.. gap=.. stability=.. reasons=[..]`

### EvidenceProbe

**职责**: 桥接器（Step1-4 事件 → Evidence）

**证据映射规则**:
1. SceneDecisionEvent → SCENE_INDOOR/OUTDOOR/TRANSITION (ttl=5s)
2. LandmarkMatchEvent → LANDMARK_MATCH (ttl=8s)
3. PositionUpdateEvent → VISUAL_STABILITY (滑动均值, ttl=5s)
4. GPS stability → GPS_STABILITY (手动摄入)

---

## 🔌 如何接入

### 基本接入

```python
from navigation.evidence_probe import EvidenceProbe
from common.event_bus import EventBus
from common.logger import get_logger

event_bus = EventBus()
logger = get_logger("your_module")

# 创建证据探针
probe = EvidenceProbe(event_bus=event_bus, logger=logger, enable_debug_log=True)

# 现在会自动订阅 Step1-4 事件并转换为证据
# 可以通过事件总线发布事件，自动响应
```

### 手动摄入证据

```python
# 手动摄入 GPS stability
probe.ingest_gps_stability(value=0.8, ttl_s=5.0)

# 获取当前快照
snapshot = probe.get_snapshot()
if snapshot:
    print(f"dominant_candidate: {snapshot.dominant_candidate}")
    print(f"confidence_gap: {snapshot.confidence_gap}")
```

### 订阅快照事件

```python
from navigation.events import TOPIC_CONFIDENCE_SNAPSHOT

def on_snapshot(event):
    print(f"Snapshot: {event.dominant_candidate}, gap: {event.confidence_gap}")

event_bus.subscribe(TOPIC_CONFIDENCE_SNAPSHOT, on_snapshot)
```

---

## 🧪 如何运行最小自测

```bash
cd /Users/luanlei/Desktop/Luna-2/luna_badge_v1_2
python3 demo_runner/test_nav_evidence_confidence_skeleton.py
```

**预期输出**:
- ✅ 打印证据添加日志：`[EVIDENCE_ADD] ...`
- ✅ 打印快照日志：`[CONF_SNAPSHOT] ...`
- ✅ 快照输出稳定（不会因单个事件瞬变反复跳）
- ✅ 冲突惩罚正常触发

---

## 📊 测试结果

### 测试场景 1: INDOOR + visual_confidence 高 + landmark_match 高

**结果**: ✅ 通过
- 场景证据摄入正常
- Visual stability 计算正常
- Landmark match 摄入正常
- 快照计算正确：
  - visual_score: 0.663
  - map_vision_score: 0.850 (boost 规则生效)
  - dominant_candidate: MAP_VISION
  - 冲突惩罚正常触发

### 测试场景 2: OUTDOOR + gps_stability 低 + visual_stability 高

**结果**: ✅ 通过
- Visual stability 高（> 0.7）
- GPS stability 低（< 0.4）
- GPS 惩罚正常触发：
  - gps_score 被降低
  - reason_trace 包含 "penalize_gps_due_to_visual_stable_gps_unstable"

---

## 🔍 验收标准验证

### ✅ 代码层面

1. ✅ 新增模块可 import（无循环依赖、无类型错误）
2. ✅ 所有模块都有明确的职责边界
3. ✅ 所有决策都包含 reason_trace

### ✅ 功能层面

1. ✅ 能看到 `[EVIDENCE_ADD]` 日志
2. ✅ 能看到 `[CONF_SNAPSHOT]` 日志
3. ✅ 快照输出稳定（不会因单个事件瞬变反复跳）
4. ✅ 冲突惩罚正常触发

### ✅ 行为层面

1. ✅ 不影响旧导航行为（只插桩，不接管）

---

## 🔌 Step 3 可选接入说明

**注意**: 由于 Step 3 的模块（PositionAuthorityManager）在当前版本中不存在，接入说明如下：

### 如果 Step 3 模块存在

在 `navigation/position_authority_manager.py` 中可谨慎更新：

```python
# 增加可选输入字段
def decide_authority(
    self, 
    context: PositionAuthorityContext,
    snapshot: Optional[AuthorityConfidenceSnapshot] = None  # 新增
) -> PositionAuthorityDecision:
    # 若 snapshot 存在，替代 map_landmark_match
    if snapshot:
        context.map_landmark_match = snapshot.map_vision_score
    
    # 保留原规则优先级
    # ...
```

**配置开关**: `ENABLE_STEP5_SNAPSHOT_INPUT` 默认 False

---

## 📝 关键设计原则

### 1. 只插桩，不接管

- ✅ 所有模块只发布快照事件
- ✅ 不修改现有导航控制逻辑
- ✅ ConfidenceModel 不是融合器，只提供"态势快照"
- ✅ Step 3 仍是裁决者

### 2. 证据衰减

- ✅ 采用指数衰减：`effective = value * exp(-age / ttl_s)`
- ✅ EvidenceBus 负责"保留未过期"
- ✅ 衰减在 ConfidenceModel 里做

### 3. 冲突惩罚（对抗而非平均）

- ✅ Visual 稳定但 GPS 不稳定 → 惩罚 GPS
- ✅ 强地标匹配 → 加速锁定 MAP_VISION

---

## 🚫 重要禁令

1. **不得修改现有导航控制逻辑**
2. **ConfidenceModel 不是融合器**，只提供"态势快照"
3. **Step 3 仍是裁决者**，不得改成融合器
4. **只插桩，不接管**

---

## 📈 下一步

### Step 6: 室内视觉主权接管策略

- 从概念变成接管策略（分阶段接管）
- 决定何时把 Step3 从"读事件"升级为"读 snapshot + 锁定窗口"

---

## 📚 相关文档

- `docs/V1_4_8_NAV_FOUNDATION_STEP5.md`: Step 5 完整架构文档
- `navigation/evidence_models.py`: 数据模型定义
- `demo_runner/test_nav_evidence_confidence_skeleton.py`: 测试示例

---

**变更摘要完成时间**: 2025-12-12  
**状态**: ✅ 所有文件已创建，测试通过







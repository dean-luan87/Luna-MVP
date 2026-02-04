# Navigation Foundation Step 5 (v1.4.8)

## 📋 Step 5: EvidenceBus × ConfidenceModel

### 概述

Step 5 提供证据容器、衰减/过期机制和置信度快照输出（Snapshot）。

**重要原则**:
- Step 5 只做：证据容器 + 衰减/过期 + 置信度快照输出
- Step 3 不得改成融合器：Step 5 只提供"态势快照"，Step 3 仍是裁决者
- 现阶段：只插桩，不接管

---

## 🎯 模块职责

### EvidenceBus（证据总线）

**职责**: 存储/衰减/查询证据

**功能**:
- 维护滑动窗口（默认 window_s=10.0）
- 内部存储：collections.deque
- 提供 add/get_window/purge/size 接口

**衰减函数**:
- 采用简单指数衰减：`effective = value * exp(-age / ttl_s)`
- EvidenceBus 负责"保留未过期"
- 衰减在 ConfidenceModel 里做

**日志插桩**:
- `[EVIDENCE_ADD] kind=... src=... value=.. ttl=.. meta=...`
- `[EVIDENCE_PURGE] removed=.. remain=..`

---

### ConfidenceModel（置信度模型）

**职责**: 规则+衰减+冲突惩罚

**输入/输出**:
- 输入：时间戳 + 证据列表
- 输出：AuthorityConfidenceSnapshot

**证据聚合**:
- 对窗口内 evidence 做衰减后按 kind 聚合（取 max）

**分数计算**（硬编码权重，可解释）:

```
map_vision_score = 
  0.70 * landmark_match +
  0.20 * visual_stability +
  0.10 * path_consistency

visual_score = 
  0.60 * visual_stability +
  0.25 * path_consistency +
  0.15 * landmark_match

gps_score = 
  0.70 * gps_stability +
  0.30 * path_consistency
```

**冲突惩罚**（必须实现，体现"对抗"而非平均）:

- 若 visual_stability > 0.7 且 gps_stability < 0.4：
  - gps_score *= 0.7
  - reason_trace += ["penalize_gps_due_to_visual_stable_gps_unstable"]

- 若 landmark_match > 0.75：
  - map_vision_score = max(map_vision_score, 0.85)
  - reason_trace += ["boost_map_vision_due_to_strong_landmark"]

**dominant_candidate 与 confidence_gap**:
- 取三者最高分为 dominant
- gap = top1 - top2
- stability = clamp(top1, 0..1) * clamp(gap*2, 0..1)

**日志**:
- `[CONF_SNAPSHOT] vis=.. map=.. gps=.. dom=.. gap=.. stability=.. reasons=[..]`

---

### EvidenceProbe（桥接器）

**职责**: 把 Step1–4 输出变成 Evidence

**功能**:
- 订阅 Step1–4 相关事件
- 将它们转成 EvidenceIngestEvent 并送入 EvidenceBus
- 周期性触发 compute，发布 SnapshotEvent

**证据映射规则**（最小实现）:

1. **SceneDecisionEvent**:
   - INDOOR → EvidenceKind.SCENE_INDOOR value=decision.confidence ttl=5s
   - OUTDOOR → SCENE_OUTDOOR ttl=5s
   - TRANSITION → SCENE_TRANSITION ttl=5s

2. **LandmarkMatchEvent**:
   - EvidenceKind.LANDMARK_MATCH value=match_score ttl=8s

3. **Visual stability**:
   - 使用最近 N 个 PositionUpdateEvent 的 visual_confidence 做滑动均值
   - ttl=5s

4. **GPS stability**:
   - 骨架版可留空或从上游提供
   - 代码要支持 future ingest

---

### AuthorityConfidenceSnapshot（核心产物）

**注意**: dominant_candidate 只是"候选态势"，不是裁决结果

**字段说明**:

- `visual_score`: Visual 定位分数
- `map_vision_score`: Map+Vision 融合分数
- `gps_score`: GPS 定位分数
- `dominant_candidate`: 主导候选（"VISUAL" / "MAP_VISION" / "GPS"）
- `confidence_gap`: 置信度差距（top1 - top2）
- `stability`: 稳定性分数
- `decay_state`: 衰减状态（各证据的当前值）
- `reason_trace`: 原因追踪（冲突惩罚等）
- `ts`: 时间戳
- `window_s`: 时间窗口大小

---

## 🔌 Step 3 接入（可选）

在 `navigation/position_authority_manager.py` 中谨慎更新：

- 增加可选输入字段：`snapshot: Optional[AuthorityConfidenceSnapshot]`
- 若 snapshot 存在，仅替代 `map_landmark_match` 的来源为 `snapshot.map_vision_score`
- 但保留原规则优先级：
  - scene == INDOOR -> VISUAL 永远最高
  - navigation_mode == GPS_DOMINANT -> GPS_PRIMARY 仍有效

**配置开关**: `ENABLE_STEP5_SNAPSHOT_INPUT` 默认 False

---

## 📊 事件流

```
Step1-4 事件
  ↓
EvidenceProbe（转换）
  ↓ EvidenceIngestEvent
EvidenceBus（存储）
  ↓
ConfidenceModel（计算）
  ↓ AuthorityConfidenceSnapshotEvent
下游（仅插桩，不接管）
```

---

## 🚫 当前阶段禁令

1. **不得修改现有导航控制逻辑**
2. **ConfidenceModel 不是融合器**，只提供"态势快照"
3. **Step 3 仍是裁决者**，不得改成融合器
4. **只插桩，不接管**

---

## 📈 后续计划

### Step 6: 室内视觉主权接管策略

- 从概念变成接管策略（分阶段接管）
- 决定何时把 Step3 从"读事件"升级为"读 snapshot + 锁定窗口"

---

**文档版本**: v1.4.8 Step 5  
**最后更新**: 2025-12-12







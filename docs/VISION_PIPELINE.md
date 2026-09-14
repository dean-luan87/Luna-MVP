# 视觉流水线整体流程（LV2–LV7）

## Engineering Oriented Flow Spec（Draft v1）

**目标：**
在保证导航实时优先的前提下，实现视觉信息的高效筛选、合理调度、异步建模、可纠错反馈，避免系统过载与认知回路爆炸。

---

## 一、全局时序总览（先给一张"脑图级"流程）

```
[Camera / Vision Sensor]
        ↓
[LV2 Quality Gate]
        ↓
[LV3 Semantic Router]
        ├──▶ [LV4.1 Navigation Executor] ──▶ 即时反馈
        │
        └──▶ [LV4.2 World Modeling Executor]
                    └──（含内容抽取子流程）
                           ↓
                    [LV6 World State Manager]
                           ↑
[LV5 Task-aware Aggregator] ◀───────┘
        ↓
     用户反馈
        ↓
[LV7 Feedback Correction & Update]
```

### 关键原则（写死）

- **实时链路**：LV2 → LV3 → LV4.1 → LV5
- **异步链路**：LV3 → LV4.2 → LV6
- **任何模块不得逆向调用上游**
- **只有 LV4.1 / 上层控制中心 可以请求重新观察**

---

## 二、模块级时序与运算逻辑（逐层）

下面每一层我都按统一结构写清楚：
- 运算目标
- 输入
- 核心逻辑
- 输出
- 调度 / 生命周期规则

---

### LV2｜Quality Gate（质量过滤层）

#### 运算目标

用最小算力，筛掉不值得浪费后端资源的帧

#### 输入

- 原始图像帧（含时间戳、相机参数）

#### 核心运算逻辑

**纯物理质量评估，不涉及任何语义**

1. **清晰度评估**
   - 模糊度（Laplacian variance）
   - 高频信息比例

2. **稳定性评估**
   - 连续帧特征点位移

3. **曝光评估**
   - 亮度直方图

4. **冗余评估**
   - 帧间相似度（hash / SSIM）

统一输出一个：`quality_score ∈ [0,1]`

#### 输出

```python
{
  "frame_id": "...",
  "quality_score": 0.78,
  "pass": true
}
```

#### 调度规则

- 同步执行
- 极低延迟（毫秒级）
- 可并行
- 不得触发重拍

#### 本模块禁止做什么

- ❌ 禁止做任何语义理解
- ❌ 禁止调用下游模块
- ❌ 禁止修改输入帧
- ❌ 禁止触发重拍请求

---

### LV3｜Semantic Router（一级语义调度层）

#### 运算目标

决定这帧是否必须进入实时链路

#### 输入

- LV2 合格图像帧
- 当前任务态（来自上层控制中心）
- 是否在导航
- 是否存在危险态
- 是否空闲

#### 核心运算逻辑

**只做粗分类，不做理解**

判断问题只有一个：

> 这帧是否"可能影响当前任务的即时决策"？

输出两类：
- `navigation_candidate`
- `non_navigation_candidate`

⚠️ **分类阈值随任务态动态变化**

#### 输出

```python
{
  "frame_id": "...",
  "route": "navigation | non_navigation",
  "priority": "high | low"
}
```

#### 调度规则

- 同步
- 可被任务态热更新
- 策略来源只允许：
  - 上层控制中心
  - LV4.1 导航即时反馈

#### 本模块禁止做什么

- ❌ 禁止做深度语义理解
- ❌ 禁止直接调用 LV4.1 或 LV4.2
- ❌ 禁止修改任务态
- ❌ 禁止触发感知重拍

---

### LV4｜并行执行层（Executors）

**真正消耗算力的地方，必须严格调度**

---

### LV4.1｜Navigation Executor（主线）

#### 运算目标

保证行走安全与路径正确

#### 输入

- 导航类帧
- 当前位姿 / 方向
- 世界模型弱先验（可选）

#### 核心逻辑

- 导航标识识别
- 路径判断
- 危险检测
- 偏航判断

#### 输出

```python
{
  "navigation_action": "...",
  "confidence": "high | medium | low",
  "requires_reobserve": false
}
```

#### 调度规则

- 最高优先级
- 可抢占其他 LV4 任务
- 唯一允许请求前端重拍的模块之一

#### 本模块禁止做什么

- ❌ 禁止写世界模型（只读）
- ❌ 禁止调用 LV4.2
- ❌ 禁止修改任务态
- ❌ 禁止触发内容抽取

---

### LV4.2｜World Modeling Executor（异步）

#### 运算目标

构建低频、可复用的世界结构

#### 输入

- 非导航帧
- 历史世界模型（只读）

#### 核心逻辑

1. **稳定实体识别**
   - 建筑
   - 出入口
   - 通道
   - 广告牌（作为地标）

2. **内容抽取（子流程）**
   - 广告 / 通告
   - 粗四要素：时间、地点、品牌、功能

3. **历史复用判断**
   - 是否已存在
   - 是否需要更新

⚠️ **不生成最终记忆，只生成候选增量**

#### 输出

```python
{
  "entity_candidates": [...],
  "content_candidates": [...],
  "confidence": "low | medium"
}
```

#### 调度规则

- 异步
- 可暂停 / 降频
- 在导航激活时自动让路

#### 本模块禁止做什么

- ❌ 禁止影响导航决策
- ❌ 禁止直接写 Library
- ❌ 禁止调用 LV4.1
- ❌ 禁止触发重拍
- ❌ 禁止修改任务态

---

### LV5｜Task-aware Aggregator（整合反馈层）

#### 运算目标

把系统状态翻译成"人能理解的反馈"

#### 输入

- LV4.1 导航结果
- 当前任务链状态
- 可选：世界模型弱提示

#### 核心逻辑

- 按任务选择信息
- 合成反馈语句
- 生成兜底策略

#### 输出（强制格式）

```python
{
  "task_context": "...",
  "action_suggestion": "...",
  "confidence_level": "high | medium | low",
  "fallback_instruction": "...",
  "update_trigger": true
}
```

#### 调度规则

- 同步
- 不写记忆
- 不触发感知

#### 本模块禁止做什么

- ❌ 禁止写世界模型
- ❌ 禁止触发感知
- ❌ 禁止修改任务态
- ❌ 禁止调用 LV4.1 / LV4.2

---

### LV6｜World State Manager（暂略细节）

只接收 LV4.2 的候选结果

负责合并、去重、时效判断、版本管理

（本轮先冻结接口，不展开）

#### 本模块禁止做什么

- ❌ 禁止直接调用 LV4.1
- ❌ 禁止影响导航决策
- ❌ 禁止触发感知重拍

---

### LV7｜Feedback Correction & Update（纠错层）

#### 运算目标

纠正"我刚才说的话"，而不是立刻重构世界

#### 输入

- 用户否定反馈
- 行为反证（走反、未执行）
- 新一轮感知结果

#### 核心逻辑

- 标记低可信反馈
- 触发 LV5 更新
- 对 LV6 打可信度标记（不直接改）

#### 输出

```python
{
  "correction_type": "...",
  "confidence_adjustment": "down",
  "re_feedback_required": true
}
```

#### 调度规则

- 异步
- 不阻塞导航
- 不触发感知重拍

#### 本模块禁止做什么

- ❌ 禁止直接修改世界模型
- ❌ 禁止触发感知重拍
- ❌ 禁止影响导航决策
- ❌ 禁止调用 LV4.1 / LV4.2

---

## 三、工程落地指导（给 Cursor 用的）

### 你现在可以立刻做的 3 件事

1. **按 LV2–LV7 建目录 / 模块边界**

```
core/vision/
├── lv2_quality_gate.py
├── lv3_semantic_router.py
├── lv4/
│   ├── navigation_executor.py
│   └── world_modeling_executor.py
├── lv5_task_aggregator.py
├── lv6_world_state_manager.py
└── lv7_feedback_correction.py
```

2. **给每个模块文件头写一句：**

```python
# -*- coding: utf-8 -*-
"""
LV2: Quality Gate（质量过滤层）

本模块禁止做什么：
- ❌ 禁止做任何语义理解
- ❌ 禁止调用下游模块
- ❌ 禁止修改输入帧
- ❌ 禁止触发重拍请求
"""
```

3. **把所有"跨层调用"列为 TODO / REFACTOR**

```python
# TODO: REFACTOR - 跨层调用
# 当前：LV5 直接读取 LV4.1 结果
# 目标：通过事件总线 / 消息队列解耦
```

---

## 四、数据流与接口规范

### 实时链路数据流

```
Camera → LV2 → LV3 → LV4.1 → LV5 → User
```

**特点：**
- 同步执行
- 低延迟（< 100ms）
- 可中断（用户反馈）

### 异步链路数据流

```
Camera → LV2 → LV3 → LV4.2 → LV6 → (World Model)
```

**特点：**
- 异步执行
- 可暂停 / 降频
- 不阻塞实时链路

### 反馈链路数据流

```
User → LV7 → LV5 → (Update Feedback)
         ↓
      LV6 (Mark Confidence)
```

**特点：**
- 异步执行
- 不触发感知重拍
- 只标记，不直接修改

---

## 五、调度优先级规则（写死）

### 优先级排序

1. **P0（最高）**：LV4.1 Navigation Executor
   - 可抢占所有其他任务
   - 唯一允许请求重拍

2. **P1（高）**：LV2 Quality Gate + LV3 Semantic Router
   - 必须同步执行
   - 不得被抢占

3. **P2（中）**：LV5 Task-aware Aggregator
   - 同步执行
   - 不阻塞导航

4. **P3（低）**：LV4.2 World Modeling Executor
   - 异步执行
   - 可暂停 / 降频

5. **P4（最低）**：LV6 World State Manager + LV7 Feedback Correction
   - 完全异步
   - 不阻塞任何实时链路

### 抢占规则

- LV4.1 可以抢占 LV4.2
- LV4.1 可以抢占 LV6
- LV4.1 可以抢占 LV7
- 其他模块不得互相抢占

---

## 六、错误处理与降级策略

### LV2 失败

- 降级：跳过质量检查，直接进入 LV3
- 日志：记录质量评估失败原因

### LV3 失败

- 降级：默认路由到 `non_navigation`
- 日志：记录路由失败原因

### LV4.1 失败

- 降级：使用上一次有效结果
- 日志：记录导航执行失败原因
- 告警：触发上层控制中心

### LV4.2 失败

- 降级：静默失败，不影响实时链路
- 日志：记录世界建模失败原因

### LV5 失败

- 降级：使用兜底反馈语句
- 日志：记录聚合失败原因

---

## 七、性能指标与监控

### 实时链路性能指标

- LV2 延迟：< 10ms
- LV3 延迟：< 20ms
- LV4.1 延迟：< 50ms
- LV5 延迟：< 20ms
- **总延迟：< 100ms**

### 异步链路性能指标

- LV4.2 处理时间：< 500ms（可接受）
- LV6 处理时间：< 200ms（可接受）
- LV7 处理时间：< 300ms（可接受）

### 监控指标

- 帧率（FPS）
- 各层延迟分布
- 错误率
- 资源占用（CPU / GPU / Memory）

---

## 八、阶段性冻结结论

- ✅ 这条链路工程上闭环
- ✅ 实时与异步完全解耦
- ✅ 广告 / 内容不会污染导航
- ✅ 后续可以无痛扩展多模态

---

## 九、下一步建议

- **B**：拿 v1.8.5 的代码，对照这份流程逐个模块映射
- **C**：把 LV4.2 的 world schema 正式定稿

**你这一步已经是系统架构冻结前的最后一次大对齐，非常关键，也非常正确。**

---

## 附录：模块映射检查清单

### v1.8.5 模块映射

- [ ] `SceneRegistry` → LV6 World State Manager
- [ ] `RiskAdvisoryService` → LV4.1 Navigation Executor（危险检测部分）
- [ ] `TaskPlanner` → LV5 Task-aware Aggregator
- [ ] `MemoryRegistry` → LV6 World State Manager
- [ ] `UserReportRouter` → LV7 Feedback Correction & Update

### 待实现模块

- [ ] LV2 Quality Gate
- [ ] LV3 Semantic Router
- [ ] LV4.1 Navigation Executor（完整实现）
- [ ] LV4.2 World Modeling Executor
- [ ] LV5 Task-aware Aggregator（完整实现）
- [ ] LV6 World State Manager（接口冻结）
- [ ] LV7 Feedback Correction & Update

### 跨层调用检查

- [ ] 检查所有模块是否遵守"禁止逆向调用上游"规则
- [ ] 检查所有模块是否遵守"禁止跨层调用"规则
- [ ] 检查所有模块是否遵守调度优先级规则



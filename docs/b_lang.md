# B-Lang：B 模块内部语言与职责定义
## 冻结版 · v1.0

---

## 0. 文件地位

B-Lang 定义了 **B 模块内部允许存在的语言、概念与职责边界**。

- B 可以在内部使用丰富、冗余、不稳定的感知语言
- 但 **B 对外（跨模块）只能通过 DTL 说话**
- 本文件用于：
  - 约束 B 的能力边界
  - 防止 B 逐渐演化为"世界模型"或"决策中心"

---

## 1. B 的核心角色（再次确认）

> **B 不是世界理解者，  
而是 C 的远距行为风险放大器 + 本地知识缓存。**

B 的所有能力，必须服务于以下两点之一：
1. 是否影响 C 在未来 t_horizon 内的行为
2. 是否补全 C 感知范围之外的必要背景信息

---

## 2. B 内部允许存在的语言（Internal-Only）

以下语言 **只允许存在于 B 内部**，  
**禁止**直接跨模块输出。

---

### 2.1 远距感知语言（Perception Signals）

```text
- distant_crowd_density
- crowd_flow_direction
- vehicle_crossing_trajectory
- surface_irregularity_score
- temporary_obstacle_presence
- visual_occlusion_level
```

**说明：**
- 这些是 **连续、噪声大、不稳定** 的信号
- 仅用于 B 内部评估
- 不得直接影响 C

---

### 2.2 环境候选描述（Candidate Descriptions）

```text
- possible_market_area
- possible_construction_zone
- possible_intersection_ahead
```

**说明：**
- 仅为 B 内部的"假设"
- 不具备确定性
- 不允许以任何形式直接传递给 C

---

### 2.3 本地知识缓存（Local Knowledge Cache）

```text
- known_intersection
- known_traffic_light
- known_crosswalk
- known_building_function
```

**说明：**
- 来源可能是：
  - 地图
  - 互联网
  - 历史记忆
- 不主动推送
- 仅在 C 请求或行为相关时使用

---

## 3. B 的内部评估语言（Evaluation Layer）

这是 B 的"思考层"，但不是"表达层"。

---

### 3.1 行为影响评估（Behavior Impact Evaluation）

```text
- predicted_path_risk
- predicted_conflict_probability
- predicted_comfort_drop
```

**说明：**
- 这些评估用于回答：
  > "是否影响 C 在 t_horizon 内的行为？"
- 评估结果必须被 **翻译成 DTL.ActionImpact**
- 无法翻译 → 不允许输出

---

### 3.2 信息生命周期标注

B 必须在内部区分：

- **EphemeralSignal**   # 行人、车辆、临时事件
- **PersistentSignal**  # 红绿灯、路口、固定结构

**规则：**
- EphemeralSignal 必须携带有效期
- PersistentSignal 可写入长期缓存
- 重启后：
  - EphemeralSignal 默认失效
  - PersistentSignal 可复用

---

## 4. B 对外唯一允许的语言（External Output）

### 4.1 唯一合法输出形式

- **DTL.ActionImpact**

或

- **NO_OP / SILENT**

---

### 4.2 明确禁止的对外语言

B 严禁输出以下内容：
- 世界状态判断（如：环境切换、进入市场）
- 抽象环境分类
- 连续世界建模结果
- "我看到什么"式描述

---

## 5. NO_OP / SILENT 的定义（非常重要）

### 5.1 NO_OP 的含义

> **NO_OP ≠ 没有工作**  
> **NO_OP = 已评估，但判断对 C 行为无影响**

这是 B 的 **成熟能力标志**，不是缺失能力。

---

### 5.2 触发 NO_OP 的典型场景

- 风险存在但距离过远（FAR）
- 变化不足以影响当前 t_horizon
- 场景被 gate（如室内、镜头不稳定）
- 信息为低价值背景，不影响行为

---

## 6. B 的职责边界（冻结）

### B 负责

- 远距风险放大
- 路况变化补丁
- 本地环境背景缓存
- 行为前视评估

### B 不负责

- 实时导航控制
- 近场决策
- 世界全量建模
- 情绪、心理或高层语义理解

---

## 7. 与 DTL 的关系（强约束）

- **B 的任何对外输出：**
  - 必须可映射到 DTL
  - 无法映射：
    - 必须丢弃或保留在内部
- **任何绕过 DTL 的字段：**
  - 视为架构违规

---

## 8. 冻结原则

- 本文件为 B-Lang v1.0 冻结版
- 修改必须：
  - 同步升级版本号
  - 同步审查 DTL 兼容性
  - 禁止私下扩展外部语言

---

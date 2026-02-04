# B–C Definition & Translation Layer (DTL)
## 冻结版 · v1.1

---

## 0. 文件地位（宪法级）

DTL（Definition & Translation Layer）是 B 模块与 C 模块之间的**唯一合法通信层**。

- B 与 C 不得直接交换原始语义
- 所有跨模块信息必须映射到 DTL 定义
- DTL 不做感知、不做判断、不做学习  
  **只定义语义、生命周期、权限边界与转译规则**

---

## 1. 时间语义（Time Semantics）

### 1.1 标准时间字段

```text
t_now           : float   # 当前时间（秒，统一系统时间）
t_horizon       : float   # 行为预测窗口（秒，仅由 C 提供）
t_valid_until   : float   # 信息/影响的有效截止时间
```

### 1.2 生命周期原则（冻结）

DTL 明确区分两类信息：

- **Ephemeral（时效信息）**
  - 行人、车辆、临时障碍、流动事件
  - 必须携带 `t_valid_until`
  - 设备重启后默认失效
- **Persistent（长期信息）**
  - 红绿灯、路口、固定结构
  - 可跨 session 复用
  - 不强制要求 `t_valid_until`

### 1.3 时间约束

- **t_now**：系统统一提供，B/C 不可修改
- **t_horizon**：
  - 只能由 C 设定
  - B 不得自行推断或调整
  - B 的判断语义必须满足：
    > "在 t_horizon 内，是否影响当前行为"

---

## 2. 距离语义（Distance Semantics）

### 2.1 距离单位与分区

- **唯一距离单位**：米（meter）

```text
NEAR : 0m  – 3m
MID  : 3m  – 10m
FAR  : >10m
```

### 2.2 场景化 gating 原则（冻结）

- **室内场景**：
  - B 不生效
  - C 代替 B 承担环境记忆与判断
- **室外 / 开阔场景**：
  - B 可对 MID / FAR 区域提供影响评估

DTL 负责裁剪 B 在无资格场景下的输出。

---

## 3. 路况与通行语义（Path & Traversability）

### 3.1 核心原则

> DTL 不描述"世界是什么"，  
> 只描述"是否可安全、舒适地通过"。

### 3.2 PathState（唯一合法状态）

```text
CLEAR        # 可正常通行
DEGRADED     # 可通行，但风险上升
UNCERTAIN    # 通行性不确定
BLOCKED      # 不可通行
```

### 3.3 PathReason（可多选）

```text
CROWD             # 人流密集
VEHICLE_FLOW      # 车流 / 轨迹冲突
SURFACE_CHANGE    # 路面变化（台阶、坑洼、积水）
TEMP_OBSTACLE     # 临时障碍
STRUCTURE_CHANGE  # 结构变化（施工、封闭）
SIGNAL_CONTROL    # 信号控制（红绿灯、闸机）
```

### 3.4 价值优先级（冻结）

路径选择遵循以下优先级：

> **安全 > 舒适 > 距离**

---

## 4. 行为影响语义（Action Impact）

### 4.1 ImpactType（固定枚举）

```text
SAFE_CONTINUE     # 可继续当前行为
NEED_SLOW_DOWN   # 需要减速
NEED_STOP        # 需要停止
NEED_DETOUR      # 需要绕行
PATH_UNCERTAIN   # 路径不确定（提升感知/谨慎）
NO_OP            # 明确表示"不影响 C 行为"
```

### 4.2 ActionImpact 标准结构

```python
{
  "impact_type": "NEED_SLOW_DOWN",
  "confidence": 0.0,
  "effective_zone": "MID",
  "path_state": "DEGRADED",
  "reasons": ["CROWD"],
  "time_horizon": 6.0,
  "t_valid_until": 123.4
}
```

### 4.3 输出约束（冻结）

- **B 只能** 输出 ActionImpact
- **若评估结果对 C 行为无影响**：
  - 必须输出 `NO_OP` 或保持沉默
- **B 禁止** 输出：
  - 世界状态
  - 环境分类
  - 抽象场景描述

---

## 5. 回执语义（Feedback Semantics）

### 5.1 C → B 回执结构

```python
{
  "advice_id": "uuid",
  "accepted": true,
  "executed": false,
  "outcome": "SAFE_PASS | REROUTED | STOPPED",
  "latency_sec": 1.2
}
```

### 5.2 回执原则（冻结）

- **建议不存在"失败"概念**
- **可能情况仅包括**：
  - 建议被采纳但未执行（C 的自主判断）
  - 正常执行并完成
- **系统错误**（crash / 不可用）：
  - 属于系统监控层
  - 不属于 DTL 语义

---

## 6. DTL 的职责与非职责

### DTL 负责

- 语义定义
- 生命周期区分
- 权限与 gating
- 跨模块转译

### DTL 不负责

- 感知
- 判断
- 策略生成
- 在线学习

---

## 7. 冻结原则

- 本文件为 DTL v1.1 冻结版
- 任何修改必须：
  - 升级版本号
  - 同步更新 B-Lang / C-Lang
  - 禁止私下扩展字段

---

# v1.8.5 C1 Controller 工程搭建文档

## 一、C1 的工程定位

**一句话定位**：
C1 不是一个模型，也不是一个算法，而是一个"视觉是否工作、如何工作"的调度与安全控制系统。

**核心职责**：
- 决定是否允许抽帧
- 决定抽哪一帧
- 决定抽多少（fps）
- 决定是否暂停视觉
- 决定是否强制安全优先

**架构位置**：
```
Camera / Sensor
      ↓
[C1: Continuous Vision Controller]   ← C1 在这里
      ↓
LV2 Quality Gate
      ↓
LV3 Semantic Router
      ↓
LV4 Executors
```

**关键点**：
- C1 在 PipelineController 之前
- C1 有权短路整个视觉链路
- C1 不做识别，只做"是否看、怎么看"

---

## 二、模块结构

### 2.1 目录结构

```
c1_controller/
├── __init__.py              # 模块导出
├── c1_controller.py         # 主控制器（唯一对外入口）
├── c1_types.py              # 结构化输入输出（C1State, C1Input, C1Decision）
├── c1_state.py              # 状态机基础逻辑
├── c1_triggers.py           # 状态触发条件
├── c1_policy.py             # 抽帧 / 观察策略
├── c1_governor.py           # 抽帧频率与资源控制
├── c1_safety_guard.py       # 安全 & 兜底机制
└── c1_privacy_guard.py      # 隐私场景规则
```

### 2.2 模块职责

| 模块 | 职责 |
|------|------|
| `c1_controller.py` | 主控制器，唯一对外接口，协调所有子模块 |
| `c1_types.py` | 定义 C1State、C1Input、C1Decision 数据结构 |
| `c1_state.py` | 状态职责对齐表，状态到配置的映射 |
| `c1_triggers.py` | 根据输入信号评估状态转换 |
| `c1_policy.py` | 根据状态和输入信号决定抽帧策略（动态抽帧） |
| `c1_governor.py` | 限制 fps 在合理范围内（防算力爆炸、防完全失明） |
| `c1_safety_guard.py` | 检测严重晃动、频闪、静态遮挡、恶意画面 |
| `c1_privacy_guard.py` | 隐私场景硬规则（Class A/B/C） |

---

## 三、核心状态机

### 3.1 状态定义

```python
class C1State(Enum):
    STABLE = "stable"            # 环境稳定
    TRANSITION = "transition"    # 即将变化
    ALERT = "alert"              # 突发风险
    SUSPENDED = "suspended"      # 感知暂停（晃动/隐私）
```

**注意**：不要一开始就加太多状态，这 4 个已经覆盖 90% 真实世界。

### 3.2 状态职责对齐

| 状态 | 是否抽帧 | 抽帧频率 | 观察范围 |
|------|---------|---------|---------|
| STABLE | 可 | 低（2 fps） | 前方 |
| TRANSITION | 可 | 中（5 fps） | 前方 + 周边 |
| ALERT | 必须 | 高（10 fps） | 威胁源 |
| SUSPENDED | 禁止 | 0 | 无 |

---

## 四、输入信号（不依赖复杂模型）

### 4.1 C1Input 结构

```python
@dataclass
class C1Input:
    frame_timestamp: float
    
    # 运动 / 稳定性
    motion_score: float          # 镜头晃动强度（0-1，越高越晃）
    frame_diff_score: float      # 画面变化幅度（0-1，越高变化越大）
    
    # 世界与记忆
    next_scene_hint: Optional[str]   # 未来场景提示（来自地图/记忆）
    risk_hint: Optional[str]         # 潜在风险提示
    
    # 用户与系统
    privacy_zone: Optional[str]      # 是否处于隐私区域（Class A/B/C）
    user_camera_override: bool        # 用户是否强制要求开启
```

**关键点**：
- 所有信号都是"廉价信号"，不依赖复杂模型（YOLO/OCR/Qwen）
- 所有信号都可以先 mock，不影响工程推进

### 4.2 输入信号来源（未来实现）

| 信号 | 来源 |
|------|------|
| `motion_score` | IMU / 视觉特征点位移 |
| `frame_diff_score` | 帧间差异计算 |
| `next_scene_hint` | 地图 / 记忆系统 |
| `risk_hint` | 风险系统 |
| `privacy_zone` | 场景识别 / 用户设置 |
| `user_camera_override` | 用户输入 |

---

## 五、输出决策

### 5.1 C1Decision 结构

```python
@dataclass
class C1Decision:
    allow_frame: bool                # 是否允许抽帧
    target_fps: int                  # 建议抽帧频率（0 表示暂停）
    observation_mode: str            # forward / surround / local
    priority: str                    # safety / navigation / environment
    reason: str                      # 决策原因（用于调试 & 解释）
    state: Optional[C1State] = None  # 当前 C1 状态
```

**关键点**：
- PipelineController 只看这一个结果
- `reason` 字段用于调试和解释，帮助理解决策过程

---

## 六、关键机制

### 6.1 动态抽帧（不是定时）

**位置**：`c1_policy.py`

**逻辑**：
- 输入：C1State + C1Input
- 输出：是否抽帧 + target_fps
- **抽帧是状态机结果，不是计时器**

**调整规则**：
- TRANSITION 状态：如果 `next_scene_hint` 存在，提高 fps
- ALERT 状态：如果 `risk_hint` 存在，提高 fps
- STABLE 状态：如果 `frame_diff` 很低，降低 fps（节省资源）

### 6.2 严重晃动 → 暂停视觉

**位置**：`c1_safety_guard.py`

**逻辑**：
```python
if motion_score > HARD_SHAKE_THRESHOLD (0.8):
    state = C1State.SUSPENDED
```

**恢复条件**：
- `motion_score` 连续 N 帧（默认 5 帧）低于阈值
- 再触发一次"环境重识别"

### 6.3 隐私场景硬规则

**位置**：`c1_privacy_guard.py`

**规则**：
- **Class A（公共环境）**：正常
- **Class B（半隐私）**：默认关闭，用户不可强开
- **Class C（强隐私）**：强制关闭，不可协商

**关键结论**：
**Class B 不允许用户强制开启镜头**（即使 `user_camera_override=True`）

### 6.4 抽帧频率 Governor

**位置**：`c1_governor.py`

**限制**：
- 最小 fps：1（防完全失明）
- 最大 fps：15（防算力爆炸）
- ALERT 状态最大 fps：10（不能无限高）

### 6.5 频闪 / 静态遮挡 / 恶意画面

**位置**：`c1_safety_guard.py`

**检测**：
- `frame_diff` 长时间 ≈ 0 → 静态遮挡
- `frame_diff` 高频剧烈变化 → 频闪攻击
- 行为：降频 / 暂停 / 标记异常

---

## 七、决策流程

### 7.1 决策流程图

```
C1Input
  ↓
[1] 检查隐私阻断（最高优先级）
  ├─ Class C → SUSPENDED
  └─ Class B → SUSPENDED（即使 user_camera_override=True）
  ↓
[2] 检查安全阻断（严重晃动等）
  ├─ motion_score > 0.8 → SUSPENDED
  └─ 频闪/静态遮挡 → 降频/暂停
  ↓
[3] 评估状态转换（如果没有被阻断）
  ├─ risk_hint → ALERT
  ├─ next_scene_hint → TRANSITION
  └─ 默认 → STABLE
  ↓
[4] 应用策略（决定抽帧频率）
  └─ 根据状态和输入信号调整 fps
  ↓
[5] 应用频率限制（Governor）
  └─ 限制在 [MIN_FPS, MAX_FPS] 范围内
  ↓
[6] 生成 C1Decision
```

### 7.2 优先级顺序

1. **隐私阻断**（最高优先级）
2. **安全阻断**（严重晃动等）
3. **状态转换**（ALERT > TRANSITION > STABLE）
4. **策略应用**（动态调整 fps）
5. **频率限制**（Governor）

---

## 八、使用示例

### 8.1 基本使用

```python
from c1_controller import C1Controller, C1Input
import time

# 初始化 C1Controller
c1 = C1Controller()

# 创建输入信号
input_signal = C1Input(
    frame_timestamp=time.time(),
    motion_score=0.1,
    frame_diff_score=0.3,
    next_scene_hint="即将进入商场",
)

# 获取决策
decision = c1.decide(input_signal)

# 使用决策结果
if decision.allow_frame:
    # 允许抽帧，使用 decision.target_fps
    print(f"允许抽帧，目标 fps: {decision.target_fps}")
else:
    # 禁止抽帧
    print("禁止抽帧（视觉已暂停）")
```

### 8.2 集成到 PipelineController

**TODO**：在 `PipelineController.process_frame()` 之前调用 C1Controller

```python
# 在 PipelineController.process_frame() 中
def process_frame(self, frame, ...):
    # 1. 准备 C1Input（从 frame 和其他信号构建）
    c1_input = self._build_c1_input(frame, ...)
    
    # 2. 调用 C1Controller
    c1_decision = self.c1_controller.decide(c1_input)
    
    # 3. 如果 C1 禁止抽帧，直接返回
    if not c1_decision.allow_frame:
        return {"c1_decision": c1_decision, "skipped": True}
    
    # 4. 根据 decision.target_fps 决定是否处理这一帧
    # （需要实现帧率控制逻辑）
    
    # 5. 继续正常的 Pipeline 流程
    ...
```

---

## 九、测试验证

### 9.1 Mock 测试脚本

**文件**：`examples/c1_controller_demo.py`

**测试场景**：
1. ✅ STABLE 状态（正常环境）
2. ✅ TRANSITION 状态（场景变化提示）
3. ✅ ALERT 状态（风险提示）
4. ✅ SUSPENDED 状态（严重晃动）
5. ✅ SUSPENDED 状态（隐私区域 Class C）
6. ✅ SUSPENDED 状态（隐私区域 Class B，用户不可强开）
7. ✅ 恢复（从 SUSPENDED 恢复到 STABLE）

**运行方式**：
```bash
cd /Users/luanlei/Desktop/Luna-2
python3 examples/c1_controller_demo.py
```

**测试结果**：
✅ 所有场景测试通过

---

## 十、工程状态

### 10.1 已完成

- ✅ 目录结构和模块文件
- ✅ C1State、C1Input、C1Decision 数据结构
- ✅ 状态机基础逻辑
- ✅ 状态触发条件
- ✅ 抽帧/观察策略
- ✅ 频率控制（Governor）
- ✅ 安全守卫（严重晃动、频闪、静态遮挡）
- ✅ 隐私守卫（Class A/B/C 规则）
- ✅ 主控制器（C1Controller）
- ✅ Mock 测试脚本

### 10.2 待完成

- ⏳ 集成到 PipelineController（在 `process_frame()` 之前调用）
- ⏳ 实现真实的输入信号构建（从 frame/IMU/地图/记忆系统）
- ⏳ 实现帧率控制逻辑（根据 `target_fps` 决定是否处理这一帧）
- ⏳ 单元测试（更详细的测试覆盖）

---

## 十一、下一步

### 11.1 集成到 PipelineController

**任务**：
1. 在 `PipelineController.__init__()` 中初始化 `C1Controller`
2. 在 `PipelineController.process_frame()` 之前调用 `C1Controller.decide()`
3. 根据 `C1Decision.allow_frame` 决定是否继续处理
4. 根据 `C1Decision.target_fps` 实现帧率控制

### 11.2 实现真实输入信号

**任务**：
1. 从 frame 计算 `motion_score` 和 `frame_diff_score`
2. 从地图/记忆系统获取 `next_scene_hint`
3. 从风险系统获取 `risk_hint`
4. 从场景识别/用户设置获取 `privacy_zone`

### 11.3 单元测试

**任务**：
1. 测试每个状态转换
2. 测试频率限制（Governor）
3. 测试安全守卫（严重晃动、频闪、静态遮挡）
4. 测试隐私守卫（Class A/B/C 规则）

---

## 十二、设计原则

### 12.1 核心原则

1. **C1 不做识别**：只做"是否看、怎么看"
2. **C1 有权短路**：可以禁止整个视觉链路
3. **C1 在 Pipeline 之前**：所有视觉处理都要经过 C1
4. **动态抽帧**：不是定时，而是状态机结果
5. **安全优先**：隐私和安全阻断优先级最高

### 12.2 工程原则

1. **最小可用**：先实现核心功能，再逐步扩展
2. **可测试**：所有输入信号都可以 mock
3. **可解释**：每个决策都有 `reason` 字段
4. **可扩展**：状态和策略都可以扩展

---

## 十三、总结

**C1 Controller 工程搭建完成** ✅

**当前状态**：
- ✅ 核心模块已实现
- ✅ 状态机已定义
- ✅ 安全/隐私守卫已实现
- ✅ Mock 测试通过

**下一步**：
- ⏳ 集成到 PipelineController
- ⏳ 实现真实输入信号
- ⏳ 单元测试

**关键价值**：
C1 解决了绝大多数系统都翻车的问题："什么时候不该看"。这是一个非常高级、而且极少有人认真做的能力。

---

**文档版本**：v1.0  
**最后更新**：2024-12-19



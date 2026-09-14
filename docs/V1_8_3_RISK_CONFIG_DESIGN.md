# v1.8.3 风险评估参数化设计

## Prompt 3 结果：参数抽象设计

### 1. 当前实现分析

**文件**: `core/risk_assessor.py`

**当前硬编码条件**:

#### 1.1 关键词检测（第47-80行）

**水边风险关键词**:
```python
water_keywords = ["water", "水", "河", "湖", "池", "海", "edge", "边缘"]
```

**道路风险关键词**:
```python
road_keywords = ["road", "路", "马路", "街道", "car", "车", "traffic", "交通"]
```

#### 1.2 LV2 → LV1 升级阈值（第58-75行）

**TTC 阈值**:
```python
if motion_state.estimated_ttc is not None and motion_state.estimated_ttc <= 3.0:
    # LV1: 立即风险
```

**距离阈值**:
- 当前代码中没有明确的距离阈值判断
- 但 `assess_risk()` 函数接受 `distance` 参数，暗示需要距离判断

#### 1.3 风险类型优先级（隐含）

- 水边风险 (`water_edge`) 和道路风险 (`road`) 使用相同的判断逻辑
- 没有区分不同风险类型的严重程度

---

### 2. 隐含判断条件清单

| 条件类型 | 当前值 | 位置 | 说明 |
|---------|--------|------|------|
| **TTC 临界阈值** | `3.0` 秒 | 第58行 | 碰撞时间阈值，≤ 3.0s 升级为 LV1 |
| **水边关键词列表** | 8 个关键词 | 第47行 | 检测水边风险的关键词 |
| **道路关键词列表** | 8 个关键词 | 第60行 | 检测道路风险的关键词 |
| **距离阈值** | 未实现 | - | 当前代码接受但未使用 |
| **风险类型优先级** | 未区分 | - | 所有风险类型使用相同逻辑 |

---

### 3. RiskConfig 结构设计

#### 方案 A：dataclass 结构（推荐）

```python
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class RiskTypeConfig:
    """单个风险类型的配置"""
    keywords: List[str]  # 关键词列表
    ttc_threshold: float  # TTC 阈值（秒）
    distance_threshold: Optional[float] = None  # 距离阈值（米），None 表示不使用
    priority: int = 1  # 优先级（1=低，2=中，3=高）

@dataclass
class RiskConfig:
    """风险评估配置"""
    # 全局阈值
    global_ttc_critical: float = 3.0  # 全局 TTC 临界值（秒）
    global_min_safe_distance: Optional[float] = None  # 全局最小安全距离（米）
    
    # 风险类型配置
    water_edge: RiskTypeConfig = None
    road: RiskTypeConfig = None
    obstacle: RiskTypeConfig = None
    stair: RiskTypeConfig = None
    
    def __post_init__(self):
        """初始化默认值"""
        if self.water_edge is None:
            self.water_edge = RiskTypeConfig(
                keywords=["water", "水", "河", "湖", "池", "海", "edge", "边缘"],
                ttc_threshold=3.0,
                distance_threshold=None,
                priority=3
            )
        if self.road is None:
            self.road = RiskTypeConfig(
                keywords=["road", "路", "马路", "街道", "car", "车", "traffic", "交通"],
                ttc_threshold=3.0,
                distance_threshold=None,
                priority=3
            )
        if self.obstacle is None:
            self.road = RiskTypeConfig(
                keywords=["obstacle", "障碍", "block", "阻挡", "wall", "墙"],
                ttc_threshold=5.0,
                distance_threshold=2.0,
                priority=2
            )
        if self.stair is None:
            self.stair = RiskTypeConfig(
                keywords=["stair", "楼梯", "step", "台阶"],
                ttc_threshold=4.0,
                distance_threshold=1.5,
                priority=2
            )
```

#### 方案 B：Dict 结构（简化版）

```python
from typing import Dict, Any, List, Optional

RiskConfig = Dict[str, Any]

# 默认配置
DEFAULT_RISK_CONFIG: RiskConfig = {
    # 全局阈值
    "global_ttc_critical": 3.0,  # 秒
    "global_min_safe_distance": None,  # 米
    
    # 风险类型配置
    "risk_types": {
        "water_edge": {
            "keywords": ["water", "水", "河", "湖", "池", "海", "edge", "边缘"],
            "ttc_threshold": 3.0,
            "distance_threshold": None,
            "priority": 3
        },
        "road": {
            "keywords": ["road", "路", "马路", "街道", "car", "车", "traffic", "交通"],
            "ttc_threshold": 3.0,
            "distance_threshold": None,
            "priority": 3
        },
        "obstacle": {
            "keywords": ["obstacle", "障碍", "block", "阻挡", "wall", "墙"],
            "ttc_threshold": 5.0,
            "distance_threshold": 2.0,
            "priority": 2
        },
        "stair": {
            "keywords": ["stair", "楼梯", "step", "台阶"],
            "ttc_threshold": 4.0,
            "distance_threshold": 1.5,
            "priority": 2
        }
    }
}
```

---

### 4. 推荐方案：dataclass（可读性 + 可调试）

**优点**:
- ✅ 类型安全（IDE 自动补全）
- ✅ 可读性强（结构清晰）
- ✅ 可调试（`print(config)` 直接输出）
- ✅ 支持默认值（`__post_init__`）

**使用示例**:
```python
# 创建默认配置
config = RiskConfig()

# 自定义配置
custom_config = RiskConfig(
    global_ttc_critical=2.5,  # 更严格的 TTC
    water_edge=RiskTypeConfig(
        keywords=["water", "水", "河"],
        ttc_threshold=2.0,
        priority=3
    )
)

# 调试输出
print(config)  # 直接打印所有配置
print(config.water_edge.ttc_threshold)  # 访问具体值
```

---

### 5. 函数签名修改建议（不破坏现有接口）

**当前签名**:
```python
def assess_risk(scene_state: Any, motion_state: Optional[MotionState] = None) -> RiskResult:
```

**修改后签名**:
```python
def assess_risk(
    scene_state: Any, 
    motion_state: Optional[MotionState] = None,
    config: Optional[RiskConfig] = None  # 新增，默认 None 使用内置默认值
) -> RiskResult:
```

**向后兼容性**:
- ✅ 现有调用 `assess_risk(scene_state, motion_state)` 仍然有效
- ✅ `config=None` 时使用内置默认配置
- ✅ 新代码可以传入自定义配置

---

### 6. 配置参数完整清单

| 参数路径 | 类型 | 默认值 | 说明 |
|---------|------|--------|------|
| `global_ttc_critical` | `float` | `3.0` | 全局 TTC 临界值（秒） |
| `global_min_safe_distance` | `Optional[float]` | `None` | 全局最小安全距离（米） |
| `water_edge.keywords` | `List[str]` | `["water", "水", ...]` | 水边风险关键词 |
| `water_edge.ttc_threshold` | `float` | `3.0` | 水边 TTC 阈值 |
| `water_edge.distance_threshold` | `Optional[float]` | `None` | 水边距离阈值 |
| `water_edge.priority` | `int` | `3` | 水边风险优先级 |
| `road.keywords` | `List[str]` | `["road", "路", ...]` | 道路风险关键词 |
| `road.ttc_threshold` | `float` | `3.0` | 道路 TTC 阈值 |
| `road.distance_threshold` | `Optional[float]` | `None` | 道路距离阈值 |
| `road.priority` | `int` | `3` | 道路风险优先级 |
| `obstacle.keywords` | `List[str]` | `["obstacle", ...]` | 障碍物风险关键词 |
| `obstacle.ttc_threshold` | `float` | `5.0` | 障碍物 TTC 阈值 |
| `obstacle.distance_threshold` | `float` | `2.0` | 障碍物距离阈值 |
| `obstacle.priority` | `int` | `2` | 障碍物风险优先级 |
| `stair.keywords` | `List[str]` | `["stair", ...]` | 楼梯风险关键词 |
| `stair.ttc_threshold` | `float` | `4.0` | 楼梯 TTC 阈值 |
| `stair.distance_threshold` | `float` | `1.5` | 楼梯距离阈值 |
| `stair.priority` | `int` | `2` | 楼梯风险优先级 |

---

### 7. 实现建议（最小改动）

**步骤 1**: 在 `risk_assessor.py` 中添加 `RiskConfig` 定义

**步骤 2**: 修改 `assess_risk()` 函数，添加 `config` 参数

**步骤 3**: 在函数内部使用 `config` 替代硬编码值

**关键原则**:
- ✅ `config=None` 时使用内置默认配置
- ✅ 不改变现有调用接口
- ✅ 保持函数行为一致性

---

## 结论

**推荐方案**: 使用 `dataclass` 结构的 `RiskConfig`

**优势**:
1. ✅ 可读性强：结构清晰，IDE 自动补全
2. ✅ 可调试：直接 `print(config)` 查看所有参数
3. ✅ 类型安全：避免参数名拼写错误
4. ✅ 向后兼容：现有代码无需修改

**下一步**: 实现 `RiskConfig` 并修改 `assess_risk()` 函数签名（保持向后兼容）



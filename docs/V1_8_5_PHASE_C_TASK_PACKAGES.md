# v1.8.5 Phase C 任务包（Cursor 可执行）

**状态**：✅ 工程任务清单  
**日期**：2024-12-XX  
**版本**：v1.8.5 Phase C

---

## 任务包执行顺序

**必须按顺序执行，保证不返工、不互相打架**：
1. **包 A**：TaskPlanner + RiskBias（最容易先跑通）
2. **包 B**：PositionState + Relocalization Gate（全局护栏）
3. **包 C**：UserReport Router（接口预留）

---

## 📦 包 A：TaskPlanner + RiskBias

### A1. 文件清单

```
core/task_chain/
  __init__.py
  types.py                # RiskBias / ContextBundle
  task_planner.py         # TaskPlanner（扩展 risk_cost）
examples/
  phase_c_task_chain_with_risk_demo.py
```

### A2. 函数签名与数据结构

**core/task_chain/types.py**：

```python
@dataclass
class RiskBias:
    """风险偏置（来自 risk 模块聚合后的"区域风险偏置"）"""
    risk_level: float          # 0.0 ~ 1.0
    risk_attention_boost: float # 0.0 ~ 1.0
    avoid_bias: float          # 0.0 ~ 1.0
    reasons: List[Dict[str, Any]]  # 可追责来源

@dataclass
class ContextBundle:
    """上下文包（任务链消费的统一接口）"""
    scene: Optional[SceneState]
    map_hint: MapHint
    memory_bias: Optional[ExperienceMemory]
    risk_bias: Optional[RiskBias]  # NEW
```

**core/task_chain/task_planner.py**：

```python
class TaskPlanner:
    def choose_path(
        self,
        paths: List[Path],
        context: ContextBundle,
        risk_weight: float = 0.4,  # 风险权重
    ) -> Tuple[Path, float]:
        """
        选择路径（基于上下文，包含风险）
        
        评分公式：
        final_score = base_utility - length_cost - map_risk_cost 
                    - memory_discomfort_cost - risk_cost
        
        其中：
        - risk_cost = risk_bias.risk_level * risk_weight
        """
```

### A3. 验收标准

- ✅ RiskBias 正确集成到 ContextBundle
- ✅ TaskPlanner 正确计算 risk_cost
- ✅ Demo 运行：捷径更短但靠近水边（risk 高）→ 选安全路
- ✅ 可追责：输出 reasons（来自 risk/map/memory 的贡献项）

---

## 📦 包 B：PositionState + Relocalization Gate

### B1. 文件清单

```
core/world_model/common/
  types.py                # PositionState 扩展字段
  relocalization_gate.py  # 统一重定位闸门（NEW）
core/world_model/scene/
  scene_registry.py       # 增加 relocalization gate
core/world_model/memory/
  memory_registry.py      # 增加 relocalization gate
  candidate_pool.py       # 增加 relocalization gate
core/world_model/library/
  library_registry.py     # 增加 relocalization gate
examples/
  phase_c_relocalization_demo.py
```

### B2. 函数签名与数据结构

**core/world_model/common/types.py**（扩展）：

```python
@dataclass
class PositionState:
    position: Tuple[float, float]
    stability_score: float
    stable: bool
    source: str = "vision"              # "vision" | "gps" | "fused"
    drift_suspected: bool = False       # NEW: 识别到失衡/漂移
    relocalizing: bool = False          # NEW: 正在重定位
    anchor_gps: Optional[Tuple[float, float]] = None  # NEW: GPS 弱锚点
```

**core/world_model/common/relocalization_gate.py**（NEW）：

```python
def check_relocalization_gate(position_state: PositionState) -> bool:
    """
    统一重定位闸门（全局护栏）
    
    规则：
    - 如果 drift_suspected=True 或 relocalizing=True，返回 False
    - 否则返回 True
    
    返回 False 时：
    - SceneRegistry：冻结 current_scene，不切
    - MemoryRegistry：禁止写入
    - CandidatePool：禁止升级
    - Library：不消费
    """
```

### B3. 验收标准

- ✅ PositionState 扩展字段正确
- ✅ 统一重定位闸门在所有 Registry 中生效
- ✅ Demo 运行：正常走路 → 视觉失衡跳变 → 冻结 → GPS 弱锚点恢复 → 解冻
- ✅ 不污染：relocalizing/drift 状态下，三库不写入、不升级

---

## 📦 包 C：UserReport Router

### C1. 文件清单

```
core/world_model/interfaces/
  __init__.py
  user_report_iface.py    # UserReportEvent（NEW）
core/world_model/memory/
  user_report_router.py   # 路由逻辑（NEW）
examples/
  phase_c_user_report_demo.py
```

### C2. 函数签名与数据结构

**core/world_model/interfaces/user_report_iface.py**（NEW）：

```python
@dataclass
class UserReportEvent:
    """用户报告事件（一期接口）"""
    raw_text: str
    report_type: str       # "DISCOMFORT" | "FACT_CONFIRM" | "FACT_CONFLICT" | "PREFERENCE"
    tags: List[str]
    claimed_fact: Optional[Dict[str, Any]] = None
    intensity: Optional[float] = None
    ts: float = 0.0
```

**core/world_model/memory/user_report_router.py**（NEW）：

```python
class UserReportRouter:
    """
    用户报告路由器
    
    分流规则（写死，防污染）：
    - DISCOMFORT → 只进 Memory（体验资产）
    - PREFERENCE → 只进 Memory（偏好）
    - FACT_CONFIRM / FACT_CONFLICT → 只进 CandidatePool（事实信号）
    - 任何 user_report 不允许直接写 Library
    
    额外护栏：
    - user_report 不提升 confidence
    - 限频：同一用户、同一 Scene、同一 claim_type，在窗口内只允许计 1 次 support
    """
    
    def route(
        self,
        event: UserReportEvent,
        scene_id: str,
        map_id: Optional[str],
        position_state: PositionState,
        memory: MemoryRegistry,
    ) -> Dict[str, Any]:
        """路由用户报告到 Memory 或 CandidatePool"""
```

### C3. 验收标准

- ✅ UserReportEvent 数据结构正确
- ✅ 分流规则正确（DISCOMFORT → Memory，FACT_* → CandidatePool）
- ✅ 限频机制生效（同一 claim_type 在窗口内只计 1 次）
- ✅ Demo 运行：用户说"这里路滑"→ Memory，用户说"这里封路了"→ CandidatePool

---

## 统一验收标准（三块一起做时，必须满足）

1. ✅ **不污染**：relocalizing/drift 状态下，三库（Memory/Candidate/Library）不写入、不升级
2. ✅ **连续性**：Scene 不会因为 GPS 抖动或视觉失衡频繁切换
3. ✅ **可追责**：TaskPlanner 每次选择路径，都能输出 reasons（来自 risk/map/memory 的贡献项）
4. ✅ **可回归**：demo 运行结果固定（seed 固定、输入脚本固定）

---

**文档版本**：v1.8.5 Phase C 任务包  
**最后更新**：2024-12-XX  
**状态**：✅ 工程任务清单



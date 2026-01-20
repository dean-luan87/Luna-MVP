# Luna Badge v1.8.1 任务拆解（Engineering Breakdown）

**版本类型**: 能力改造型（Behavior Upgrade）  
**新增核心概念**: Observer Mode（视角观察模式）  
**原则**: 最小侵入式改造，不破坏 v1.8 冻结态

---

## 版本总览

### 改造原则
- ❌ 不新增模型
- ❌ 不新增硬件
- ❌ 不改变主流程
- ✅ 只改「状态机 + 策略 + 输出层」

### 核心能力
- **Observer Mode**: 主动观察、确认、干预
- **三态输出**: BACKGROUND / CONFIRM / INTERVENE
- **行为判断升级**: 导航 → 行为建议
- **人工求助策略**: 复杂场景降级

---

## 任务优先级

| 优先级 | 模块 | 预计工时 |
|--------|------|----------|
| P0 | Observer Mode 管理器 | 2-3天 |
| P0 | 三态视觉输出 | 2-3天 |
| P0 | 行为判断适配 | 2天 |
| P1 | 任务链联动 | 1-2天 |
| P1 | 人工求助 | 1-2天 |
| P2 | 社会规则弹性 | 1天 |
| P2 | 日志与指标 | 1天 |

---

## 模块 1: Observer Mode 状态管理器

**文件**: `core/observer_mode_manager.py`  
**优先级**: P0  
**依赖**: 无

### 任务 1.1: 状态定义与数据结构

**输入**:
- 无

**输出**:
- `ObserverMode` 数据类定义
- 状态枚举：`background | confirm | intervene`

**代码结构**:
```python
@dataclass
class ObserverMode:
    active: bool
    level: str  # "background" | "confirm" | "intervene"
    last_trigger: float  # timestamp
    confidence: float  # 0.0 - 1.0
```

**验收标准**:
- [ ] 数据类定义完整
- [ ] 类型注解正确
- [ ] 支持序列化（JSON）

---

### 任务 1.2: 激活条件判断

**输入**:
- `navigation_state`: 导航状态
- `scene`: 当前场景
- `user_utterance`: 用户语音输入

**输出**:
- `observer_mode.active = True` 或 `False`

**触发条件（任一满足）**:
- `navigation_state == "active"`
- `scene in ["hospital", "mall", "metro", "gov_hall"]`
- `user_utterance` 包含关键词：["帮我看", "不确定", "是不是"]

**代码位置**:
```python
def should_activate_observer_mode(
    navigation_state: str,
    scene: str,
    user_utterance: str
) -> bool:
    # 实现激活逻辑
```

**验收标准**:
- [ ] 三个触发条件都能正确判断
- [ ] 关键词匹配支持模糊匹配
- [ ] 返回布尔值

---

### 任务 1.3: 降频/退出逻辑

**输入**:
- `task_state`: 任务状态
- `user_command`: 用户指令
- `destination_reached`: 是否到达目的地

**输出**:
- `observer_mode.active = False` 或降级到 `background`

**逻辑规则**:
1. 主任务暂停 → 降频（只监听危险，level = "background"）
2. 用户明确说"停一下/不用看了" → 关闭（active = False）
3. 到达目的地 → 自动关闭（active = False）

**代码位置**:
```python
def update_observer_mode(
    observer_mode: ObserverMode,
    task_state: str,
    user_command: str,
    destination_reached: bool
) -> ObserverMode:
    # 实现降频/退出逻辑
```

**验收标准**:
- [ ] 三种退出条件都能正确处理
- [ ] 降频时保持 active=True，但 level 降级
- [ ] 退出时 active=False

---

## 模块 2: 视觉识别输出重构（三态输出）

**文件**: `core/vision_output_controller.py`  
**优先级**: P0  
**依赖**: 模块 1

### 任务 2.1: 输出态枚举定义

**输入**:
- 无

**输出**:
- `VisionOutputState` 枚举类

**代码结构**:
```python
class VisionOutputState(Enum):
    BACKGROUND = "background"
    CONFIRM = "confirm"
    INTERVENE = "intervene"
```

**验收标准**:
- [ ] 枚举定义完整
- [ ] 支持字符串转换

---

### 任务 2.2: 状态判定规则

**输入**:
- `risk_level`: 风险等级
- `has_fork`: 是否有分叉
- `target_visible`: 目标是否可见

**输出**:
- `VisionOutputState` 枚举值

**判定规则**:
| 条件 | 输出态 |
|------|--------|
| 无风险 + 无分叉 | BACKGROUND |
| 分叉 / 目标确认 | CONFIRM |
| 危险环境 | INTERVENE |

**代码位置**:
```python
def determine_output_state(
    risk_level: str,
    has_fork: bool,
    target_visible: bool
) -> VisionOutputState:
    # 实现判定逻辑
```

**验收标准**:
- [ ] 三种状态都能正确判定
- [ ] 优先级：INTERVENE > CONFIRM > BACKGROUND
- [ ] 边界条件处理正确

---

### 任务 2.3: 输出模板标准化

**输入**:
- `output_state`: VisionOutputState
- `context`: 上下文信息（目标名称、危险描述等）

**输出**:
- 标准化的语音输出文本

**模板定义**:
- BACKGROUND: "我在看着，前方通道正常。"
- CONFIRM: "你现在对着的是【X】，对吗？"
- INTERVENE: "停一下，前方是【危险描述】。"

**强制规则**:
- INTERVENE 必须打断当前播报（interrupt=True）
- CONFIRM 必须等待用户 Yes/No（需要响应）

**代码位置**:
```python
def generate_output_text(
    output_state: VisionOutputState,
    context: Dict[str, Any]
) -> Tuple[str, bool, bool]:  # (text, interrupt, wait_response)
    # 实现模板生成
```

**验收标准**:
- [ ] 三种模板都能正确生成
- [ ] INTERVENE 返回 interrupt=True
- [ ] CONFIRM 返回 wait_response=True
- [ ] 模板文本符合规范

---

## 模块 3: 导航 → 行为判断升级

**文件**: `core/behavior_judgement_adapter.py`  
**优先级**: P0  
**依赖**: 现有导航模块

### 任务 3.1: 复用已有能力映射

**输入**:
- 现有导航判断结果

**输出**:
- 行为判断结果

**映射规则**:
- `NAV_OFF_ROUTE` → `BEHAVIOR_DIRECTION_ERROR`
- `PATH_BLOCKED` → `VIEW_NOT_PASSABLE`
- `SUGGEST_REROUTE` → `SUGGEST_TURN_AROUND`

**代码位置**:
```python
def adapt_navigation_to_behavior(
    nav_result: NavigationResult
) -> BehaviorJudgement:
    # 实现映射逻辑
```

**验收标准**:
- [ ] 所有导航状态都能正确映射
- [ ] 不触发重新规划（v1.8.1 限制）
- [ ] 只给动作级建议

---

### 任务 3.2: 行为建议输出

**输入**:
- `behavior_type`: 行为类型
- `context`: 上下文信息

**输出**:
- 标准化的行为建议文本

**输出示例**:
- "你现在面对的方向不对，建议原地转身。"

**代码位置**:
```python
def generate_behavior_suggestion(
    behavior_type: str,
    context: Dict[str, Any]
) -> str:
    # 实现建议生成
```

**验收标准**:
- [ ] 建议文本清晰明确
- [ ] 不包含导航规划指令
- [ ] 只给动作级建议

---

## 模块 4: 任务链 × Observer Mode 联动

**文件**: `core/task_chain_manager.py`（修改现有文件）  
**优先级**: P1  
**依赖**: 模块 1, 现有任务链模块

### 任务 4.1: 任务链新增字段

**输入**:
- 现有任务链数据结构

**输出**:
- 增加 `observer_mode` 字段

**字段定义**:
```python
{
    "observer_mode": {
        "active": bool,
        "level": str,
        ...
    }
}
```

**验收标准**:
- [ ] 字段定义完整
- [ ] 向后兼容（现有任务链不受影响）
- [ ] 支持序列化

---

### 任务 4.2: 继承规则实现

**输入**:
- 主任务状态
- 插入任务状态

**输出**:
- 更新后的 observer_mode 状态

**继承规则**:
1. 主任务 active → observer_mode = true
2. 插入任务 → observer_mode 自动继承
3. 插入任务结束 → 回到主任务 + observer_mode 继续

**代码位置**:
```python
def sync_observer_mode_with_task_chain(
    main_task: Task,
    inserted_task: Optional[Task]
) -> ObserverMode:
    # 实现继承逻辑
```

**验收标准**:
- [ ] 三种继承规则都能正确处理
- [ ] 插入任务不影响主任务的 observer_mode
- [ ] 任务恢复时 observer_mode 正确恢复

---

### 任务 4.3: 等待态逻辑

**输入**:
- `waiting_state`: 是否处于等待态
- `observer_mode`: 当前观察模式

**输出**:
- 更新后的 observer_mode（只允许 INTERVENE）

**逻辑规则**:
- `waiting_state == True` → observer_mode 保持 active，但只允许 INTERVENE

**代码位置**:
```python
def handle_waiting_state_observer_mode(
    waiting_state: bool,
    observer_mode: ObserverMode
) -> ObserverMode:
    # 实现等待态逻辑
```

**验收标准**:
- [ ] 等待态时只允许 INTERVENE
- [ ] 等待态时保持 active=True
- [ ] 等待态结束后恢复正常

---

## 模块 5: 社会规则弹性提示

**文件**: `core/social_rule_hint.py`  
**优先级**: P2  
**依赖**: 模块 2

### 任务 5.1: 触发条件判断

**输入**:
- `path_type`: 路径类型
- `has_hazard_sign`: 是否有高危标识
- `vision_confirmed`: 视觉确认结果

**输出**:
- 是否触发社会规则提示

**触发条件（全部满足）**:
- 非标准路径
- 无高危标识
- 视觉确认通过

**代码位置**:
```python
def should_trigger_social_rule_hint(
    path_type: str,
    has_hazard_sign: bool,
    vision_confirmed: bool
) -> bool:
    # 实现触发判断
```

**验收标准**:
- [ ] 三个条件都能正确判断
- [ ] 只有全部满足才触发

---

### 任务 5.2: 输出模板实现

**输入**:
- `risk_assessment`: 风险评估结果

**输出**:
- 标准化的提示文本

**模板**:
"这不是常规通行路线，但我判断前方地面平整、没有车流，风险较低。是否继续？"

**必须包含**:
- 明确"非标准"
- 明确"风险判断"
- 明确"选择权在用户"

**代码位置**:
```python
def generate_social_rule_hint(
    risk_assessment: Dict[str, Any]
) -> str:
    # 实现模板生成
```

**验收标准**:
- [ ] 模板包含三个必须要素
- [ ] 文本清晰明确
- [ ] 给用户选择权

---

## 模块 6: 人工求助策略模块

**文件**: `core/human_assist_fallback.py`  
**优先级**: P1  
**依赖**: 模块 1, 模块 2

### 任务 6.1: 触发规则实现

**输入**:
- `confirm_fail_count`: CONFIRM 失败次数
- `observer_confidence`: Observer 置信度
- `scene_risk_level`: 场景风险等级

**输出**:
- 是否触发人工求助

**触发规则（任一满足）**:
- 连续 2 次 CONFIRM 失败
- Observer confidence < threshold（如 0.3）
- scene_risk_level == "HIGH"

**代码位置**:
```python
def should_trigger_human_assist(
    confirm_fail_count: int,
    observer_confidence: float,
    scene_risk_level: str
) -> bool:
    # 实现触发判断
```

**验收标准**:
- [ ] 三个触发条件都能正确判断
- [ ] 阈值可配置

---

### 任务 6.2: 输出模板实现

**输入**:
- `has_staff_detected`: 是否检测到工作人员
- `staff_direction`: 工作人员方向（如有）

**输出**:
- 标准化的求助提示文本

**模板**:
- 有工作人员: "这个场景不太适合我继续指引，建议你向右前方的工作人员求助。"
- 无工作人员: "这个场景不太适合我继续指引，建议你询问路人或前往前台。"

**代码位置**:
```python
def generate_human_assist_hint(
    has_staff_detected: bool,
    staff_direction: Optional[str]
) -> str:
    # 实现模板生成
```

**验收标准**:
- [ ] 两种场景都能正确处理
- [ ] 文本清晰明确
- [ ] 给出具体建议

---

## 模块 7: 日志与评估

**文件**: `core/observer_mode_logger.py`  
**优先级**: P2  
**依赖**: 所有模块

### 任务 7.1: 新增日志字段

**输入**:
- Observer Mode 事件

**输出**:
- 结构化日志数据

**字段定义**:
```python
{
    "observer_mode_triggered": bool,
    "observer_level": str,  # "background" | "confirm" | "intervene"
    "intervene_reason": str,  # 如 "construction_detected"
    "user_response": str,  # "accepted" | "rejected" | "ignored"
    "timestamp": float
}
```

**验收标准**:
- [ ] 所有字段都能正确记录
- [ ] 支持 JSON 序列化
- [ ] 时间戳准确

---

### 任务 7.2: 核心评估指标计算

**输入**:
- 日志数据

**输出**:
- 评估指标

**核心指标**:
- CONFIRM 成功率 = accepted / (accepted + rejected + ignored)
- INTERVENE 提前率 = 危险前干预次数 / 总干预次数
- 人工求助触发率 = 触发次数 / 总会话次数
- 用户中断率 = 用户主动中断次数 / 总会话次数

**代码位置**:
```python
def calculate_observer_metrics(
    log_data: List[Dict[str, Any]]
) -> Dict[str, float]:
    # 实现指标计算
```

**验收标准**:
- [ ] 四个指标都能正确计算
- [ ] 处理边界情况（除零等）
- [ ] 返回格式标准化

---

## v1.8.1 验收清单（Definition of Done）

### 功能验收
- [ ] 能在导航中"主动打断危险"（INTERVENE）
- [ ] 能在关键节点"先确认再行动"（CONFIRM）
- [ ] 能在复杂场景"主动建议找人"（人工求助）
- [ ] Observer Mode 能正确激活和退出
- [ ] 任务链联动正常工作

### 技术验收
- [ ] 无新增模型依赖
- [ ] 无新硬件依赖
- [ ] 不破坏 v1.8 冻结态
- [ ] 向后兼容现有功能
- [ ] 日志和指标正常记录

### 测试验收
- [ ] 单元测试覆盖率 > 80%
- [ ] 集成测试通过
- [ ] 场景测试通过（医院/商场/地铁/政务大厅）
- [ ] 性能测试通过（无显著延迟）

---

## 关键判断

**v1.8.1 不是功能升级，是"责任边界与交互哲学"的第一次落地。**

这意味着：
- 不是简单的功能堆砌
- 是交互范式的转变
- 需要仔细设计用户体验
- 需要完整的评估体系

---

## 下一步

1. **按模块拆成 Cursor 可直接执行的任务卡** ✅（本文档）
2. **v1.8.1 的 PRD**（待创建）

---

**文档版本**: v1.0  
**创建日期**: 2025-12-29  
**维护者**: V1.8.1 开发团队



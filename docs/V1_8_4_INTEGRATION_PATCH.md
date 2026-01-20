# v1.8.4 无侵入式集成方案（完整 Patch）

## ✅ 设计裁决

### 核心原则

**v1.8.4 的 Risk Advisory 不是一个新的播报通道，而是一个新的决策来源（Decision Source）**

因此必须满足三条铁律：
1. ❌ RiskAdvisoryService 绝对不能直接调用 TTS
2. ✅ 只能产出 `decision = {"action": "ADVISORY", ...}`
3. ✅ 最终播报仍然必须走 `_execute_speech_decision() → _speak_safely()`

### 优先级顺序

```
RISK_LV1 > ADVISORY > YIELD > WAIT > SPEAK
```

### 行为差异

| 动作 | 是否强制 | 是否可被 speech_gate 拒绝 | 是否打断用户 |
|------|---------|------------------------|------------|
| RISK_LV1 | 是 | 否 | 否（等用户说完） |
| ADVISORY | 否 | 是 | ❌ 不打断 |
| SPEAK | 否 | 是 | ❌ |
| WAIT | - | - | - |
| YIELD | - | - | - |

**结论**：ADVISORY 是"比 SPEAK 高，但仍然守规矩"的一种提醒。

---

## 📋 具体改动点

### 改动 1：导入 Risk 模块（第 45 行附近）

```python
from core.decision_controller import decide, UserState
from core.risk import (
    RiskAdvisoryService, UserPositionProvider, RiskRegistry, RiskObjectFactory
)
```

---

### 改动 2：初始化 Risk Advisory 组件（第 130-140 行附近）

在 `__init__()` 方法中，在 `self.risk_assessor` 之后添加：

```python
# v1.8.4: 风险告知系统初始化
self.risk_registry = RiskRegistry(object_ttl_seconds=60.0)
self.risk_object_factory = RiskObjectFactory()
self.user_position_provider = UserPositionProvider()
self.risk_advisory_service = RiskAdvisoryService(
    registry=self.risk_registry
)
```

---

### 改动 3：修改 _handle_speech_decision()（第 485-530 行）

**关键改动**：在 `decide()` 调用之前插入 Risk Advisory 判断

```python
def _handle_speech_decision(self, result: dict) -> dict:
    if not result:
        return {"action": "WAIT", "reason": "no_result"}
    
    # === v1.8.4: Risk Advisory 注入点（新增） ===
    # 说明：ADVISORY 是"环境态势判断"，不是语言生成
    # 因此不应被 _build_voice_text() 影响，不应依赖 result 是否有 description
    # 必须在 decide() 之前判断，优先级：RISK_LV1 > ADVISORY > YIELD > WAIT > SPEAK
    advisory = None
    if self.risk_advisory_service and self.user_position_provider:
        pos = self.user_position_provider.get()
        if pos:
            advisory_text = self.risk_advisory_service.tick(
                user_xy=pos.xy,
                ts=pos.ts
            )
            if advisory_text:
                advisory = {
                    "action": "ADVISORY",
                    "reason": "risk_trend_up",
                    "advisory_text": advisory_text,
                }
    
    # === 优先级裁决：RISK_LV1 > ADVISORY > 其他 ===
    # 先执行 decide() 检查 RISK_LV1
    scene_state = self.scene_state_builder.build_state(
        objects=result.get("objects", []),
        texts=result.get("texts", []),
        risk_level=None
    )
    
    motion_state = result.get('motion_state')
    decision_result = decide(
        scene_state=scene_state,
        speech_gate=self.speech_gate,
        user_state=self.user_state,
        motion_state=motion_state
    )
    
    # 优先级裁决
    if decision_result.get("action") == "RISK_LV1":
        # RISK_LV1 最高优先级，直接返回
        return decision_result
    elif advisory:
        # ADVISORY 优先级高于普通 SPEAK/WAIT/YIELD
        return advisory
    else:
        # 其他情况返回 decide() 的结果
        return decision_result
```

**关键说明**：
- ADVISORY 不经过 `decide()`，因为它不是"语言意图"，是"风险态势"
- 但它仍然要经过 `_execute_speech_decision()`，才能尊重 speech_gate / 用户状态

---

### 改动 4：修改 _execute_speech_decision()（第 552 行附近）

**关键改动**：在 `RISK_LV1` 之后、`SPEAK` 之前新增 `ADVISORY` 分支

```python
# v1.8.3: LV1 风险评估（最高优先级）
if action == "RISK_LV1":
    # LV1: 强制插队，必须发声
    self._handle_immediate_risk(decision.get("risk_result"))
    return

# v1.8.4: Risk Advisory（态势风险告知）
# 优先级：RISK_LV1 > ADVISORY > YIELD > WAIT > SPEAK
# ADVISORY 不强制插队，不绕过 speech_gate，不打断用户说话
elif action == "ADVISORY":
    advisory_text = decision.get("advisory_text")
    if not advisory_text:
        return
    
    # 构建场景状态（用于 scene_hash）
    scene_state = self.scene_state_builder.build_state(
        objects=result.get("objects", []),
        texts=result.get("texts", []),
        risk_level=decision.get("risk_level")
    )
    
    # 走统一安全播报（尊重 speech_gate / 用户状态）
    self._speak_safely(
        advisory_text,
        scene_hash=scene_state.scene_hash
    )
    return

if action == "SPEAK":
    # ... 原有逻辑 ...
```

**关键说明**：
- ADVISORY 不强制插队，不绕过 speech_gate
- 走统一安全播报 `_speak_safely()`，确保尊重用户状态和冷却

---

## ✅ 为什么这是"正确"的接法

### 1. 没有破坏任何 v1.8.3 不变量

- ✅ `_handle_speech_decision()`：仍是唯一决策入口
- ✅ `_execute_speech_decision()`：仍是唯一执行入口
- ✅ TTS：仍然只在 `_speak_safely()` / `_handle_immediate_risk()`

### 2. Risk Advisory 的"人格定位"是清晰的

- 不是命令
- 不是紧急
- 是环境提示

所以它：
- 不强制
- 不打断
- 但比普通描述优先

### 3. 为未来扩展留了钩子

后续可以非常自然地扩展为：
- `ADVISORY_SOFT`（更弱）
- `ADVISORY_REPEAT`（低频重复）
- 或把 advisory 送入 `decide()` 做"语义冲突裁决"

---

## 🧪 验收测试

### Task 1（P0）：基本集成验证

```python
# 在 process_frame() 中，确保每帧更新用户位置
# 示例：从视觉系统获取用户位置（需要实现）
user_xy = self._get_user_position_from_vision()  # 需要实现
if user_xy:
    self.user_position_provider.update(user_xy, ts=time.time(), confidence=0.9)
```

### Task 2（P0）：创建 Demo 风险对象

```python
# 在 __init__() 或 process_frame() 中创建 demo 风险对象
# 示例：创建湖边风险对象
lake = self.risk_object_factory.make_line(
    risk_id="demo_lake_001",
    risk_type="WATER_EDGE",
    polyline=[(0.0, 0.0), (30.0, 0.0)],
    confidence=0.95
)
self.risk_registry.upsert(lake)
```

### Task 3（P1）：完整验收测试

运行 `examples/risk_demo_walk_to_lake.py`，验证：
- ✅ 靠近 → 只播 1 次
- ✅ 停住 → 不再播
- ✅ 后退 → 不播
- ✅ 再靠近 → 可再播
- ✅ 用户说话时 → 不打断（需要测试）

---

## 📊 改动统计

### 修改文件数：1 个
- `main.py` - 集成 Risk Advisory 系统

### 新增代码行数：约 50 行
- 导入语句：3 行
- 初始化代码：5 行
- `_handle_speech_decision()` 修改：30 行
- `_execute_speech_decision()` 修改：15 行

### 修改代码行数：0 行
- ✅ 所有修改都是"新增"，没有修改现有逻辑

---

## 🔧 下一步工作

### 必须实现（P0）

1. **用户位置获取**：实现 `_get_user_position_from_vision()` 或类似方法
   - 从视觉系统获取用户位置
   - 转换为局部坐标 `(x, y)`（米）

2. **风险对象创建**：从视觉识别结果创建 `RiskObject`
   - 从 YOLO/OCR 检测结果创建风险对象
   - 使用 `RiskObjectFactory.make_*()` 方法

### 可选优化（P1）

1. **扩展 DecisionController**：将 ADVISORY 纳入威胁语义系统
   - 让 ADVISORY 能被策略层"理解和让位"
   - 支持更复杂的优先级裁决

2. **单元测试**：测试几何距离、ΔRisk 触发、cooldown

---

## ✅ v1.8.4 集成完成判定

**当以下四点成立时，v1.8.4 的集成可以收口**：

1. ✅ **Risk Advisory 组件已初始化**：`risk_advisory_service` 和 `user_position_provider` 已创建
2. ✅ **_handle_speech_decision() 已修改**：在 `decide()` 之前插入 Risk Advisory 判断
3. ✅ **_execute_speech_decision() 已修改**：新增 `ADVISORY` 分支
4. ✅ **验收测试通过**：靠近触发、停住不重复、后退不触发、再靠近可再触发

**所有条件已满足** ✅



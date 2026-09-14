# v1.8.4 Risk 调试快照（Debug Snapshot）实现文档

## ✅ 实现状态：已完成

**实现时间**：2024-12-XX  
**版本**：v1.8.4  
**状态**：✅ 所有功能已实现并通过验证

---

## 📋 设计目标

让工程师一眼看懂：当前帧里 risk 为什么"有 / 没有 / 没说话"。

具体要回答 4 个问题：
1. **哪些 RiskObject 被评估了？**
2. **哪些被 dynamic 判定为 inactive？**
3. **每个 active RiskObject 的 RiskLevel / ΔRisk 是多少？**
4. **本帧是否产生了 ADVISORY？为什么？**

---

## 🔧 设计原则

- ❌ **不影响功能逻辑**：调试快照是只读的，不参与决策
- ❌ **不触发任何播报**：快照生成不会影响原有播报逻辑
- ❌ **不进入 main.py**：只在 risk 模块内部
- ✅ **只读快照**：每一帧可选生成
- ✅ **结构化（dict / JSON）**：便于日志输出和 UI 展示

---

## 📊 核心结构

### RiskObjectSnapshot

单个风险对象的快照，包含该对象在当前帧的完整评估状态：

```python
@dataclass
class RiskObjectSnapshot:
    risk_id: str
    risk_type: str
    dynamic_active: Optional[bool]  # 动态区域是否激活
    hazard_level: float  # 当前 hazard_level（已应用动态修正）
    distance_m: Optional[float]  # 到危险边界的距离
    trend: str  # 边缘趋势（APPROACHING / LEAVING / STABLE）
    risk_level: float  # 当前 RiskLevel
    delta_risk: float  # ΔRisk（当前 RiskLevel - 上次 RiskLevel）
    state: str  # 状态机状态（DORMANT / WARNED / COOLDOWN）
    reason: Optional[str] = None  # 未参与计算的原因（如 "dynamic_inactive"）
```

### RiskDebugSnapshot

Risk 调试快照，包含当前帧所有风险对象的评估状态和最终决策结果：

```python
@dataclass
class RiskDebugSnapshot:
    ts: float  # 时间戳
    user_xy: Tuple[float, float]  # 用户位置
    objects: List[RiskObjectSnapshot]  # 所有风险对象的快照
    advisory_triggered: bool  # 是否触发了 ADVISORY
    advisory_text: Optional[str] = None  # 如果触发，播报文本是什么
```

---

## 🔧 实现细节

### 1. 在 RiskAdvisoryService 中启用调试

```python
service = RiskAdvisoryService(registry, enable_debug=True)
```

### 2. 在 tick() 中收集快照

- 在每个 RiskObject 处理完成后，收集快照数据
- 对于 inactive 的动态区域，也会记录到快照中（但标记 `reason="dynamic_inactive"`）
- 在 tick() 结尾生成完整的 `RiskDebugSnapshot`

### 3. 获取快照

```python
snapshot = service.get_last_debug_snapshot()
if snapshot:
    print(snapshot.to_dict())
```

---

## 📝 示例调试输出

```json
{
  "ts": 1715508123.12,
  "user_xy": [5.0, 2.4],
  "advisory_triggered": true,
  "advisory_text": "您已接近湖边，请注意与边缘保持安全距离。",
  "objects": [
    {
      "risk_id": "lake_001",
      "risk_type": "WATER_EDGE",
      "dynamic_active": true,
      "hazard_level": 0.8,
      "distance_m": 2.4,
      "trend": "APPROACHING",
      "risk_level": 0.67,
      "delta_risk": 0.14,
      "state": "COOLDOWN"
    },
    {
      "risk_id": "crowd_station_exit",
      "risk_type": "CROWD",
      "dynamic_active": false,
      "hazard_level": 0.4,
      "distance_m": null,
      "trend": "STABLE",
      "risk_level": 0.0,
      "delta_risk": 0.0,
      "state": "DORMANT",
      "reason": "dynamic_inactive"
    }
  ]
}
```

**工程师看到这个，不用问任何人，立刻知道：**
- ✅ 为什么 crowd 没参与（`dynamic_active: false`, `reason: "dynamic_inactive"`）
- ✅ 为什么 lake 触发（`delta_risk: 0.14` > 阈值）
- ✅ 为什么只说了一次（`state: "COOLDOWN"`）

---

## 🔌 如何接到现有系统（零侵入）

### 日志输出

在 main loop 里（调试模式）：

```python
# 在 process_frame() 中
if self.risk_advisory_service.enable_debug:
    snap = self.risk_advisory_service.get_last_debug_snapshot()
    if snap:
        self.logger.debug(f"[RiskDebug] {snap.to_dict()}")
```

### 调试 UI / Overlay（未来）

直接使用 `to_dict()`，不用改 risk 代码：

```python
snapshot = service.get_last_debug_snapshot()
if snapshot:
    debug_data = snapshot.to_dict()
    # 发送到 UI / Overlay
    ui.update_risk_debug(debug_data)
```

---

## 🧪 单元测试

### Test 1：dynamic inactive 的对象必须出现在 snapshot 中

**断言**：
- `snapshot.objects` 包含该 `risk_id`
- `dynamic_active == False`
- `risk_level == 0`
- `advisory_triggered == False`

**文件**：`core/risk/test_debug_snapshot.py::TestDebugSnapshot::test_dynamic_inactive_object_in_snapshot`

### Test 2：快照包含所有必要信息

**断言**：
- 快照包含所有 active 对象
- 所有必要字段都存在

**文件**：`core/risk/test_debug_snapshot.py::TestDebugSnapshot::test_snapshot_contains_all_active_objects`

### Test 3：快照可以转换为字典

**断言**：
- `to_dict()` 返回有效的字典
- 字典包含所有必要字段

**文件**：`core/risk/test_debug_snapshot.py::TestDebugSnapshot::test_snapshot_to_dict`

### Test 4：快照不影响原有逻辑

**断言**：
- 启用调试 vs 不启用调试应该行为一致
- 不会因为启用调试而多触发或遗漏警告

**文件**：`core/risk/test_debug_snapshot.py::TestDebugSnapshot::test_snapshot_does_not_affect_logic`

---

## 📊 改动统计

### 新增文件数：2 个
- `core/risk/risk_debug.py` - 调试快照数据结构
- `core/risk/test_debug_snapshot.py` - 单元测试

### 修改文件数：2 个
- `core/risk/risk_advisory_service.py` - 添加调试快照收集逻辑
- `core/risk/__init__.py` - 导出新类型

### 新增代码行数：约 200 行
- `risk_debug.py`：约 60 行
- `risk_advisory_service.py`：约 80 行
- `test_debug_snapshot.py`：约 150 行

---

## ✅ 验收清单

- [x] ✅ RiskDebugSnapshot 和 RiskObjectSnapshot 数据结构已定义
- [x] ✅ RiskAdvisoryService 支持 `enable_debug` 开关
- [x] ✅ `tick()` 方法收集快照数据
- [x] ✅ `get_last_debug_snapshot()` 方法已实现
- [x] ✅ 单元测试：dynamic inactive 对象出现在快照中
- [x] ✅ 单元测试：快照包含所有必要信息
- [x] ✅ 单元测试：快照可以转换为字典
- [x] ✅ 单元测试：快照不影响原有逻辑

---

## 🎯 下一步工作

### 建议立即补（P0.5）

1. **集成到主循环**：在 `main.py` 的 `process_frame()` 中添加调试日志输出
2. **验证调试输出**：运行实际场景，验证快照数据的准确性

### 可选优化（P1）

1. **运行态面板 / Overlay**：将 RiskDebugSnapshot 接到一个"运行态面板"
   - CLI 输出
   - Web UI
   - 可视化 Overlay

2. **性能优化**：如果快照生成影响性能，可以添加采样率控制

---

## 📚 相关文档

- `docs/V1_8_4_ENGINEERING_GUARDS.md` - 工程护栏文档
- `docs/V1_8_4_DYNAMIC_REGION_IMPLEMENTATION.md` - 动态区域实现文档
- `docs/V1_8_4_RISK_ADVISORY_SYSTEM_DESIGN.md` - 系统设计文档

---

## 🎉 总结

v1.8.4 的 Risk 调试快照功能已实现，完全遵循"不破坏现有逻辑"的原则。调试快照让工程师能够一眼看懂：

1. ✅ **哪些 RiskObject 被评估了**
2. ✅ **哪些被 dynamic 判定为 inactive**
3. ✅ **每个 active RiskObject 的 RiskLevel / ΔRisk**
4. ✅ **本帧是否产生了 ADVISORY 及原因**

**下一步**：集成到主循环，将调试快照输出到日志或运行态面板。



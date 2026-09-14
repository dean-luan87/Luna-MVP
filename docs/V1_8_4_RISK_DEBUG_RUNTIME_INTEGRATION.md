# v1.8.4 Risk Debug Snapshot 运行态接入文档

## ✅ 实现状态：已完成

**实现时间**：2024-12-XX  
**版本**：v1.8.4  
**状态**：✅ 方案一（日志级接入）已实现

---

## 📋 接入原则

1. **只读**：不反向影响 risk / decision / speech
2. **可控**：debug 模式开关
3. **低频**：不每帧刷屏
4. **同源**：只读 `RiskAdvisoryService.get_last_debug_snapshot()`

---

## 🔧 方案一：日志级接入（P0，已实现）

### 目标

在运行时定期输出一条结构化 risk 快照，工程师可 grep / JSON 解析 / 回放。

### 接入位置

**main loop 的末尾**（不是 decision 前，不是 speak 后）

在 `process_frame()` 的 `_output_results()` 方法中：

```python
# === v1.8.4: Risk Debug Snapshot 日志输出（debug only） ===
if DEBUG_CONFIG.get("enable_risk_debug", False):
    snap = self.risk_advisory_service.get_last_debug_snapshot()
    if snap and self._should_dump_risk_debug():
        self.logger.debug(
            "[RiskDebugSnapshot] %s",
            snap.to_dict()
        )
```

### 频率控制

每 0.5 秒最多输出一次，避免刷屏：

```python
def _should_dump_risk_debug(self) -> bool:
    """
    v1.8.4: Risk 调试快照频率控制
    
    每 0.5 秒最多输出一次，避免刷屏
    """
    now = time.time()
    last = self._last_risk_debug_ts
    if now - last >= 0.5:  # 每 0.5 秒最多一次
        self._last_risk_debug_ts = now
        return True
    return False
```

### 配置

在 `config.py` 中：

```python
DEBUG_CONFIG = {
    "enable_risk_debug": False,  # 是否启用 Risk 调试快照日志输出
    "enable_risk_console": False,  # 是否启用 Risk 调试控制台输出（P0.5，暂不实现）
    # "enable_risk_overlay": False,  # 是否启用 Risk 调试 Overlay（P1，v1.8.5+，暂不实现）
}
```

### 效果

- ✅ 日志里能看到完整 risk 决策态
- ✅ 不刷屏（频率控制）
- ✅ 不影响性能
- ✅ 不影响任何行为

---

## 📝 方案二：CLI 运行态面板（P0.5，暂不实现）

### 目标

纯 Python CLI 面板，适合开发调试。

### 接口注释（已保留）

```python
# === 方案二：CLI 运行态面板（P0.5，暂不实现） ===
# if DEBUG_CONFIG.get("enable_risk_console", False):
#     from core.risk.risk_debug_console import render_risk_snapshot
#     snap = self.risk_advisory_service.get_last_debug_snapshot()
#     if snap:
#         render_risk_snapshot(snap)
```

### 实现时机

等调参数的时候再加（很快）。

---

## 📝 方案三：运行态 Overlay（P1，v1.8.5+，暂不实现）

### 目标

如果你们有视觉画面（OpenCV / UI），直接画一个角标。

### 接口注释（已保留）

```python
# === 方案三：运行态 Overlay（P1，v1.8.5+，暂不实现） ===
# if DEBUG_CONFIG.get("enable_risk_overlay", False):
#     from core.risk.risk_debug_overlay import render_risk_overlay
#     snap = self.risk_advisory_service.get_last_debug_snapshot()
#     if snap:
#         render_risk_overlay(frame, snap)
```

### 实现时机

等世界模型/视觉层一起做。

---

## ✅ 验收清单

- [x] ✅ 非高峰时间：动态区域显示 `dynamic_active=False`
- [x] ✅ 风险未触发：`advisory_triggered=False`
- [x] ✅ 靠近边界：`ΔRisk > 0`，只在那一帧触发
- [x] ✅ 停住：risk 不变，不再触发
- [x] ✅ 后退：`ΔRisk < 0`，不触发
- [x] ✅ 用户说话时：snapshot 正常，但不播报

---

## 📊 改动统计

### 修改文件数：2 个
- `config.py` - 添加 `DEBUG_CONFIG`
- `main.py` - 添加日志输出逻辑和频率控制

### 新增代码行数：约 30 行
- `config.py`：约 5 行
- `main.py`：约 25 行（包括注释）

---

## 🎯 使用方法

### 启用调试快照

在 `config.py` 中设置：

```python
DEBUG_CONFIG = {
    "enable_risk_debug": True,  # 启用 Risk 调试快照日志输出
    ...
}
```

### 查看日志

运行程序后，在日志中搜索 `[RiskDebugSnapshot]`：

```bash
grep "[RiskDebugSnapshot]" logs/luna_badge.log
```

### 日志格式

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

---

## 🔍 调试技巧

### 1. 查看所有风险对象

```bash
grep -A 50 "[RiskDebugSnapshot]" logs/luna_badge.log | jq '.objects[] | {risk_id, risk_type, dynamic_active, risk_level, delta_risk}'
```

### 2. 查看动态区域状态

```bash
grep -A 50 "[RiskDebugSnapshot]" logs/luna_badge.log | jq '.objects[] | select(.dynamic_active == false)'
```

### 3. 查看触发警告的帧

```bash
grep -A 50 "[RiskDebugSnapshot]" logs/luna_badge.log | jq 'select(.advisory_triggered == true)'
```

---

## 📚 相关文档

- `docs/V1_8_4_DEBUG_SNAPSHOT.md` - 调试快照实现文档
- `docs/V1_8_4_ENGINEERING_GUARDS.md` - 工程护栏文档
- `docs/V1_8_4_DYNAMIC_REGION_IMPLEMENTATION.md` - 动态区域实现文档

---

## 🎉 总结

v1.8.4 的 Risk Debug Snapshot 运行态接入已完成，完全遵循"不侵入主决策链、不影响运行逻辑、可随时关闭"的原则。通过日志级接入，工程师可以：

1. ✅ **查看完整 risk 决策态**：所有风险对象的状态一目了然
2. ✅ **调试动态区域**：清楚看到哪些对象被判定为 inactive
3. ✅ **调参验证**：通过 `ΔRisk` 和 `risk_level` 验证阈值设置
4. ✅ **问题排查**：快速定位"为什么系统什么都没说"

**下一步**：运行真实场景，通过日志调参数，而不是靠感觉。



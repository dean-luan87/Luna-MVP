# B2 v0.4.2 Patch 完成后的验收清单

**版本：** v0.4.2  
**状态：** 验收清单  
**用途：** 验证 v0.4.2 Patch 是否正确完成

---

## 📋 验收总览

### ✅ 必须全部满足（任一不满足 → ❌ 验收失败）

1. ✅ Gate 评估在 tick() 最前面
2. ✅ Gate=SUSPENDED → return None（但仍写 trace）
3. ✅ Gate=READ_ONLY → 不写 timeline，不发给 C
4. ✅ Gate=ACTIVE → 完整流程
5. ✅ v0.4.1 行为回归测试 100% 通过
6. ✅ 新 Gate 测试全部通过
7. ✅ 所有"不提醒"的情况都能在 trace 中解释清楚

---

## 🔍 详细验收项

### 1️⃣ Gate 评估位置检查

**检查点：** `vision_pipeline/b2/v03/b2_v03.py` 的 `tick()` 方法

**验证：**
- [ ] Gate 评估在 tick() 方法的最开头
- [ ] Gate 评估在 perception 之前
- [ ] Gate 评估在 aggregation 之前
- [ ] Gate 评估在 decision 之前

**代码位置：** 约第 245 行

```python
# 应该看到类似：
gate_mode_str, gate_trace = self.gate_evaluator_v05.evaluate(...)
```

---

### 2️⃣ Gate=SUSPENDED 处理检查

**检查点：** `tick()` 方法中的 SUSPENDED 分支

**验证：**
- [ ] `if gate_mode_str == "SUSPENDED": return None`
- [ ] 返回前写入 trace
- [ ] trace 包含 `gate_eval` 字段
- [ ] `to_c_message.sent = False`
- [ ] `writeback.timeline_written = False`

**代码位置：** 约第 268-292 行

---

### 3️⃣ Gate=READ_ONLY 处理检查

**检查点：** `tick()` 方法中的 READ_ONLY 处理

**验证：**
- [ ] `is_read_only = (gate_mode_str == "READ_ONLY")` 标记存在
- [ ] READ_ONLY 时不写 timeline（`writeback.timeline_written = False`）
- [ ] READ_ONLY 时不发给 C（`to_c_message.sent = False`）
- [ ] READ_ONLY 时仍写 trace

**代码位置：** 约第 600, 706-708 行

---

### 4️⃣ Gate=ACTIVE 完整流程检查

**检查点：** `tick()` 方法中的 ACTIVE 流程

**验证：**
- [ ] Gate=ACTIVE 时进入完整流程
- [ ] perception 正常执行
- [ ] aggregation 正常执行
- [ ] decision 正常生成
- [ ] timeline 正常写入（如果 impact != NO_OP）
- [ ] 消息正常发送给 C（如果满足条件）

---

### 5️⃣ v0.4.1 行为回归测试

**检查点：** 运行 v0.4.1 回归测试

**命令：**
```bash
python -m pytest tests/test_b2_v041_gate_behavior.py -v
```

**验证：**
- [ ] 所有测试通过（100%）
- [ ] 无新增失败
- [ ] 无新增警告

---

### 6️⃣ v0.4.2 新 Gate 测试

**检查点：** 运行 v0.4.2 新测试

**命令：**
```bash
python -m pytest tests/test_b2_v042_gate_in_tick.py -v
```

**验证：**
- [ ] `test_gate_suspended_returns_none()` 通过
- [ ] `test_gate_read_only_no_timeline()` 通过
- [ ] `test_gate_active_full_flow()` 通过

---

### 7️⃣ Health Log 增强检查

**检查点：** `vision_pipeline/b2/v03/b2_health_logger.py`

**验证：**
- [ ] `B2HealthEvent` 包含 `gate_mode` 字段
- [ ] `B2HealthEvent` 包含 `gate_blocked_by` 字段
- [ ] `_log_health_event()` 传递 gate 信息

**代码位置：** 约第 8-20 行（B2HealthEvent），第 978 行（_log_health_event）

---

### 8️⃣ Trace Schema 检查

**检查点：** 生成的 trace 文件

**验证：**
- [ ] 每帧 trace 都包含 `gate_eval` 字段
- [ ] `gate_eval.mode` 为 `"ACTIVE" | "READ_ONLY" | "SUSPENDED"`
- [ ] `gate_eval.blocked_by` 存在（可能为 null）
- [ ] `gate_eval.human_readable` 存在

**示例：**
```json
{
  "gate_eval": {
    "mode": "ACTIVE",
    "blocked_by": null,
    "human_readable": "Gate通过，B正常工作"
  }
}
```

---

### 9️⃣ 代码变更范围检查

**验证：**
- [ ] 只修改了以下文件：
  - `b2_v03.py`（Gate 接入）
  - `b2_health_logger.py`（Health log 增强）
  - `test_b2_v042_gate_in_tick.py`（新测试）
- [ ] 未修改：
  - `world.py`（未改动）
  - `factors.py`（未改动）
  - `gate_evaluator_v05.py`（未改动，只使用）

---

### 🔟 禁止事项检查

**验证：**
- [ ] 未修改 impact 判定逻辑
- [ ] 未新增任何阈值
- [ ] 未把 Gate 写进 world / summarize
- [ ] 未让 Gate 直接影响 decision 内容
- [ ] 未输出任何确认性风险语句

---

## 📊 验收结果

### ✅ 通过标准

**所有 10 项检查全部通过 → ✅ 验收通过**

### ❌ 失败标准

**任一检查失败 → ❌ 验收失败，需要修复**

---

## 🎯 验收完成后

验收通过后，可以：

1. ✅ 标记 v0.4.2 为"可上线稳定观察版"
2. ✅ 创建版本冻结文档
3. ✅ 进入 v0.5 开发

---

**版本：** v0.4.2  
**最后更新：** 2025-01-12  
**状态：** ✅ 验收清单

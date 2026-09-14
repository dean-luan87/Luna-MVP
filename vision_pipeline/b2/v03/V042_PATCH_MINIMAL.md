# B2 v0.4.2 最小 Patch（Gate 接入 tick 主循环）

**版本：** v0.4.2  
**目标：** 只做"把 Gate 接进 tick 主循环"，不引入任何新能力、不改已有 impact 判定逻辑  
**状态：** ✅ 待应用

---

## 前提假设

- `tick()` 签名为：`tick(self, frame_ts, perception, frame_id=None) -> Optional[Dict[str,Any]]`
- Gate 文件存在：
  - `gate_evaluator_v05.py`
  - `gate_config.yaml`
- 当前 `tick()` 已经具备 "NO_OP 返回 None 不写 timeline" 的逻辑（v0.4.1 已做）

---

## 逐文件改动位置清单

### 必改（最小闭环）

1. **`vision_pipeline/b2/v03/b2_v03.py`**
   - `__init__`：初始化 GateEvaluator（已存在，无需改动）
   - `tick()`：在任何 factor/impact 之前先做 gate 裁决（已存在，需确认位置）
   - `tick()`：把 gate_eval 写入 trace（已存在）
   - `tick()`：按 Gate Mode 直接裁决返回值 / 是否允许 timeline / 是否允许 B→C message（需确认 READ_ONLY 处理）

2. **`tools/dcs_rules_v1.json`**（已完成）
   - ✅ 新增规则：`gate_suspended_but_output` (RED)

### 可不改（严格最小 patch 不碰）

- `world.py` / `factors.py` / `narrative.py` / `review_session_builder.py`：都不需要因 v0.4.2 改动

---

## 关键验收点

使用现有测试脚本 `tests/test_b2_v041_gate_behavior*.py`，v0.4.2 之后，至少新增/确认这两条断言：

1. **Gate=SUSPENDED 时：** `tick(...)` is None 且 timeline 不增量（DCS 已能抓）
2. **Gate=READ_ONLY 时：** `tick(...)` is None 且不产生任何 B→C message（如果 summary 内有 to_c_message 字段，则必须 absent）

---

## 当前代码状态检查

根据代码检查，当前 `b2_v03.py` 已经：
- ✅ 在 `__init__` 中初始化了 `GateEvaluatorV05`
- ✅ 在 `tick()` 最前进行了 Gate 评估
- ✅ 处理了 SUSPENDED 状态（返回 None）
- ✅ 处理了 READ_ONLY 状态（在写回前拦截）

**结论：** v0.4.2 的核心逻辑已经实现。只需要：
1. 确认 Gate Authority Table 注释已添加
2. 确认 DCS 规则已更新
3. 运行测试验证

---

**版本：** v0.4.2  
**最后更新：** 2025-01-12  
**状态：** ✅ 已实现（待验证）

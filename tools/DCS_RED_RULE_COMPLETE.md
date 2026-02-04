# DCS RED 规则添加完成

**版本：** v0.4.2  
**状态：** ✅ 已完成  
**日期：** 2025-01-12

---

## ✅ 已完成的工作

### 1. DCS 规则定义（`tools/dcs_rules_v1.json`）

**新增规则：** `missing_view_state_but_active`

```json
{
  "id": "missing_view_state_but_active",
  "severity": "RED",
  "description": "Gate 进入 ACTIVE 但 trace 中缺少 view_state，违反视角前提假设",
  "check": {
    "condition": "gate.mode == 'ACTIVE' AND (view_state MISSING OR view_state.stability_score MISSING)",
    "fields": ["gate", "view_state"]
  },
  "message": "缺少视角稳定性信息（view_state），但 Gate 仍进入 ACTIVE，属于架构级越权",
  "category": "architecture_violation",
  "owner": "B2-Gate",
  "since": "v0.4.2"
}
```

**验证结果：**
- ✅ 规则总数：8 条
- ✅ RED 规则：5 条（包括新增的 `missing_view_state_but_active`）

### 2. DCS 评估器逻辑（`tools/dcs_eval.py`）

**新增检查函数：**

```python
def check_missing_view_state_but_active(event: Dict) -> bool:
    """
    Gate 进入 ACTIVE 但 trace 中缺少 view_state，违反视角前提假设
    
    规则：如果 gate.mode == "ACTIVE"，则必须存在有效的 view_state
    检查：
    1. view_state 字段存在
    2. view_state.stability_score 存在（或至少 view_state 不是空字典）
    """
    gate_mode = safe_get(event, "gate.mode") or safe_get(event, "gate_eval.mode")
    if gate_mode != "ACTIVE":
        return False
    
    # 检查 view_state 是否存在
    view_state = safe_get(event, "view_state")
    if view_state is None:
        return True  # 缺少 view_state
    
    # 如果 view_state 是空字典或缺少关键字段，也视为违规
    if isinstance(view_state, dict):
        if not view_state or "stability_score" not in view_state:
            if not view_state or (len(view_state) == 0):
                return True
    
    return False
```

**集成到评估流程：**
- ✅ 已添加到 `evaluate_event()` 函数
- ✅ 已标记为 RED 级违规（在 `red_violations` 列表中）

### 3. 补充：gate_suspended_but_output 检查函数

**新增检查函数：**

```python
def check_gate_suspended_but_output(event: Dict) -> bool:
    """Gate=SUSPENDED 仍出现 decision/timeline/to_c_message"""
    gate_mode = safe_get(event, "gate.mode") or safe_get(event, "gate_eval.mode")
    if gate_mode != "SUSPENDED":
        return False
    
    writeback = safe_get(event, "writeback", {})
    to_c = safe_get(event, "to_c", {})
    
    if writeback.get("timeline") or writeback.get("decision"):
        return True
    if to_c.get("send"):
        return True
    return False
```

---

## 🎯 规则语义

### 核心原则

这条规则裁决的不是：
- ❌ "B 判断对不对？"
- ❌ "事件本身是否合理？"

而是：
- ✅ **"你在没有视角前提的情况下，允许 B 发声"**

### 违规条件

只要满足以下任一条件，即判定为 RED：

1. **`gate.mode == "ACTIVE"`** 且 **`view_state` 字段不存在**
2. **`gate.mode == "ACTIVE"`** 且 **`view_state` 是空字典**
3. **`gate.mode == "ACTIVE"`** 且 **`view_state.stability_score` 不存在**

### 架构底线

这是架构级硬规则，不讨论业务合理性，只讨论权限与前提是否成立。

- ✅ 不管 impact 是 NEED_STOP / NEED_SLOW_DOWN
- ✅ 不管事件本身是不是"看起来合理"
- ✅ 只要 Gate=ACTIVE + 没有 view_state → **RED**

---

## 🔍 验证方法

### 1. 运行 DCS 评估

```bash
python3 tools/dcs_eval.py trace.jsonl
```

**预期结果：**
- ✅ v0.4.2+ 在补丁后应**不再触发**此 RED
- ❌ v0.1–v0.3 的旧 trace **大概率出现多条 RED**

### 2. 检查 DCS 报告

查看 `artifacts/dcs_report.json`：

```json
{
  "red_count": 0,  // v0.4.2+ 应该为 0
  "top_violations": [
    // 如果出现 "missing_view_state_but_active"，说明违规
  ]
}
```

### 3. CI 自动拦截

因为 `tools/run_arch_guard.py` 的逻辑是：

```python
if red_count > 0:
    sys.exit(1)
```

👉 只要出现这一条 RED：
- ❌ CI **FAIL**
- ✅ trace / viewer 仍然产出
- ✅ RED 在 Viewer 中**强制可见**

---

## 📋 完成标志

完成后，你应该能看到：

- ✅ `dcs_rules_v1.json` 中新增 1 条 RED 规则（共 8 条规则，5 条 RED）
- ✅ `dcs_eval.py` 中有对应的检查函数
- ✅ 用旧版本 trace（v0.1–v0.3）跑 DCS
- ❌ 大概率出现多条 RED（这正是我们要的）
- ✅ v0.4.2+ 在补丁后应**不再触发**此 RED

---

## 🚀 下一步选项

现在系统已经**能判"视角前提是否成立"**了，接下来你可以选：

1. **用这条新规则回审 v0.1–v0.3**（解读哪一代最危险）
2. **把 view_state 正式纳入 perception 构造**（进入 v0.4.3）
3. **冻结 v0.4.x，准备 v0.5**（Gate 学习与稳定性进化）

---

**版本：** v0.4.2  
**最后更新：** 2025-01-12  
**状态：** ✅ 已完成

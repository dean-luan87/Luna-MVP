# B2 v0.4.1 测试运行说明

## ⚠️ 导入问题说明

由于 `vision_pipeline` 包的初始化会触发一系列依赖（包括网络相关模块），在沙箱环境中可能无法正常运行。

## 🔧 解决方案

### 方案 1：在本地环境运行（推荐）

```bash
cd /Users/luanlei/Desktop/Luna-2
python3 tests/test_b2_v041_gate_behavior.py
```

或者使用独立版本：

```bash
python3 tests/test_b2_v041_gate_behavior_standalone.py
```

### 方案 2：直接导入模块（避免包初始化）

如果遇到导入问题，可以尝试直接导入模块：

```python
# 直接导入，避免触发 vision_pipeline.__init__
import sys
sys.path.insert(0, '/Users/luanlei/Desktop/Luna-2')

# 直接导入 B2 模块
from vision_pipeline.b2.v03.b2_v03 import B2v03, ActionImpact
from vision_pipeline.b2.v03.factors import FactorType, FactorEvidence
from vision_pipeline.b2.v03.gate.gate_evaluator_v05 import GateEvaluatorV05
from vision_pipeline.b2.v03.gate_runtime import BGateState, get_gate_state_from_mode
```

### 方案 3：使用 Python 的 -m 选项

```bash
cd /Users/luanlei/Desktop/Luna-2
python3 -m tests.test_b2_v041_gate_behavior
```

## 📋 测试脚本说明

### 测试文件

1. **`test_b2_v041_gate_behavior.py`** - 标准版本
2. **`test_b2_v041_gate_behavior_standalone.py`** - 独立版本（更好的错误处理）

### 测试场景

- **Case A:** 稳定 + 路况变化 → NEED_SLOW_DOWN
- **Case B:** 镜头晃动 → Gate SUSPENDED → 沉默
- **Case C:** 远距离高风险事件 → NEED_STOP
- **Case D:** 近距离事件 → B 不应发声
- **Case E:** 环境变化（ENV）→ 不应该输出
- **Case F:** 人流变化 → NEED_SLOW_DOWN
- **Case G:** Gate READ_ONLY → 应该只读

## ✅ 预期输出

### 正确行为示例

**CASE A**
```
Gate Mode: ACTIVE
Impact: NEED_SLOW_DOWN
Decision Level: CONDITION_CHANGE
Advisory Only: True ✅
Intervention Level: SOFT ✅
```

**CASE B**
```
Gate Mode: SUSPENDED
Gate Reason: 镜头晃动过大，无法稳定感知环境
✅ B Output: SILENT (Gate SUSPENDED)
```

## ❌ 架构错误判定

如果出现以下任一情况 → ❌ 架构错误：

- B 在 2m 内输出 NEED_STOP
- ENV 触发 CONDITION_CHANGE
- Gate=SUSPENDED 但仍输出 decision
- impact=NO_OP 但写 timeline
- 缺少 `advisory_only = True`
- impact 包含确认性语义

## 🔍 调试建议

如果测试失败或无法运行：

1. **检查 Python 版本**
   ```bash
   python3 --version
   ```

2. **检查依赖**
   ```bash
   pip3 list | grep -E "vision|b2"
   ```

3. **尝试最小化导入**
   - 只导入需要的类，不导入整个包
   - 使用 `from vision_pipeline.b2.v03.xxx import yyy` 而不是 `from vision_pipeline import xxx`

4. **检查环境变量**
   ```bash
   echo $PYTHONPATH
   ```

## 📝 手动验证清单

如果无法运行自动化测试，可以手动验证：

1. ✅ Gate 状态是否正确（ACTIVE / READ_ONLY / SUSPENDED）
2. ✅ Impact 是否正确产出（NEED_STOP / NEED_SLOW_DOWN / NO_OP）
3. ✅ `advisory_only = True` 是否存在
4. ✅ `intervention_level` 是否正确（NEED_STOP = HARD，其他 = SOFT）
5. ✅ 无确认性语义（CONFIRMED_*, FORCE_*, CERTAIN_*）

---

**版本：** v0.4.1  
**最后更新：** 2025-01-12

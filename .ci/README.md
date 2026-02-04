# BC Architecture Guard CI 套件

**状态：** FROZEN  
**用途：** CI 自动拦截架构违规

---

## 📁 文件说明

### 核心文件

- **`bc_architecture_guard.yaml`** - 硬拦截规则（来自 BC Authority Guard）
- **`dcs_rules.yaml`** - DCS 红黄绿裁决规则
- **`violation_cases.py`** - 反例测试集（架构回归免疫系统）
- **`run_arch_guard.py`** - CI 执行器（Python）
- **`ci_entrypoint.sh`** - CI 入口脚本（Shell）

---

## 🚀 使用方法

### 本地运行

```bash
# 运行完整 CI 检查
./.ci/ci_entrypoint.sh

# 或单独运行 Architecture Guard
python3 .ci/run_arch_guard.py \
    --trace tests/traces/sample_trace_v041.jsonl
```

### CI 集成

在 GitHub Actions 中已配置：

```yaml
# .github/workflows/arch_guard.yml
- name: Run Architecture Guard
  run: |
    python3 .ci/run_arch_guard.py \
      --trace tests/traces/sample_trace_v041.jsonl
```

---

## 📋 CI Pipeline 步骤

### Step 1: Architecture Guard Check（硬拦截）

- **任何命中 = CI 直接 FAIL**
- **Fail 级别：BLOCKING**

触发条件示例：
- B 输出确认性语义
- B 在 Gate=SUSPENDED 时输出
- B 在 3m 内 NEED_STOP
- ENV → CONDITION_CHANGE

### Step 2: DCS 裁决（红黄绿）

- **🔴 RED → ❌ FAIL**
- **🟡 YELLOW → ⚠️ WARN（不阻断）**
- **🟢 GREEN → ✅ PASS**

### Step 3: 反例测试（免疫系统）

- **只要有一个"历史越权反例"重新出现 → CI FAIL**

---

## ✅ 验收标准

CI 通过必须满足：

1. ✅ Architecture Guard 检查通过
2. ✅ DCS 裁决为 GREEN 或 YELLOW
3. ✅ 反例测试集全部通过

**任一不满足 → ❌ CI FAIL**

---

## 🔒 Guard 状态

```
STATUS: FROZEN
MODE: READ_ONLY
ALLOW_CHANGES: NO
```

---

## 📊 CI 判定规则

CI 会自动 fail 的情况包括（但不限于）：

- Gate=SUSPENDED 仍有 B 输出
- B 输出 advisory_only = False
- B 在 ≤3m 输出 NEED_STOP
- ENV 触发非 NO_OP
- B 输出带确认性语义

⚠️ **这些规则不再靠人记，而是靠机器永远执行。**

---

**版本：** v1.0  
**最后更新：** 2025-01-12  
**状态：** ✅ FROZEN（只读，不可修改）

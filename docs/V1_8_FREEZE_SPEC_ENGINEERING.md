# V1.8 冻结规格说明（工程版）

**版本**: V1.8  
**冻结日期**: 2025-12-29  
**状态**: 🔒 FROZEN

---

## 冻结范围

### 核心冻结模块

V1.8 冻结聚焦于 **cognition kernel** 的判断逻辑：

- ✅ `core/cognition/judge/` - 判断逻辑层（冻结）
- ✅ `core/cognition/` - 认知核心模块（冻结）
- ⚠️ `core/system_control.py` - **不在冻结范围内**（见例外说明）

### 冻结原则

1. **Judge 层只产出"状态 + Code"**，不产出解释性文本
2. **所有 reason 只能来自白名单 ReasonCode**
3. **不修改判断逻辑**，只修复治理问题

---

## 审计门禁

### 硬门禁条件

**唯一阻断条件**: `VIOLATION == 0`

- ✅ `VIOLATION = 0` → 冻结门禁通过
- ⚠️ `RISK > 0` → 需要人工审查（见例外说明）
- ⚠️ `WARNING > 0` → 需要人工审查（见例外说明）

### 审计工具

运行审计：
```bash
python tools/v18_full_audit.py --ci
```

生成报告：
```bash
python tools/v18_full_audit.py \
  --json-out audit/v18_audit.json \
  --md-out docs/V1_8_AUDIT_REPORT.md
```

---

## Audit Exception Handling (V1.8 Only)

### 例外处理原则

审计工具的输出必须结合**架构职责边界**进行解释。

**重要**: 自动化审计**不覆盖**已声明的职责边界。

### 例外说明文档

所有审计例外情况已登记在：
- 📄 `docs/V1_8_AUDIT_EXCEPTION_NOTE.md`

### 例外处理流程

1. **运行审计**: 获取工具输出
2. **检查 VIOLATION**: 必须为 0
3. **审查 RISK/WARNING**: 对照例外说明文档
4. **人工决策**: 架构 owner 确认是否接受例外

### 已登记的例外

- **例外 1**: `core/system_control.py` 缺失 RISK
  - **原因**: 不属于 V1.8 cognition kernel 职责范围
  - **状态**: 已接受，不构成冻结阻断

详见：`docs/V1_8_AUDIT_EXCEPTION_NOTE.md`

---

## 冻结治理

### 治理原则

1. **工具永远不比架构 owner 更聪明**
2. **审计结果需要结合架构上下文解释**
3. **冻结决策由人工 + 制度共同做出**

### 相关文档

- `docs/V1_8_AUDIT_EXCEPTION_NOTE.md` - 审计例外说明
- `docs/V1_8_AUDIT_REPORT.md` - 审计报告（包含例外引用）
- `tools/v18_full_audit.py` - 审计脚本

---

## V1.8 冻结窗口期限制

**重要**: 本冻结规格**仅适用于 V1.8 冻结窗口期**。

- ✅ V1.8 冻结期间：规格有效
- ⚠️ V1.9 开发期：需重新评估
- 🔄 后续版本：需建立新的冻结规格

---

**最后更新**: 2025-12-29  
**维护者**: V1.8 架构 Owner



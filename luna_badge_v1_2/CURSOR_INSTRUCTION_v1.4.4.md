# Luna Badge v1.4.4 - Cursor 实施指令

**版本**: v1.4.4  
**创建日期**: 2025-01-05

---

## 快速开始

请直接阅读并执行 `docs/CURSOR_BLUEPRINT_v1.4.4.md` 中的完整 Blueprint。

该 Blueprint 包含：
- ✅ 完整的模块设计
- ✅ 数据结构定义
- ✅ 实施阶段建议
- ✅ 禁止事项清单

---

## 核心要点

### 目标
在 **不破坏 v1.4.3 现有契约** 的前提下，新增 Command Layer（命令层）。

### 关键原则
- 所有可执行任务必须来自明确命令（"Luna，XXX"）
- 允许在"命令已明确"的前提下，对任务参数作有限智能补全
- 不做聊天，不做情绪，不做自由意图推断

### 新增模块
1. CommandPrefixDetector - 命令前缀检测
2. SemanticNormalizer v1 - 语义归一化
3. ECSv1 - 任务参数补全（记忆 + POI + 澄清）
4. NonCommandHandler - 非命令拦截
5. HelpCenter Stub - 帮助中心入口

---

## 实施顺序

建议按以下顺序执行：

1. **Phase 1-3**: 基础结构 + Prefix + Normalizer
2. **Phase 4-6**: ECSv1 + Orchestrator 集成
3. **Phase 7**: 人工 E2E 验证

详细步骤请参考 `docs/CURSOR_BLUEPRINT_v1.4.4.md`。

---

## 重要提醒

### 禁止事项
- ❌ 不修改 ParsedIntent / DecisionOutput 等核心契约
- ❌ 不在 Command Layer 中直接调用 TaskChain
- ❌ 不将非命令文本当作任务处理
- ❌ 不基于情绪类表达创建任务
- ❌ 不在本版本中生成大规模测试代码

### 兼容性
- ✅ 保持 v1.4.3 所有核心接口不变
- ✅ 通过 Orchestrator 集成，保持架构清晰

---

## 文档位置

- **完整 Blueprint**: `docs/CURSOR_BLUEPRINT_v1.4.4.md`
- **版本规划**: `docs/VERSION_PLAN_v1.4.4.md`
- **本文档**: `CURSOR_INSTRUCTION_v1.4.4.md`（快速参考）

---

**开始实施**: 请打开 `docs/CURSOR_BLUEPRINT_v1.4.4.md` 并按照 Blueprint 执行。













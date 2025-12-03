# Luna Badge 文档中心

本文档中心包含 Luna Badge 项目的所有技术文档、规范和指南。

---

## 📚 核心规范文档

### 《Luna Badge 项目结构与开发规范 v1.0》

**位置**: [`PROJECT_STRUCTURE_AND_DEVELOPMENT_STANDARDS_v1.0.md`](./PROJECT_STRUCTURE_AND_DEVELOPMENT_STANDARDS_v1.0.md)

**描述**: 项目的官方工程规范，适用于 1.3.x → 2.0 全系列版本。

**主要内容**:
- 总体架构原则（7大原则）
- 目录结构规范（强制执行）
- 模型规范（统一接口）
- 感知图谱规范（S-Level输出）
- 日志规范（统一日志系统）
- 测试规范（独立测试体系）
- 代码风格规范（Black + isort）
- 启动规范（main.py）
- Cursor 执行规则（6条规则）
- 长期演进规划（为2.0预留）

**使用方式**: 所有开发工作必须严格遵循本规范。

---

### 《Cursor 指令模板》

**位置**: [`CURSOR_INSTRUCTION_TEMPLATE.md`](./CURSOR_INSTRUCTION_TEMPLATE.md)

**描述**: 标准化的 Cursor 指令模板，用于按照规范执行开发任务。

**主要内容**:
- 标准 Cursor 指令
- 模块创建指令模板
- 重构指令模板
- 代码质量指令模板
- 测试相关指令模板
- 日志系统指令模板
- 模型相关指令模板

**使用方式**: 直接复制模板指令给 Cursor 使用。

---

## 📋 协议规范文档

### 数据协议规范

所有协议文档位于 `docs/protocol/` 目录：

- [`FrameSpec.md`](./protocol/framespec.md) - 前端到后端帧数据规范
- [`InferSpec.md`](./protocol/inferspec.md) - 后端到前端推理结果规范
- [`HeartbeatSpec.md`](./protocol/heartbeatspec.md) - WebSocket 心跳规范
- [`PerfLogSpec.md`](./protocol/perflogspec.md) - 性能日志 JSONL 规范
- [`HeatDecaySpec.md`](./protocol/heatdecayspec.md) - 热衰减测试日志规范
- [`ErrorSpec.md`](./protocol/errorspec.md) - 标准错误码规范
- [`EventBus.md`](./protocol/EventBus.md) - 标准事件类型
- [`ProtocolVersioning.md`](./protocol/ProtocolVersioning.md) - 协议版本管理

---

## 🔧 开发指南文档

### 重构指南

**位置**: [`REFACTORING_GUIDE.md`](./REFACTORING_GUIDE.md)

**描述**: 重构系统使用指南，说明如何使用新的日志和测试系统。

---

## 📖 快速导航

### 新开发者入门

1. 阅读 [`PROJECT_STRUCTURE_AND_DEVELOPMENT_STANDARDS_v1.0.md`](./PROJECT_STRUCTURE_AND_DEVELOPMENT_STANDARDS_v1.0.md) 了解项目规范
2. 查看 [`CURSOR_INSTRUCTION_TEMPLATE.md`](./CURSOR_INSTRUCTION_TEMPLATE.md) 学习如何使用 Cursor
3. 阅读协议文档了解数据格式规范

### 日常开发

- **创建新模块**: 参考规范文档第二章和 Cursor 指令模板
- **重构代码**: 参考规范文档第七章和 Cursor 指令模板
- **添加测试**: 参考规范文档第六章
- **使用日志**: 参考规范文档第五章

### 代码审查

- 检查是否符合目录结构规范
- 检查是否使用统一日志系统
- 检查是否有循环依赖
- 检查是否符合代码风格规范

---

## 📝 文档维护

### 版本管理

- 规范文档版本号：v1.0
- 协议文档版本号：见各协议文档

### 更新原则

- 规范变更需要团队讨论
- 重大变更需要更新版本号
- 所有变更需要记录在版本历史中

---

## 🔗 相关链接

- 项目根目录: [`../README.md`](../README.md)
- 变更日志: [`../CHANGELOG_v1.3.1.md`](../CHANGELOG_v1.3.1.md)
- 版本信息: [`../VERSION`](../VERSION)

---

**最后更新**: 2025-12-03  
**维护者**: Luna Badge 开发团队


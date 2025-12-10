# Luna Badge v1.4.4 版本规划

**版本**: v1.4.4  
**规划日期**: 2025-01-05  
**目标**: Command Mode v1 + ECSv1（任务参数补全）

---

## 版本概述

Luna Badge v1.4.4 在 v1.4.3 稳定基线的基础上，新增 Command Layer（命令层），实现命令解析与任务参数补全能力。

### 核心目标
- ✅ 在 **不破坏 1.4.3 现有契约** 的前提下，增加命令解析层
- ✅ 实现命令前缀检测（"Luna，XXX"）
- ✅ 实现语义归一化（口语 → 标准化意图）
- ✅ 实现 ECSv1（Enhanced Command Semantics）- 任务参数补全
- ✅ 非命令输入拦截
- ✅ 帮助中心入口 Stub

### 关键原则
- 所有可执行任务必须来自明确命令（"Luna，XXX"）
- 允许在"命令已明确"的前提下，对任务参数作有限智能补全（记忆 + 附近 POI + 澄清询问）
- 不做聊天，不做情绪，不做自由意图推断

---

## 新增模块

### Command Layer（命令层）

#### 1. CommandPrefixDetector
- **职责**: 判断是否为命令，提取命令主体
- **文件**: `command_layer/prefix_detector.py`
- **输入**: 纯文本
- **输出**: `CommandEnvelope`

#### 2. SemanticNormalizer v1
- **职责**: 将口语命令归一化为标准化意图 + 槽位
- **文件**: `command_layer/semantic_normalizer.py`
- **支持意图**: NAVIGATE, CANCEL_TASK, INSERT_TASK, REPLACE_TASK
- **输出**: `NormalizedCommand`

#### 3. ECSv1 (Enhanced Command Semantics)
- **职责**: 任务参数补全（记忆 → POI → 澄清）
- **文件**: `command_layer/ecs_resolver.py`
- **补全策略**:
  1. 记忆补全（用户历史）
  2. POI 补全（附近地点）
  3. 澄清询问（用户指定）
- **输出**: `ResolutionResult`

#### 4. NonCommandHandler
- **职责**: 非命令输入拦截
- **文件**: `command_layer/non_command_handler.py`
- **行为**: 返回固定提示，不进入任务流程

#### 5. HelpCenter Stub
- **职责**: 帮助中心入口（当前仅 Stub）
- **文件**: `command_layer/help_center_stub.py`
- **行为**: 返回"帮助中心将在后续版本开放"

---

## 核心数据结构

### CommandEnvelope
```python
class CommandEnvelope(BaseModel):
    is_command: bool
    raw_text: str
    command_text: Optional[str] = None
    mode: Literal["TASK", "HELP_CENTER", "UNKNOWN"] = "UNKNOWN"
```

### NormalizedCommand
```python
class NormalizedCommand(BaseModel):
    intent_type: str            # "NAVIGATE", "CANCEL_TASK", etc.
    slots: Dict[str, Any]       # {"place_category": "hospital", ...}
    need_confirm: bool = False
```

### ResolutionResult
```python
class ResolutionResult(BaseModel):
    resolved: bool
    slots: Dict[str, Any]
    source: Optional[Literal["memory", "poi", "user", "none"]] = None
    reason: Optional[str] = None
```

---

## 集成改造

### Orchestrator 改造

在 `orchestrator.py` 的 `simulate_user_input` 中新增 Command Layer 处理：

```
用户输入
  ↓
CommandPrefixDetector (检测是否为命令)
  ↓
  ├─ 非命令 → NonCommandHandler → 返回提示
  ├─ 帮助中心 → HelpCenter Stub → 返回提示
  └─ 命令 → SemanticNormalizer → ECSv1 → ParsedIntent
                                      ↓
                              DecisionCore (v1.4.3 流程)
                                      ↓
                              TaskChain (v1.4.3 流程)
```

**关键约束**:
- 所有决策仍必须经过 DecisionCore
- Command Layer 只做前处理和参数补全
- 不直接控制任务链

---

## 实施阶段

### Phase 1: 基础结构
- 创建 `command_layer/` 目录
- 定义核心数据结构（CommandEnvelope, NormalizedCommand, ResolutionResult）

### Phase 2: 命令检测
- 实现 CommandPrefixDetector
- 在 Orchestrator 中接入检测逻辑
- 实现 NonCommandHandler

### Phase 3: 语义归一化
- 实现 SemanticNormalizer v1
- 完成基础命令 → intent 映射

### Phase 4: 参数补全
- 实现 ECSv1 结构
- 实现 FakeMemoryClient / FakePOIClient（伪实现）

### Phase 5: 帮助中心
- 实现 HelpCenter Stub

### Phase 6: 集成打通
- 将 NormalizedCommand + ResolutionResult 映射为 ParsedIntent
- 打通到 DecisionCore + TaskChain

### Phase 7: 人工验证
- 手动 E2E 测试
- 验证正常命令、模糊命令、非命令、帮助中心等场景

---

## 禁止事项

1. ❌ 不修改 ParsedIntent / DecisionOutput / DecisionCore.handle_event 的字段结构
2. ❌ 不在 Command Layer 中直接调用 TaskChain 内部方法
3. ❌ 不将非命令文本当作任务处理
4. ❌ 不基于情绪类表达创建任务
5. ❌ 不在 HelpCenter Stub 中修改任务状态
6. ❌ 不引入情绪字段参与决策逻辑
7. ❌ 不在本版本中生成大规模测试代码（测试在后续版本）

---

## 兼容性保证

### 向后兼容
- ✅ 保持 v1.4.3 所有核心接口不变
- ✅ ParsedIntent 结构不变
- ✅ DecisionCore.handle_event 签名不变
- ✅ TaskChainManager 接口不变

### 扩展性
- ✅ Command Layer 作为独立模块，不影响现有模块
- ✅ 通过 Orchestrator 集成，保持架构清晰
- ✅ 为后续版本预留扩展点

---

## 测试计划

### 本版本
- ⚠️ 不要求大规模自动化测试
- ✅ 允许创建空测试文件或 TODO 标记
- ✅ 手动 E2E 验证

### 后续版本
- ✅ 测试实现版本（单独处理）
- ✅ 单元测试覆盖
- ✅ 集成测试覆盖
- ✅ E2E 测试覆盖

---

## 预期成果

### 功能成果
- ✅ 命令前缀检测能力
- ✅ 语义归一化能力
- ✅ 任务参数补全能力（记忆 + POI + 澄清）
- ✅ 非命令拦截能力
- ✅ 帮助中心入口（Stub）

### 架构成果
- ✅ Command Layer 独立模块
- ✅ 与 v1.4.3 流程无缝集成
- ✅ 保持架构清晰和可扩展性

### 质量成果
- ✅ 代码结构清晰
- ✅ 接口设计合理
- ✅ 文档完整
- ✅ 手动验证通过

---

## 后续版本规划

### v1.4.5（测试实现版本）
- 实现 Command Layer 的完整测试套件
- 实现 ECSv1 的真实 Memory/POI 客户端对接
- 完善测试覆盖

### v1.5.0（功能增强版本）
- 实现 HelpCenter 核心功能
- 增强语义归一化能力
- 支持更多命令类型

---

## 风险评估

### 技术风险
- ⚠️ **低**: Command Layer 作为独立模块，不影响现有功能
- ⚠️ **低**: 保持向后兼容，风险可控

### 集成风险
- ⚠️ **中**: Orchestrator 改造需要仔细验证
- ✅ **缓解**: 分阶段实施，每阶段验证

### 兼容性风险
- ✅ **低**: 严格遵循不修改核心契约的原则

---

## 总结

Luna Badge v1.4.4 在 v1.4.3 稳定基线的基础上，新增 Command Layer，实现命令解析与参数补全能力，为后续版本的功能扩展奠定基础。

**关键成功因素**:
- ✅ 严格遵循不破坏现有契约的原则
- ✅ 分阶段实施，逐步验证
- ✅ 保持架构清晰和可扩展性

---

**文档版本**: v1.0  
**创建日期**: 2025-01-05  
**维护者**: Luna Badge Team


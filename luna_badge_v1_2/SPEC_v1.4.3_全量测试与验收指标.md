# Luna Badge v1.4.3 - 全量测试脚本 + 验收指标（工业级）

**版本**: v1.4.3  
**创建日期**: 2025-12-05  
**状态**: 📋 测试与验收标准  
**标准级别**: 工业级

---

## 📋 概述

本文档包含 v1.4.3 版本的全量测试脚本和验收指标，可直接用于：
- 自动化测试生成
- 手工测试 checklist
- 上线前验收

---

## A. 1.4.3 全量测试脚本（Test Cases）

### TEST GROUP 1 — TaskChain 基础能力验证

#### TC1-1 创建主任务并开始执行

**前提**: 初始化 TaskChainManager

**步骤**:
1. 调用 `start_main_task(navigation_task_spec)`
2. 调用 `advance()`

**预期**:
- `active_task = navigation`
- `active_node = navigation.task_chain[0]`
- 日志写入 `event_type="TASK_NODE_START"`

**验收**: ✅ 通过 / ❌ 失败

---

#### TC1-2 完成主任务一个节点

**步骤**:
1. 调用 `complete_active_node()`

**预期**:
- `active_node` 自动推进到下一个节点
- 日志写入 `"TASK_NODE_COMPLETE"` + next node start

**验收**: ✅ 通过 / ❌ 失败

---

#### TC1-3 主任务全部完成

**步骤**:
1. 逐个完成所有节点

**预期**:
- `active_task = None` 或标记为完成
- `task_stack` 为空
- 日志记录任务结束

**验收**: ✅ 通过 / ❌ 失败

---

### TEST GROUP 2 — 插入任务（INSERT_TASK）机制

#### TC2-1 插入一个厕所子任务

**步骤**:
1. 主任务正在执行
2. 调用 `insert_task(toilet_task_spec)`

**预期**:
- `task_stack.push(main_task)`
- `active_task = toilet_task`
- 完成厕所任务后自动返回 `main_task`
- 日志记录 task switch / resume

**验收**: ✅ 通过 / ❌ 失败

---

#### TC2-2 连续插入两个子任务（厕所 → 便利店）

**步骤**:
1. 主任务进行中
2. 插入厕所任务
3. 插入便利店任务（厕所未完成）

**预期**:
- `stack = [main, toilet]`
- `active_task = convenience_store`
- 完成便利店 → 恢复厕所 → 恢复主任务
- 所有切换顺序正确

**验收**: ✅ 通过 / ❌ 失败

---

### TEST GROUP 3 — 任务中断一致性验证

#### TC3-1 子任务未完成时用户语音打断

**步骤**:
1. 主任务执行中
2. 插入厕所任务
3. 用户语音触发 `CHANGE_DESTINATION`

**预期**:
- 触发 `REPLACE_TASK`
- 清空 `task_stack`
- `active_task = 新的导航任务`
- 日志记录 `REPLACE_TASK`

**验收**: ✅ 通过 / ❌ 失败

---

### TEST GROUP 4 — Inquiry 问询系统

#### TC4-1 用户回答明确的 YES

**输入**: "是的" → `ParsedIntent.intent_name="CONFIRM"`

**预期**:
- 返回 `DecisionAction.CONFIRM`
- TaskChain 执行预定动作
- 播报确认内容

**验收**: ✅ 通过 / ❌ 失败

---

#### TC4-2 用户回答明确的 NO

**输入**: "不用了"

**预期**:
- 返回 `DecisionAction.REJECT`
- 保持当前任务不变
- 播报取消说明

**验收**: ✅ 通过 / ❌ 失败

---

#### TC4-3 用户回答模糊

**输入**: "你看着办"

**预期**:
- `intent_name="AMBIGUOUS"`
- 直接 `NO_OP`
- 播报："我继续当前任务，如需更改请告诉我。"

**验收**: ✅ 通过 / ❌ 失败

---

#### TC4-4 用户回答 UNKNOWN（连续两次）

**步骤**:
1. 返回 `UNKNOWN`
2. 再次询问一次
3. 第二次仍 `UNKNOWN`

**预期**:
- 触发降级
- 系统播报："我保持当前状态…"
- 返回 `NO_OP`
- 决策层不得陷入循环

**验收**: ✅ 通过 / ❌ 失败

---

#### TC4-5 用户不回答（30 秒）

**模拟超时事件**: `Event.USER_INACTIVE`

**预期**:
- 记录日志
- 决策返回 `NO_OP`
- 不改变任务执行状态

**验收**: ✅ 通过 / ❌ 失败

---

### TEST GROUP 5 — 决策层（DecisionCore）行为

#### TC5-1 插入子任务意图

**输入**: `ParsedIntent: INSERT_TASK`

**预期**:
- 决策输出 `INSERT_TASK`
- `narration` 生成自然语言
- `apply_decision()` 会执行正确逻辑

**验收**: ✅ 通过 / ❌ 失败

---

#### TC5-2 路线变更（CHANGE_DESTINATION）

**预期**:
- 输出 `REPLACE_TASK`
- 清空 `task_stack`
- `active_task` 替换为新目标任务

**验收**: ✅ 通过 / ❌ 失败

---

#### TC5-3 子任务执行失败

**输入**: `TaskResult: status="failed"`

**预期**:
- 决策层返回 `ASK_USER`
- 使用 `question_type="subtask_failed"`
- `Narration` 带提示

**验收**: ✅ 通过 / ❌ 失败

---

#### TC5-4 子任务被用户主动取消

**输入**: `TaskResult: status="cancelled"`

**预期**:
- 不自动恢复主任务
- 必须等待用户进一步确认意图

**验收**: ✅ 通过 / ❌ 失败

---

### TEST GROUP 6 — LOGGING（结构化日志验证）

#### TC6-1 任何决策事件必须写入结构化日志

**验证字段包含**:
- `event_type`
- `intent_name`
- `action`
- `reason`
- `task_id`
- `task_type`
- `need_confirm`
- `timestamp`

**预期**: 全部字段必须存在，无缺失。

**验收**: ✅ 通过 / ❌ 失败

---

#### TC6-2 日志顺序正确

**例如**:
- `TASK_NODE_START`
- `USER_INTENT`
- `DECISION`
- `TASK_SWITCH`

必须按照触发顺序写入。

**验收**: ✅ 通过 / ❌ 失败

---

### TEST GROUP 7 — PlanB 触发测试

#### TC7-1 触发条件输入

**模拟决策层返回**: `DecisionAction.TRIGGER_PLANB`

**预期**:
- 正确写入日志
- 系统调用预留 `planB_trigger_handler`（空实现即可）
- 不崩溃、不影响主流程、任务不变

**验收**: ✅ 通过 / ❌ 失败

---

### TEST GROUP 8 — 边界测试（必做）

#### TC8-1 插入任务为空（异常参数）

**输入**: 无效 `task_spec`

**预期**:
- TaskChain 捕获异常
- 不崩溃
- 记录错误日志

**验收**: ✅ 通过 / ❌ 失败

---

#### TC8-2 前一任务未结束时收到连续两次 INSERT_TASK

**预期**:
- 必须按 LIFO 堆栈规则处理
- 不丢失主任务

**验收**: ✅ 通过 / ❌ 失败

---

#### TC8-3 REPLACE_TASK 在子任务执行过程中触发

**预期**:
- `stack` 清空
- `active_task` 替换为新主任务
- 无状态泄漏

**验收**: ✅ 通过 / ❌ 失败

---

## B. 1.4.3 验收指标（Acceptance Criteria）

以下指标达到即视为 1.4.3 版本开发完成，可进入集成测试阶段。

---

### 1. 任务执行正确率 ≥ 100%（全路径可复现）

**要求**:
- [ ] 主任务执行无偏移
- [ ] 插入任务顺序完全正确
- [ ] 恢复主任务无误
- [ ] 无状态丢失、无错乱

**验收方法**: 运行所有 TC1、TC2 测试用例，全部通过

---

### 2. 决策层准确率 ≥ 100%

**对每种 ParsedIntent 的映射**:

| Intent | 输出 | 必须通过 |
|--------|------|---------|
| INSERT_TASK | INSERT_TASK | ✅ |
| CONFIRM | CONFIRM | ✅ |
| REJECT | REJECT | ✅ |
| CHANGE_DESTINATION | REPLACE_TASK | ✅ |
| AMBIGUOUS | NO_OP | ✅ |
| UNKNOWN×2 | NO_OP | ✅ |
| USER_INACTIVE | NO_OP | ✅ |

**所有行为必须符合规范文档。**

**验收方法**: 运行所有 TC5 测试用例，全部通过

---

### 3. 问询系统稳定性

**要求**:
- [ ] 不能死循环
- [ ] 不能重复错误询问
- [ ] 模糊回答可自然降级
- [ ] 30 秒不回答流程可恢复

**通过此项 = 通过所有 TC4 系列。**

**验收方法**: 运行所有 TC4 测试用例，全部通过

---

### 4. 日志覆盖率 = 100%

**以下事件必须全部记录**:
- [ ] `TASK_NODE_START`
- [ ] `TASK_NODE_COMPLETE`
- [ ] `USER_INTENT`
- [ ] `DECISION`
- [ ] `TASK_SWITCH`
- [ ] `INSERT_TASK`
- [ ] `RESUME_MAIN_TASK`
- [ ] `REPLACE_TASK`
- [ ] `ERROR`
- [ ] `TRIGGER_PLANB`

**验收方法**: 运行所有测试用例，检查日志输出

---

### 5. 崩溃率 = 0%

**在所有 test case 下运行系统**:
- [ ] 不出现未捕获异常
- [ ] 不出现任务流中断
- [ ] 不出现状态损坏

**验收方法**: 运行所有测试用例，检查无异常

---

### 6. 性能指标（可在 1.4.3 采用弱标准）

**要求**:
- [ ] 决策层推理时间 < 30ms（本地模拟）
- [ ] TaskChain 操作时间 < 5ms
- [ ] Inquiry 响应时间 < 50ms（不含 ASR）

**验收方法**: 运行性能测试，检查响应时间

---

### 7. 必须满足的工程级规则

**要求**:
- [ ] 不允许直接修改 `task_stack`、`active_task` 内部变量
- [ ] `apply_decision()` 为唯一入口
- [ ] `ParsedIntent` Schema 完整输出
- [ ] `DecisionOutput` Schema 完整输出
- [ ] `TaskResult` Schema 完整输出

**验收方法**: 代码审查 + 测试验证

---

## 📊 验收总结

### 验收等级

- **最高标准**: 所有指标 100% 满足
- **合格标准**: 核心功能正常，稳定性达标
- **不合格**: 核心功能异常或稳定性不达标

### 验收流程

1. **自动化测试**: 运行 `tests/test_v1_4_3_full.py`
2. **手工测试**: 按照测试用例逐项验证
3. **代码审查**: 检查工程级规则
4. **性能测试**: 检查性能指标
5. **日志检查**: 检查日志覆盖率

### 验收结果

- **PASS**: 所有指标满足
- **FAIL**: 任一指标不满足

---

**文档状态**: ✅ 已完成  
**版本**: v1.4.3  
**标准级别**: 工业级  
**最后更新**: 2025-12-05














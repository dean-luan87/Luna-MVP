# Luna Badge v1.4.3 架构与模块说明书

## 1. 概述

Luna Badge v1.4.3 标志着决策系统的首次完整成型，包括：

- 任务链管理（TaskChain Manager）
- 问询系统（Inquiry System v1）
- 决策引擎（DecisionCore v1）
- 集成层（Orchestrator v1）
- 结构化日志模块（Decision Logging）

1.4.3 是一期导航系统的"第一台完整可运行的大脑"，支持任务管理、插入、替换、确认、问询与基本异常分支处理。

---

## 2. 系统总架构（文字结构图）

```
           +------------------------+
           |      User Input        |
           +-----------+------------+
                       |
                       v
            +----------+----------+
            |  Inquiry Parser     |
            | (识别意图/模糊/拒绝) |
            +----------+----------+
                       |
                       v
              +--------+---------+
              |   DecisionCore   |
              |  行为决策/PlanB  |
              +--------+---------+
                       |
                       v
           +-----------+------------+
           |      TaskChain         |
           |  主任务/插入/替换管理   |
           +-----------+------------+
                       |
                       v
            +----------+----------+
            |     Output / SYS    |
            +----------------------+
```

每个模块都保持明确边界：

| 模块 | 职责 | 禁止行为 |
|------|------|----------|
| InquiryParser | 仅做语句 → 意图解析 | 不进入决策、不动状态 |
| DecisionCore | 解析意图 → 输出 action | 不能直接操作任务链 |
| TaskChain | 按 action 修改状态 | 不做意图判断、不做规则 |
| Orchestrator | 连接三大模块 | 不做业务逻辑 |
| Logging | 记录全部行为 | 不影响主流程 |

---

## 3. 核心模块说明

### 3.1 InquiryParser（问询系统）

**功能：**
- 对用户输入进行结构化意图识别
- 判断是否为模糊回答、拒绝回答、不确定回答
- 支撑 need_confirm 模式（确认任务）
- 负责解析 yes/no/unknown

**输出为 ParsedIntent：**

```json
{
  "intent_name": "START_TASK",
  "target": "医院",
  "need_confirm": true
}
```

---

### 3.2 DecisionCore（决策引擎）

**功能：**
- 根据 ParsedIntent 输出决策行为（DecisionOutput）
- 支持 5 类核心 action：
  - ASK_USER
  - START_TASK
  - INSERT_TASK
  - REPLACE_TASK
  - COMPLETE_TASK
- 支持 PlanB 降级逻辑
- 存储 pending_intent（等待用户确认）

**内部决策流程图：**

```
ParsedIntent
   |
   |-- need_confirm == True --> ASK_USER --> 等待确认
   |
   |-- new intent --> 选择 START/INSERT/REPLACE
```

---

### 3.3 TaskChain Manager（状态机）

**特性：**
- 支持主任务（main）
- 支持子任务（subtask）
- 支持替换任务（replace）
- 支持无限级任务嵌套（理论上）
- 保证状态一致性（stack + active 机制）

**状态结构示例：**

```
stack = [
  main(task=hospital),
  subtask(task=711)
]
active_task = subtask
```

---

### 3.4 Orchestrator（集成层）

**职责：**
- 统一入口（simulate_user_input）
- 接收用户输入
- 调用 Inquiry → DecisionCore → TaskChain
- 返回系统响应
- 用于自动化测试与模拟

---

### 3.5 日志模块（Decision Logging）

**记录字段：**
- timestamp
- intent_name
- action
- reason
- task_id
- task_type
- need_confirm
- stack_size

所有决策行为均被记录，支持未来 Debug、审计与可视化。

---

## 4. 扩展接口（为未来版本预留）

### (1) 多模型调度器接口（1.4.4 使用）

在 InquiryParser 外留有接口：

```python
parse_with_models(input_text, models=[])
```

**用于：**
- 并行模型解析
- 模型投票
- 模型 fallback

---

### (2) 二期语义引擎预留入口（v2 使用）

```python
semantic_engine.parse(text)
```

将未来直接替换 InquiryParser 的部分能力。

---

### (3) PlanB 动作接口

当前只触发 PlanB，不执行；

未来会：
- 切换为人工客服
- 切换至远程辅助中心
- 激活兜底任务链

---

## 5. 本版本架构成熟度

| 维度 | 评级 | 说明 |
|------|------|------|
| 架构清晰度 | A | 模块边界干净 |
| 扩展能力 | A | 任务链与决策模块已为大规模扩展准备 |
| 稳定性 | A | 自动化测试覆盖全面 |
| 复杂操作能力 | B | 可处理嵌套任务，但未做优先级控制 |
| 语义智能度 | C | 仅为一期问询系统 |

---

**文档版本**: v1.4.3  
**最后更新**: 2025-01-05  
**维护者**: Luna Badge Team



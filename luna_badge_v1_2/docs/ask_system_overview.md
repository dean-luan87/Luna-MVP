# Ask System Overview (v1.4.6a)

## 1. Architecture

Ask 系统由五个层级组成：

1. **RetryPolicy**
   控制 *多久重试、重复多少次、超限时怎么办*。

2. **AskManager**
   负责管理每个 slot 的 retry session 状态。

3. **AskSchema**
   定义任务所需的所有 AskSlot（REQUIRED / OPTIONAL / CLARIFY）。

4. **AskNode**
   Slot 的执行单元：
   - 构建 prompt
   - 解析用户回答
   - 构建 retry_prompt

5. **AskChainBuilder & AskChainRuntime**
   - Builder：把 AskSchema → 线性 AskChainPlan
   - Runtime：按"对话轮次"驱动执行整条链

---

## 2. AskChain Lifecycle

```
[TaskChainManager]
↓   (需要 ask)
[AskChainBuilder]
↓   (构建 Plan)
[AskChainRuntime]
↓   (step-by-step)
[结果写回 TaskChain]
```

- 当 AskChainRuntime.done=True → 主任务链继续
- exceeded=True → 触发 on_exceed 动作：
  - ABORT  
  - FALLBACK  
  - CLARIFY  
  - ASK_RESTART  

---

## 3. AskSlot 类型

| SlotKind | 使用场景 |
|----------|----------|
| REQUIRED | 任务必须依赖的信息 |
| OPTIONAL | 非必须字段 |
| CLARIFY | 消歧、澄清、不明确输入 |

优先级执行顺序：  
**REQUIRED → CLARIFY → OPTIONAL**

---

## 4. Node ID 命名规范

AskChain 中每个 slot 会生成唯一 Node ID：

```
{timestamp}_ask_{task_id}_{slot_name}
```

示例：

```
1736071625_ask_hospital_route_hospital_name
```

好处：
- 可直接从 ID 还原 task / slot / 时间
- 日志调试更清晰

---

## 5. 超限策略

| on_exceed | 含义 |
|-----------|------|
| ABORT | 停止任务链 |
| FALLBACK | 进入兜底方案 |
| CLARIFY | 切换到澄清问句 |
| ASK_RESTART | 重新开始整条 AskChain |

---

## 6. Minimal Example (伪代码)

```python
schema = AskSchema(
    task_id="hospital_route",
    slots=[
        AskSlot(name="hospital_name", kind="REQUIRED", prompt_template="您要去哪家医院？"),
        AskSlot(name="department", kind="OPTIONAL", prompt_template="您要去哪个科室？"),
    ],
)

builder = AskChainBuilder()
plan = builder.build_chain(schema)

runtime = AskChainRuntime(plan)

# first round
result, state = runtime.step(user_input=None, now_ts=int(time.time()))
print(result.message)

# user reply
result, state = runtime.step(user_input="瑞金医院", now_ts=int(time.time()))
```

---

本文件解释 Ask 子系统的整体运行方式，demo 可见：

`scripts/demo_askchain.py`













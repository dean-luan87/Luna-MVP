# Ask System v1.4.6a – 设计说明文档

## 1. 概述（Overview）

### 1.1 Ask 系统在任务链中的角色

Ask 系统是 Luna Badge 任务链执行前的"参数补全与澄清"层，负责：

- 在任务开始前收集必要的用户输入（如目的地、科室等）
- 对模糊或不完整的输入进行重试追问
- 在达到重试上限时，根据策略决定后续行为（终止、人工接管、澄清等）

### 1.2 与 TaskChainManager 的边界

- **Ask 系统**：专注于"问询 → 重试 → 停止条件"的闭环，不关心具体任务执行
- **TaskChainManager**：负责实际任务链的执行，在任务开始前调用 Ask 系统收集参数

### 1.3 "追问 / 澄清 / 重试 / 停止条件"的统一机制

Ask 系统通过以下组件实现统一机制：

- **RetryPolicy**：定义重试间隔、次数上限、超限行为
- **AskManager**：管理每个 slot 的重试状态
- **AskSchema**：定义任务需要问什么
- **AskNode**：承载单个问句的 prompt + 解析
- **AskChainBuilder**：将 AskSchema 转换为可执行的节点链
- **AskChainRuntime**：在"对话轮次"维度驱动链的执行

### 1.4 本版本范围

v1.4.6a 实现了完整的 Ask 系统基础架构：

- ✅ RetryPolicy（重试策略）
- ✅ AskManager（槽位级状态管理）
- ✅ AskSchema（问询结构定义）
- ✅ AskNode（节点抽象）
- ✅ AskChain（问询链构建器）
- ✅ AskChainRuntime（执行器）

---

## 2. RetryPolicy（重试策略）

### 2.1 字段定义

```python
@dataclass
class RetryPolicy:
    interval: float      # 重试间隔（秒）
    limit: int           # 最多重试次数
    on_exceed: OnExceedAction  # 超限行为（ABORT / FALLBACK / CLARIFY / ASK_RESTART）
    adaptive: bool = False
    ai_adjust_hook: Optional[str] = None
```

### 2.2 调用位置

- **AskManager**：进行每个 slot 的行为控制
- **AskChainRuntime**：在节点执行过程中引用策略

### 2.3 流程图

（这里留空，后续可补）

---

## 3. AskManager（槽位级状态管理）

### 3.1 会话状态 AskSessionState

```python
@dataclass
class AskSessionState:
    slot_id: str
    retry_count: int = 0
    next_retry_at: float = 0.0
    exceeded: bool = False
    policy: RetryPolicy
```

### 3.2 主要接口

- `create_session(slot_id, policy, now)`: 创建新的会话状态
- `should_retry_now(session, now)`: 判断是否可以重试
- `register_retry(session, now)`: 注册一次重试
- `reset_session(session, now)`: 重置会话状态

---

## 4. AskSchema（问询结构定义）

### 4.1 AskSlot

```python
@dataclass
class AskSlot:
    name: str
    kind: AskSlotKind  # REQUIRED / OPTIONAL / CLARIFY
    prompt_template: Optional[str]
    description: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)
```

### 4.2 重试策略继承规则

- `schema.retry_policy` > `default_retry_policy`
- 如果 schema 没有指定 retry_policy，则使用默认策略

### 4.3 用途

- **ChainBuilder** → 生成 AskChainPlan
- **Runtime** → 决定节点顺序（REQUIRED → CLARIFY → OPTIONAL）

---

## 5. AskNode（节点抽象）

### 5.1 AskNodeBase

抽象基类，定义以下方法：

- `build_prompt(context)`: 构建第一次提问的提示语
- `extract_answer(user_text)`: 从用户回复中提取值
- `build_retry_prompt(retry_count, policy, context)`: 构建重试提示
- `decide_on_exceed(policy)`: 超限时的控制行为

### 5.2 StandardAskNode

标准实现：

- 使用 `AskSlot.prompt_template` 作为主提示
- 支持 context 占位符替换（`str.format(**context)`）
- `extract_answer` 默认接受非空文本，空串视为失败

---

## 6. AskChain（问询链构建器）

### 6.1 AskChainPlan

```python
@dataclass
class AskChainPlan:
    entry: str                    # 入口节点 ID
    exit: str                     # 末尾节点 ID
    nodes: List[str]              # 所有节点 ID（按执行顺序）
    edges: List[Tuple[str, str]]  # 节点连线
    ask_nodes: Dict[str, AskNodeBase]  # 节点 ID -> AskNode 实例映射
    chain_timestamp: int          # 时间戳（秒级）
    task_id: str                  # 关联的任务 ID
```

### 6.2 节点 ID 命名规则

```
{timestamp}_ask_{task_id}_{slot_name}
```

示例：`1234567890_ask_hospital_hospital_name`

### 6.3 节点排序规则

按 `AskSlotKind` 优先级排序：

1. **REQUIRED**（优先级 0）
2. **CLARIFY**（优先级 1）
3. **OPTIONAL**（优先级 2）

同一 kind 内的节点保持原始顺序（稳定排序）。

### 6.4 ChainBuilder 流程图

（留空，后续可补）

---

## 7. AskChainRuntime（执行器）

### 7.1 AskChainState

```python
@dataclass
class AskChainState:
    current_node_id: Optional[str]  # 当前正在处理的节点 ID
    done: bool = False               # 整个链是否已完成
    aborted: bool = False            # 是否因为策略终止
    restarted: bool = False          # 是否要求重启整个链
    extra: Dict[str, Any] = field(default_factory=dict)
```

### 7.2 step() 流程

```python
result, state = runtime.step(user_input=None, now_ts=now, context={})
```

**执行流程：**

1. **无输入** → 返回当前节点的 prompt
2. **有输入** → 调用 `extract_answer` 解析
3. **解析成功** → 跳到下一个 slot 或结束链
4. **解析失败** → 检查是否允许重试
   - 允许 → 返回 retry prompt
   - 不允许 → 触发超限处理

### 7.3 超限行为

根据 `RetryPolicy.on_exceed` 决定：

- **ABORT**：终止当前任务链
- **FALLBACK**：交给人工或其他模块
- **CLARIFY**：进入澄清链
- **ASK_RESTART**：重新开始整个问询

---

## 8. 整体执行示例

参见 `scripts/demo_ask_chain_runtime.py`。

**成功路径示例：**

```
Round 0: 无输入 → prompt "请问你想去哪个医院？"
Round 1: 用户输入 "中山医院" → 解析成功 → 进入下一个 slot
Round 2: prompt "如果方便的话，请告诉我科室名称。"
Round 3: 用户输入 "皮肤科" → 解析成功 → 链完成
```

**失败路径示例：**

```
Round 0: 无输入 → prompt "请问你想去哪个医院？"
Round 1: 用户输入空串 → 解析失败 → retry prompt
Round 2: 用户再次输入空串 → 达到 limit → 触发 ABORT → 链终止
```

---

## 9. 后续计划（1.4.6b+）

### 9.1 链级总上限

- 全局 fail 限制（整个链最多允许多少次失败）
- 跨 slot 的重试计数

### 9.2 澄清链自动生成

- 根据 `CLARIFY` slot 自动生成澄清流程
- 支持多轮澄清对话

### 9.3 更复杂的自然语言理解

- 集成 NLP 模型进行意图识别
- 支持模糊匹配和同义词识别
- 上下文感知的答案提取

### 9.4 TaskChainManager 集成

- 在任务开始前自动插入 AskChain
- 根据 AskChainState 决定是否继续执行主任务链
- 支持 AskChain 与主任务链的数据传递

---

## 10. API 参考

### 10.1 快速开始

```python
from task_engine.ask import (
    AskSlot, AskSlotKind, AskSchema,
    AskChainBuilder, AskChainRuntime, AskManager,
    RetryPolicy, OnExceedAction
)

# 1. 定义 AskSchema
schema = AskSchema(
    task_id="hospital",
    slots=[
        AskSlot(
            name="hospital_name",
            kind=AskSlotKind.REQUIRED,
            prompt_template="请问你想去哪个医院？"
        ),
    ],
    retry_policy=RetryPolicy(
        interval=0.0,
        limit=1,
        on_exceed=OnExceedAction.ABORT
    )
)

# 2. 构建链
builder = AskChainBuilder()
plan = builder.build_chain(schema)

# 3. 创建 Runtime
ask_manager = AskManager()
effective_policy = schema.effective_retry_policy()
runtime = AskChainRuntime(plan, ask_manager, retry_policy=effective_policy)

# 4. 执行
result, state = runtime.step(user_input=None, now_ts=int(time.time()))
print(result.message)  # "请问你想去哪个医院？"

result, state = runtime.step(user_input="中山医院", now_ts=int(time.time()))
print(state.done)  # True（如果只有一个 slot）
```

---

## 11. 测试

所有测试用例位于 `luna_badge_tests/tests/v1_4_6a/`：

- `test_retry_policy.py`: RetryPolicy 单元测试
- `test_ask_manager_retry.py`: AskManager 重试逻辑测试
- `test_ask_schema.py`: AskSchema 测试
- `test_ask_node.py`: AskNode 测试
- `test_ask_chain.py`: AskChain 构建测试
- `test_ask_runtime.py`: AskChainRuntime 执行测试

运行所有测试：

```bash
cd luna_badge_tests
pytest tests/v1_4_6a/ -v
```













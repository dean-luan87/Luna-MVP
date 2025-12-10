# Luna Badge v1.4.4 Cursor Blueprint

**版本**: v1.4.4  
**创建日期**: 2025-01-05  
**目标**: Command Mode v1 + ECSv1（任务参数补全）

---

## BEGIN CURSOR BLUEPRINT v1.4.4

### 0. Version & Context

- **Project**: Luna Badge – Decision & Task System
- **Current stable baseline**: v1.4.3 (已通过 64 个自动化测试用例)
- **This blueprint**: v1.4.4 – Command Mode v1 + ECSv1（任务参数补全）
- **本版本目标**: 在 **不破坏 1.4.3 现有契约** 的前提下，增加一层"命令解析与任务参数补全"能力。

> **关键原则：**
> - 所有可执行任务必须来自明确命令（"Luna，XXX"）。
> - 允许在"命令已明确"的前提下，对任务参数作有限智能补全（记忆 + 附近 POI + 澄清询问）。
> - 不做聊天，不做情绪，不做自由意图推断。

---

### 1. Scope – 本次版本需要完成的内容

#### 1.1 必须新增的逻辑层

在现有 `Inquiry → DecisionCore → TaskChain` 之前新增一层 Command Layer：

1. **CommandPrefixDetector**
   - 判断是否为命令
   - 截出命令主体文本

2. **SemanticNormalizer v1**
   - 将口语命令归一化为有限几种意图 + 槽位结构

3. **ECSv1 (Enhanced Command Semantics)**
   - 当命令参数不完整时：
     1) 先用记忆补全（用户历史）
     2) 再用附近 POI 补全（根据地理位置）
     3) 最后用澄清询问让用户说完整

4. **NonCommandHandler**
   - 对非命令输入统一返回"当前仅支持明确指令"的提示
   - 不进入 Inquiry / DecisionCore / TaskChain

5. **HelpCenter Stub**（仅入口，不实现核心功能）
   - 识别"帮助中心"模式
   - 当前版本只返回"帮助中心将在后续版本开放"

#### 1.2 本版本显式不做

- 不实现聊天 / 闲聊 / 情绪相关逻辑
- 不基于"情绪/语气"推断任务目标
- 不改变 1.4.3 的核心接口签名（包括 `handle_event`、`ParsedIntent`、`DecisionOutput` 等）
- 不编写大规模测试实现（只允许创建最小骨架或 TODO，真正测试在后续单独版本做）

---

### 2. 目录与文件结构建议

在不破坏现有结构前提下，建议新增以下模块与文件：

```text
project_root/
  command_layer/
    __init__.py
    envelope.py              # CommandEnvelope 数据结构
    prefix_detector.py       # CommandPrefixDetector 实现
    semantic_normalizer.py   # SemanticNormalizer v1
    ecs_resolver.py          # ECSv1：记忆 + POI + 澄清
    non_command_handler.py   # 非命令拦截逻辑
    help_center_stub.py      # 帮助中心入口 Stub

  # 现有模块（不要移动 / 大改接口）
  inquiry/
  decision/
  taskchain/
  decision_logging/
  orchestrator.py
```

**要求：**
- Command Layer 必须是一个独立模块，不要把逻辑散落在 orchestrator / DecisionCore 里面。
- 所有新模块都必须是"可被单元测试调用的纯逻辑代码"。

---

### 3. 核心数据结构（Hard Contract）

#### 3.1 CommandEnvelope

新建 `command_layer/envelope.py`：

```python
from pydantic import BaseModel
from typing import Optional, Literal

class CommandEnvelope(BaseModel):
    is_command: bool
    raw_text: str
    command_text: Optional[str] = None  # 去掉"Luna"后的命令主体
    mode: Literal["TASK", "HELP_CENTER", "UNKNOWN"] = "UNKNOWN"
```

#### 3.2 NormalizedCommand

新建 `command_layer/semantic_normalizer.py` 中的核心模型：

```python
from pydantic import BaseModel
from typing import Dict, Any

class NormalizedCommand(BaseModel):
    intent_type: str            # e.g. "NAVIGATE", "CANCEL_TASK", "INSERT_TASK", "REPLACE_TASK"
    slots: Dict[str, Any]       # e.g. {"place_category": "hospital", "place_name": None}
    need_confirm: bool = False
```

#### 3.3 ResolutionResult（ECSv1 输出）

在 `command_layer/ecs_resolver.py`：

```python
from pydantic import BaseModel
from typing import Dict, Any, Optional, Literal

class ResolutionResult(BaseModel):
    resolved: bool
    slots: Dict[str, Any]
    source: Optional[Literal["memory", "poi", "user", "none"]] = None
    reason: Optional[str] = None
```

#### 3.4 与现有 ParsedIntent 的映射（不要改 ParsedIntent 定义）

ParsedIntent 已在 v1.4.3 中存在，禁止修改其字段结构。

只允许在 Command Layer → Inquiry 之间新建一个转换函数，例如：

```python
# somewhere in command_layer or orchestrator
from core.intent_schema import ParsedIntent

def normalized_to_parsed_intent(cmd: NormalizedCommand, resolution: ResolutionResult) -> ParsedIntent:
    # 结合 intent_type + slots 生成 ParsedIntent
    ...
```

**约束：**
- `ParsedIntent.intent_name` 由 `intent_type` 映射得出（固定映射表）。
- `ParsedIntent.slots` 优先使用 `place_name`，否则可以用 `place_category`。
- `need_confirm` 从 `NormalizedCommand` 透传。

---

### 4. 模块行为要求（详细）

#### 4.1 CommandPrefixDetector

**文件**: `command_layer/prefix_detector.py`

**目标**: 判断一条文本是否为 Luna 命令，并提取命令主体。

**输入**: 纯 str 文本（由上层语音识别转为文本后传入）。

**规则：**
- 支持以下前缀形式：
  - "Luna，"
  - "Luna,"
  - "Luna 请" / "Luna请"
  - "Luna 帮我" 等变体
- 去掉前缀后，剩余部分作为 `command_text`。
- 若整条语句只有 "Luna" 或 "Luna…" 没有实际命令内容，仍视为 `is_command = True`，但后续应返回"请给出明确指令"的提示。

**输出**: `CommandEnvelope`

```python
def detect_prefix(text: str) -> CommandEnvelope:
    ...
```

#### 4.2 SemanticNormalizer v1

**文件**: `command_layer/semantic_normalizer.py`

**目标**: 将各种口语化的命令文本归一化成有限几种 `intent_type` + `slots`。

**只需支持：**
- `NAVIGATE`
- `CANCEL_TASK`
- `INSERT_TASK`
- `REPLACE_TASK`

**示例映射：**
- "带我去医院", "导航到医院", "我得去趟医院"
  → `intent_type = "NAVIGATE"`, `slots = {"place_category": "hospital", "place_name": None}`
- "取消导航", "停止当前任务"
  → `intent_type = "CANCEL_TASK"`
- "顺便去711", "先去711"
  → `intent_type = "INSERT_TASK"`, `slots = {"place_category": "convenience_store", "place_name": "711"}`

**约束：**
- 不允许在 Normalizer 里做"自由意图推断"（即不根据情绪 / 主观句推任务）。
- 对于无法识别的命令，返回一个明确的错误结果，由上层决定如何提示用户。

#### 4.3 ECSv1 – 任务参数补全

**文件**: `command_layer/ecs_resolver.py`

**核心函数：**

```python
def resolve_slots(
    normalized: NormalizedCommand,
    memory_client: Optional[MemoryClient] = None,
    poi_client: Optional[POIClient] = None,
) -> ResolutionResult:
    ...
```

**处理流程：（顺序不能变）**

1. **MemoryResolver：**
   - 若 `slots["place_name"]` 为空，且 `place_category` 存在
   - 使用 `memory_client` 查询最近相关地点记录（例如最近三次医院地址）
   - 若有候选 → 生成一个"需要用户确认"的问句（由 DecisionCore / Orchestrator 播报），`source = "memory"`

2. **POIResolver：**
   - 若记忆无结果或用户拒绝
   - 使用 `poi_client` 查询附近同类 POI（医院 / 711 / 银行等），按距离排序
   - 提示："附近最近的是 XX，您是要去这里吗？"

3. **ClarificationPrompt：**
   - 若用户拒绝所有候选或搜索不到
   - 设置 `resolved = False`, `reason = "need_user_specify_target"`
   - 由上一层生成："请说出具体的 XXX 名称。"

**实现注意：**
- 本版本允许 ECSv1 只输出结构，不完全实现与真实 memory / POI 系统的对接，可以提供 `FakeMemoryClient` / `FakePOIClient` 方便后续测试。
- 不允许 ECSv1 自行新建任务，只能补全 slots 或返回 `resolved = False`。

#### 4.4 NonCommandHandler

**文件**: `command_layer/non_command_handler.py`

统一输出固定结构，例如：

```python
def handle_non_command(text: str) -> dict:
    return {
        "type": "NON_COMMAND_RESPONSE",
        "message": "我现在处于任务模式，只能执行明确的指令。如果你想聊天或问问题，这部分能力会在后续版本开放。"
    }
```

**禁止：**
- 在 NonCommandHandler 内调用 TaskChain / DecisionCore。
- 修改任何与任务相关的状态。

#### 4.5 HelpCenter Stub

**文件**: `command_layer/help_center_stub.py`

**识别模式：**
- 当 `command_text` 中包含 "帮助中心"/"帮助" 等关键词时，将 `mode` 设置为 `"HELP_CENTER"`。

**当前版本行为：**

```python
def handle_help_center(command_text: str) -> dict:
    return {
        "type": "HELP_CENTER_STUB",
        "message": "帮助中心将在后续版本开放。"
    }
```

不修改任何任务状态。

---

### 5. Orchestrator 集成改造（关键）

在 `orchestrator.py` 中，对 `simulate_user_input` 做分层改造：

**大致逻辑（伪代码）：**

```python
from command_layer.prefix_detector import detect_prefix
from command_layer.semantic_normalizer import normalize_command
from command_layer.ecs_resolver import resolve_slots
from command_layer.non_command_handler import handle_non_command
from command_layer.help_center_stub import handle_help_center
from core.intent_schema import ParsedIntent

def simulate_user_input(text: str, context: Optional[dict] = None) -> dict:
    env = detect_prefix(text)

    if not env.is_command:
        # 非命令路径，直接返回提示，不进入 Inquiry/Decision/TaskChain
        return handle_non_command(text)

    if env.mode == "HELP_CENTER":
        # 帮助中心入口 Stub
        return handle_help_center(env.command_text or "")

    # 正常 TASK 模式：
    normalized = normalize_command(env.command_text or "")

    # 针对 NAVIGATE / INSERT_TASK / REPLACE_TASK 等需要参数的命令，调用 ECSv1
    resolution = resolve_slots(normalized, memory_client=..., poi_client=...)

    # 将 normalized + resolution 合并为 ParsedIntent
    parsed_intent: ParsedIntent = normalized_to_parsed_intent(normalized, resolution)

    # 进入原有的 v1.4.3 流程：
    decision_output = decision_core.handle_event(
        event_type="USER_INTENT",
        payload={"parsed_intent": parsed_intent},
        context=context or {},
    )

    # TaskChain 根据 decision_output 执行动作
    result = task_manager.apply_decision(decision_output)

    # 整合为一个对外响应
    return {
        "decision": decision_output.to_dict(),
        "task_state": task_manager.snapshot(),
    }
```

**重点：**
- 1.4.4 不允许绕过 `handle_event`/DecisionCore，所有决策仍然必须经过 DecisionCore。
- Command Layer 只做"前处理 + 参数补全"，不直接控制任务链。

---

### 6. 禁止事项汇总（Hard Rules）

实现时，Cursor 必须遵守以下禁止项：

1. 不修改 `ParsedIntent` / `DecisionOutput` / `DecisionCore.handle_event` 的字段结构和核心契约。
2. 不在 Command Layer 中调用 TaskChain 的内部方法（所有状态改变必须经 DecisionCore → TaskChain）。
3. 不将非命令文本当作任务处理。
4. 不基于情绪类表达（"我好累""我不开心"）创建任何任务。
5. 不在 HelpCenter Stub 中修改任务状态。
6. 不引入情绪字段（emotion / mood）参与任何决策逻辑。
7. 不在本版本中自动生成大规模测试代码（测试实现将在后续版本中单独处理；如需，可创建空测试文件或 TODO 标记）。

---

### 7. 实施阶段建议（可按阶段执行）

如果需要分阶段开发，建议按以下顺序：

1. **Phase 1**: 创建 `command_layer/` 目录与基础数据结构（CommandEnvelope / NormalizedCommand / ResolutionResult）。
2. **Phase 2**: 实现 CommandPrefixDetector，并在 orchestrator 中接入 `detect_prefix` 与 NonCommandHandler 分支。
3. **Phase 3**: 实现 SemanticNormalizer v1，完成基础命令 → intent 映射。
4. **Phase 4**: 实现 ECSv1 的结构和伪实现（可先用 FakeMemoryClient / FakePOIClient）。
5. **Phase 5**: 实现 HelpCenter Stub 模式分支。
6. **Phase 6**: 将 NormalizedCommand + ResolutionResult 映射为 ParsedIntent，打通到 DecisionCore + TaskChain。
7. **Phase 7**: 做一次手动端到端测试（人工模拟几条命令：正常命令、模糊命令、非命令、帮助中心），确认行为符合预期。

**注意**: 自动化测试（pytest 等）本蓝图中不要求 Cursor 立即实现，将在下一轮"测试实现版本"中单独做。

---

## END CURSOR BLUEPRINT v1.4.4

---

## 实施建议

### 下一步建议流程

1. **先让 Cursor 按 Phase 1–3 完成基础结构 + Prefix + Normalizer。**
2. **然后再做 ECSv1 + Orchestrator 集成。**
3. **最后由你自己先做一轮人工 E2E 验证（和 1.4.3 一样），确认行为正确，再进入"测试实现版本"。**

### 审查要点

当你把 Cursor 的第一轮实现结果/总结贴回来，我可以帮你做一次"结构 + 行为"的人工审查。

---

**文档版本**: v1.0  
**创建日期**: 2025-01-05  
**维护者**: Luna Badge Team


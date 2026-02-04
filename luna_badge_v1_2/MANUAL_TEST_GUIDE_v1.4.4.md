# Luna Badge v1.4.4 手动测试指南

**版本**: v1.4.4  
**日期**: 2025-01-05

---

## 快速开始

### 方法 1: 使用 Python 交互式环境

```bash
cd /Users/luanlei/Desktop/Luna-2/luna_badge_v1_2
python3
```

然后在 Python 中运行：

```python
from orchestrator import Orchestrator

# 创建实例
o = Orchestrator()

# 测试用例 1: 带完整地点名称的命令
result1 = o.simulate_user_input("Luna，请带我去虹口医院")
print("测试 1 结果:")
print(result1)
print()

# 测试用例 2: 需要参数补全的命令
result2 = o.simulate_user_input("Luna，请带我去医院")
print("测试 2 结果:")
print(result2)
print()

# 测试用例 3: 非命令输入
result3 = o.simulate_user_input("我想出去走走")
print("测试 3 结果:")
print(result3)
print()

# 测试用例 4: 取消任务
result4 = o.simulate_user_input("Luna，取消任务")
print("测试 4 结果:")
print(result4)
print()

# 测试用例 5: 替换任务
result5 = o.simulate_user_input("Luna，我要换成去瑞金医院")
print("测试 5 结果:")
print(result5)
print()

# 测试用例 6: 帮助中心
result6 = o.simulate_user_input("Luna，打开帮助中心")
print("测试 6 结果:")
print(result6)
```

---

### 方法 2: 使用测试脚本

运行提供的测试脚本：

```bash
cd /Users/luanlei/Desktop/Luna-2/luna_badge_v1_2
python3 test_manual_v1_4_4.py
```

---

### 方法 3: 一行命令测试

```bash
cd /Users/luanlei/Desktop/Luna-2/luna_badge_v1_2
python3 -c "
from orchestrator import Orchestrator
o = Orchestrator()
print('测试:', o.simulate_user_input('Luna，请带我去医院'))
"
```

---

## 测试用例清单

### 基础功能测试

| 测试用例 | 输入 | 预期结果 |
|---------|------|---------|
| 完整地点名称 | `Luna，请带我去虹口医院` | 识别为 START_TASK，提取地点名称 |
| 参数补全 | `Luna，请带我去医院` | 从记忆补全，返回候选地点 |
| 非命令拦截 | `我想出去走走` | 返回 NON_COMMAND_RESPONSE |
| 取消任务 | `Luna，取消任务` | 识别为 CANCEL_TASK |
| 替换任务 | `Luna，我要换成去瑞金医院` | 识别为 CHANGE_DESTINATION |
| 帮助中心 | `Luna，打开帮助中心` | 返回 HELP_CENTER_STUB |

### 边界测试

| 测试用例 | 输入 | 预期结果 |
|---------|------|---------|
| 空命令 | `Luna` | 返回 EMPTY_COMMAND 提示 |
| 模糊命令 | `Luna，去某个地方` | 返回需要澄清 |
| 插入任务 | `Luna，顺便去711` | 识别为 INSERT_TASK |

---

## 查看结果说明

### 成功响应的结构

```python
{
    'parsed_intent': ParsedIntent(...),  # 解析后的意图
    'decision_output': DecisionOutput(...),  # 决策输出
    'taskchain_state': {...}  # 任务链状态
}
```

### 非命令响应的结构

```python
{
    'type': 'NON_COMMAND_RESPONSE',
    'message': '我现在处于任务模式...',
    'raw_text': '...'
}
```

### 帮助中心响应的结构

```python
{
    'type': 'HELP_CENTER_STUB',
    'message': '帮助中心将在后续版本开放。',
    'command_text': '...'
}
```

---

## 调试技巧

### 1. 查看详细日志

运行时会自动输出决策日志，格式如下：
```
[Decision] {"event_type": "user_intent", "intent_name": "START_TASK", ...}
```

### 2. 检查意图解析

```python
result = o.simulate_user_input("Luna，请带我去医院")
print("意图名称:", result['parsed_intent'].intent_name)
print("槽位信息:", result['parsed_intent'].slots)
print("来源:", result['parsed_intent'].source)
```

### 3. 检查决策输出

```python
result = o.simulate_user_input("Luna，请带我去医院")
print("决策动作:", result['decision_output'].action)
print("参数:", result['decision_output'].params)
print("播报文案:", result['decision_output'].narration)
```

### 4. 检查任务链状态

```python
result = o.simulate_user_input("Luna，请带我去医院")
print("当前任务:", result['taskchain_state']['active_task'])
print("当前节点:", result['taskchain_state']['active_node'])
print("子任务栈大小:", result['taskchain_state']['sub_task_stack_size'])
```

---

## 常见问题

### Q: 导入错误怎么办？

**A**: 确保在项目根目录运行：
```bash
cd /Users/luanlei/Desktop/Luna-2/luna_badge_v1_2
python3
```

### Q: 如何测试参数补全功能？

**A**: 使用不完整的地点信息：
```python
# 只有类别，没有具体名称
result = o.simulate_user_input("Luna，请带我去医院")
# 应该从 FakeMemoryClient 补全为 "北京协和医院"
```

### Q: 如何查看 Command Layer 的中间结果？

**A**: 可以直接测试 Command Layer 模块：
```python
from command_layer.prefix_detector import detect_prefix
from command_layer.semantic_normalizer import normalize_command
from command_layer.ecs_resolver import resolve_slots, FakeMemoryClient, FakePOIClient

# 测试命令检测
envelope = detect_prefix("Luna，请带我去医院")
print("是否命令:", envelope.is_command)
print("命令文本:", envelope.command_text)

# 测试语义归一化
normalized = normalize_command("请带我去医院")
print("意图类型:", normalized.intent_type)
print("槽位:", normalized.slots)

# 测试参数补全
memory_client = FakeMemoryClient()
poi_client = FakePOIClient()
resolution = resolve_slots(normalized, memory_client, poi_client)
print("补全结果:", resolution.resolved)
print("补全来源:", resolution.source)
print("补全后槽位:", resolution.slots)
```

---

## 测试脚本

已创建 `test_manual_v1_4_4.py`，可以直接运行进行完整测试。

---

**提示**: 如果遇到问题，检查：
1. 是否在正确的目录
2. Python 版本（建议 3.9+）
3. 是否有循环导入错误（已修复）













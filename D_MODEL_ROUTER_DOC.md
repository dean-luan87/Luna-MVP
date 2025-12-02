# 🔵 D｜模型路由器（Model Router）设计文档（仅 L1 + L2）

Luna Badge v1.3.0 版本采用双模型协同架构的模型路由器实现。

## 📋 目录

- [设计概述](#设计概述)
- [架构说明](#架构说明)
- [路由原则](#路由原则)
- [输入输出](#输入输出)
- [代码结构](#代码结构)
- [使用方法](#使用方法)
- [测试验证](#测试验证)
- [扩展说明](#扩展说明)

---

## 设计概述

### 双模型架构

- **L1 → 小模型（0.5B / 1.5B）**
  - 设备侧/边缘执行
  - 快速、离线、稳定
  - 用于：实时安全判断 / 命令词 / 简易导航 / 任务链状态转移

- **L2 → 主模型（3B）**
  - 近端服务器/主服务执行
  - 负责：自然对话、复杂语义、任务链生成、场景解释

### 模型路由器的职责

模型路由器（Router）是两者之间的调度大脑，负责决定：

**"当前输入应该由 L1 处理，还是交给 L2？"**

---

## 架构说明

```
用户输入
   ↓
Router 决策
   ├─→ 危险场景？ → L1（强制）
   ├─→ 简单导航？ → L1
   ├─→ 复杂语义？ → L2
   └─→ L2 失败？ → L1（降级）
   ↓
输出结果
```

---

## 路由原则

### D1｜Router 总体原则

Router 按以下硬规则工作：

#### 1）安全优先原则

只要出现任何"危险 / 临近危险情形"，
→ **强制用 L1**（因为延迟最小、稳定性最高）

包括：
- "停下 / 有人 / 有车 / 有障碍物"
- 摄像头检测到危险区域
- 偏航、逆行、错方向
- 设备本身信号异常（如定位跳变）

#### 2）语义分层原则

复杂语义始终由 L2 处理：
- 规划类表达
- 多步骤意图
- 医院/地铁/商业场景
- 情绪表达、问题、解释
- 用户需要陪伴 / 安抚

#### 3）降级原则

若 L2 异常、超时、资源不足
→ **自动回退到 L1**

---

## 输入输出

### D2｜Router 输入结构（Input Context）

Router 决策依赖三类输入：

```python
{
    "text": "用户原话",
    "scene_type": "street" / "hospital" / "traffic" / "...",
    "critical_flag": True / False,        # 系统级危险标识
    "task_state": "navigating" / "paused" / "idle",
    "user_confused": True / False,        # 从对话中检测（L2 会给出）
    "vision_alert": True / False          # 来自视觉系统
}
```

其中：
- `critical_flag`：系统级危险标识
- `vision_alert`：视觉模型触发的实时危险
- `user_confused`：从对话中检测（L2 会给出）

### D3｜Router 决策逻辑（仅 L1 + L2）

Router 的决策树如下：

```
Step 1: 如果 critical_flag=True → L1
Step 2: 使用 L1 做意图分类
Step 3: 如果意图属于 "简单导航/确认/方向" → L1
Step 4: 否则 → L2
Step 5: 如果 L2 执行失败 → 回退 L1（降级策略）
```

#### 用文字解释：

1. **紧急情况 → 强制 L1**
   - 保证毫秒级响应，不做复杂推理

2. **常规导航语义 → L1**

   例如：
   - "往左"
   - "继续走吗？"
   - "前面是什么？"
   - "我是不是走错了？"
   - "还有多远？"

   这些不需要 L2，只需要结构化结果。

3. **复杂意图 → L2**

   例如：
   - "先去711再去医院"
   - "我应该去哪一个窗口挂号？"
   - "为什么你说我偏航了？"
   - "我有点紧张，你帮我一下。"
   - "能不能给我讲一下流程？"

4. **L2 异常 → 降级到 L1**

   如果：
   - L2 超时
   - L2 返回空
   - L2 内部错误
   - L2 上下文解析失败

   → Router 自动改为 L1 模式。

### D4｜Router 输出结构

Router 返回统一结构，便于主程序处理：

```python
{
    "model": "L1" / "L2",
    "response": {
        "text": "模型响应文本",
        "intent": "意图类型（L1）",
        "confidence": 0.8
    },
    "reason": "critical" / "simple_nav" / "complex_semantic" / "fallback_L2_error"
}
```

---

## 代码结构

### 文件组织

```
luna_badge_v1_2/core/
    ├── model_router.py      # 模型路由器主文件
    ├── qwen_loader.py       # Qwen 模型加载器
    └── test_model_router.py # 测试脚本
```

### 核心类

#### 1. `QwenModelLoader`

负责加载 L1 和 L2 模型。

**主要方法：**
- `load_l1(model_size="0.5B")` - 加载 L1 模型
- `load_l2(model_size="3B")` - 加载 L2 模型
- `get_l1_callable()` - 获取 L1 模型可调用对象
- `get_l2_callable()` - 获取 L2 模型可调用对象

**便捷函数：**
- `load_l1()` - 快速加载 L1 模型
- `load_l2()` - 快速加载 L2 模型

#### 2. `ModelRouter`

模型路由器的核心类。

**主要方法：**
- `route(text, context)` - 路由主入口
- `_call_L1(text, reason)` - 调用 L1 模型
- `_call_L2(text, reason)` - 调用 L2 模型

---

## 使用方法

### 安装依赖

```bash
pip install transformers accelerate tiktoken
```

### 基本使用

```python
from luna_badge_v1_2.core.qwen_loader import load_l1, load_l2
from luna_badge_v1_2.core.model_router import ModelRouter

# 1. 加载模型
l1_model = load_l1(model_size="0.5B")  # 或 "1.5B"
l2_model = load_l2(model_size="3B")

# 2. 创建路由器
router = ModelRouter(l1_model=l1_model, l2_model=l2_model)

# 3. 使用路由器
result = router.route(
    text="往左走",
    context={
        "scene_type": "street",
        "critical_flag": False,
        "vision_alert": False
    }
)

print(f"使用的模型: {result['model']}")
print(f"路由原因: {result['reason']}")
print(f"响应: {result['response']['text']}")
```

### 高级使用

```python
from luna_badge_v1_2.core.qwen_loader import QwenModelLoader
from luna_badge_v1_2.core.model_router import ModelRouter

# 使用加载器类（更灵活）
loader = QwenModelLoader()

# 加载 L1 模型（1.5B）
loader.load_l1(model_size="1.5B", device_map="auto")

# 加载 L2 模型（3B）
loader.load_l2(model_size="3B", device_map="auto")

# 创建路由器
router = ModelRouter(
    l1_model=loader.get_l1_callable(),
    l2_model=loader.get_l2_callable()
)

# 危险场景（强制 L1）
result = router.route(
    text="停下",
    context={"critical_flag": True}
)
# result['model'] == "L1"
# result['reason'] == "critical"

# 简单导航（L1）
result = router.route(
    text="往左走",
    context={}
)
# result['model'] == "L1"
# result['reason'] == "simple_nav"

# 复杂语义（L2）
result = router.route(
    text="我应该去哪一个窗口挂号？",
    context={}
)
# result['model'] == "L2"
# result['reason'] == "complex_semantic"
```

---

## 测试验证

### 运行测试脚本

```bash
cd /Users/luanlei/Desktop/Luna-2
python3 luna_badge_v1_2/core/test_model_router.py
```

### 测试用例

测试脚本包含以下测试场景：

1. **危险场景测试**：验证 `critical_flag` 和 `vision_alert` 是否强制使用 L1
2. **简单导航测试**：验证简单导航意图是否路由到 L1
3. **复杂语义测试**：验证复杂语义是否路由到 L2
4. **降级机制测试**：验证 L2 失败时是否自动降级到 L1
5. **无模型测试**：验证无模型时的错误处理

---

## 扩展说明

### 未来升级路径（L3 预留）

当前版本仅实现 L1 + L2，但保留了扩展接口：

1. **L3 模型**：可以添加 `load_l3()` 方法
2. **更复杂的路由策略**：可以在 `route()` 方法中添加 L3 路由逻辑
3. **动态模型选择**：可以基于模型负载动态选择

### 意图分类扩展

当前使用简单的关键词匹配进行意图分类，未来可以：

1. **使用专门的分类模型**：训练一个轻量级意图分类器
2. **基于上下文的历史记录**：利用对话历史进行更准确的分类
3. **多轮对话理解**：处理多轮对话中的上下文依赖

---

## 模型下载

### L1 模型（0.5B）

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-0.5B-Instruct",
    device_map="auto"
)
```

### L1 模型（1.5B）

```python
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B-Instruct")
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-1.5B-Instruct",
    device_map="auto"
)
```

### L2 模型（3B）

```python
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-3B-Instruct")
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-3B-Instruct",
    device_map="auto"
)
```

---

## 总结

✅ **D 部分（仅 L1 + L2）已经完全实现完毕**

- ✅ 模型路由器核心逻辑
- ✅ Qwen 模型加载器
- ✅ 完整的测试脚本
- ✅ 清晰的文档说明

现在结构完全干净、无 L3 逻辑、可直接使用。

---

## 下一步建议

可以继续开发：

1. **E｜Router 调试模式**：打印每步决策过程
2. **E｜Router 与任务链对接机制**：集成到任务链系统中
3. **E｜Router 与导航模块的集成**：与导航系统集成
4. **E｜性能监控**：添加模型调用性能统计
5. **E｜缓存机制**：对常见问题添加响应缓存










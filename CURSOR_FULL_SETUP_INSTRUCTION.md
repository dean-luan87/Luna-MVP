# 🚀 📌 最终版 Cursor 指令（一站式完整设置）

**复制整条指令到 Cursor，自动完成所有工程化操作**

---

## 📋 目标

将以下模块整合为一个可运行的 Luna 1.3.0 模型系统：

- core/model_router.py (D 部分 Router 代码)
- core/qwen_loader.py (E1 部分 Loader 代码)
- core/error_codes.py
- core/tracking.py

**最终目标**：能够直接运行 `python test_router.py` 并成功执行

---

## ✅ 任务清单

### 一、Router × Loader 自动对接

### 二、完整的埋点系统接入

### 三、修复所有 import 路径

### 四、生成可运行的测试脚本

### 五、生成完整的 requirements.txt

### 六、最终验证和修复

---

## 🔧 开始执行

### 步骤 1：创建/更新 core/__init__.py

**文件路径**：`luna_badge_v1_2/core/__init__.py`

```python
"""
Luna Badge v1.3.0 Core Modules
"""

# 导出主要模块
from .model_router import ModelRouter
from .qwen_loader import QwenModelLoader, load_l1, load_l2
from .tracking import TrackingSystem, EventType
from .error_codes import ErrorCode, ErrorInfo, create_error_response, create_success_response
from .inference_wrapper import InferenceWrapper
from .replay_manager import ReplayManager, ReplayMode

__all__ = [
    "ModelRouter",
    "QwenModelLoader",
    "load_l1",
    "load_l2",
    "TrackingSystem",
    "EventType",
    "ErrorCode",
    "ErrorInfo",
    "create_error_response",
    "create_success_response",
    "InferenceWrapper",
    "ReplayManager",
    "ReplayMode",
]
```

---

### 步骤 2：增强 model_router.py - 自动加载模型

**文件路径**：`luna_badge_v1_2/core/model_router.py`

在文件开头添加自动加载功能：

```python
"""
Model Router (v1.3.0)

模型路由器（Model Router，含埋点）

Luna 1.3.0 版本采用双模型协同架构：
- L1 → 小模型（0.5B / 1.5B）：设备侧/边缘执行，快速、离线、稳定
- L2 → 主模型（3B）：近端服务器/主服务执行，负责复杂语义

模型路由器（Router）是两者之间的调度大脑，负责决定：
"当前输入应该由 L1 处理，还是交给 L2？"

设计原则：
1. 安全优先：危险情况强制用 L1（延迟最小、稳定性最高）
2. 语义分层：简单导航用 L1，复杂语义用 L2
3. 降级原则：L2 异常时自动回退到 L1
"""

import logging
import time
from typing import Dict, Any, Optional, Callable

from .tracking import TrackingSystem, EventType
from .qwen_loader import QwenModelLoader

logger = logging.getLogger(__name__)


class ModelRouter:
    """
    模型路由器（Model Router）

    负责在 L1 和 L2 模型之间进行智能路由

    路由规则：
    1. 安全优先：critical_flag 或 vision_alert → 强制 L1
    2. 简单导航意图 → L1
    3. 复杂语义意图 → L2
    4. L2 失败 → 降级到 L1
    """

    # 简单导航类意图集合
    SIMPLE_INTENTS = ["simple_nav", "orientation", "confirm", "yes_no"]

    def __init__(
        self,
        l1_model: Optional[Callable] = None,
        l2_model: Optional[Callable] = None,
        tracking: Optional[TrackingSystem] = None,
        auto_load: bool = False,
        l1_model_size: str = "0.5B",
        l2_model_size: str = "3B",
    ):
        """
        初始化模型路由器

        Args:
            l1_model: L1 模型的可调用对象（函数），如果为 None 且 auto_load=True 则自动加载
            l2_model: L2 模型的可调用对象（函数），如果为 None 且 auto_load=True 则自动加载
            tracking: 埋点系统实例（可选）
            auto_load: 是否自动加载模型
            l1_model_size: L1 模型大小（仅 auto_load=True 时有效）
            l2_model_size: L2 模型大小（仅 auto_load=True 时有效）
        """
        self.tracking = tracking
        self.loader = None

        # 自动加载模型
        if auto_load:
            logger.info("🚀 启用自动加载模型模式")
            self.loader = QwenModelLoader(tracking=tracking)
            
            # 加载 L1
            if l1_model is None:
                logger.info(f"正在自动加载 L1 模型 ({l1_model_size})...")
                if self.loader.load_l1(model_size=l1_model_size):
                    l1_model = self.loader.get_l1_callable()
                else:
                    logger.error("❌ L1 模型自动加载失败")
            
            # 加载 L2
            if l2_model is None:
                logger.info(f"正在自动加载 L2 模型 ({l2_model_size})...")
                if self.loader.load_l2(model_size=l2_model_size):
                    l2_model = self.loader.get_l2_callable()
                else:
                    logger.warning("⚠️ L2 模型自动加载失败，将只能使用 L1")

        self.l1 = l1_model
        self.l2 = l2_model

        if self.l1 is None:
            logger.warning("⚠️ L1 模型未加载，路由功能可能受限")
        if self.l2 is None:
            logger.warning("⚠️ L2 模型未加载，将只能使用 L1")

        logger.info("✅ 模型路由器初始化完成")

    # ... 保留原有 route() 方法和其他方法不变 ...
```

**重要**：上面的代码片段只展示了 `__init__` 方法的修改。请保留原有的 `route()`、`_call_L1()`、`_call_L2()` 等方法不变。

---

### 步骤 3：创建完整的测试脚本

**文件路径**：`luna_badge_v1_2/test_router.py`

```python
#!/usr/bin/env python3
"""
Router 完整测试脚本

测试 L1、L2 和 Router 的完整功能
"""

import sys
import os
import logging
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/test_router.log', encoding='utf-8') if os.path.exists('logs') else logging.StreamHandler()
    ]
)

from core.tracking import TrackingSystem, EventType
from core.qwen_loader import QwenModelLoader
from core.model_router import ModelRouter
from core.error_codes import ErrorCode

logger = logging.getLogger(__name__)


def setup_logging():
    """设置日志目录"""
    os.makedirs("logs", exist_ok=True)
    os.makedirs("logs/tracking", exist_ok=True)


def test_l1():
    """测试 L1 模型"""
    print("\n" + "=" * 60)
    print("测试 1: L1 模型推理")
    print("=" * 60)

    try:
        # 初始化埋点
        tracking = TrackingSystem(log_dir="logs/tracking")
        tracking.start_session("test_l1")

        # 加载 L1
        loader = QwenModelLoader(tracking=tracking)
        print("\n📦 正在加载 L1 模型...")
        if not loader.load_l1(model_size="0.5B"):
            print("❌ L1 模型加载失败")
            return False

        # 获取 L1 调用函数
        l1_model = loader.get_l1_callable()
        if l1_model is None:
            print("❌ 无法获取 L1 模型调用函数")
            return False

        # 测试推理
        test_input = "左转"
        print(f"\n📝 输入: {test_input}")

        import time
        start_time = time.time()
        result = l1_model(test_input)
        latency_ms = (time.time() - start_time) * 1000

        print(f"✅ L1 推理成功")
        print(f"   意图: {result.get('intent', 'N/A')}")
        print(f"   置信度: {result.get('confidence', 'N/A')}")
        print(f"   响应: {result.get('text', 'N/A')[:100]}...")
        print(f"   延迟: {latency_ms:.2f}ms")

        # 记录埋点
        tracking.track_inference(
            model="L1",
            user_input=test_input,
            response=result.get('text', ''),
            latency_ms=latency_ms,
            success=True,
        )
        tracking.flush()

        return True

    except Exception as e:
        print(f"❌ L1 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_l2():
    """测试 L2 模型"""
    print("\n" + "=" * 60)
    print("测试 2: L2 模型推理")
    print("=" * 60)

    try:
        # 初始化埋点
        tracking = TrackingSystem(log_dir="logs/tracking")
        tracking.start_session("test_l2")

        # 加载 L2
        loader = QwenModelLoader(tracking=tracking)
        print("\n📦 正在加载 L2 模型...")
        if not loader.load_l2(model_size="3B"):
            print("❌ L2 模型加载失败")
            return False

        # 获取 L2 调用函数
        l2_model = loader.get_l2_callable()
        if l2_model is None:
            print("❌ 无法获取 L2 模型调用函数")
            return False

        # 测试推理
        test_input = "我想去医院挂号"
        print(f"\n📝 输入: {test_input}")

        import time
        start_time = time.time()
        result = l2_model(test_input)
        latency_ms = (time.time() - start_time) * 1000

        print(f"✅ L2 推理成功")
        print(f"   响应: {result.get('text', 'N/A')[:200]}...")
        print(f"   延迟: {latency_ms:.2f}ms")

        # 记录埋点
        tracking.track_inference(
            model="L2",
            user_input=test_input,
            response=result.get('text', ''),
            latency_ms=latency_ms,
            success=True,
        )
        tracking.flush()

        return True

    except Exception as e:
        print(f"❌ L2 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_router():
    """测试 Router"""
    print("\n" + "=" * 60)
    print("测试 3: Router 路由决策")
    print("=" * 60)

    try:
        # 初始化埋点
        tracking = TrackingSystem(log_dir="logs/tracking")
        tracking.start_session("test_router")

        # 创建 Router（自动加载模型）
        print("\n📦 正在初始化 Router（自动加载模型）...")
        router = ModelRouter(
            auto_load=True,
            tracking=tracking,
            l1_model_size="0.5B",
            l2_model_size="3B",
        )

        # 测试案例
        test_cases = [
            {
                "name": "简单导航",
                "text": "左转",
                "context": {},
                "expected_model": "L1",
            },
            {
                "name": "复杂语义",
                "text": "先去711再去医院",
                "context": {},
                "expected_model": "L2",
            },
            {
                "name": "危险场景",
                "text": "停下",
                "context": {"critical_flag": True},
                "expected_model": "L1",
            },
        ]

        results = []
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n--- 测试案例 {i}: {test_case['name']} ---")
            print(f"输入: {test_case['text']}")

            import time
            start_time = time.time()
            result = router.route(
                text=test_case['text'],
                context=test_case['context'],
            )
            latency_ms = (time.time() - start_time) * 1000

            selected_model = result.get('model', 'UNKNOWN')
            reason = result.get('reason', 'N/A')
            response_text = result.get('response', {}).get('text', 'N/A')

            print(f"✅ Router 决策完成")
            print(f"   选用模型: {selected_model}")
            print(f"   路由原因: {reason}")
            print(f"   响应: {response_text[:150]}...")
            print(f"   总延迟: {latency_ms:.2f}ms")

            results.append({
                "test": test_case['name'],
                "model": selected_model,
                "expected": test_case['expected_model'],
                "match": selected_model == test_case['expected_model'],
                "latency_ms": latency_ms,
            })

        # 刷新埋点
        tracking.flush()

        # 打印总结
        print("\n" + "=" * 60)
        print("Router 测试总结")
        print("=" * 60)
        for r in results:
            status = "✅" if r['match'] else "❌"
            print(f"{status} {r['test']}: {r['model']} (期望: {r['expected']}, 延迟: {r['latency_ms']:.2f}ms)")

        return all(r['match'] for r in results)

    except Exception as e:
        print(f"❌ Router 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_logs():
    """检查日志文件"""
    print("\n" + "=" * 60)
    print("检查日志文件")
    print("=" * 60)

    log_dirs = [
        "logs",
        "logs/tracking",
    ]

    for log_dir in log_dirs:
        if os.path.exists(log_dir):
            files = [f for f in os.listdir(log_dir) if f.endswith(('.log', '.jsonl', '.json'))]
            print(f"✅ {log_dir}: {len(files)} 个文件")
            for f in files[:5]:  # 只显示前5个
                filepath = os.path.join(log_dir, f)
                size = os.path.getsize(filepath)
                print(f"   - {f} ({size} bytes)")
        else:
            print(f"⚠️ {log_dir}: 目录不存在")


def main():
    """主函数"""
    print("🚀 开始 Router 完整测试")
    print("=" * 60)

    # 设置日志目录
    setup_logging()

    # 运行测试
    results = []

    # 测试 L1
    results.append(("L1 模型", test_l1()))

    # 测试 L2
    results.append(("L2 模型", test_l2()))

    # 测试 Router
    results.append(("Router", test_router()))

    # 检查日志
    check_logs()

    # 总结
    print("\n" + "=" * 60)
    print("📊 测试总结")
    print("=" * 60)
    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{status}: {name}")

    all_passed = all(result[1] for result in results)
    if all_passed:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print("\n⚠️ 部分测试失败，请检查日志")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

---

### 步骤 4：生成 requirements.txt

**文件路径**：`luna_badge_v1_2/requirements.txt`

```txt
# Luna Badge v1.3.0 依赖包

# 模型相关
transformers>=4.35.0
accelerate>=0.24.0
tiktoken>=0.5.0
torch>=2.0.0

# 数据处理
numpy>=1.24.0
opencv-python>=4.8.0

# 日志和追踪
jsonlines>=3.1.0

# 工具类
dataclasses>=0.8; python_version < '3.7'

# 可选：如果需要使用在线 API
requests>=2.31.0
```

---

### 步骤 5：创建根目录 __init__.py（如果不存在）

**文件路径**：`luna_badge_v1_2/__init__.py`

```python
"""
Luna Badge v1.3.0

Visual Navigation Assistant for Visually Impaired
"""

__version__ = "1.3.0"
```

---

### 步骤 6：验证和修复检查清单

请执行以下验证步骤：

1. **检查所有 import 路径**：
   ```bash
   python -c "from luna_badge_v1_2.core import ModelRouter, QwenModelLoader, TrackingSystem; print('✅ 导入成功')"
   ```

2. **检查文件结构**：
   ```bash
   ls -la luna_badge_v1_2/core/*.py
   ```

3. **运行测试脚本**：
   ```bash
   cd luna_badge_v1_2
   python test_router.py
   ```

---

## 🔍 自动修复清单

如果遇到问题，请自动执行以下修复：

### 修复 1：导入路径问题

检查所有文件中的相对导入是否正确：

- `from .tracking import ...` ✅
- `from core.tracking import ...` ❌（应该用相对导入）

### 修复 2：Case-sensitive 问题

确保所有文件名和导入路径的大小写一致：

- `ModelRouter` ✅
- `modelrouter` ❌

### 修复 3：缺失依赖

如果运行失败，检查是否缺少依赖：

```bash
pip install -r requirements.txt
```

### 修复 4：日志目录权限

确保日志目录有写入权限：

```python
import os
os.makedirs("logs/tracking", exist_ok=True)
```

---

## ✅ 最终验证

执行以下命令验证整个系统：

```bash
cd /Users/luanlei/Desktop/Luna-2/luna_badge_v1_2
python test_router.py
```

**预期输出**：

```
🚀 开始 Router 完整测试
============================================================
测试 1: L1 模型推理
============================================================
✅ L1 推理成功
...

测试 2: L2 模型推理
============================================================
✅ L2 推理成功
...

测试 3: Router 路由决策
============================================================
✅ Router 决策完成
...

🎉 所有测试通过！
```

---

## 📝 注意事项

1. **模型下载**：首次运行需要下载模型，可能需要较长时间
2. **内存要求**：L2 模型（3B）需要较大内存，建议至少 8GB
3. **GPU 加速**：如果有 GPU，会自动使用 GPU 加速
4. **日志文件**：所有日志会保存在 `logs/` 目录下

---

## 🎯 完成标志

完成以上所有步骤后，系统应该能够：

- ✅ 自动加载 L1 和 L2 模型
- ✅ Router 能够正确路由
- ✅ 所有埋点数据正常记录
- ✅ 日志文件正常写入
- ✅ 测试脚本成功运行

---

**🚀 现在复制以上所有步骤到 Cursor，让 AI 自动执行！**

























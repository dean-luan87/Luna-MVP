# Step 13.3: TTS 调用规范化迁移计划

## 迁移目标

将所有 `tts_manager.speak()` 调用替换为 `TTSRouterFacade` 的统一入口。

## 迁移规则

| 旧调用 | 新调用 | 类别 |
|--------|--------|------|
| `tts_manager.speak("导航提示")` | `tts_router.speak_nav("导航提示")` | NAVIGATION |
| `tts_manager.speak("停止")` | `tts_router.speak_safety("停止")` | SAFETY |
| `tts_manager.speak("任务开始")` | `tts_router.speak_task("任务开始")` | TASK |
| `tts_manager.speak("系统消息")` | `tts_router.speak_system("系统消息")` | SYSTEM |
| `tts_manager.speak("闲聊")` | `tts_router.speak_chat("闲聊")` | CHAT |

## 需要迁移的文件

### 1. `task_engine/ask/ask_runtime.py` (10 处)
- **类别**: ASK / TASK
- **替换**: 使用 `speak_task()` 或新增 `speak_ask()`（如果 TTSCategory 有 ASK）

### 2. `core/flow_engine/runtime.py` (4 处)
- **类别**: TASK
- **替换**: 使用 `speak_task()`

### 3. `task_engine/scene/scene_runtime.py` (3 处)
- **类别**: TASK / SYSTEM
- **替换**: 使用 `speak_task()` 或 `speak_system()`

### 4. `task_chain/task_chain_manager.py` (5 处)
- **类别**: TASK / SYSTEM
- **替换**: 使用 `speak_task()` 或 `speak_system()`

### 5. `decision_core/decision_core.py` (3 处)
- **类别**: TASK / SYSTEM
- **替换**: 使用 `speak_task()` 或 `speak_system()`

## 不需要迁移的文件

以下文件包含 `tts_manager.speak()` 但属于文档、测试或已废弃代码，**不需要修改**：

- `docs/*.md` - 文档文件
- `scripts/demo_*.py` - Demo 脚本（可选择性更新）
- `scripts/manual_test_*.py` - 测试脚本
- `releases/*.md` - 发布说明
- `mobile_bridge_server.py` - 旧代码（可能已废弃）
- `src/tasks/task_chain/navigation_task.py` - 旧代码路径

## 迁移步骤

1. 在每个文件顶部添加导入：
   ```python
   from task_engine.tts.router_facade import get_tts_router_facade
   tts_router = get_tts_router_facade()
   ```

2. 替换所有 `tts_manager.speak(...)` 调用为对应的语义化接口

3. 移除 `from task_engine.tts import tts_manager` 导入（如果不再需要）

4. 运行测试验证功能正常


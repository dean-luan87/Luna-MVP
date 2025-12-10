# TTS 调用迁移审计报告（v1.4.6d）

本文档列出所有 `tts_manager.speak()` 的调用位置，并标识哪些需要迁移到 `NavigationVoiceAdapter`。

---

## 📊 统计概览

- **总调用数**: 65 处（包含文档和测试文件）
- **实际代码调用**: ~25 处
- **需要迁移到 NavigationVoiceAdapter**: ~1 处（导航相关）
- **系统级调用（保留）**: ~24 处

---

## 🎯 需要迁移的文件（导航相关）

### 1. `tasks/navigation_task.py` ⚠️ **需要迁移**

**位置**: 第 292 行

```python
self.tts_manager.speak(speech_event)
```

**迁移建议**:
- 这是导航任务中的语音播报
- 需要根据 `speech_event` 的内容判断是导航指引还是安全提示
- 建议迁移到 `NavigationVoiceAdapter` 的对应方法

**迁移优先级**: 🔴 **高**（这是导航模块的核心调用）

---

## ✅ 系统级调用（保留，不需要迁移）

以下调用属于系统级功能，**不需要**迁移到 `NavigationVoiceAdapter`：

### 1. `task_chain/task_chain_manager.py` (5 处)

**用途**: 任务生命周期管理

- 第 162 行: 暂停任务提示
- 第 181 行: 恢复任务提示
- 第 200 行: 取消任务提示
- 第 261 行: 切换任务提示
- 第 443 行: 场景结束提示

**建议**: 保留，这些是任务管理相关的系统提示，不属于导航播报。

---

### 2. `decision_core/decision_core.py` (3 处)

**用途**: 决策核心的任务控制

- 第 113 行: 开始执行任务
- 第 190 行: 暂停任务
- 第 205 行: 恢复任务

**建议**: 保留，这些是决策层的系统提示。

---

### 3. `task_engine/ask/ask_runtime.py` (8 处)

**用途**: AskChain 问询播报

- 第 201 行: 首次提问
- 第 222 行: 重试提示
- 第 237 行: 超限提示（abort）
- 第 246 行: 超限提示（fallback）
- 第 264 行: 超限提示（clarify）
- 第 273 行: 澄清提示
- 第 278 行: 重启提示
- 第 305 行: 重试提示
- 第 323 行: 完成提示
- 第 342 行: 下一个节点提示

**建议**: 保留，这些是问询系统的专用播报，不属于导航。

---

### 4. `task_engine/scene/scene_runtime.py` (3 处)

**用途**: 场景切换播报

- 第 47 行: 场景进入
- 第 82 行: 场景事件
- 第 113 行: 场景退出

**建议**: 保留，这些是场景系统的专用播报。

---

### 5. `core/flow_engine/runtime.py` (4 处)

**用途**: 流程运行时播报

- 第 18 行: 任务链启动
- 第 60 行: 节点执行前
- 第 78 行: 任务中止
- 第 93 行: 任务完成

**建议**: 保留，这些是流程引擎的专用播报。

---

## 📝 文档和测试文件（不需要修改）

以下文件包含 `tts_manager.speak()` 的引用，但属于文档或测试，**不需要修改**：

- `docs/navigation_voice_migration_guide.md` - 迁移指南（示例代码）
- `scripts/manual_test_v1_4_6.py` - 手动测试脚本
- `releases/v1.4.6_release_note.md` - 发布说明
- 其他历史文档和报告文件

---

## 🎯 迁移行动计划

### 阶段 1: 导航任务迁移（高优先级）

**目标文件**: `tasks/navigation_task.py`

**步骤**:
1. 分析 `speech_event` 的内容和类型
2. 根据内容判断应该调用 `NavigationVoiceAdapter` 的哪个方法
3. 替换 `self.tts_manager.speak(speech_event)` 为对应的适配器方法

**示例**:
```python
# 旧代码
self.tts_manager.speak(speech_event)

# 新代码（需要根据 speech_event 内容判断）
from task_engine.navigation import NavigationVoiceAdapter
voice = NavigationVoiceAdapter()

# 如果是转向提示
if "左转" in speech_event or "右转" in speech_event:
    voice.announce_turn(direction=..., distance_m=...)
# 如果是安全提示
elif "障碍物" in speech_event or "危险" in speech_event:
    voice.announce_obstacle_warning(...)
# 等等
```

---

### 阶段 2: 系统级调用优化（可选，低优先级）

虽然系统级调用不需要迁移到 `NavigationVoiceAdapter`，但可以考虑：

1. **统一使用 TTS 策略体系**:
   - 将系统提示改为使用 `speak_task()` 或 `speak_system()`
   - 避免手写 `priority` 和 `interrupt`

2. **示例优化**:
   ```python
   # 旧代码
   tts_manager.speak("已暂停当前任务", level="info", channel="tts", ...)
   
   # 新代码
   from task_engine.tts import speak_task
   speak_task("已暂停当前任务", meta={"stage": "task_pause", "task_id": task_id})
   ```

---

## ✅ 迁移检查清单

- [ ] 分析 `tasks/navigation_task.py` 中的 `speech_event` 类型
- [ ] 创建 `speech_event` → `NavigationVoiceAdapter` 方法的映射
- [ ] 替换 `tasks/navigation_task.py` 中的调用
- [ ] 运行测试验证功能正常
- [ ] 检查是否有其他导航相关的 TTS 调用遗漏
- [ ] （可选）优化系统级调用，使用 TTS 策略体系

---

## 📚 相关文档

- `docs/navigation_voice_migration_guide.md`: 导航语音迁移指南
- `task_engine/navigation/navigation_voice_adapter.py`: 适配器实现
- `docs/tts_policy_usage.md`: TTS 策略使用指南

---

**最后更新**: 2025-01-XX  
**审计人员**: [待填写]


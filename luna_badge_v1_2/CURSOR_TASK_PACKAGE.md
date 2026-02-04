# Cursor 任务包：Luna Badge v1.4.2 完整实现

## 任务描述

实现 Luna Badge v1.4.2 核心系统，包括视觉管线、系统恢复、任务管理、导航控制、语音处理等模块。所有代码要求完整实现，无 TODO、无 pass 空实现。

## 执行步骤

### 1. 创建目录结构

```bash
mkdir -p infra
mkdir -p core/system
mkdir -p core/vision
mkdir -p core/task
mkdir -p navigation
mkdir -p speech
mkdir -p tests
```

### 2. 创建所有文件（按顺序）

#### 基础设施
- [ ] `infra/__init__.py` - 空文件
- [ ] `infra/logging_manager.py` - 日志管理器

#### 系统模块
- [ ] `core/system/system_monitor.py` - 系统监控
- [ ] `core/system/safe_mode.py` - 安全模式
- [ ] `core/system/system_recovery_center.py` - 系统恢复中心

#### 视觉模块
- [ ] `core/vision/camera_router.py` - 摄像头路由
- [ ] `core/vision/vision_scheduler.py` - 视觉调度器
- [ ] `core/vision/vision_fail_safe.py` - 视觉降级

#### 任务模块
- [ ] `core/task/task_transition_manager.py` - 任务转换管理器
- [ ] `core/task/multi_target_buffer.py` - 多目标缓存
- [ ] `core/task/query_bus.py` - 问询总线

#### 导航模块
- [ ] `navigation/__init__.py` - 空文件
- [ ] `navigation/navigation_controller.py` - 导航控制器

#### 语音模块
- [ ] `speech/__init__.py` - 空文件
- [ ] `speech/intent_parser.py` - 意图解析器
- [ ] `speech/speech_pipeline.py` - 语音管线

#### 主程序
- [ ] `main.py` - 主循环

#### 测试文件
- [ ] `tests/__init__.py` - 空文件
- [ ] `tests/test_vision_scheduler.py` - 视觉调度器测试
- [ ] `tests/test_vision_fail_safe.py` - 视觉降级测试
- [ ] `tests/test_task_transition.py` - 任务转换测试
- [ ] `tests/test_query_bus.py` - 问询总线测试
- [ ] `tests/test_stress_vision.py` - 压力测试

### 3. 验证步骤

#### 3.1 安装依赖
```bash
pip install pytest
```

#### 3.2 运行测试
```bash
cd luna_badge_v1_2
pytest -q tests/
```

预期结果：所有测试通过

#### 3.3 运行主程序（可选）
```bash
python main.py
```

预期结果：主循环正常运行（使用 Dummy ASR/TTS）

### 4. 代码检查清单

- [ ] 所有文件已创建
- [ ] 所有 `__init__.py` 文件已创建
- [ ] 无 TODO 注释
- [ ] 无 `pass` 空实现
- [ ] 所有导入路径正确
- [ ] 测试用例全部通过

## 文件内容

所有文件内容已在上面的代码块中提供，直接复制粘贴即可。

## 注意事项

1. **路径依赖**：确保所有模块的导入路径正确
2. **Python 版本**：需要 Python 3.8+
3. **类型注解**：使用了 `str | None` 语法（Python 3.10+），如果使用旧版本需要改为 `Optional[str]`
4. **Dummy 模块**：ASR/TTS/Camera 都是 Dummy 实现，真机需要替换为实际实现

## 完成标志

- ✅ 所有文件创建完成
- ✅ `pytest -q` 全部通过
- ✅ `main.py` 可以正常运行（Ctrl+C 退出）

## 后续工作

1. 替换 Dummy 模块为真实实现
2. 集成到现有项目（如果有冲突文件，需要做对齐）
3. 添加更多测试用例
4. 性能优化和调优
















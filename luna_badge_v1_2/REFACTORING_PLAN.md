# Luna Badge 项目重构计划

**版本**: v1.4.0  
**日期**: 2025-12-02  
**目标**: 测试与日志分离 + 代码结构清理规范化

## 📋 重构目标

1. ✅ 测试模块完全独立，不再和主系统耦合
2. ✅ 日志体系独立成子系统，可随时总开关
3. 🔄 代码整体结构清理：目录、模块、接口、无用代码
4. 🔄 后续扩展多模型、多线程、任务链时不会乱

## ✅ 已完成

### 1. 测试系统独立化
- ✅ 创建 `/tests` 目录结构
- ✅ 创建测试工具 (`tests/utils/test_helpers.py`)
- ✅ 创建测试运行脚本 (`run_all_tests.py`, `run_vision_tests.py`, `run_nav_tests.py`)

### 2. 统一日志系统
- ✅ 创建 `/core/logging/` 模块
- ✅ 实现日志配置 (`log_config.py`)
- ✅ 实现日志写入器 (`log_writer.py`)
- ✅ 实现日志轮转 (`log_rotator.py`)
- ✅ 实现统一日志接口 (`logger.py`)

## 🔄 进行中

### 3. 测试文件迁移
- 🔄 迁移根目录测试文件到 `/tests`
- 🔄 按类别分类到对应子目录
- 🔄 重命名为 `test_*.py` 格式

## 📝 待执行

### 4. 项目结构重构

#### 目标结构：
```
/src (或保持根目录)
    /core
        /config          # 统一配置中心
        /logging         # ✅ 已完成
        /utils           # 工具函数
        /state_machine   # 状态机（预留）
        /event_bus       # 事件总线
        /async_runner    # 异步运行器
    
    /vision
        /models          # YOLO, 分割, OCR 等模型
        /pipeline        # 视觉处理流水线
        /fusion          # 融合逻辑
        /perception_graph # 感知图谱（预留）
        /model_registry  # 模型注册表
    
    /navigation
        /planner         # 路径规划
        /path_eval       # 路径评估
        /map_builder     # 地图构建
        /obstacle_handler # 障碍物处理
    
    /audio
        /asr             # 语音识别
        /tts             # 语音合成
        /audio_router    # 音频路由
    
    /tasks
        /task_chain      # 任务链
        /task_manager    # 任务管理
        /task_cache      # 任务缓存
    
    /system
        /device          # 设备管理
        /camera          # 摄像头
        /sensors         # 传感器
        /recovery        # 恢复机制
```

### 5. 模块移动计划

#### Vision 模块
- `core/yolo_detector.py` → `vision/models/yolo/`
- `core/yolo_loader.py` → `vision/models/yolo/`
- `core/model_registry.py` → `vision/model_registry.py`
- `vision/` 目录下的文件 → 按功能分类移动

#### Navigation 模块
- `core/navigation_logic.py` → `navigation/planner/`
- `navigation/` 目录下的文件 → 按功能分类

#### Audio 模块
- `audio/tts_manager.py` → `audio/tts/`
- `speech/` → `audio/`

#### Tasks 模块
- `core/task/` → `tasks/task_chain/`
- `core/taskchain/` → `tasks/task_manager/`

### 6. 清理工作
- 删除废弃代码
- 删除未引用文件
- 删除临时文件
- 统一代码风格

### 7. 创建统一入口
- 创建 `main.py` 作为系统启动入口

## 📊 执行进度

- [x] 步骤 1: 创建测试系统目录
- [x] 步骤 2: 创建统一日志系统
- [ ] 步骤 3: 迁移测试文件
- [ ] 步骤 4: 创建新目录结构
- [ ] 步骤 5: 移动模块文件
- [ ] 步骤 6: 更新导入路径
- [ ] 步骤 7: 清理废弃代码
- [ ] 步骤 8: 代码格式化
- [ ] 步骤 9: 创建统一入口

## ⚠️ 注意事项

1. **分步执行**: 每个大步骤先输出重构计划，再执行
2. **保持兼容**: 重构过程中保持系统可运行
3. **测试验证**: 每步完成后进行基本测试
4. **备份重要**: 重要变更前先提交代码


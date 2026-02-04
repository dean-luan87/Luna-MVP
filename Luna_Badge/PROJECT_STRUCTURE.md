# Luna_Badge 项目完整结构文档

> 生成时间: 2025-01-18
> 
> 本文档包含 Luna_Badge 项目的完整目录结构、文件列表和模块说明。

---

## 📋 目录

1. [项目概览](#项目概览)
2. [一级目录结构](#一级目录结构)
3. [前端JS模块详细列表](#前端js模块详细列表)
4. [核心Python模块分类](#核心python模块分类)
5. [配置文件列表](#配置文件列表)
6. [主要入口文件](#主要入口文件)
7. [测试文件列表](#测试文件列表)
8. [文档文件列表](#文档文件列表)
9. [项目统计](#项目统计)
10. [新创建的导航系统模块](#新创建的导航系统模块)

---

## 项目概览

Luna_Badge 是一个智能导航辅助系统，包含完整的前后端架构：

- **前端**: 53个JavaScript模块，实现导航、场景推理、任务链等功能
- **后端**: 126个Python核心模块，提供视觉处理、导航、TTS等能力
- **配置**: 10个YAML/JSON配置文件
- **文档**: 113个Markdown文档

---

## 一级目录结构

| 目录名 | 说明 | 文件数量 |
|--------|------|----------|
| `frontend/` | 前端JS模块 | 53个JS文件 |
| `core/` | 核心Python模块 | 126个Python文件 |
| `docs/` | 文档文件 | 113个Markdown文档 |
| `config/` | 配置文件 | 10个配置文件 |
| `data/` | 数据存储 | JSON/图片等数据文件 |
| `bridge/` | 桥接模块 | WebSocket/YOLO桥接 |
| `backend/` | 后端模块 | 引擎/导航/TTS |
| `task_engine/` | 任务引擎 | 任务图/状态管理 |
| `src/luna_badge/` | 源代码包 | v1.4场景记忆系统 |
| `hal_embedded/` | 嵌入式硬件抽象 | ESP32等硬件接口 |
| `hal_mac/` | Mac硬件抽象 | Mac平台硬件接口 |
| `assets/` | 资源文件 | 字体/图标/纹理 |
| `logs/` | 日志文件 | 运行时日志 |
| `memory_store/` | 记忆存储 | 本地记忆/上传包 |
| `task_chain/` | 任务链 | 定时器/上传器 |
| `tools/` | 工具脚本 | 审计/测试工具 |
| `test_reports/` | 测试报告 | 测试结果 |
| `tts_cache/` | TTS缓存 | 语音缓存文件 |
| `v1_core/` | v1核心 | 路径结构生成器 |
| `v2_render/` | v2渲染 | 情感地图渲染器 |

---

## 前端JS模块详细列表

### 🆕 新创建的导航系统模块（13个）

这些模块是本次完整导航系统集成的核心组件：

| 文件名 | 大小 | 说明 |
|--------|------|------|
| `task_logger.js` | 1.2KB | 统一任务日志系统，支持前端→后端日志上传 |
| `task_fsm.js` | 1.5KB | 任务状态机，管理任务状态流转（idle/pending/running/waiting/paused/finished/failed） |
| `intent_tracker.js` | 955B | 意图识别器，识别用户语音意图（cancel/resume/insert/replace/continue） |
| `navigation_fsm.js` | 3.8KB | 导航状态机，管理导航状态（IDLE/NAVIGATING/ARRIVED） |
| `navigation_executors.js` | 2.5KB | 导航执行器，将NAV_*任务转换为语音行为 |
| `minimap.js` | 5.4KB | 小地图可视化，显示自己/危险点/节点/导航方向 |
| `node_memory.js` | 1.7KB | 节点记忆系统，按区域存储场景节点的长期记忆 |
| `zone_manager.js` | 690B | 区域管理器，管理A区/B区/医院区/地铁区等 |
| `zone_auto_detector.js` | 2.2KB | 自动区域识别，根据节点特征自动推断当前区域 |
| `scene_nodes.js` | 2.2KB | 场景节点引擎，管理场景节点（挂号窗口/电梯/洗手间等） |
| `scene_node_detector.js` | 978B | 场景节点检测器，将YOLO识别结果转换为场景节点 |
| `node_task_bridge.js` | 717B | 节点任务桥接，将"去某个节点"转换为任务链 |
| `scene_pattern_reasoner.js` | 3.2KB | 场景模式推理器，记录节点序列并推测下一步节点 |

### 🧭 导航相关模块（4个）

| 文件名 | 大小 | 说明 |
|--------|------|------|
| `navigation_accelerator.js` | 9.0KB | 导航加速器，整合节点记忆和重定位 |
| `navigation_logger.js` | 3.0KB | 导航日志记录器 |
| `navigation_task_executors.js` | 4.8KB | 导航任务执行器（旧版，与新版navigation_executors.js功能相似） |
| `waypoint_system.js` | 8.4KB | 航点系统 |

### 🗺️ 地图/空间模块（5个）

| 文件名 | 大小 | 说明 |
|--------|------|------|
| `map_memory.js` | 9.4KB | 地图记忆系统 |
| `map_memory_pro.js` | 9.3KB | 地图记忆系统Pro版 |
| `spatial_engine.js` | 15.2KB | 空间引擎 |
| `spatial_engine_pro.js` | 5.7KB | 空间引擎Pro版 |
| `spatial_semantic.js` | 4.2KB | 空间语义化 |

### 🎯 场景推理模块（5个）

| 文件名 | 大小 | 说明 |
|--------|------|------|
| `scene_reasoner.js` | 15.6KB | 场景推理器 |
| `structure_analyzer.js` | 2.8KB | 结构分析器 |
| `topology_builder.js` | 1.8KB | 拓扑构建器 |
| `bottleneck_detector.js` | 1.6KB | 瓶颈检测器 |
| `path_feasibility.js` | 2.5KB | 路径可行性分析 |

### 🔊 语音/TTS模块（4个）

| 文件名 | 大小 | 说明 |
|--------|------|------|
| `speech_rhythm.js` | 3.4KB | 语音节奏管理 |
| `memory_aware_voice.js` | 2.8KB | 记忆敏感语音引擎 |
| `goal_awareness.js` | 4.3KB | 目标距离×阶段播报引擎 |
| `de_navigation_audio.js` | 13.6KB | 导航音频管线（AudioPipeline/NavigationFSM/DangerEnginePro） |

### 📋 任务链模块（3个）

| 文件名 | 大小 | 说明 |
|--------|------|------|
| `task_chain.js` | 52.5KB | 任务链核心系统（已集成FSM/Logger/Executors） |
| `task_chain_integrator.js` | 7.2KB | 任务链集成器 |
| `task_state_machine.js` | 4.4KB | 任务状态机（旧版，与新版task_fsm.js功能相似） |

### 👁️ 视觉模块（4个）

| 文件名 | 大小 | 说明 |
|--------|------|------|
| `vision_enhancer.js` | 11.5KB | 视觉增强器 |
| `event_flow.js` | 5.7KB | 事件流 |
| `event_flow_pro.js` | 11.0KB | 事件流Pro版 |
| `action_guidance.js` | 5.3KB | 动作级导航引擎 |

### 🧠 节点系统模块（6个）

| 文件名 | 大小 | 说明 |
|--------|------|------|
| `node_engine.js` | 5.2KB | 节点引擎 |
| `node_inference.js` | 7.3KB | 节点推理系统 |
| `node_bridge.js` | 1.6KB | 节点桥接 |
| `node_dynamic_update.js` | 5.8KB | 节点动态更新 |
| `node_relocalization.js` | 5.8KB | 节点重定位 |
| `node_memory_zone.js` | 2.8KB | 节点记忆区域管理 |

### 📝 日志/恢复模块（5个）

| 文件名 | 大小 | 说明 |
|--------|------|------|
| `logger.js` | 2.6KB | 日志系统 |
| `e_logging_memory.js` | 7.7KB | 日志+记忆审计系统 |
| `auto_recovery.js` | 10.3KB | 自动恢复系统 |
| `recovery_mode.js` | 7.6KB | 恢复模式 |
| `safe_mode.js` | 5.3KB | 安全模式 |

### 🎭 其他模块（4个）

| 文件名 | 大小 | 说明 |
|--------|------|------|
| `emotion_hook.js` | 4.8KB | 情绪钩子 |
| `voice_intent_handler.js` | 3.5KB | 语音意图处理器 |
| `unified_events.js` | 8.9KB | 统一事件系统 |
| `intent_tracker_simple.js` | 1.2KB | 意图追踪器简化版（旧版） |

---

## 核心Python模块分类

### 🧭 导航系统（12个模块）

- `core/navigation/navigation_runtime.py` - 导航运行时核心
- `core/navigation/direction_evaluator.py` - 方向评估器
- `core/navigation/environment_scanner.py` - 环境扫描器
- `core/navigation/scene_context.py` - 场景上下文
- `core/navigation/scene_node.py` - 场景节点定义
- `core/navigation/scene_node_layer.py` - 场景节点层
- `core/navigation_manager.py` - 导航管理器
- `core/navigation_optimizer.py` - 导航优化器
- `core/path_planner.py` - 路径规划器
- `core/path_evaluator.py` - 路径评估器
- `core/path_growth.py` - 路径增长管理
- `core/path_resolver.py` - 路径解析器

### 🎯 场景推理（4个模块）

- `core/scene_reasoner_sg.py` - 场景推理器（基于SceneGraph）
- `core/scene_graph.py` - 场景图定义和构建
- `core/structure_map_parser.py` - 结构地图解析器
- `core/scene_memory_system.py` - 场景记忆系统

### 📋 任务系统（7个模块）

- `core/task_dispatcher.py` - 任务分发器
- `core/task_intent.py` - 任务意图解析
- `core/task_center.py` - 任务中心
- `core/task_chain_manager.py` - 任务链管理器
- `core/task_conversation.py` - 任务对话
- `core/task_engine.py` - 任务引擎
- `core/task_graph_templates.py` - 任务图模板

### 👁️ 视觉处理（12个模块）

- `core/vision_ocr_engine.py` - 视觉OCR引擎
- `core/vision_pipeline.py` - 视觉管线
- `core/signboard_detector.py` - 标识牌检测器
- `core/facility_detector.py` - 设施检测器
- `core/hazard_detector.py` - 危险检测器
- `core/step_detector.py` - 台阶检测器
- `core/doorplate_reader.py` - 门牌读取器
- `core/doorplate_inference.py` - 门牌推理
- `core/ocr_scanner.py` - OCR扫描器
- `core/ocr_advanced_reader.py` - OCR高级读取器
- `core/visual_language_fusion.py` - 视觉-语言融合
- `core/visual_localization.py` - 视觉定位

### 🗺️ 地图生成（8个模块）

- `core/local_map_generator.py` - 本地地图生成器
- `core/map_card_generator.py` - 地图卡片生成器
- `core/emotional_map_card_generator_v2.py` - 情感地图卡片生成器v2
- `core/handdrawn_map_generator.py` - 手绘地图生成器
- `core/icon_map_generator.py` - 图标地图生成器
- `core/illustrated_map_generator.py` - 插画地图生成器
- `core/enhanced_map_generator.py` - 增强地图生成器
- `core/luna_map_loader.py` - Luna地图加载器

### 🧠 记忆系统（5个模块）

- `core/memory_store.py` - 记忆存储
- `core/memory_caller.py` - 记忆调用器
- `core/memory_control.py` - 记忆控制
- `core/memory_entry_builder.py` - 记忆条目构建器
- `core/memory_cache_manager.py` - 记忆缓存管理器

### 🔊 语音/TTS（9个模块）

- `core/whisper_recognizer.py` - Whisper语音识别器
- `core/voice_wakeup.py` - 语音唤醒
- `core/voice_wakeup_manager.py` - 语音唤醒管理器
- `core/real_voice_wakeup.py` - 真实语音唤醒
- `core/complete_voice_wakeup.py` - 完整语音唤醒
- `core/voice_clone_tts.py` - 语音克隆TTS
- `core/fast_tts_cache.py` - 快速TTS缓存
- `core/tts_manager.py` - TTS管理器
- `core/speech_style_manager.py` - 语音风格管理器

### ⚙️ 系统管理（8个模块）

- `core/system_orchestrator.py` - 系统编排器
- `core/system_orchestrator_enhanced.py` - 系统编排器增强版
- `core/system_control.py` - 系统控制
- `core/startup_manager.py` - 启动管理器
- `core/first_boot_manager.py` - 首次启动管理器
- `core/module_registry.py` - 模块注册表
- `core/enhanced_module_registry.py` - 增强模块注册表
- `core/mmp.py` - 模块管理平台

### 🔗 其他核心模块（8个）

- `core/log_manager.py` - 日志管理器
- `core/config.py` - 配置管理
- `core/config_validator.py` - 配置验证器
- `core/event_bus.py` - 事件总线
- `core/enhanced_event_bus.py` - 增强事件总线
- `core/unified_config_manager.py` - 统一配置管理器
- `core/unified_data_models.py` - 统一数据模型
- `core/base_module.py` - 基础模块

---

## 配置文件列表

| 文件名 | 大小 | 说明 |
|--------|------|------|
| `ai_models.yaml` | 848B | AI模型配置 |
| `hardware.yaml` | 1.5KB | 硬件配置 |
| `memory_schema.json` | 1.6KB | 记忆模式JSON |
| `memory_schema.yaml` | 69B | 记忆模式YAML |
| `modules_enabled.yaml` | 281B | 模块启用配置 |
| `navigation.yaml` | 975B | 导航配置 |
| `safety_policy.yaml` | 259B | 安全策略配置 |
| `system_config.yaml` | 174B | 系统配置 |
| `tts_config.yaml` | 183B | TTS配置 |
| `user_config.json` | 118B | 用户配置 |

---

## 主要入口文件

| 文件名 | 大小 | 说明 |
|--------|------|------|
| `web_test_server.py` | 678.8KB | Web测试服务器（主入口，包含所有前端模块内联） |
| `main_mac.py` | 9.5KB | Mac平台主程序 |
| `main_embedded.py` | 6.8KB | 嵌入式平台主程序 |
| `main_with_integrated_features.py` | 11.2KB | 集成功能主程序 |
| `startup_demo.py` | 6.8KB | 启动演示程序 |
| `quick_test.py` | 3.6KB | 快速测试脚本 |

---

## 测试文件列表

项目包含42个测试文件，主要测试文件包括：

- `test_all_modules.py` - 所有模块测试
- `test_all_new_modules.py` - 新模块测试
- `test_all_scene_modules.py` - 场景模块测试
- `test_architecture.py` - 架构测试
- `test_backend_integration.py` - 后端集成测试
- `test_complete_integration.py` - 完整集成测试
- `test_complete_integration_v16.py` - v1.6完整集成测试
- `test_complete_map_generation.py` - 完整地图生成测试
- `test_complete_path_planning.py` - 完整路径规划测试
- `test_emotional_map_complete.py` - 情感地图完整测试
- `test_emotional_map_enhanced.py` - 情感地图增强测试
- `test_emotional_map_v2.py` - 情感地图v2测试
- `test_enhanced_map_generation.py` - 增强地图生成测试
- `test_handdrawn_map.py` - 手绘地图测试
- `test_icon_map.py` - 图标地图测试
- `test_integrated_features.py` - 集成功能测试
- `test_offline_navigation.py` - 离线导航测试
- `test_orchestrator_integration.py` - 编排器集成测试
- `test_p1_modules_unit.py` - P1模块单元测试
- `test_p1_real_scenarios_integration.py` - P1真实场景集成测试
- `test_path_planning.py` - 路径规划测试
- `test_performance_optimization.py` - 性能优化测试
- `test_real_scenarios.py` - 真实场景测试
- `test_real_wakeup.py` - 真实唤醒测试
- `test_realtime_system.py` - 实时系统测试
- `test_scene_memory.py` - 场景记忆测试
- `test_startup_flow.py` - 启动流程测试
- `test_structure.py` - 结构测试
- `test_system_orchestrator.py` - 系统编排器测试
- `test_tracker.py` - 追踪器测试
- `test_tts_integration.py` - TTS集成测试
- `test_v12_modules.py` - v1.2模块测试
- `test_v12_modules_345.py` - v1.2模块345测试
- `test_v15_v16_auto.py` - v1.5/v1.6自动测试
- `test_v15_v16_voice_interaction.py` - v1.5/v1.6语音交互测试
- `test_vision_ocr.py` - 视觉OCR测试
- `test_whisper_demo.py` - Whisper演示测试
- `test_whisper_integration.py` - Whisper集成测试
- `test_whisper_live.py` - Whisper实时测试
- `test_whisper_simple.py` - Whisper简单测试
- `test_whisper_tts_integration.py` - Whisper TTS集成测试
- `test_wifi_interactive.py` - WiFi交互测试

---

## 文档文件列表

项目包含113个Markdown文档，关键文档包括：

### 架构和设计文档
- `docs/COMPLETE_PROJECT_SUMMARY.md` - 完整项目总结
- `docs/MODULES_SUMMARY.md` - 模块总结
- `docs/Luna_Badge_Architecture_v1_Summary.md` - 架构v1总结
- `docs/LUNA_ARCHITECTURE.md` - Luna架构
- `docs/ARCHITECTURE_VALIDATION.md` - 架构验证

### 测试文档
- `docs/TEST_REPORT.md` - 测试报告
- `docs/BACKEND_TEST_REPORT.md` - 后端测试报告
- `docs/P1_TESTING_COMPLETE.md` - P1测试完成
- `docs/REALTIME_SYSTEM_TEST_REPORT.md` - 实时系统测试报告

### 功能指南
- `docs/COMPLETE_PATH_PLANNING_GUIDE.md` - 完整路径规划指南
- `docs/LOCAL_MAP_GENERATOR_SUMMARY.md` - 本地地图生成器总结
- `docs/SIGNBOARD_DETECTOR_GUIDE.md` - 标识牌检测器指南
- `docs/PRIVACY_PROTECTION_SUMMARY.md` - 隐私保护总结
- `docs/TTS_INTEGRATION_GUIDE.md` - TTS集成指南
- `docs/WHISPER_INTEGRATION_GUIDE.md` - Whisper集成指南

### 任务引擎文档
- `task_engine/COMPLETE_DELIVERY_REPORT.md` - 完整交付报告
- `task_engine/FINAL_TEST_REPORT.md` - 最终测试报告
- `task_engine/DELIVERY_CHECKLIST.md` - 交付清单

---

## 项目统计

| 类别 | 数量 |
|------|------|
| 前端JS模块 | 53个 |
| 核心Python模块 | 126个 |
| 配置文件 | 10个 |
| 文档文件 | 113个 |
| 测试文件 | 42个 |
| 任务图文件 | 6个 |

---

## 新创建的导航系统模块

本次完整导航系统集成新增了13个核心模块，完整实现了"导航 + 小地图 + 场景节点 + 场景模式 + 任务状态机"的完整功能。

### 模块依赖关系

```
task_logger.js (基础日志)
    ↓
task_fsm.js (任务状态机)
    ↓
intent_tracker.js (意图识别)
    ↓
task_chain.js (任务链核心，已集成上述模块)
    ↓
navigation_fsm.js (导航状态机)
    ↓
navigation_executors.js (导航执行器)
    ↓
minimap.js (小地图，依赖node_memory.js)
    ↓
node_memory.js (节点记忆)
    ↓
zone_manager.js (区域管理)
    ↓
zone_auto_detector.js (自动区域识别)
    ↓
scene_nodes.js (场景节点引擎)
    ↓
scene_node_detector.js (场景节点检测器)
    ↓
node_task_bridge.js (节点任务桥接)
    ↓
scene_pattern_reasoner.js (场景模式推理器)
```

### 集成状态

✅ **所有模块已创建**
✅ **所有模块已在 web_test_server.py 中内联**
✅ **task_chain.js 已集成所有新模块**
✅ **Flask 路由已存在** (`/log_task_event`, `/log_nav_event`)

### 使用示例

```javascript
// 1. 开始导航
window.NavigationFSM.start([
    {type: 'turn', direction: 'left'}, 
    {type: 'straight', distance: 10}
]);

// 2. 视觉更新
window.NavigationFSM.onVisionUpdate({direction: 'left', distance: 5});

// 3. 场景节点检测
window.SceneNodeDetector.updateDetections(yoloResults);

// 4. 用户语音处理
window.onUserSentenceRecognized('我要去医院');

// 5. 场景模式推理
window.ScenePatternReasoner.enterScene('hospital');
window.ScenePatternReasoner.recordNodeArrival('挂号窗口');
const next = window.ScenePatternReasoner.predictNext('挂号窗口');
```

---

## 注意事项

### 相似文件（可能需要清理）

以下文件可能是不同版本，建议确认当前使用的版本：

1. **意图追踪器**
   - `intent_tracker.js` (新版本，955B)
   - `intent_tracker_simple.js` (旧版本，1.2KB)

2. **任务状态机**
   - `task_fsm.js` (新版本，1.5KB)
   - `task_state_machine.js` (旧版本，4.4KB)

3. **导航执行器**
   - `navigation_executors.js` (新版本，2.5KB)
   - `navigation_task_executors.js` (旧版本，4.8KB)

### 下一步集成建议

1. **在YOLO处理函数中添加**：
   ```javascript
   window.SceneNodeDetector.updateDetections(yoloResults);
   ```

2. **在视觉分析函数中添加**：
   ```javascript
   window.NavigationFSM.onVisionUpdate({direction, distance});
   ```

3. **在语音识别回调中添加**：
   ```javascript
   window.onUserSentenceRecognized(userText);
   ```

4. **在节点到达确认时添加**：
   ```javascript
   window.ScenePatternReasoner.recordNodeArrival(nodeName);
   ```

---

## 总结

Luna_Badge 项目结构完整，包含：

- ✅ 53个前端JS模块（包含13个新创建的导航系统模块）
- ✅ 126个核心Python模块
- ✅ 完整的配置和文档系统
- ✅ 42个测试文件
- ✅ 完整的任务引擎系统

所有新创建的导航系统模块已正确集成，项目已就绪，可以开始测试。

---

*文档生成时间: 2025-01-18*




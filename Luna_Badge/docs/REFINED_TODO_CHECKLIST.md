# 📋 Luna Badge 精简TODO清单（嵌入式版本）

**生成时间**: 2025-10-31  
**目标**: Demo收口阶段的真实任务列表  
**平台**: 嵌入式版本（移除Mac平台支持）

---

## ✅ 已完成清理

### 移除内容
- ✅ 删除Mac平台类（4个）和初始化逻辑
- ✅ 统一使用嵌入式平台实现
- ✅ 简化平台分支代码

---

## 🎯 精简后的待办清单

### 📊 优先级分类

| 优先级 | 数量 | 说明 |
|--------|------|------|
| 🔴 高优先级 | 3个 | 核心功能，影响Demo |
| 🟡 中优先级 | 5个 | 体验增强，建议补充 |
| 🟢 低优先级 | 25个 | 辅助功能，可延后 |

---

## 🔴 高优先级 (3个) - 立即补充

### 1. TTS集成完善
- [ ] **luna_usage_guide.py:119** - 接入TTS模块
  - 位置: 使用指南播报
  - 影响: 用户交互体验

### 2. 语音询问逻辑
- [ ] **camera_manager.py:232** - 实现语音询问逻辑
  - 位置: 摄像头关闭前询问
  - 影响: 控制中枢流程

### 3. Whisper bytes识别
- [ ] **system_orchestrator_enhanced.py:118** - 实现bytes识别
  - 位置: 系统控制中枢
  - 影响: 边缘场景支持

---

## 🟡 中优先级 (5个) - Demo后补充

### 1. 语音交互增强 (2个)
- [ ] **voice_wakeup_manager.py:125** - 倒计时逻辑
  - 影响: 待机体验优化

### 2. 嵌入式AI导航 (4个)
- [ ] **ai_navigation.py:501** - 环境检测逻辑
  - 位置: EmbeddedEnvironmentDetector
  - 影响: 场景感知能力

- [ ] **ai_navigation.py:511** - 天气检查逻辑
  - 位置: EmbeddedWeatherFailSafe
  - 影响: 故障保护

- [ ] **ai_navigation.py:519** - 指示牌检测逻辑
  - 位置: EmbeddedSignboardNavigation
  - 影响: 指示牌导航

- [ ] **ai_navigation.py:527** - 语音路径理解逻辑
  - 位置: EmbeddedSpeechRouteUnderstand
  - 影响: 语音导航

---

## 🟢 低优先级 (25个) - 生产阶段

### WiFi/网络配置 (3个)
- [ ] voice_wifi_setup.py:343 - WiFi连接
- [ ] network_connection_strategy.py:132 - Wi-Fi连接逻辑
- [ ] network_connection_strategy.py:167 - 二维码生成

### 硬件上传 (1个)
- [ ] hardware_identity_logger.py:149 - 上传逻辑

### 导航优化 (3个)
- [ ] path_evaluator.py:337 - 视觉检测集成
- [ ] path_evaluator.py:358 - 调头判断
- [ ] path_evaluator.py:439 - 实际数据获取

### 人脸识别 (3个) ⏸️ 三期扩展
- [ ] subject_tracker.py:152 - 人脸识别逻辑
- [ ] subject_tracker.py:232 - 位置计算
- [ ] family_face_registry.py:236 - 特征提取

### 语音相关 (2个)
- [ ] voice_wakeup_manager.py:67 - 真实唤醒词
- [ ] voice_recognition.py:136 - Vosk/PicoVoice集成

### 导航相关 (5个)
- [ ] toilet_navigator.py:156 - 咨询台查询
- [ ] toilet_navigator.py:205 - 路径规划调用
- [ ] facility_locator.py:126 - 地图API调用
- [ ] facility_locator.py:207 - 地图API调用
- [ ] bus_direction_checker.py:92 - 线路号比较

### 视觉相关 (3个)
- [ ] luna_integration.py:158 - 视觉检测逻辑
- [ ] luna_integration.py:173 - 路径分析逻辑
- [ ] traffic_light_detector.py:203 - OCR红绿灯倒计时

### 用户管理 (1个)
- [ ] user_manager.py:195 - 短信服务

---

## 📋 完整清单（按文件分类）

### ai_navigation.py (4个)
```
  [ ] 501: 环境检测逻辑
  [ ] 511: 天气检查逻辑
  [ ] 519: 指示牌检测逻辑
  [ ] 527: 语音路径理解逻辑
```

### path_evaluator.py (3个)
```
  [ ] 337: 视觉检测集成
  [ ] 358: 调头判断增强
  [ ] 439: 实际数据获取
```

### voice_wakeup_manager.py (2个)
```
  [ ] 67: 真实唤醒词检测
  [ ] 125: 倒计时逻辑
```

### facility_locator.py (2个)
```
  [ ] 126: 地图API调用
  [ ] 207: 地图API调用
```

### network_connection_strategy.py (2个)
```
  [ ] 132: Wi-Fi连接逻辑
  [ ] 167: 二维码生成
```

### toilet_navigator.py (2个)
```
  [ ] 156: 咨询台查询
  [ ] 205: 路径规划调用
```

### luna_integration.py (2个)
```
  [ ] 158: 视觉检测逻辑
  [ ] 173: 路径分析逻辑
```

### subject_tracker.py (2个)
```
  [ ] 152: 人脸识别逻辑
  [ ] 232: 位置计算逻辑
```

### 其他文件 (10个)
- system_orchestrator_enhanced.py: 1个 - Whisper bytes
- camera_manager.py: 1个 - 语音询问
- voice_wifi_setup.py: 1个 - WiFi连接
- hardware_identity_logger.py: 1个 - 上传逻辑
- bus_direction_checker.py: 1个 - 线路号比较
- traffic_light_detector.py: 1个 - OCR倒计时
- luna_usage_guide.py: 1个 - TTS接入
- voice_recognition.py: 1个 - Vosk集成
- user_manager.py: 1个 - 短信服务
- family_face_registry.py: 1个 - 特征提取

---

## 🎯 实施建议

### 当前阶段：Demo准备

**建议**: **仅处理高优先级3个TODO**

**工作量**: 1-2天
**影响**: Demo演示更完整

### Demo后阶段

**建议**: 补充中优先级5个TODO
**工作量**: 3-5天
**影响**: 体验显著提升

### 生产阶段

**建议**: 逐步补齐所有低优先级TODO
**工作量**: 持续迭代

---

## ✅ 最终建议

### 立即行动（高优先级）
1. TTS集成 - 1天
2. 语音询问 - 半天
3. Whisper bytes - 半天

**总计**: 2天工作量

### 暂缓行动
- ❌ 所有人脸识别TODO → 三期扩展
- ❌ 公交方向/红绿灯 → 三期扩展
- ⏸️ 其他低优先级 → 生产阶段

---

**文档版本**: v2.0 (精简版)  
**状态**: 📋 可执行  
**建议**: 先处理高优先级3个，直接进入Demo


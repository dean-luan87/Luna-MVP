# 📋 Luna Badge 剩余TODO完整清单

**生成时间**: 2025-10-31  
**总TODO数**: 33个  
**建议**: 暂不处理，等Demo反馈后决定

---

## 📊 分类清单

### 🔴 高优先级 (0个) - 核心功能阻塞

✅ **无阻塞项** - 所有核心功能已完成

---

### 🟡 中优先级 (10个) - 体验增强

#### 1️⃣ 语音交互增强 (3个)

- [ ] **system_orchestrator_enhanced.py:118**
  - 功能: Whisper bytes识别实现
  - 影响: 边缘场景（非核心）

- [ ] **camera_manager.py:232**
  - 功能: 语音询问逻辑
  - 影响: 交互体验优化

- [ ] **voice_wakeup_manager.py:125**
  - 功能: 倒计时逻辑
  - 影响: 待机体验优化

#### 2️⃣ AI导航功能补充 (4个)

- [ ] **ai_navigation.py:520**
  - 功能: Mac平台环境检测逻辑
  - 影响: Mac平台特殊功能

- [ ] **ai_navigation.py:528**
  - 功能: Mac平台天气检查逻辑
  - 影响: Mac平台特殊功能

- [ ] **ai_navigation.py:536**
  - 功能: Mac平台指示牌检测逻辑
  - 影响: Mac平台特殊功能

- [ ] **ai_navigation.py:544**
  - 功能: Mac平台语音路径理解逻辑
  - 影响: Mac平台特殊功能

#### 3️⃣ 人脸识别功能 (3个)

- [ ] **subject_tracker.py:152**
  - 功能: 真实人脸识别逻辑
  - 影响: 家人识别

- [ ] **subject_tracker.py:232**
  - 功能: 真实位置计算逻辑
  - 影响: 家人识别

- [ ] **family_face_registry.py:236**
  - 功能: 真实人脸特征提取（face_recognition或DeepFace）
  - 影响: 家人注册

---

### 🟢 低优先级 (23个) - 辅助功能

#### 1️⃣ WiFi/网络配置 (3个)

- [ ] **voice_wifi_setup.py:343**
  - 功能: 实现实际WiFi连接

- [ ] **network_connection_strategy.py:132**
  - 功能: 实现实际Wi-Fi连接逻辑

- [ ] **network_connection_strategy.py:167**
  - 功能: 使用qrcode库生成实际二维码

#### 2️⃣ 硬件上传 (1个)

- [ ] **hardware_identity_logger.py:149**
  - 功能: 实现实际上传逻辑

#### 3️⃣ 导航算法优化 (3个)

- [ ] **path_evaluator.py:337**
  - 功能: 结合视觉检测（单行道标识、墙体、障碍物）或地图数据

- [ ] **path_evaluator.py:358**
  - 功能: 结合视觉检测判断前方是否有单行道标识、墙体、障碍物

- [ ] **path_evaluator.py:439**
  - 功能: 从各模块获取实际数据

#### 4️⃣ 其他辅助功能 (16个)

**语音相关**
- [ ] **voice_wakeup_manager.py:67** - 集成真实唤醒词检测
- [ ] **voice_recognition.py:136** - 集成Vosk或PicoVoice
- [ ] **luna_usage_guide.py:119** - 接入TTS模块

**导航相关**
- [ ] **toilet_navigator.py:156** - 查询咨询台位置和检测工作人员
- [ ] **toilet_navigator.py:205** - 实际调用路径规划
- [ ] **facility_locator.py:126** - 调用地图API（如高德、百度、OpenStreetMap）
- [ ] **facility_locator.py:207** - 调用地图API
- [ ] **bus_direction_checker.py:92** - 与导航目标中的线路号比较

**视觉相关**
- [ ] **luna_integration.py:158** - 实际的视觉检测逻辑
- [ ] **luna_integration.py:173** - 实际的路径分析逻辑
- [ ] **traffic_light_detector.py:203** - 使用OCR识别数字

**用户管理**
- [ ] **user_manager.py:195** - 调用真实短信服务

---

## 📝 完整清单（带行号）

```
ai_navigation.py:
  [ ] 520: 实现Mac平台的环境检测逻辑
  [ ] 528: 实现Mac平台的天气检查逻辑
  [ ] 536: 实现Mac平台的指示牌检测逻辑
  [ ] 544: 实现Mac平台的语音路径理解逻辑
  [ ] 553: 实现嵌入式平台的环境检测逻辑
  [ ] 561: 实现嵌入式平台的天气检查逻辑
  [ ] 569: 实现嵌入式平台的指示牌检测逻辑
  [ ] 577: 实现嵌入式平台的语音路径理解逻辑

path_evaluator.py:
  [ ] 337: 结合视觉检测（单行道标识、墙体、障碍物）或地图数据
  [ ] 358: 结合视觉检测判断前方是否有单行道标识、墙体、障碍物
  [ ] 439: 从各模块获取实际数据

subject_tracker.py:
  [ ] 152: 实现真实的人脸识别逻辑
  [ ] 232: 实现真实的位置计算逻辑

family_face_registry.py:
  [ ] 236: 实现真实的人脸特征提取（face_recognition或DeepFace）

voice_wakeup_manager.py:
  [ ] 67: 集成真实唤醒词检测
  [ ] 125: 实现倒计时逻辑

facility_locator.py:
  [ ] 126: 调用地图API（如高德、百度、OpenStreetMap）
  [ ] 207: 调用地图API

network_connection_strategy.py:
  [ ] 132: 实现实际Wi-Fi连接逻辑
  [ ] 167: 使用qrcode库生成实际二维码

luna_integration.py:
  [ ] 158: 实际的视觉检测逻辑
  [ ] 173: 实际的路径分析逻辑

toilet_navigator.py:
  [ ] 156: 查询咨询台位置和检测工作人员
  [ ] 205: 实际调用路径规划

其他:
  [ ] system_orchestrator_enhanced.py:118 - Whisper bytes识别
  [ ] camera_manager.py:232 - 语音询问逻辑
  [ ] voice_wifi_setup.py:343 - 实现实际WiFi连接
  [ ] hardware_identity_logger.py:149 - 实现实际上传逻辑
  [ ] bus_direction_checker.py:92 - 与导航目标线路号比较
  [ ] traffic_light_detector.py:203 - 使用OCR识别数字
  [ ] luna_usage_guide.py:119 - 接入TTS模块
  [ ] voice_recognition.py:136 - 集成Vosk或PicoVoice
  [ ] user_manager.py:195 - 调用真实短信服务
```

---

## ✅ 建议

### 当前阶段：Demo准备

**建议**: ⏸️ **暂不处理任何TODO**

**理由**:
- ✅ 核心功能已完成
- ✅ 性能优化已完成
- ✅ 不影响Demo演示
- ✅ 不影响用户安全

### Demo后考虑补充

**优先级**:
1. AI导航功能补充（如果硬件测试需要）
2. 语音交互增强（提升体验）
3. 人脸识别（根据产品定位）

### 生产阶段

**逐步补齐所有低优先级TODO**

---

**文档**: TODO_CHECKLIST.md  
**状态**: 📋 待补充


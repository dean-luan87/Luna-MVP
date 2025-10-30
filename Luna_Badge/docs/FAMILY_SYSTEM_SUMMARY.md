# Luna Badge 家庭组 × 多主体识别系统总结

## 📋 系统概述

实现了家庭组 × 多主体识别系统，用于家人脸部信息注册、关系管理、实时追踪和陌生人检测。

## ✅ 核心模块

### F1: family_face_registry.py
**功能**: 家人脸部信息注册与身份绑定

**核心特性**:
- 用户可通过语音发起注册流程（如"这是我妈"）
- 调用摄像头拍摄目标人脸，保存多张图像
- 提取人脸特征向量（可复用已有人脸检测模块）
- 将特征向量 + 语义标签存入本地数据库

**输出格式**:
```json
{
  "face_id": "face_001",
  "label": "妈妈",
  "relationship": "mother",
  "feature_vector": "...",
  "registered_at": "2025-10-28T10:30:00"
}
```

**存储路径**: `data/family_faces.json`

### F2: relationship_mapper.py
**功能**: 管理人与人之间的语义关系与行为偏好

**核心特性**:
- 建立面向用户的"关系图谱"，支持多个身份标签
- 每个face_id绑定称谓、社交属性、播报偏好
- 提供可调用接口

**数据结构示例**:
```json
{
  "face_001": {
    "relation": "mother",
    "nickname": "小妈",
    "preferred_tone": "gentle",
    "alert_level": "none",
    "emotion_tag": "calm"
  }
}
```

**可调用接口**:
- `get_relation_by_face(face_id)`
- `get_broadcast_preference(face_id)`
- `list_all_known_faces()`

**存储路径**: `data/relationship_map.json`

### F3: subject_tracker.py
**功能**: 实时检测和追踪家庭成员 vs 陌生人状态

**核心特性**:
- 在运行过程中持续识别画面中人脸
- 比对 family_faces.json 中的向量
- 判断家人进入/离开视野事件
- 陌生人持续靠近输出安全提醒

**输出事件格式**:

家人检测:
```json
{
  "event": "face_detected",
  "face_id": "face_001",
  "position": "left-front",
  "type": "known",
  "relation": "哥哥",
  "confidence": 0.92,
  "timestamp": "..."
}
```

陌生人检测:
```json
{
  "event": "face_detected",
  "face_id": "unknown",
  "position": "rear-left",
  "type": "unknown",
  "alert_level": "medium",
  "timestamp": "..."
}
```

**存储路径**: `logs/subject_tracking.json`

## 📦 存储与日志

| 文件 | 用途 |
|------|------|
| `data/family_faces.json` | 家人识别数据库 |
| `data/relationship_map.json` | 角色与偏好设定 |
| `logs/subject_tracking.json` | 日常出现/消失记录，统计热度、位置、时间 |

## 🔗 模块联动

| 联动模块 | 联动方式 |
|---------|---------|
| memory_store.py | 支持对某个face_id附加记忆："妈妈喜欢…" |
| speech_style_manager.py | 不同家庭成员 → 播报语气切换 |
| tts_manager.py | 支持nickname个性播报（如"小妈在您前方"） |
| path_evaluator.py | 家人跟随时可提升安全等级或降低播报频率 |
| user_feedback_handler.py | 用户纠错："这是我弟弟" → 更新身份标签 |

## ✅ 测试结果

### 集成测试
- ✅ 成功注册妈妈（face_id: face_20251028_002）
- ✅ 成功创建关系配置（昵称：小妈）
- ✅ 成功检测家人和陌生人
- ✅ 成功获取播报偏好（gentle tone）

### 功能验证
- ✅ 语音注册流程正常
- ✅ 关系图谱映射正常
- ✅ 多主体追踪正常
- ✅ 事件日志记录正常

## 🎯 技术特点

1. **语音驱动注册**: 通过自然语言命令注册家人
2. **关系图谱**: 建立完整的家庭关系网络
3. **实时追踪**: 持续监控家人和陌生人状态
4. **个性化播报**: 根据关系调整播报语气和内容
5. **安全预警**: 陌生人接近时提供安全提醒

## 📈 未来扩展

- 集成真实人脸识别引擎（face_recognition/DeepFace）
- 添加更多关系类型和社交属性
- 实现人脸质量评估和特征优化
- 支持多人同时注册和识别
- 添加隐私保护机制

---

**实现日期**: 2025年10月27日  
**版本**: v1.2+  
**状态**: ✅ 核心功能测试通过

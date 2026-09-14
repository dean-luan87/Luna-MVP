# v1.8.3 代码结构分析报告

## Prompt 1 结果：代码结构扫描

### 1. 决策流程（decision / controller）的主入口

**文件路径**: `main.py`
- **函数名**: `_handle_speech_decision()` (第457行)
- **调用关系**: 
  - `process_frame()` → `_handle_speech_decision()` → `decide()` (来自 `core/decision_controller.py`)

**文件路径**: `core/decision_controller.py`
- **函数名**: `decide()` (第32行)
- **调用关系**: 
  - 被 `main.py` 的 `_handle_speech_decision()` 调用
  - 返回决策结果：`{"action": "SPEAK" | "WAIT" | "YIELD" | "RISK_LV1", "reason": str}`

---

### 2. 场景描述（scene description）生成位置

**文件路径**: `main.py`
- **函数名**: `process_frame()` (第382行)
- **关键代码片段**:
  ```python
  # 第415行：生成场景描述
  description = self.qwen_processor.generate_description(frame, objects, texts)
  ```

**文件路径**: `utils/model_interfaces.py`
- **函数名**: `QwenVLProcessor.generate_description()` (第161行)
- **调用关系**: 
  - `main.py` 的 `process_frame()` → `qwen_processor.generate_description()`
  - 输入：图像、物体列表、文字列表
  - 输出：场景描述文本

**文件路径**: `main.py`
- **函数名**: `_build_voice_text()` (第262行)
- **调用关系**: 
  - `_handle_speech_decision()` → `_build_voice_text()`
  - 将场景描述、物体、文字组合成语音播报文本

---

### 3. TTS 的统一调用入口

**文件路径**: `main.py`
- **函数名**: `_speak_safely()` (第157行)
- **调用关系**: 
  - `_execute_speech_decision()` → `_speak_safely()`
  - `_handle_immediate_risk()` → 直接调用 `submit_tts()` (LV1 风险)
- **关键特性**:
  - ✅ 所有正常 TTS 调用都通过 `speech_gate.can_speak()` 检查
  - ✅ 通过 `core/audio_worker.py` 的 `submit_tts()` 投递到音频工作线程
  - ✅ LV1 风险警报使用 `speech_gate.force_acquire()` 强制获取

**文件路径**: `core/audio_worker.py`
- **函数名**: `submit_tts()` (全局函数)
- **调用关系**: 
  - `_speak_safely()` → `submit_tts()`
  - 投递到音频工作线程队列，非阻塞

**统计结果**:
- `main.py` 中 `_speak_safely` 出现 28 次（全部通过 speech_gate）
- ✅ **确认：所有 TTS 调用都通过 speech_gate**

---

### 4. motion_state（用户移动、方向、速度）相关逻辑

**当前状态**: ⚠️ **未找到专门的 motion_state 模块**

**文件路径**: `core/risk_assessor.py`
- **类名**: `MotionState` (第24行)
- **当前状态**: 仅定义，未实现实际计算逻辑
- **属性**:
  - `is_moving_towards_edge: bool`
  - `estimated_ttc: Optional[float]`
  - `estimated_distance: Optional[float]`

**其他相关模块**（不在当前主流程中）:
- `Luna_Badge/core/direction_estimator.py` - 方向估算器（未接入）
- `Luna_Badge/core/navigation_manager.py` - 导航管理器（未接入）
- `Luna_Badge/core/doorplate_inference.py` - 门牌推理（包含运动分析，未接入）

**结论**: 
- motion_state 目前是占位实现
- 需要从视觉数据（YOLO/OCR）中提取运动信息
- 或从连续帧变化中估算速度和方向

---

## 调用关系图（简化）

```
main.py::process_frame()
    ├─> YOLO 检测 (objects)
    ├─> OCR 识别 (texts)
    ├─> QwenVL 生成描述 (description)
    └─> _handle_speech_decision()
            ├─> scene_state_builder.build_state()  # 构建场景状态
            ├─> _build_voice_text()  # 构建语音文本
            └─> decide()  # 决策控制器
                    ├─> assess_risk()  # 风险评估（v1.8.3 新增）
                    └─> speech_gate.can_speak()  # 语音总闸检查
                        └─> _execute_speech_decision()
                            ├─> _speak_safely()  # 正常播报
                            │       └─> submit_tts()  # 投递到音频线程
                            └─> _handle_immediate_risk()  # LV1 风险警报
                                    └─> submit_tts()  # 直接投递（强制）
```

---

## 关键发现

1. ✅ **决策流程已统一**: 所有语音决策都通过 `decide()` 函数
2. ✅ **TTS 调用已统一**: 所有 TTS 都通过 `speech_gate` 检查
3. ⚠️ **motion_state 缺失**: 需要实现从视觉数据提取运动信息
4. ✅ **场景描述生成独立**: 在 `process_frame()` 中生成，不影响决策流程

---

## 下一步建议

根据 Prompt 2，需要确定：
- `assess_risk()` 的最佳调用位置（已在 `decide()` 中）
- `motion_state` 的提取位置（需要在 `process_frame()` 中计算）



# 实时检测优化方案

## 📊 当前实现分析

### 1. 视觉检测（当前）
- **方式**：每2秒用`setInterval`分析一次画面
- **流程**：
  1. 从video获取帧 → Canvas
  2. Canvas转Blob（图像压缩）
  3. 发送到服务器（网络传输）
  4. 服务器处理（YOLO + OCR + 其他检测）
  5. 返回结果
- **内存占用**：
  - Canvas缓冲区：~5-10MB（1280x720）
  - Blob对象：~200-500KB（压缩后）
  - 服务器端：每次处理需要加载图像到内存
- **CPU占用**：中等（每2秒一次处理）

### 2. 语音检测（当前）
- **方式**：实时VAD检测（每100ms检测一次）
- **流程**：
  1. AudioContext持续运行
  2. AnalyserNode分析频率数据（256点FFT）
  3. 检测到语音 → 启动MediaRecorder
  4. 录音完成 → 发送到服务器识别
- **内存占用**：
  - AudioContext：~1-2MB（持续）
  - AnalyserNode缓冲区：~512字节（很小）
  - MediaRecorder：只在录音时占用（~100-200KB）
- **CPU占用**：低（FFT计算很轻量）

## ⚠️ 内存占用评估

### 视觉检测
- **客户端**：每次处理 ~5-10MB（Canvas + Blob）
- **服务器端**：每次处理 ~10-20MB（图像加载 + 模型推理）
- **总计**：~15-30MB/次，每2秒一次

### 语音检测
- **客户端**：~1-2MB（AudioContext持续）
- **服务器端**：每次识别 ~5-10MB（音频加载 + Whisper模型）
- **总计**：持续占用 ~1-2MB，识别时额外 ~5-10MB

## ✅ 优化方案

### 方案1：智能检测（推荐）

#### 视觉检测优化
```javascript
// 1. 使用requestAnimationFrame替代setInterval（更高效）
// 2. 降低检测频率（3-5秒）
// 3. 图像压缩和降采样
// 4. 帧差检测（只在画面变化时检测）

let lastFrameHash = null;
let frameSkipCount = 0;
const FRAME_SKIP = 5; // 每5帧检测一次（约1秒）

function analyzeVisualGuidanceOptimized() {
    if (frameSkipCount++ < FRAME_SKIP) {
        requestAnimationFrame(analyzeVisualGuidanceOptimized);
        return;
    }
    frameSkipCount = 0;
    
    // 计算帧差（简单哈希）
    const currentHash = calculateFrameHash();
    if (currentHash === lastFrameHash) {
        // 画面未变化，跳过检测
        requestAnimationFrame(analyzeVisualGuidanceOptimized);
        return;
    }
    lastFrameHash = currentHash;
    
    // 降采样（降低分辨率）
    canvas.width = video.videoWidth / 2;
    canvas.height = video.videoHeight / 2;
    
    // 压缩质量降低
    canvas.toBlob(async (blob) => {
        // 发送检测...
    }, 'image/jpeg', 0.6); // 降低质量到60%
}
```

#### 语音检测优化
```javascript
// 1. 降低VAD检测频率（200ms而不是100ms）
// 2. 降低采样率（如果可能）
// 3. 使用更轻量的VAD算法

analyser.fftSize = 128; // 降低FFT大小（256 → 128）
const DETECTION_INTERVAL = 200; // 200ms检测一次

function detectVoiceActivityOptimized() {
    // 每200ms检测一次
    setTimeout(() => {
        if (!productModeActive) return;
        // VAD检测逻辑...
        detectVoiceActivityOptimized();
    }, DETECTION_INTERVAL);
}
```

### 方案2：按需检测（最省资源）

#### 视觉检测
- **触发条件**：
  - 用户移动手机（陀螺仪/加速度计）
  - 画面变化超过阈值
  - 用户主动触发
- **优点**：大幅降低资源占用
- **缺点**：可能错过某些场景

#### 语音检测
- **触发条件**：
  - 用户按下按钮
  - 检测到唤醒词
- **优点**：零资源占用（不检测时）
- **缺点**：需要用户主动触发

### 方案3：混合模式（平衡）

#### 视觉检测
- **低频率检测**：每5秒检测一次（基础检测）
- **高频率检测**：检测到变化时临时提升到1秒/次
- **智能降级**：如果连续多次无变化，降低到10秒/次

#### 语音检测
- **轻量VAD**：持续运行（低资源）
- **智能录音**：只在检测到语音时录音
- **超时保护**：如果长时间无语音，暂停VAD

## 🎯 推荐方案

### 短期优化（立即实施）
1. **视觉检测**：
   - 降低检测频率：2秒 → 3-5秒
   - 图像压缩：质量60-70%
   - 降采样：分辨率减半
   - 使用requestAnimationFrame

2. **语音检测**：
   - 降低VAD频率：100ms → 200ms
   - 降低FFT大小：256 → 128
   - 优化录音时长：0.5-2秒

### 中期优化（性能优化）
1. **视觉检测**：
   - 实现帧差检测
   - 使用Web Workers处理图像
   - 添加检测结果缓存

2. **语音检测**：
   - 使用更轻量的VAD算法
   - 本地预处理音频
   - 批量发送识别请求

### 长期优化（架构优化）
1. **边缘计算**：
   - 客户端预处理（降采样、压缩）
   - 服务器端只做关键检测
   - 使用WebAssembly加速

2. **智能调度**：
   - 根据场景动态调整检测频率
   - 优先级队列（重要检测优先）
   - 资源池管理

## 📈 预期效果

### 内存占用
- **当前**：~20-35MB（视觉+语音）
- **优化后**：~5-10MB（降低70%）

### CPU占用
- **当前**：中等（持续处理）
- **优化后**：低（按需处理）

### 响应速度
- **当前**：视觉2秒，语音1-2秒
- **优化后**：视觉3-5秒（可接受），语音1-2秒（保持）

## 🔧 实施建议

1. **先实施短期优化**（风险低，效果明显）
2. **监控资源使用**（添加性能监控）
3. **根据实际效果调整**（动态优化）
4. **用户反馈**（平衡性能和体验）







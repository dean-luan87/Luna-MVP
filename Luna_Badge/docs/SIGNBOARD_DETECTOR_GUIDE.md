# 标识牌识别模块使用指南

## 📋 模块概述

标识牌识别模块 (`core/signboard_detector.py`) 用于检测和识别图像中的功能性标识牌，支持多种类型的标识识别。

## ✅ 支持的类型

1. **洗手间** (TOILET)
   - 关键词: 洗手间, 卫生间, 厕所, 男厕, 女厕
   - 颜色特征: 蓝色/白色背景

2. **电梯** (ELEVATOR)
   - 关键词: 电梯, 升降梯, 升降机
   - 支持中英文

3. **出口** (EXIT)
   - 关键词: 出口, 安全出口, 疏散口

4. **导览图** (MAP)
   - 关键词: 导览图, 平面图, 地图, 示意图

5. **安全出口** (SAFETY_EXIT)
   - 关键词: 安全出口, 紧急出口, 疏散通道
   - 颜色特征: 绿色背景

6. **禁烟标识** (NO_SMOKING)
   - 关键词: 禁止吸烟, 禁烟, 请勿吸烟
   - 颜色特征: 红色圆形

## 🚀 快速开始

### 基本使用

```python
import cv2
import numpy as np
from core.signboard_detector import SignboardDetector

# 创建检测器
detector = SignboardDetector()

# 读取图像
image = cv2.imread('path/to/image.jpg')

# 检测标识牌
results = detector.detect_signboard(image)

# 处理结果
for result in results:
    print(f"类型: {result.type.value}")
    print(f"文字: {result.text}")
    print(f"置信度: {result.confidence:.2f}")
    print(f"位置: {result.bbox}")
```

### 结构化数据输出

每个检测结果包含以下字段：

```python
@dataclass
class SignboardResult:
    type: SignboardType          # 标识牌类型
    text: str                    # 识别的文字
    confidence: float            # 置信度 (0-1)
    bbox: Tuple[int, int, int, int]  # 边界框 (x, y, w, h)
    center: Tuple[int, int]      # 中心点坐标
    
    def to_dict(self) -> Dict[str, Any]:  # 转换为字典
```

## 💡 使用示例

### 示例1: 实时摄像头检测

```python
import cv2
from core.signboard_detector import SignboardDetector

detector = SignboardDetector()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # 检测标识牌
    results = detector.detect_signboard(frame)
    
    # 绘制结果
    for result in results:
        x, y, w, h = result.bbox
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, result.type.value, (x, y-10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.imshow('Signboard Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### 示例2: 批量图像处理

```python
import cv2
from pathlib import Path
from core.signboard_detector import SignboardDetector

detector = SignboardDetector()
image_dir = Path('images')

for image_path in image_dir.glob('*.jpg'):
    image = cv2.imread(str(image_path))
    results = detector.detect_signboard(image)
    
    print(f"\n{image_path.name}:")
    for result in results:
        print(f"  - {result.type.value} ({result.confidence:.2f})")
```

### 示例3: 语音播报集成

```python
import cv2
from core.signboard_detector import SignboardDetector
import edge_tts
import asyncio

async def detect_and_announce(image):
    detector = SignboardDetector()
    results = detector.detect_signboard(image)
    
    for result in results:
        if result.confidence > 0.7:  # 置信度阈值
            announcement = f"检测到{result.type.value}"
            
            # 生成语音
            communicate = edge_tts.Communicate(announcement, 'zh-CN-XiaoxiaoNeural')
            await communicate.save('announcement.mp3')
            
            # 播放语音
            # os.system('afplay announcement.mp3')  # macOS
            print(f"播报: {announcement}")

# 使用示例
image = cv2.imread('signboard.jpg')
asyncio.run(detect_and_announce(image))
```

## 📊 检测方法

模块使用两种方法进行检测：

### 1. OCR文字识别
- 使用图像处理和文字识别
- 匹配关键词确定类型
- 支持中英文识别

### 2. 颜色特征识别
- 基于HSV颜色空间
- 识别特定颜色的标识牌
- 结合形状特征提高准确率

## 🎯 检测流程

1. **图像预处理**
   - 转换为HSV颜色空间
   - 灰度化处理
   - 形态学操作

2. **双重检测**
   - OCR文字识别
   - 颜色特征识别

3. **结果处理**
   - 去重合并
   - 按置信度排序
   - 生成结构化数据

## 📝 API参考

### `SignboardDetector`

主要检测器类

#### 方法

- `detect_signboard(image) -> List[SignboardResult]`
  - 检测图像中的标识牌
  - 参数: 输入图像 (BGR格式)
  - 返回: 检测结果列表

- `get_detection_summary(results) -> Dict[str, Any]`
  - 获取检测结果摘要
  - 参数: 检测结果列表
  - 返回: 摘要字典

### `SignboardResult`

检测结果数据类

#### 字段

- `type: SignboardType` - 标识牌类型
- `text: str` - 识别的文字
- `confidence: float` - 置信度
- `bbox: Tuple[int, int, int, int]` - 边界框
- `center: Tuple[int, int]` - 中心点

#### 方法

- `to_dict() -> Dict[str, Any]` - 转换为字典

## 🔧 高级配置

### 自定义关键词

```python
detector = SignboardDetector()

# 添加自定义关键词
detector.keywords[SignboardType.TOILET].append("WC")
detector.keywords[SignboardType.EXIT].append("Way Out")
```

### 调整置信度阈值

```python
# 过滤低置信度结果
high_confidence_results = [r for r in results if r.confidence > 0.8]
```

### 自定义颜色范围

```python
# 调整HSV颜色范围
detector.color_features[SignboardType.SAFETY_EXIT] = [
    (10, 20, 200, 50, 100, 255),  # 绿色背景
]
```

## ⚠️ 注意事项

1. **OCR依赖**: 完整功能需要安装OCR库
   - Tesseract: `pip install pytesseract`
   - EasyOCR: `pip install easyocr`

2. **性能优化**: 对于实时应用，建议：
   - 降低图像分辨率
   - 使用ROI检测
   - 缓存检测结果

3. **误检处理**: 
   - 设置合适的置信度阈值
   - 结合上下文信息
   - 多帧融合结果

## 📈 未来改进

- [ ] 集成深度学习模型
- [ ] 支持更多标识类型
- [ ] 提高OCR准确率
- [ ] 支持实时跟踪
- [ ] 添加距离估算

## 📚 相关文档

- [模块代码](../core/signboard_detector.py)
- [测试用例](../tests/test_signboard_detector.py)
- [使用示例](../examples/signboard_demo.py)

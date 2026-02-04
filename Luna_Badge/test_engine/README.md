# Luna TestEngine v1.0

## 简介

Luna TestEngine 是一个完整的自动化场景测试系统，可以：
- ✅ 自动搜图（百度图片，无需 API）
- ✅ 自动检测（YOLO + OCR）
- ✅ 自动分类匹配 vs 不匹配
- ✅ 自动聚类错判
- ✅ 自动生成训练数据（JSON / CSV）
- ✅ 自动生成测试报告

## 快速开始

### 1. 安装依赖（可选）

```bash
# 自动搜图功能
pip install beautifulsoup4

# OCR 功能（可选）
pip install paddleocr

# 高级错误聚类（可选）
pip install scikit-learn numpy
```

### 2. 使用示例

```python
from test_engine import ScenarioRunner

# 创建运行器
runner = ScenarioRunner()

# 运行场景测试
result = runner.run("test_engine/scenarios/stairs.json")

# 查看结果
print(result["report"])
print(f"平均准确率: {result['summary']['avg_accuracy']:.2%}")
```

### 3. 命令行使用

```bash
cd Luna_Badge
python3 -c "from test_engine import ScenarioRunner; runner = ScenarioRunner(); runner.run('test_engine/scenarios/stairs.json')"
```

## 场景配置

场景配置文件位于 `test_engine/scenarios/` 目录，格式如下：

```json
{
  "name": "stairs",
  "keyword": "上下楼梯 场景",
  "expected_labels": ["person", "stairs"]
}
```

### 已包含的场景

- `stairs.json` - 楼梯场景
- `crosswalk.json` - 斑马线场景
- `bus_enter.json` - 公交站场景
- `mall_navigation.json` - 商场导航场景
- `residential_path.json` - 住宅区道路场景

## 输出文件

运行测试后，会在以下目录生成文件：

- `test_engine/data/fetched/` - 下载的图片
- `test_engine/dataset/` - 训练数据（JSON + CSV）
- `test_engine/reports/` - 测试报告（TXT）

## 模块说明

- `scenario_runner.py` - 核心执行器
- `image_fetcher.py` - 自动搜图模块
- `detector.py` - YOLO 视觉检测模块
- `ocr_reader.py` - OCR 识别模块
- `evaluator.py` - 规则判断与标签匹配
- `cluster_engine.py` - 错判自动聚类
- `dataset_manager.py` - 训练数据生成
- `reporter.py` - 测试报告生成

## 集成到现有系统

TestEngine 完全独立，不会影响现有的 Luna Badge 功能。它会：
- 自动使用现有的 `vision_engine`（如果可用）
- 自动降级到简化版本（如果依赖不可用）
- 所有文件保存在 `test_engine/` 目录下

## 下一步

- v1.1: 浏览器 UI 面板版本
- v1.2: 支持视频自动检测
- v1.3: 支持多场景 Playlist
- v2.0: 自动从运行设备收集数据 → 指标分析 → 反馈优化



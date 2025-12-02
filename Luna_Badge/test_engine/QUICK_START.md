# TestEngine v1.0 快速开始

## 最简单的使用方式

```python
from test_engine import ScenarioRunner

runner = ScenarioRunner()
result = runner.run("test_engine/scenarios/stairs.json", limit=10)
print(result["report"])
```

## 文件结构

```
test_engine/
├── __init__.py              # 模块入口
├── scenario_runner.py       # 核心执行器 ⭐
├── image_fetcher.py        # 自动搜图
├── detector.py             # YOLO 检测
├── ocr_reader.py           # OCR 识别
├── evaluator.py            # 规则判断
├── cluster_engine.py        # 错误聚类
├── reporter.py             # 测试报告
├── dataset_manager.py      # 训练数据生成
├── scenarios/              # 场景配置
│   ├── stairs.json
│   ├── crosswalk.json
│   ├── bus_enter.json
│   ├── mall_navigation.json
│   └── residential_path.json
├── data/                   # 运行时数据
│   └── fetched/           # 下载的图片
├── dataset/                # 训练数据输出
└── reports/                # 测试报告输出
```

## 核心功能

1. **自动搜图** - 从百度图片搜索并下载
2. **自动检测** - YOLO + OCR 识别
3. **自动评估** - 判断正确/错误/漏检/错检
4. **自动聚类** - 错误样本聚类分析
5. **自动生成** - JSON/CSV 训练数据 + 测试报告

## 依赖（全部可选）

- `beautifulsoup4` - 自动搜图
- `paddleocr` - OCR 功能
- `scikit-learn` - 高级聚类

**注意**: 所有依赖都有降级方案，不安装也能运行（功能受限）

## 下一步

查看 `README.md` 和 `USAGE.md` 获取详细文档。

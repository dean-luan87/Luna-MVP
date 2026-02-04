# TestEngine v1.0 使用指南

## 快速开始

### 1. 基本使用

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

### 2. 命令行使用

```bash
cd Luna_Badge
python3 -c "
from test_engine import ScenarioRunner
runner = ScenarioRunner()
result = runner.run('test_engine/scenarios/stairs.json', limit=10)
print(result['report'])
"
```

### 3. 运行多个场景

```python
from test_engine import ScenarioRunner
import os

runner = ScenarioRunner()
scenarios_dir = "test_engine/scenarios"

for filename in os.listdir(scenarios_dir):
    if filename.endswith(".json"):
        scene_file = os.path.join(scenarios_dir, filename)
        print(f"\n运行场景: {filename}")
        result = runner.run(scene_file, limit=10)
        print(f"平均准确率: {result['summary']['avg_accuracy']:.2%}")
```

## 场景配置

### 创建新场景

在 `test_engine/scenarios/` 目录下创建 JSON 文件：

```json
{
  "name": "my_scene",
  "keyword": "搜索关键词",
  "expected_labels": ["label1", "label2", "label3"]
}
```

### 场景字段说明

- `name`: 场景名称（用于生成报告和数据集文件名）
- `keyword`: 搜索关键词（用于自动搜图）
- `expected_labels`: 期望检测到的标签列表（YOLO 类别名称）

## 输出文件

运行测试后，会在以下目录生成文件：

### 1. 下载的图片
- `test_engine/data/fetched/` - 自动下载的图片

### 2. 训练数据
- `test_engine/dataset/<scene_name>.json` - JSON 格式训练数据
- `test_engine/dataset/<scene_name>.csv` - CSV 格式训练数据

### 3. 测试报告
- `test_engine/reports/<scene_name>_report.txt` - 文本格式测试报告

## 高级用法

### 1. 不使用自动搜图（使用已有图片）

```python
result = runner.run(
    "test_engine/scenarios/stairs.json",
    fetch_images=False,  # 不自动搜图
    limit=20
)
```

### 2. 禁用错误聚类

```python
result = runner.run(
    "test_engine/scenarios/stairs.json",
    run_clustering=False  # 不运行错误聚类
)
```

### 3. 自定义 vision_engine

```python
from web_test_server import vision_engine
from test_engine import ScenarioRunner

runner = ScenarioRunner(vision_engine=vision_engine)
result = runner.run("test_engine/scenarios/stairs.json")
```

## 依赖说明

### 必需依赖
- 无（所有模块都有降级方案）

### 可选依赖（推荐）

```bash
# 自动搜图功能
pip install beautifulsoup4

# OCR 功能（可选）
pip install paddleocr

# 高级错误聚类（可选）
pip install scikit-learn numpy
```

### 降级行为

- **没有 beautifulsoup4**: 自动搜图功能不可用
- **没有 paddleocr**: OCR 功能使用现有的 vision_engine（如果可用）
- **没有 scikit-learn**: 错误聚类使用简化版本（按错误类型分组）

## 集成到现有系统

TestEngine 完全独立，不会影响现有的 Luna Badge 功能：

1. **自动使用现有模块**: 如果 `vision_engine` 可用，会自动使用
2. **独立目录**: 所有文件保存在 `test_engine/` 目录下
3. **优雅降级**: 缺少依赖时自动使用简化版本

## 故障排除

### 问题1: 导入失败

**原因**: PaddleOCR 依赖问题

**解决**: TestEngine 会自动降级，不影响其他功能

### 问题2: 搜图失败

**原因**: BeautifulSoup 未安装或网络问题

**解决**: 
- 安装 `beautifulsoup4`
- 或使用 `fetch_images=False` 使用已有图片

### 问题3: 检测结果为空

**原因**: vision_engine 未初始化

**解决**: 
- 确保 `web_test_server.py` 已启动
- 或手动传入 `vision_engine` 实例

## 下一步

- v1.1: 浏览器 UI 面板版本
- v1.2: 支持视频自动检测
- v1.3: 支持多场景 Playlist
- v2.0: 自动从运行设备收集数据 → 指标分析 → 反馈优化



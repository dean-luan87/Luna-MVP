# 自动化测试系统 V6.1

## 功能说明

V6.1 包含以下功能：
- ✅ V2: 单张自动测试 + 人工校对 + CSV 导出
- ✅ V3: 批量自动测试
- ✅ V4: 评分系统（准确率、Precision、Recall、F1）
- ✅ V5: 错误聚类分析
- ✅ V6: 训练数据收集和导出
- ✅ V6.1: 自动搜图 + 错误聚类 + 训练数据生成

## 可选依赖安装

### 自动搜图功能（DuckDuckGo）

```bash
pip install duckduckgo-search
```

### 错误聚类功能（KMeans）

```bash
pip install scikit-learn numpy
```

**注意**：如果没有安装这些依赖，系统会自动降级到简化版本：
- 没有 `duckduckgo-search`：自动搜图功能不可用，但可以使用本地图库
- 没有 `scikit-learn`：错误聚类使用简化版本（按关键词分组）

## 使用说明

### 1. 准备测试图片

#### 方式一：本地图库
```bash
mkdir -p test_images/医院挂号大厅
# 将图片放入对应目录
```

#### 方式二：自动搜图（需要安装 duckduckgo-search）
在测试页面输入关键词列表，点击"自动搜索并下载图片"

### 2. 运行测试

1. 打开 `http://localhost:9001`
2. 切换到"综合检测"标签页
3. 选择测试方式：
   - **单张测试**：选择关键词 → 自动测试 → 查看结果
   - **批量测试**：选择多个关键词 → 批量测试 → 查看统计
   - **自动搜图测试**：输入关键词列表 → 自动搜图 → 批量测试 + 错误聚类

### 3. 人工校对

- 点击测试结果项 → 打开人工校对界面
- 填写错误类型/场景标签（可选）
- 点击"AI判断正确"或"AI判断错误（加入训练集）"

### 4. 导出训练数据

- 点击"导出 CSV"按钮
- 下载 `luna_training_samples.csv`
- 可用于 fine-tuning、规则优化、prompt 训练

## 文件结构

```
Luna_Badge/
├── auto_test/
│   └── training_samples.jsonl  # 训练样本存储
├── downloads/                   # 自动下载的图片
│   ├── 电梯/
│   ├── 斑马线/
│   └── ...
└── test_images/                 # 本地测试图片库
    ├── 医院挂号大厅/
    ├── 地铁入口/
    └── ...
```

## API 接口

- `GET /api/auto/keywords` - 获取支持的关键词列表
- `GET /api/auto/run_full_test/<kw>` - 单张测试
- `POST /api/auto/run_batch_test` - 批量测试
- `POST /api/auto/auto_search_images` - 自动搜图
- `POST /api/auto/run_batch_with_clustering` - 批量测试 + 错误聚类
- `POST /api/auto/training_samples/add` - 添加训练样本
- `GET /api/auto/training_samples/export` - 导出训练样本



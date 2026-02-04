# Luna Badge v1.2.0 版本文档

## 📋 版本信息

- **版本号**: 1.2.0
- **发布日期**: 2024-11-20
- **状态**: 稳定版（Stable）
- **构建日期**: 2024-11-20

## 🎯 版本目标

v1.2.0 的主要目标是实现完整的自动化测试系统，包括：
1. 浏览器 UI 面板版自动测试（v1.1）
2. 视频自动检测（v1.2）
3. 多场景 Playlist 自动测试（v1.3）
4. 真实设备数据上报骨架（v2.0）
5. TestEngine v1.0 完整框架

## ✨ 主要功能

### 1. 自动化测试系统

#### v1.1: 浏览器 UI 面板版自动测试
- 单张图片上传 + 关键词测试
- 自动场景描述 + 匹配判断
- 人工校对界面
- CSV 导出功能

#### v1.2: 视频自动检测
- 视频上传 + 自动抽帧
- 批量场景描述 + 匹配统计
- 整体准确率计算

#### v1.3: 多场景 Playlist 自动测试
- 一次性测试多个场景关键词
- 基于单张图片循环测试
- 汇总表格展示

### 2. 设备数据上报系统（v2.0）

- 设备事件上报接口
- 简单指标统计
- 日志存储（JSONL 格式）

### 3. TestEngine v1.0

- 完整的自动化测试框架
- 支持场景配置化测试
- 自动搜图、检测、评估、聚类、报告生成

### 4. V6.1 增强功能

- 自动搜图（DuckDuckGo）
- 错误聚类分析
- 训练数据自动生成

## 📁 文件结构

### 新增目录

```
Luna_Badge/
├── backend/auto_test/          # v1.1 + v1.2 后端模块
├── test_engine/                # TestEngine v1.0 完整系统
├── device_logs/                # v2.0 设备日志存储
├── downloads/                  # V6.1 自动下载的图片
└── auto_test/                  # 文档和总结
```

### 新增文件清单

**后端模块（4个）**：
- `backend/auto_test/auto_test_judger.py`
- `backend/auto_test/video_frame_extractor.py`
- `backend/auto_image_search.py`
- `backend/auto_test_clustering.py`

**路由模块（1个）**：
- `routes/telemetry_routes.py`

**TestEngine 系统（14个）**：
- 9 个 Python 模块
- 5 个场景配置文件
- 3 个文档文件

**文档（7个）**：
- `CHANGELOG.md`
- `RELEASE_NOTES_v1.2.0.md`
- `VERSION`
- `version_info.json`
- `auto_test/V1_COMPLETE_SUMMARY.md`
- `auto_test/V6.1_SUMMARY.md`
- `test_engine/README.md` 等

## 🔌 API 接口

### 新增 API

**自动测试 API**：
- `POST /api/auto/run_full_test` - v1.1: 单张图片自动测试
- `POST /api/auto/run_video_test` - v1.2: 视频自动测试
- `POST /api/auto/auto_search_images` - V6.1: 自动搜索并下载图片
- `POST /api/auto/run_batch_with_clustering` - V6.1: 批量测试 + 错误聚类

**Telemetry API**：
- `POST /api/telemetry/event` - v2.0: 设备上报事件
- `GET /api/telemetry/metrics` - v2.0: 指标统计

### API 统计

- `auto_test_api`: 11 个路由
- `telemetry_api`: 2 个路由

## 📊 功能统计

### 测试能力

- ✅ 单张图片测试（v1.1）
- ✅ 视频测试（v1.2）
- ✅ 批量测试（v3/v4/v5）
- ✅ Playlist 测试（v1.3）
- ✅ 自动搜图测试（V6.1）
- ✅ 错误聚类分析（v5/V6.1）
- ✅ 训练数据生成（v6/V6.1）

### 关键词支持

- v1.1: 17 个关键词（新判断器）
- V2-V6: 60+ 个关键词（原有判断器）

## 🔄 依赖变更

### 新增可选依赖

- `beautifulsoup4` - 自动搜图功能
- `duckduckgo-search` - DuckDuckGo 图片搜索
- `paddleocr` - OCR 功能（可选）
- `scikit-learn` - 高级错误聚类（可选）

**注意**：所有依赖都有降级方案，不安装也能运行（功能受限）

## 🐛 已知问题

1. **sklearn 兼容性问题**
   - 当前环境存在 numpy/pandas 版本冲突
   - 已实现降级方案（使用简化版聚类）
   - 不影响核心功能

2. **PaddleOCR 依赖问题**
   - 当前环境存在 numpy 兼容性问题
   - 已实现降级方案（使用现有 vision_engine）
   - 不影响核心功能

## 📝 使用说明

### 快速开始

1. **启动服务器**：
   ```bash
   cd Luna_Badge
   python3 web_test_server.py
   ```

2. **访问测试页面**：
   ```
   http://localhost:9001
   ```

3. **使用自动测试**：
   - 切换到"综合检测"标签页
   - 使用 v1.1、v1.2、v1.3 测试面板

### TestEngine 使用

```python
from test_engine import ScenarioRunner

runner = ScenarioRunner()
result = runner.run("test_engine/scenarios/stairs.json", limit=10)
print(result["report"])
```

## 🔮 后续计划

- 场景标准 × 情感标准 × 设备反馈标准的统一规范
- 更复杂的指标分析
- 自动微调训练数据生成
- 版本对比功能

## 📚 相关文档

- `CHANGELOG.md` - 完整更新日志
- `RELEASE_NOTES_v1.2.0.md` - 发布说明
- `test_engine/README.md` - TestEngine 文档
- `auto_test/V1_COMPLETE_SUMMARY.md` - v1.1-v2.0 功能总结

---

**版本**: 1.2.0  
**最后更新**: 2024-11-20



# Luna Badge 更新日志

## [1.2.0] - 2024-11-20

### 🎉 重大更新

本次版本（1.2.0）是一个重要的功能增强版本，主要包含自动化测试系统的完整实现，从 v1.1 到 v2.0 的所有功能。

---

## ✨ 新增功能

### 🔹 v1.1: 浏览器 UI 面板版自动测试

**功能描述**：
- 在 `/test` 页面提供完整的自动测试 UI 面板
- 支持上传图片 + 输入关键词进行自动场景描述测试
- 自动判断匹配结果（匹配成功/匹配失败）
- 提供人工校对界面，支持标记 AI 判断正确/错误
- 一键导出 CSV 训练数据

**新增文件**：
- `backend/auto_test/auto_test_judger.py` - 自动测试判断器（17个关键词规则）

**新增路由**：
- `POST /api/auto/run_full_test` - 单张图片自动测试接口

**前端更新**：
- 新增"自动场景测试 v1.1"面板
- 匹配成功/失败分类显示
- 人工校对界面
- CSV 导出功能

**支持的关键词**（17个）：
- 斑马线、红绿灯、人行道、盲道
- 道路施工、台阶、坡道
- 公交站牌、地铁入口、自动扶梯、电梯入口
- 商场入口、医院挂号大厅、医院科室门牌
- 小区大门、小区停车场、小区道路

---

### 🔹 v1.2: 视频自动检测

**功能描述**：
- 支持上传视频文件进行自动测试
- 自动从视频中提取帧（每隔10帧抽一帧，最多30帧）
- 对每一帧进行场景描述和匹配判断
- 输出整体准确率统计

**新增文件**：
- `backend/auto_test/video_frame_extractor.py` - 视频帧提取器

**新增路由**：
- `POST /api/auto/run_video_test` - 视频自动测试接口

**前端更新**：
- 新增"视频自动测试 v1.2"面板
- 视频上传 + 关键词输入
- 测试结果显示（总帧数、匹配帧、准确率）

---

### 🔹 v1.3: 多场景 Playlist 自动测试

**功能描述**：
- 支持一次性测试多个场景关键词
- 基于单张图片，循环测试多个关键词
- 输出每个场景的准确率汇总表

**前端更新**：
- 新增"场景 Playlist 自动测试 v1.3"面板
- 场景列表输入（逗号分隔，默认17个关键词）
- 每个场景测试次数设置
- 汇总表格显示

**使用流程**：
1. 在 v1.1 面板上传一张测试图片
2. 在 v1.3 面板设置场景列表和测试次数
3. 点击"运行 Playlist 测试"
4. 查看汇总表格

---

### 🔹 v2.0: 真实设备数据上报骨架

**功能描述**：
- 提供设备事件上报接口
- 支持多种事件类型（vision_warning, navigation_step, tts_error, scene_mismatch 等）
- 简单的指标统计功能
- 为后续"错误聚类 + 标准体系 + 情感计算联动"预留接口

**新增文件**：
- `routes/telemetry_routes.py` - Telemetry API 路由
- `device_logs/` - 日志存储目录

**新增路由**：
- `POST /api/telemetry/event` - 设备上报事件接口
- `GET /api/telemetry/metrics` - 指标统计接口

**日志格式**：
- JSONL 格式（每行一个 JSON 对象）
- 存储位置：`device_logs/telemetry_events.jsonl`

---

### 🔹 TestEngine v1.0: 自动化场景测试系统

**功能描述**：
- 完整的自动化测试框架，独立于现有系统
- 支持自动搜图、自动检测、自动评估、自动聚类、自动生成训练数据

**新增目录**：
- `test_engine/` - 完整的测试引擎系统

**核心模块**：
- `scenario_runner.py` - 核心执行器
- `image_fetcher.py` - 自动搜图模块（DuckDuckGo）
- `detector.py` - YOLO 视觉检测模块
- `ocr_reader.py` - OCR 识别模块
- `evaluator.py` - 规则判断与标签匹配
- `cluster_engine.py` - 错判自动聚类
- `reporter.py` - 测试报告生成
- `dataset_manager.py` - 训练数据自动生成

**场景配置**：
- `scenarios/stairs.json` - 楼梯场景
- `scenarios/crosswalk.json` - 斑马线场景
- `scenarios/bus_enter.json` - 公交站场景
- `scenarios/mall_navigation.json` - 商场导航场景
- `scenarios/residential_path.json` - 住宅区道路场景

**文档**：
- `test_engine/README.md` - 完整文档
- `test_engine/USAGE.md` - 使用指南
- `test_engine/QUICK_START.md` - 快速开始

---

### 🔹 V6.1: 自动搜图 + 错误聚类增强

**功能描述**：
- 自动从 DuckDuckGo 搜索并下载图片（无需 API key）
- 批量测试 + 错误聚类分析
- 自动保存错误样本到训练数据

**新增文件**：
- `backend/auto_image_search.py` - DuckDuckGo 图片搜索
- `backend/auto_test_clustering.py` - 错误聚类分析

**新增路由**：
- `POST /api/auto/auto_search_images` - 自动搜索并下载图片
- `POST /api/auto/run_batch_with_clustering` - 批量测试 + 错误聚类

**前端更新**：
- 新增"V6.1：自动搜图 + 错误聚类"面板
- 关键词列表输入
- 自动搜图按钮
- 批量测试 + 错误聚类按钮

---

## 🔧 改进和优化

### 后端改进

1. **AutoTestRunner 多目录支持**
   - 优先从 `downloads/` 目录读取图片（V6.1 自动下载）
   - 备用 `test_images/` 目录（V2-V6 本地图库）
   - 支持自定义 `base_dir`

2. **错误处理增强**
   - 所有模块都有降级方案
   - 缺少依赖时自动使用简化版本
   - 详细的错误日志记录

3. **路由组织优化**
   - 统一使用 Blueprint 组织路由
   - 清晰的 API 命名规范
   - 完整的错误码体系

### 前端改进

1. **UI 统一性**
   - 统一的样式风格
   - 清晰的视觉层次
   - 响应式布局

2. **用户体验**
   - 实时反馈（按钮状态、进度提示）
   - 错误提示友好
   - 数据导出便捷

---

## 📁 文件变更清单

### 新增文件（共 20+ 个）

**后端模块**：
- `backend/auto_test/auto_test_judger.py`
- `backend/auto_test/video_frame_extractor.py`
- `backend/auto_image_search.py`
- `backend/auto_test_clustering.py`

**路由模块**：
- `routes/telemetry_routes.py`

**TestEngine 系统**：
- `test_engine/__init__.py`
- `test_engine/scenario_runner.py`
- `test_engine/image_fetcher.py`
- `test_engine/detector.py`
- `test_engine/ocr_reader.py`
- `test_engine/evaluator.py`
- `test_engine/cluster_engine.py`
- `test_engine/reporter.py`
- `test_engine/dataset_manager.py`
- `test_engine/scenarios/stairs.json`
- `test_engine/scenarios/crosswalk.json`
- `test_engine/scenarios/bus_enter.json`
- `test_engine/scenarios/mall_navigation.json`
- `test_engine/scenarios/residential_path.json`
- `test_engine/README.md`
- `test_engine/USAGE.md`
- `test_engine/QUICK_START.md`

**文档**：
- `auto_test/V1_COMPLETE_SUMMARY.md`
- `auto_test/V6.1_SUMMARY.md`
- `auto_test/USAGE.md`
- `auto_test/README.md`
- `CHANGELOG.md`（本文件）

**目录**：
- `device_logs/` - 设备日志存储
- `downloads/` - 自动下载的图片
- `test_engine/data/` - TestEngine 运行时数据
- `test_engine/dataset/` - TestEngine 训练数据输出
- `test_engine/reports/` - TestEngine 测试报告输出

### 修改文件

- `routes/auto_test_routes.py` - 添加 v1.1 + v1.2 路由
- `web_test_server.py` - 添加前端 UI + JS（v1.1 + v1.2 + v1.3 + v2.0）
- `backend/auto_test_runner.py` - 更新支持多目录

---

## 🔌 API 变更

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

---

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

### 数据导出

- CSV 格式（训练样本）
- JSON 格式（训练样本）
- JSONL 格式（设备日志）

---

## 🔄 依赖变更

### 新增可选依赖

- `beautifulsoup4` - 自动搜图功能（V6.1）
- `duckduckgo-search` - DuckDuckGo 图片搜索（TestEngine）
- `paddleocr` - OCR 功能（TestEngine，可选）
- `scikit-learn` - 高级错误聚类（可选）

**注意**：所有依赖都有降级方案，不安装也能运行（功能受限）

---

## 🐛 已知问题

1. **sklearn 兼容性问题**
   - 当前环境存在 numpy/pandas 版本冲突
   - 已实现降级方案（使用简化版聚类）
   - 不影响核心功能

2. **PaddleOCR 依赖问题**
   - 当前环境存在 numpy 兼容性问题
   - 已实现降级方案（使用现有 vision_engine）
   - 不影响核心功能

---

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

详细文档请参考：
- `test_engine/README.md`
- `test_engine/USAGE.md`
- `auto_test/V1_COMPLETE_SUMMARY.md`

---

## 🎯 版本目标达成情况

### ✅ 已完成

- [x] v1.1: 浏览器 UI 面板版自动测试
- [x] v1.2: 视频自动检测
- [x] v1.3: 多场景 Playlist 自动跑
- [x] v2.0: 真实设备数据上报骨架
- [x] V6.1: 自动搜图 + 错误聚类
- [x] TestEngine v1.0: 完整的自动化测试框架

### 🔮 后续计划（二期）

- [ ] 场景标准 × 情感标准 × 设备反馈标准的统一规范
- [ ] 更复杂的指标分析（v2.0 扩展）
- [ ] 自动微调训练数据生成
- [ ] 版本对比功能
- [ ] 错误统计可视化

---

## 👥 贡献者

- 开发团队：Luna Badge Team
- 版本号：1.2.0
- 发布日期：2024-11-20

---

## 📄 许可证

（保持原有许可证）

---

**版本 1.2.0 封版完成**



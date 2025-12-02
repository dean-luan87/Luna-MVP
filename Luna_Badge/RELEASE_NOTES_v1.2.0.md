# Luna Badge v1.2.0 发布说明

## 🎉 版本概述

Luna Badge v1.2.0 是一个重要的功能增强版本，主要包含完整的自动化测试系统实现，从浏览器 UI 面板到真实设备数据上报的完整链路。

## 🚀 核心特性

### 1. 自动化测试系统（v1.1 - v1.3）

- **v1.1**: 浏览器 UI 面板版自动测试
  - 单张图片上传 + 关键词测试
  - 自动场景描述 + 匹配判断
  - 人工校对 + CSV 导出

- **v1.2**: 视频自动检测
  - 视频上传 + 自动抽帧
  - 批量场景描述 + 匹配统计
  - 整体准确率计算

- **v1.3**: 多场景 Playlist 自动测试
  - 一次性测试多个场景关键词
  - 基于单张图片循环测试
  - 汇总表格展示

### 2. 设备数据上报系统（v2.0）

- 设备事件上报接口
- 简单指标统计
- 日志存储（JSONL 格式）
- 为后续扩展预留接口

### 3. TestEngine v1.0

- 完整的自动化测试框架
- 支持场景配置化测试
- 自动搜图、检测、评估、聚类、报告生成

### 4. V6.1 增强功能

- 自动搜图（DuckDuckGo）
- 错误聚类分析
- 训练数据自动生成

## 📦 安装和升级

### 系统要求

- Python 3.9+
- Flask
- OpenCV
- （可选）beautifulsoup4, duckduckgo-search, paddleocr, scikit-learn

### 升级步骤

1. 备份现有配置和数据
2. 更新代码到 v1.2.0
3. 安装可选依赖（如需要）
4. 重启服务器

### 可选依赖安装

```bash
pip install beautifulsoup4      # 自动搜图功能
pip install duckduckgo-search  # DuckDuckGo 图片搜索
pip install paddleocr          # OCR 功能（可选）
pip install scikit-learn numpy # 高级错误聚类（可选）
```

## 🔧 配置变更

### 新增配置

无需额外配置，所有功能开箱即用。

### 目录结构

新增以下目录（自动创建）：
- `device_logs/` - 设备日志存储
- `downloads/` - 自动下载的图片
- `test_engine/` - TestEngine 系统文件

## 📚 文档

- `CHANGELOG.md` - 完整更新日志
- `test_engine/README.md` - TestEngine 文档
- `auto_test/V1_COMPLETE_SUMMARY.md` - v1.1-v2.0 功能总结

## 🐛 已知问题

1. sklearn/pandas 版本兼容性问题（已实现降级方案）
2. PaddleOCR 依赖问题（已实现降级方案）

## 🔮 后续计划

- 场景标准 × 情感标准 × 设备反馈标准的统一规范
- 更复杂的指标分析
- 自动微调训练数据生成
- 版本对比功能

## 📞 支持

如有问题，请查看文档或联系开发团队。

---

**版本**: 1.2.0  
**发布日期**: 2024-11-20  
**状态**: 稳定版

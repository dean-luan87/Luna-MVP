# Luna Badge v1.2.1 更新日志

## [1.2.1] - 2024-11-20

### 🔧 优化改进（P1）

本次版本主要实施 P1 优化，提升代码质量和可维护性。

---

## ✨ 新增功能

### 1. 配置管理优化

**新增文件**：
- `config/auto_test_config.py` - 自动化测试配置管理

**功能**：
- 统一管理场景描述 API 地址、超时时间、视频抽帧参数等配置
- 支持通过环境变量覆盖默认配置
- 避免硬编码，提高可配置性

**配置项**：
- `SCENE_DESC_API_BASE_URL` - 场景描述 API 基地址（默认: http://localhost:9001）
- `SCENE_DESC_API_PATH` - 场景描述接口路径（默认: /api/navigation/describe_scene）
- `HTTP_TIMEOUT` - HTTP 请求超时时间（默认: 10秒）
- `VIDEO_FRAME_STEP` - 视频抽帧步长（默认: 10帧）
- `VIDEO_MAX_FRAMES` - 视频最多抽取帧数（默认: 30帧）

**环境变量支持**：
```bash
export SCENE_DESC_API_BASE_URL="http://your-server:9001"
export AUTO_TEST_HTTP_TIMEOUT="15"
export AUTO_TEST_VIDEO_FRAME_STEP="15"
export AUTO_TEST_VIDEO_MAX_FRAMES="50"
```

---

### 2. 场景描述工具函数

**新增文件**：
- `backend/utils/scene_description_helper.py` - 场景描述工具函数

**功能**：
- 统一调用场景描述接口的逻辑
- 提供两种调用方式：
  - `call_scene_description_api()` - HTTP API 调用（用于跨服务调用）
  - `call_scene_description_engine_direct()` - 直接调用引擎（用于内部调用，避免 HTTP 开销）

**优势**：
- 避免在多个路由中重复代码
- 统一错误处理和日志记录
- 易于修改接口路径或添加参数
- 支持多种描述字段名（description, scene_description, short_description, summary）

---

### 3. 单元测试骨架

**新增文件**：
- `tests/test_auto_test_judger.py` - AutoTestJudger 单元测试

**功能**：
- 测试 AutoTestJudger 的基本匹配功能
- 测试边界情况（空描述、None 描述）
- 测试大小写不敏感
- 测试未知关键词的降级处理

**使用**：
```bash
# 运行单测
pytest tests/test_auto_test_judger.py

# 运行单测（详细输出）
pytest tests/test_auto_test_judger.py -v
```

**优势**：
- 防止修改 MATCH_RULES 时破坏现有功能
- 快速验证匹配逻辑的正确性
- 为后续功能扩展提供测试基础

---

## 🔧 修改文件

### routes/auto_test_routes.py

**修改内容**：
1. 导入新配置和工具函数
   ```python
   from config.auto_test_config import AutoTestConfig
   from backend.utils.scene_description_helper import call_scene_description_api, call_scene_description_engine_direct
   ```

2. `run_full_test()` 路由
   - 使用 `call_scene_description_api()` 替代硬编码的 HTTP 请求
   - 移除硬编码的 `localhost:9001` 和超时时间

3. `run_full_test_v1_1()` 路由
   - 使用 `call_scene_description_engine_direct()` 替代直接调用引擎
   - 简化错误处理和描述提取逻辑

4. `run_video_test()` 路由
   - 使用 `AutoTestConfig.VIDEO_FRAME_STEP` 和 `AutoTestConfig.VIDEO_MAX_FRAMES`
   - 使用 `call_scene_description_engine_direct()` 替代直接调用引擎

**优势**：
- 代码更简洁
- 配置统一管理
- 易于维护和扩展

---

## 📊 改动统计

- **新增文件**: 4 个
  - `config/auto_test_config.py`
  - `backend/utils/scene_description_helper.py`
  - `backend/utils/__init__.py`
  - `tests/test_auto_test_judger.py`
  - `tests/__init__.py`

- **修改文件**: 1 个
  - `routes/auto_test_routes.py`

- **新增代码**: ~300 行
- **重构代码**: ~50 行

---

## 🔄 向后兼容性

✅ **完全向后兼容**

- 所有 API 接口保持不变
- 默认配置与之前行为一致
- 不影响现有功能

---

## 📝 使用说明

### 配置环境变量（可选）

```bash
# 修改场景描述 API 地址
export SCENE_DESC_API_BASE_URL="http://your-server:9001"

# 修改超时时间
export AUTO_TEST_HTTP_TIMEOUT="15"

# 修改视频抽帧参数
export AUTO_TEST_VIDEO_FRAME_STEP="15"
export AUTO_TEST_VIDEO_MAX_FRAMES="50"
```

### 运行单元测试

```bash
# 安装 pytest（如果未安装）
pip install pytest

# 运行单测
pytest tests/test_auto_test_judger.py -v
```

---

## 🎯 后续计划（P2 - v1.3.0）

- [ ] 拆分 `web_test_server.py` 大文件
- [ ] 统一日志格式
- [ ] 更多单元测试覆盖

---

**版本**: 1.2.1  
**发布日期**: 2024-11-20  
**状态**: 稳定版



# 测试迁移通知

## 重要说明

**所有测试相关的内容已迁移到独立的测试项目：`luna_badge_tests/`**

## 迁移日期

2025-12-09

## 迁移内容

### 1. 测试目录迁移

- **原位置**: `luna_badge_v1_2/tests/`
- **新位置**: `luna_badge_tests/tests/`
- **状态**: ✅ 已迁移

### 2. 独立测试脚本迁移

以下文件已迁移到 `luna_badge_tests/standalone_tests/`：

- `test_manual_v1_4_4.py`
- `test_command_layer_standalone.py`
- `test_command_layer_smoke.py`
- `test_hospital_template_structure.py`
- `test_tts_direct.py`
- `test_tts_guard.py`
- `test_tts_quick.py`
- `test_voice_b1.py`
- `test_voice_complete.py`

## 测试项目位置

```
/Users/luanlei/Desktop/Luna-2/luna_badge_tests/
```

## 运行测试

### 方式 1：在测试项目中运行

```bash
cd /Users/luanlei/Desktop/Luna-2/luna_badge_tests
pytest tests/ -v
```

### 方式 2：从主项目运行（需要指定路径）

```bash
cd /Users/luanlei/Desktop/Luna-2/luna_badge_tests
pytest tests/ -v --pythonpath=/Users/luanlei/Desktop/Luna-2/luna_badge_v1_2
```

## 后续开发规范

**重要**：以后所有测试相关的内容都应放在测试项目中，与主项目一一对应：

1. **新增测试文件**：放在 `luna_badge_tests/tests/` 对应目录
2. **独立测试脚本**：放在 `luna_badge_tests/standalone_tests/`
3. **测试配置**：放在 `luna_badge_tests/` 根目录

## 主项目中的测试文件

主项目中的 `tests/` 目录和 `test_*.py` 文件**已迁移**，但为保持兼容性，暂时保留。

**建议**：后续版本可以删除主项目中的测试文件，统一使用测试项目。

---

**迁移完成日期**: 2025-12-09  
**维护者**: Luna Badge Team













# Luna Badge 测试项目

## 项目说明

本目录包含 Luna Badge 项目的所有测试代码，与主项目 `luna_badge_v1_2` 一一对应。

## 目录结构

```
luna_badge_tests/
├── README.md                 # 本文件
├── requirements.txt          # 测试依赖
├── pytest.ini               # pytest 配置
├── tests/                   # 主测试目录（与主项目对应）
│   ├── conftest.py         # pytest 全局配置
│   ├── v1_4_4/            # v1.4.4 版本测试
│   ├── v1_4_5/             # v1.4.5 版本测试
│   ├── v1_4_5a/            # v1.4.5a 版本测试
│   ├── v1_4_7/             # v1.4.7 版本测试
│   └── ...                 # 其他版本测试
└── standalone_tests/        # 独立测试脚本
    ├── test_manual_v1_4_4.py
    ├── test_command_layer_standalone.py
    └── ...
```

## 运行测试

### 运行所有测试

```bash
cd /Users/luanlei/Desktop/Luna-2/luna_badge_tests
pytest tests/ -v
```

### 运行特定版本测试

```bash
# v1.4.5 测试
pytest tests/v1_4_5/ -v

# v1.4.5a 测试
pytest tests/v1_4_5a/ -v

# v1.4.7 测试
pytest tests/v1_4_7/ -v
```

### 运行独立测试脚本

```bash
cd standalone_tests
python test_manual_v1_4_4.py
```

## 测试项目与主项目对应关系

测试项目的目录结构与主项目一一对应：

| 主项目路径 | 测试项目路径 |
|-----------|------------|
| `luna_badge_v1_2/core/` | `tests/v1_4_5/test_model_scheduler.py` 等 |
| `luna_badge_v1_2/composition/` | `tests/v1_4_5a/test_*.py` |
| `luna_badge_v1_2/pieces/` | `tests/v1_4_5a/test_*.py` |
| `luna_badge_v1_2/task_engine/scene/` | `tests/v1_4_7/test_*.py` |

## 导入路径说明

测试文件中的导入路径需要指向主项目：

```python
# 示例：测试文件中的导入
from core.flow_templates.hospital_go_template import GoHospitalTemplate
from composition.composition_engine import CompositionEngine
from pieces.registry import TaskPieceRegistry
```

**注意**：运行测试时，需要确保 Python 路径包含主项目目录：

```bash
export PYTHONPATH=/Users/luanlei/Desktop/Luna-2/luna_badge_v1_2:$PYTHONPATH
pytest tests/ -v
```

或者使用 pytest 的 `--pythonpath` 选项：

```bash
pytest tests/ -v --pythonpath=/Users/luanlei/Desktop/Luna-2/luna_badge_v1_2
```

## 测试迁移历史

- **2025-12-09**: 从 `luna_badge_v1_2/tests/` 迁移到 `luna_badge_tests/tests/`
- **2025-12-09**: 从 `luna_badge_v1_2/test_*.py` 迁移到 `luna_badge_tests/standalone_tests/`

## 后续维护

**重要规范（长期有效）**：

1. **所有测试相关内容**：必须放在测试项目中，不得放在主项目中
2. **新增测试**：所有新测试都应放在本测试项目中，与主项目结构对应
3. **版本管理**：按版本号组织测试目录（如 `v1_4_5/`, `v1_4_6/` 等）
4. **独立脚本**：独立的测试脚本放在 `standalone_tests/` 目录
5. **旧版本测试**：v1.4 之前的测试放在 `tests/legacy/` 或对应版本目录
6. **测试配置**：所有测试配置文件（pytest.ini, requirements.txt 等）放在测试项目根目录

**禁止事项**：
- ❌ 禁止在主项目中创建新的测试文件
- ❌ 禁止在主项目的 `modules/`、`scripts/` 等目录中放置测试文件
- ❌ 禁止在主项目根目录放置 `test_*.py` 文件

---

**测试项目维护者**: Luna Badge Team  
**最后更新**: 2025-12-09  
**规范生效日期**: 2025-12-09（长期有效）


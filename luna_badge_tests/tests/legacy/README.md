# Legacy Tests (v1.4 之前的测试)

## 说明

本目录包含 v1.4 之前版本的测试文件，这些测试文件来自主项目的 `modules/` 和 `scripts/` 目录。

## 目录结构

```
legacy/
├── README.md                    # 本文件
├── modules/                      # 来自 modules/ 目录的测试
│   ├── test_guard_chain.py
│   ├── test_main_events.py
│   └── test_voice_av.py
└── scripts/                      # 来自 scripts/ 目录的测试
    ├── test_voice_av.py
    ├── test_voice_av_detailed.py
    └── test_voice_av_scenarios.py
```

## 注意事项

1. 这些测试可能依赖旧版本的代码结构
2. 运行前请检查导入路径是否正确
3. 部分测试可能需要更新以适应新的项目结构

## 迁移日期

2025-12-09













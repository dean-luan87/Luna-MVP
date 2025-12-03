# Luna Badge v1.4.1 - QA 自动化测试套件

## 目录结构

```
tests/qa_1_4_1/
├── README.md                    # 本文件
├── conftest.py                  # pytest 配置和 fixtures
├── test_speed_engine.py         # Speed Engine 测试 (SE-01 ~ SE-04)
├── test_health_monitor.py       # HealthMonitor 测试 (HM-01 ~ HM-04)
├── test_fail_safe_manager.py    # FailSafeManager 测试 (FSM-01 ~ FSM-04)
├── test_emergency_voice.py      # EmergencyVoiceLayer 测试 (EV-01 ~ EV-03)
├── test_degraded_hooks.py       # DegradedHooks 测试 (DG-01 ~ DG-03)
├── test_auto_recovery.py        # AutoRecoveryManager 测试 (AR-01 ~ AR-03)
├── test_config.py               # 配置测试 (CFG-01 ~ CFG-02)
├── test_integration_stress.py   # 集成压力测试 (IT-01 ~ IT-02)
├── test_scenarios.py            # 全链路场景测试 (SC-01 ~ SC-02)
├── mocks/
│   ├── __init__.py
│   ├── mock_camera.py           # 摄像头模拟
│   ├── mock_yolo.py             # YOLO 模型模拟
│   └── mock_tts_ocr.py          # TTS/OCR 模拟
└── utils/
    ├── __init__.py
    ├── event_injector.py        # 异常事件注入器
    ├── thread_checker.py        # 线程健康检查
    └── log_analyzer.py          # 日志分析器
```

## 运行方式

### 运行所有测试
```bash
pytest tests/qa_1_4_1/ -v
```

### 运行特定模块测试
```bash
pytest tests/qa_1_4_1/test_speed_engine.py -v
```

### 运行特定用例
```bash
pytest tests/qa_1_4_1/test_speed_engine.py::test_se_01_camera_worker_normal -v
```

### 生成测试报告
```bash
pytest tests/qa_1_4_1/ --html=reports/qa_report.html --self-contained-html
```

## 测试环境要求

- Python 3.9+
- pytest
- pytest-html (可选，用于生成报告)
- psutil (用于系统监控测试)

## 注意事项

- 部分测试需要摄像头（SE-01），如果没有摄像头会自动跳过
- 压力测试（IT-02）需要较长时间，建议单独运行
- 所有测试都会自动清理资源，确保不影响后续测试


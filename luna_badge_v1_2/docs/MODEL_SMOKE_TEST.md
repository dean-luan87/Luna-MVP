# 模型冒烟测试 (Model Smoke Test)

## 📋 概述

`model_smoke_test.py` 是一个专业的模型健康检查脚本，用于验证所有注册的 YOLO 模型是否正常工作。

## 🎯 功能

- ✅ 自动读取 `configs/model_registry.yaml`
- ✅ 检查每个模型文件是否存在
- ✅ 测试模型能否成功加载 Session
- ✅ 使用虚拟图像进行单次推理测试
- ✅ 统计加载耗时和推理耗时
- ✅ 彩色输出（绿色 PASS / 红色 FAIL）
- ✅ 自动生成 JSON 和 CSV 报告

## 📦 依赖

```bash
pip install onnxruntime opencv-python numpy pyyaml
```

或使用项目的 requirements：

```bash
pip install -r realtime_lab/backend/requirements.txt
```

## 🚀 运行方式

```bash
python3 model_smoke_test.py
```

## 📊 输出示例

### 终端输出（彩色）

```
========== Luna Model Smoke Test ==========

>>> 测试模型：yolo11_nav_tiny_v1
[PASS] yolo11_nav_tiny_v1 | load 12.55ms | infer 3.72ms

>>> 测试模型：yolo11_nav_nano_v1
[PASS] yolo11_nav_nano_v1 | load 10.33ms | infer 2.91ms

报告已生成：
 - test_reports/model_smoke_report.json
 - test_reports/model_smoke_report.csv

========== 测试结束 ==========
通过: 2 / 2
✅ 全部模型正常，可投入使用。
```

### JSON 报告

```json
[
    {
        "model_name": "yolo11_nav_tiny_v1",
        "status": "PASS",
        "load_ms": 12.55,
        "infer_ms": 3.72,
        "error": null
    },
    {
        "model_name": "yolo11_nav_nano_v1",
        "status": "PASS",
        "load_ms": 10.33,
        "infer_ms": 2.91,
        "error": null
    }
]
```

### CSV 报告

```csv
model_name,status,load_ms,infer_ms,error
yolo11_nav_tiny_v1,PASS,12.55,3.72,
yolo11_nav_nano_v1,PASS,10.33,2.91,
```

## 📝 报告文件位置

- **JSON 报告**: `test_reports/model_smoke_report.json`
- **CSV 报告**: `test_reports/model_smoke_report.csv`

## ⚠️ 常见问题

### 1. 模型文件不存在

如果模型文件不存在，测试会显示：

```
[FAIL] yolo11_nav_tiny_v1 - file missing
```

**解决方案**: 下载模型文件到 `models/` 目录，或编辑 `configs/model_registry.yaml` 更新模型路径。

### 2. onnxruntime 未安装

```
❌ onnxruntime 未安装，请运行: pip install onnxruntime
```

**解决方案**: 安装依赖 `pip install onnxruntime`

### 3. 模型加载失败

如果模型文件损坏或格式不正确：

```
[FAIL] yolo11_nav_tiny_v1 - load error
```

**解决方案**: 检查模型文件是否完整，重新下载模型文件。

## 🔄 集成到 CI/CD

可以将此脚本集成到自动化测试流程中：

```bash
# 在 CI 中运行
python3 model_smoke_test.py

# 检查是否有失败
if grep -q "FAIL" test_reports/model_smoke_report.csv; then
    echo "❌ 模型测试失败"
    exit 1
fi
```

## 📚 相关文档

- [模型注册表配置](../configs/model_registry.yaml)
- [模型管理系统](../core/model_registry.py)
- [YOLO 检测器](../core/yolo_detector.py)






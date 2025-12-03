from core.logging import get_logger

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
log = get_logger("model_smoke_test")
"""
Model Smoke Test for Luna Badge
--------------------------------
一次性验证：
1. 所有注册模型文件是否存在
2. 是否能成功加载 Session
3. 是否能成功对虚拟图片进行一次推理
4. 输出加载耗时 + 推理耗时
5. 自动生成报告 JSON/CSV

运行方式：
    python3 model_smoke_test.py
"""

import time
import json
import csv
import numpy as np
from pathlib import Path
from typing import Dict, Any

try:
    import onnxruntime as ort
except ImportError:
    log.info("❌ onnxruntime 未安装，请运行: pip install onnxruntime")
    exit(1)

from core.model_registry import ModelRegistry

REPORT_DIR = Path("test_reports")
REPORT_DIR.mkdir(exist_ok=True)

JSON_PATH = REPORT_DIR / "model_smoke_report.json"
CSV_PATH = REPORT_DIR / "model_smoke_report.csv"


def now_ms():
    return round(time.perf_counter() * 1000, 3)


def load_image_mock(shape=(640, 640, 3)):
    """生成虚拟图片用于推理测试"""
    return np.random.randint(0, 255, shape, dtype=np.uint8)


def preprocess(img: np.ndarray, input_size):
    """简化预处理"""
    import cv2

    resized = cv2.resize(img, tuple(input_size))
    blob = resized.astype(np.float32) / 255.0
    blob = np.transpose(blob, (2, 0, 1))  # HWC → CHW
    blob = np.expand_dims(blob, 0)
    return blob


def run_model_test(model_name: str, model_info: Dict[str, Any]):
    """对单个模型进行 smoke test"""

    result = {
        "model_name": model_name,
        "status": "FAIL",
        "load_ms": None,
        "infer_ms": None,
        "error": None,
    }

    model_path = Path(model_info["path"])
    input_size = model_info.get("input_size", [640, 640])

    # 1) 检查文件是否存在
    if not model_path.exists():
        result["error"] = f"Model file not found: {model_path}"
        log.error(f"\033[91m[FAIL] {model_name} - file missing\033[0m")
        return result

    # 2) 加载模型
    t0 = now_ms()
    try:
        sess = ort.InferenceSession(str(model_path))
        load_time = now_ms() - t0
        result["load_ms"] = load_time
    except Exception as e:
        result["error"] = f"Load failed: {str(e)}"
        log.error(f"\033[91m[FAIL] {model_name} - load error\033[0m")
        return result

    # 3) 生成虚拟图片并推理一次
    dummy_img = load_image_mock()
    input_tensor = preprocess(dummy_img, input_size)
    input_name = sess.get_inputs()[0].name

    t1 = now_ms()
    try:
        _ = sess.run(None, {input_name: input_tensor})
        infer_time = now_ms() - t1
        result["infer_ms"] = infer_time
    except Exception as e:
        result["error"] = f"Infer failed: {str(e)}"
        log.error(f"\033[91m[FAIL] {model_name} - infer error\033[0m")
        return result

    # 全部通过
    result["status"] = "PASS"
    log.info(f"\033[92m[PASS] {model_name} | load {load_time:.2f}ms | infer {infer_time:.2f}ms\033[0m")
    return result


def write_reports(results):
    """保存 JSON & CSV 报告"""

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["model_name", "status", "load_ms", "infer_ms", "error"])
        for r in results:
            writer.writerow([
                r["model_name"],
                r["status"],
                r["load_ms"],
                r["infer_ms"],
                r["error"],
            ])

    log.info(f"\n报告已生成：\n - {JSON_PATH}\n - {CSV_PATH}")


def main():
    log.info("\n========== Luna Model Smoke Test ==========\n")

    models = ModelRegistry.list_models()
    
    if not models:
        log.info("\033[91m❌ 未找到已注册的模型，请检查 configs/model_registry.yaml\033[0m")
        return
    
    log.info(f"发现 {len(models)} 个已注册模型\n")
    
    results = []

    for name, info in models.items():
        log.info(f">>> 测试模型：{name}")
        result = run_model_test(name, info)
        results.append(result)

    write_reports(results)

    # 总结
    pass_count = sum(1 for r in results if r["status"] == "PASS")
    fail_count = len(results) - pass_count

    log.info("\n========== 测试结束 ==========")
    log.info(f"通过: {pass_count} / {len(results)}")
    log.error(f"失败: {fail_count} / {len(results)}")

    if fail_count == 0:
        log.info("\033[92m✅ 全部模型正常，可投入使用。\033[0m\n")
    else:
        log.info("\033[91m❌ 存在失败模型，请检查模型文件或注册表。\033[0m\n")


if __name__ == "__main__":
    main()


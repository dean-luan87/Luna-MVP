from core.logging import get_logger

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
log = get_logger("test_all")
"""
Luna Badge v1.3.0 稳固性测试总控脚本
目标：零误差，所有测试必须通过
"""

import subprocess
import json
import time
import sys
import os
from pathlib import Path

# 确保 test_reports 目录存在
Path("test_reports").mkdir(parents=True, exist_ok=True)

TESTS = [
    ("F1_vision_capture", "python3 tests/test_f1_capture.py"),
    ("F2_recognition", "python3 tests/test_f2_recognition.py"),
    ("F3_dispatcher", "python3 tests/test_f3_dispatcher.py"),
    ("F4_ground_state", "python3 tests/test_f4_ground_state.py"),
    ("ModelRouter", "python3 tests/test_model_router.py"),
    ("AsyncEngine", "python3 tests/test_async_engine.py"),
    ("ErrorCodes", "python3 tests/test_error_codes.py"),
    ("TaskChain", "python3 tests/test_task_chain.py"),
    ("SceneTests", "python3 tests/test_scenes.py"),
]

RESULT = {}


def run_test(name, command):
    """运行单个测试"""
    log.info(f"\n{'='*60}")
    log.info(f"Running {name}")
    log.info(f"{'='*60}")
    start = time.time()
    try:
        proc = subprocess.run(
            command, shell=True, text=True,
            capture_output=True, timeout=120  # 增加到120秒超时
        )
        output = proc.stdout + proc.stderr
        success = proc.returncode == 0
        RESULT[name] = {
            "success": success,
            "returncode": proc.returncode,
            "output": output[-1000:] if len(output) > 1000 else output,  # 只保留最后1000字符
            "time": round(time.time() - start, 2)
        }
        
        if success:
            log.info(f"✅ {name} - PASSED ({RESULT[name]['time']}s)")
        else:
            log.error(f"❌ {name} - FAILED (returncode: {proc.returncode})")
            log.info(f"输出: {output[-500:] if len(output) > 500 else output}")
            
    except subprocess.TimeoutExpired:
        RESULT[name] = {
            "success": False,
            "error": "Timeout (>120s)",
            "time": 120
        }
        log.info(f"❌ {name} - TIMEOUT (>120s)")
    except Exception as e:
        RESULT[name] = {
            "success": False,
            "error": str(e),
            "time": round(time.time() - start, 2)
        }
        log.error(f"❌ {name} - ERROR: {e}")


def main():
    log.info("="*60")
    log.info("Luna Badge v1.3.0 稳固性测试")
    log.info("目标：零误差，所有测试必须通过")
    log.info("="*60")
    log.info(f"\n开始时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 运行所有测试
    for name, command in TESTS:
        run_test(name, command)
    
    # 生成报告
    log.info("\n" + "=" * 60)
    log.info("测试总结")
    log.info("="*60")
    
    passed = sum(1 for r in RESULT.values() if r.get("success"))
    total = len(RESULT)
    failed = total - passed
    
    for name, r in RESULT.items():
        status = "✅ PASS" if r.get("success") else "❌ FAIL"
        time_str = f"({r.get('time', 0)}s)" if 'time' in r else ""
        log.info(f"{status} {name} {time_str}")
    
    log.error(f"\n总计: {passed}/{total} 通过, {failed} 失败")
    
    # 保存报告
    report_path = Path("test_reports/test_all_report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "total": total,
            "passed": passed,
            "failed": failed,
            "results": RESULT
        }, f, indent=2, ensure_ascii=False)
    
    log.info(f"\n报告已保存: {report_path}")
    
    # 判断是否全部通过
    if failed == 0:
        log.info("\n" + "=" * 60)
        log.error("✅ ALL TESTS PASSED. ZERO ERRORS.")
        log.info("="*60")
        sys.exit(0)
    else:
        log.info("\n" + "=" * 60)
        log.error(f"❌ ERROR: {failed} test(s) failed.")
        log.info("="*60")
        sys.exit(1)


if __name__ == "__main__":
    main()








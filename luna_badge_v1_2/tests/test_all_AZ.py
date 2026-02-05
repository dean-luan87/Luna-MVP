from core.logging import get_logger

#!/usr/bin/env python3
log = get_logger("test_all_AZ")
"""
Luna Badge v1.3.0 A-Z 单元测试运行器
运行所有模块的单元测试并生成汇总报告
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

REPORT_DIR = Path("test_reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# 定义所有测试模块
TEST_MODULES = [
    "test_brightness_detector",
    "test_detection",
    "test_frame_scheduler",
    "test_fusion",
    "test_grid_slicer",
    "test_hazard_detector",
    "test_image_corrector",
    "test_nav_decision",
    "test_nav_speech",
    "test_navigation",
    "test_navigation_pipeline",
    "test_navigation_task",
    "test_path_detector",
    "test_tile_enhancer",
    "test_nav_monitor",  # 新增的 NAV_STUCK 监控测试
]

def run_test_module(module_name: str) -> Dict[str, Any]:
    """运行单个测试模块"""
    log.info(f"\n[测试] {module_name}...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", f"tests/{module_name}.py", "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=300,
        )
        passed = result.returncode == 0
        output = result.stdout + result.stderr
        
        return {
            "module": module_name,
            "passed": passed,
            "output": output,
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {
            "module": module_name,
            "passed": False,
            "output": "测试超时（>300秒）",
            "returncode": -1,
        }
    except Exception as e:
        return {
            "module": module_name,
            "passed": False,
            "output": f"执行异常: {str(e)}",
            "returncode": -1,
        }

def main():
    log.info("=" * 60")
    log.info("Luna Badge v1.3.0 - A-Z 单元测试")
    log.info("=" * 60")
    
    results = []
    total = len(TEST_MODULES)
    passed_count = 0
    
    for module in TEST_MODULES:
        result = run_test_module(module)
        results.append(result)
        if result["passed"]:
            passed_count += 1
            log.info(f"  ✅ {module} - 通过")
        else:
            log.info(f"  ❌ {module} - 失败")
    
    # 生成汇总报告
    summary = {
        "timestamp": datetime.now().isoformat(),
        "total": total,
        "passed": passed_count,
        "failed": total - passed_count,
        "pass_rate": 100.0 * passed_count / total if total > 0 else 0.0,
        "results": results,
    }
    
    # 保存报告
    summary_path = REPORT_DIR / "summary.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    log.info("\n" + "=" * 60)
    log.info(f"测试完成: {passed_count}/{total} 通过 ({summary['pass_rate']:.1f}%)")
    log.info(f"报告已保存: {summary_path}")
    log.info("=" * 60")
    
    return 0 if passed_count == total else 1

if __name__ == "__main__":
    sys.exit(main())



















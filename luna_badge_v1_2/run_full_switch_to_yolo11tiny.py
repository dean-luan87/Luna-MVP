from core.logging import get_logger

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
log = get_logger("run_full_switch_to_yolo11tiny")
"""
一键切换 YOLO11-tiny 并完成全套回归测试

功能：
1. 切换主模型到 YOLO11-tiny
2. 运行全链路 Benchmark
3. 运行 YOLO 模型对比测试
4. 运行压力测试
5. 运行单元测试
6. 生成最终综合性能报告
"""

import json
import subprocess
import time
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# 项目根目录
ROOT_DIR = Path(__file__).parent
os.chdir(ROOT_DIR)

# 备份文件路径
BACKUP_DIR = ROOT_DIR / "backups"
BACKUP_DIR.mkdir(exist_ok=True)


def backup_file(file_path: Path):
    """备份文件"""
    if file_path.exists():
        backup_path = BACKUP_DIR / f"{file_path.name}.{int(time.time())}.bak"
        shutil.copy2(file_path, backup_path)
        log.info(f"  ✅ 已备份: {backup_path}")
        return backup_path
    return None


def apply_model_switch():
    """切换主模型到 YOLO11-tiny"""
    log.info("\n" + "=" * 70)
    log.info(">>> [1/6] 切换主模型到 YOLO11-tiny")
    log.info("=" * 70")
    
    # 1. 修改配置文件
    config_path = ROOT_DIR / "config" / "model_config.yaml"
    if not config_path.exists():
        # 尝试其他路径
        config_path = ROOT_DIR / "config" / "model_config.yaml"
        if not config_path.exists():
            log.info(f"  ⚠️  配置文件不存在: {config_path}")
            log.info("  📝 将直接修改代码中的模型配置")
            return
    
    backup_file(config_path)
    
    with open(config_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 替换模型名称
    original_content = content
    content = content.replace('model_name: "yolo11n"', 'model_name: "yolo11-tiny"')
    content = content.replace('model_name: "yolov8n"', 'model_name: "yolo11-tiny"')
    content = content.replace('model_name: "yolov8"', 'model_name: "yolo11-tiny"')
    
    if content != original_content:
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(content)
        log.info(f"  ✅ 已修改配置文件: {config_path}")
    else:
        log.info(f"  ℹ️  配置文件未找到需要修改的内容，可能已经是 yolo11-tiny")
    
    # 2. 检查并修改代码中的硬编码模型路径
    code_files = [
        ROOT_DIR / "core" / "vision" / "detector.py",
        ROOT_DIR / "core" / "yolo_detector.py",
        ROOT_DIR / "core" / "vision" / "model_loader.py",
    ]
    
    for code_file in code_files:
        if code_file.exists():
            backup_file(code_file)
            with open(code_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            original_content = content
            # 替换常见的模型路径
            content = content.replace('"yolov8n.pt"', '"yolo11-tiny.pt"')
            content = content.replace("'yolov8n.pt'", "'yolo11-tiny.pt'")
            content = content.replace('"yolov8n"', '"yolo11-tiny"')
            content = content.replace("'yolov8n'", "'yolo11-tiny'")
            content = content.replace('"yolo11n"', '"yolo11-tiny"')
            content = content.replace("'yolo11n'", "'yolo11-tiny'")
            
            if content != original_content:
                with open(code_file, "w", encoding="utf-8") as f:
                    f.write(content)
                log.info(f"  ✅ 已修改代码文件: {code_file}")
    
    log.info("  ✅ 模型切换完成")


def run_tests():
    """运行所有测试"""
    log.info("\n" + "=" * 70)
    log.info(">>> [2/6] 运行全链路 Benchmark")
    log.info("=" * 70")
    
    try:
        subprocess.run(
            ["python3", "benchmarks/benchmark_full_realtime.py", "--runs", "10", "--target", "250.0"],
            check=True,
            cwd=ROOT_DIR
        )
        log.info("  ✅ 全链路 Benchmark 完成")
    except subprocess.CalledProcessError as e:
        log.info(f"  ⚠️  全链路 Benchmark 失败: {e}")
    except FileNotFoundError:
        log.info("  ⚠️  全链路 Benchmark 脚本不存在，跳过")
    
    log.info("\n" + "=" * 70)
    log.info(">>> [3/6] 运行 YOLO 模型对比测试")
    log.info("=" * 70")
    
    try:
        subprocess.run(
            ["python3", "benchmarks/benchmark_yolo_models.py"],
            check=True,
            cwd=ROOT_DIR
        )
        log.info("  ✅ YOLO 模型对比测试完成")
    except subprocess.CalledProcessError as e:
        log.info(f"  ⚠️  YOLO 模型对比测试失败: {e}")
    except FileNotFoundError:
        log.info("  ⚠️  YOLO 模型对比测试脚本不存在，跳过")
    
    log.info("\n" + "=" * 70)
    log.info(">>> [4/6] 运行压力测试（60秒 × 并发4）")
    log.info("=" * 70")
    
    try:
        subprocess.run(
            ["python3", "benchmarks/stress_full_realtime.py", "--duration", "60", "--concurrency", "4", "--target", "250.0"],
            check=True,
            cwd=ROOT_DIR
        )
        log.info("  ✅ 压力测试完成")
    except subprocess.CalledProcessError as e:
        log.info(f"  ⚠️  压力测试失败: {e}")
    except FileNotFoundError:
        log.info("  ⚠️  压力测试脚本不存在，跳过")
    
    log.info("\n" + "=" * 70)
    log.info(">>> [5/6] 运行单元测试")
    log.info("=" * 70")
    
    try:
        result = subprocess.run(
            ["python3", "-m", "pytest", "tests/", "-q", "--tb=short"],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            log.info("  ✅ 单元测试全部通过")
        else:
            log.info(f"  ⚠️  部分单元测试失败")
            log.info("result.stdout")
            log.info("result.stderr")
    except FileNotFoundError:
        log.info("  ⚠️  pytest 未安装或测试目录不存在，跳过")
    
    log.info("\n  ✅ 所有测试任务已执行完成")


def generate_final_report():
    """生成最终综合性能报告"""
    log.info("\n" + "=" * 70)
    log.info(">>> [6/6] 汇总所有测试结果")
    log.info("=" * 70")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "model": "yolo11-tiny",
        "version": "1.3.0",
        "tests": {}
    }
    
    # 读取 benchmark 报告
    benchmark_path = ROOT_DIR / "test_reports" / "benchmark_full_realtime_report.json"
    if benchmark_path.exists():
        try:
            with open(benchmark_path, "r", encoding="utf-8") as f:
                report["tests"]["benchmark"] = json.load(f)
            log.info("  ✅ 已读取全链路 Benchmark 报告")
        except Exception as e:
            log.info(f"  ⚠️  读取 Benchmark 报告失败: {e}")
    
    # 读取压测报告
    stress_path = ROOT_DIR / "test_reports" / "stress_full_realtime_report.json"
    if stress_path.exists():
        try:
            with open(stress_path, "r", encoding="utf-8") as f:
                report["tests"]["stress"] = json.load(f)
            log.info("  ✅ 已读取压力测试报告")
        except Exception as e:
            log.info(f"  ⚠️  读取压力测试报告失败: {e}")
    
    # 读取 YOLO 对比报告
    yolo_bench_path = ROOT_DIR / "perf_logs" / "yolo_model_benchmark.json"
    if yolo_bench_path.exists():
        try:
            with open(yolo_bench_path, "r", encoding="utf-8") as f:
                report["tests"]["yolo_compare"] = json.load(f)
            log.info("  ✅ 已读取 YOLO 模型对比报告")
        except Exception as e:
            log.info(f"  ⚠️  读取 YOLO 对比报告失败: {e}")
    
    # 输出总报告文件
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = ROOT_DIR / "perf_logs" / f"final_report_yolo11tiny_{ts}.json"
    
    os.makedirs(out_path.parent, exist_ok=True)
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    log.info(f"\n  ✅ 最终总报告已生成: {out_path}")
    
    # 打印摘要
    log.info("\n" + "=" * 70)
    log.info("📊 测试结果摘要")
    log.info("=" * 70")
    
    if "benchmark" in report["tests"]:
        bench = report["tests"]["benchmark"]
        log.info(f"全链路 Benchmark:")
        log.info(f"  成功率: {bench.get('success', 0)}/{bench.get('runs', 0)}")
        log.info(f"  平均延迟: {bench.get('avg_total_ms', 0):.2f}ms")
    
    if "stress" in report["tests"]:
        stress = report["tests"]["stress"]
        log.info(f"压力测试:")
        log.info(f"  总请求数: {stress.get('total_runs', 0)}")
        log.error(f"  错误率: {stress.get('error_rate', 0):.2f}%")
        log.info(f"  平均延迟: {stress.get('avg_ms', 0):.2f}ms")
        log.info(f"  P99延迟: {stress.get('p99_ms', 0):.2f}ms")
    
    if "yolo_compare" in report["tests"]:
        yolo = report["tests"]["yolo_compare"]
        if "models" in yolo:
            log.info(f"YOLO 模型对比:")
            for model in yolo["models"]:
                if model.get("model") == "yolov11-tiny":
                    log.info(f"  yolo11-tiny:")
                    log.info(f"    平均延迟: {model.get('avg', 0)*1000:.3f}ms")
                    log.info(f"    P95延迟: {model.get('p95', 0)*1000:.3f}ms")
    
    log.info("=" * 70")


def main():
    """主函数"""
    log.info("\n" + "=" * 70)
    log.info("🚀 YOLO11-tiny 切换 + 全套回归测试")
    log.info("=" * 70")
    log.info(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log.info(f"工作目录: {ROOT_DIR}")
    
    try:
        # 1. 切换模型
        apply_model_switch()
        
        # 2. 运行测试
        run_tests()
        
        # 3. 生成报告
        generate_final_report()
        
        log.info("\n" + "=" * 70)
        log.info("✅ YOLO11-tiny 切换 + 全套测试完成！")
        log.info("=" * 70")
        log.info(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        log.info("\n📁 备份文件位置: backups/")
        log.info("📊 测试报告位置: perf_logs/ 和 test_reports/")
        
    except KeyboardInterrupt:
        log.info("\n\n⚠️  用户中断测试")
        sys.exit(1)
    except Exception as e:
        log.info(f"\n\n❌ 执行过程中出现错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()



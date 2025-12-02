#!/usr/bin/env python3
"""
Luna Badge v1.3.0 压力测试运行器
在指定时间内持续运行测试，收集性能指标和错误率
"""

import json
import time
import argparse
import threading
import subprocess
import sys
import psutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

REPORT_DIR = Path("test_reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

class StressTestRunner:
    def __init__(self, duration_sec: int = 60, threads: int = 2):
        self.duration_sec = duration_sec
        self.threads = threads
        self.start_time = None
        self.end_time = None
        self.errors = []
        self.test_count = 0
        self.success_count = 0
        self.cpu_samples = []
        self.mem_samples = []
        self.running = False
        
    def collect_system_metrics(self):
        """收集系统指标（CPU/MEM）"""
        while self.running:
            try:
                cpu = psutil.cpu_percent(interval=1.0)
                mem = psutil.virtual_memory().percent
                self.cpu_samples.append(cpu)
                self.mem_samples.append(mem)
            except Exception:
                pass
            time.sleep(5)
    
    def run_test_loop(self, thread_id: int):
        """单个线程的测试循环"""
        test_modules = [
            "test_navigation",
            "test_detection",
            "test_fusion",
            "test_path_detector",
        ]
        
        while self.running:
            for module in test_modules:
                if not self.running:
                    break
                    
                try:
                    result = subprocess.run(
                        [sys.executable, "-m", "pytest", f"tests/{module}.py", "-v", "--tb=line"],
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )
                    self.test_count += 1
                    if result.returncode == 0:
                        self.success_count += 1
                    else:
                        # 同时捕获 stdout 和 stderr，因为 pytest 可能将错误输出到 stdout
                        error_msg = (result.stderr or result.stdout or "")[:500]
                        if not error_msg.strip():
                            error_msg = f"Return code: {result.returncode}, no error message captured"
                        self.errors.append({
                            "thread": thread_id,
                            "module": module,
                            "error": error_msg,
                            "returncode": result.returncode,
                            "timestamp": time.time(),
                        })
                except Exception as e:
                    self.errors.append({
                        "thread": thread_id,
                        "module": module,
                        "error": str(e),
                        "timestamp": time.time(),
                    })
                time.sleep(1)
    
    def run(self):
        """执行压力测试"""
        print(f"开始压力测试: {self.duration_sec}秒, {self.threads}线程")
        self.running = True
        self.start_time = time.time()
        
        # 启动系统指标收集线程
        metrics_thread = threading.Thread(target=self.collect_system_metrics, daemon=True)
        metrics_thread.start()
        
        # 启动测试线程
        test_threads = []
        for i in range(self.threads):
            t = threading.Thread(target=self.run_test_loop, args=(i,), daemon=True)
            t.start()
            test_threads.append(t)
        
        # 等待指定时间
        time.sleep(self.duration_sec)
        
        # 停止测试
        self.running = False
        self.end_time = time.time()
        
        # 等待线程结束
        for t in test_threads:
            t.join(timeout=5)
        metrics_thread.join(timeout=5)
        
        # 生成报告
        return self.generate_report()
    
    def generate_report(self) -> Dict[str, Any]:
        """生成压力测试报告"""
        elapsed = self.end_time - self.start_time
        error_rate = 100.0 * len(self.errors) / self.test_count if self.test_count > 0 else 0.0
        success_rate = 100.0 * self.success_count / self.test_count if self.test_count > 0 else 0.0
        
        avg_cpu = sum(self.cpu_samples) / len(self.cpu_samples) if self.cpu_samples else 0.0
        avg_mem = sum(self.mem_samples) / len(self.mem_samples) if self.mem_samples else 0.0
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "duration_sec": elapsed,
            "threads": self.threads,
            "test_count": self.test_count,
            "success_count": self.success_count,
            "error_count": len(self.errors),
            "error_rate": error_rate,
            "success_rate": success_rate,
            "cpu_usage": round(avg_cpu, 2),
            "mem_usage": round(avg_mem, 2),
            "errors": self.errors[:50],  # 只保留前50个错误
        }
        
        report_path = REPORT_DIR / "stress_report.json"
        with report_path.open("w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n压力测试完成:")
        print(f"  测试次数: {self.test_count}")
        print(f"  成功: {self.success_count}")
        print(f"  错误: {len(self.errors)}")
        print(f"  错误率: {error_rate:.2f}%")
        print(f"  平均CPU: {avg_cpu:.1f}%")
        print(f"  平均内存: {avg_mem:.1f}%")
        print(f"  报告已保存: {report_path}")
        
        return report

def main():
    parser = argparse.ArgumentParser(description="Luna Badge 压力测试")
    parser.add_argument("--duration", type=int, default=60, help="测试持续时间（秒）")
    parser.add_argument("--threads", type=int, default=2, help="并发线程数")
    
    args = parser.parse_args()
    
    runner = StressTestRunner(duration_sec=args.duration, threads=args.threads)
    runner.run()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())


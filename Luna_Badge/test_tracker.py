#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Luna Badge 测试追踪报告生成器
实时追踪模块触发、日志记录、错误定位
"""

import logging
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class ModuleTrigger:
    """模块触发记录"""
    module_name: str
    triggered: bool
    timestamp: str
    duration_ms: float = 0.0
    error: Optional[str] = None
    metadata: Dict[str, Any] = None


@dataclass
class TestStep:
    """测试步骤记录"""
    step_id: str
    step_type: str  # "voice", "vision", "ocr", "simulate"
    input_data: str
    expected_modules: List[str]
    triggered_modules: List[ModuleTrigger] = None
    actual_output: str = ""
    expected_output: str = ""
    status: str = "PENDING"  # "PENDING", "RUNNING", "PASS", "FAIL", "SKIP"
    errors: List[str] = None
    warnings: List[str] = None


@dataclass
class TestCase:
    """测试用例记录"""
    case_id: str
    case_name: str
    scenario: str
    steps: List[TestStep] = None
    status: str = "PENDING"
    start_time: str = ""
    end_time: str = ""
    duration_ms: float = 0.0
    modules_coverage: Dict[str, bool] = None  # {module: triggered}
    issues: List[Dict] = None


@dataclass
class TestReport:
    """测试报告"""
    report_id: str
    test_suite: str
    start_time: str
    end_time: str
    duration_seconds: float
    
    total_cases: int = 0
    passed_cases: int = 0
    failed_cases: int = 0
    skipped_cases: int = 0
    
    cases: List[TestCase] = None
    summary: Dict[str, Any] = None
    issues_summary: Dict[str, Any] = None


class TestTracker:
    """测试追踪器"""
    
    def __init__(self, report_name: str = "luna_badge_test"):
        """初始化追踪器"""
        self.report_name = report_name
        self.current_case: Optional[TestCase] = None
        self.current_step: Optional[TestStep] = None
        self.report: Optional[TestReport] = None
        
        # 模块注册表
        self.module_registry = {
            "Whisper": False,
            "YOLO": False,
            "OCR": False,
            "Navigator": False,
            "TTS": False,
            "Memory": False,
            "LogManager": False,
            "ContextStore": False,
            "TaskInterruptor": False,
            "RetryQueue": False,
            "Vision": False,
            "Camera": False
        }
        
        # 创建报告目录
        self.report_dir = Path("test_reports")
        self.report_dir.mkdir(exist_ok=True)
        
        logger.info("📊 测试追踪器初始化完成")
    
    def start_report(self, test_suite: str = "real_scenarios"):
        """开始报告"""
        report_id = f"{test_suite}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.report = TestReport(
            report_id=report_id,
            test_suite=test_suite,
            start_time=datetime.now().isoformat(),
            end_time="",
            duration_seconds=0.0,
            cases=[],
            summary={},
            issues_summary={}
        )
        
        logger.info(f"📝 测试报告开始: {report_id}")
    
    def start_case(self, case_id: str, case_name: str, scenario: str):
        """开始用例"""
        self.current_case = TestCase(
            case_id=case_id,
            case_name=case_name,
            scenario=scenario,
            steps=[],
            start_time=datetime.now().isoformat(),
            modules_coverage={},
            issues=[]
        )
        
        # 重置模块注册表
        for module in self.module_registry:
            self.module_registry[module] = False
        
        logger.info(f"🧪 开始用例: {case_id} - {case_name}")
    
    def start_step(self, step_id: str, step_type: str, input_data: str, 
                   expected_modules: List[str], expected_output: str = ""):
        """开始步骤"""
        if not self.current_case:
            logger.error("❌ 没有激活的测试用例")
            return
        
        self.current_step = TestStep(
            step_id=step_id,
            step_type=step_type,
            input_data=input_data,
            expected_modules=expected_modules,
            expected_output=expected_output,
            triggered_modules=[],
            errors=[],
            warnings=[]
        )
        
        self.current_step.status = "RUNNING"
        logger.info(f"   ▶️ 步骤 {step_id}: {step_type} - {input_data}")
    
    def record_module_trigger(self, module_name: str, success: bool = True, 
                             error: str = None, duration_ms: float = 0.0):
        """记录模块触发"""
        if not self.current_step:
            logger.warning(f"⚠️ 没有激活的测试步骤，模块触发: {module_name}")
            return
        
        # 记录触发
        trigger = ModuleTrigger(
            module_name=module_name,
            triggered=success,
            timestamp=datetime.now().isoformat(),
            duration_ms=duration_ms,
            error=error
        )
        
        self.current_step.triggered_modules.append(trigger)
        
        # 更新模块注册表
        if module_name in self.module_registry:
            self.module_registry[module_name] = success
        
        # 更新用例模块覆盖
        if self.current_case:
            self.current_case.modules_coverage[module_name] = success
        
        logger.info(f"      {'✅' if success else '❌'} 模块触发: {module_name}" + (f" - {error}" if error else ""))
    
    def record_step_output(self, actual_output: str):
        """记录步骤输出"""
        if not self.current_step:
            return
        
        self.current_step.actual_output = actual_output
    
    def complete_step(self, status: str = "PASS"):
        """完成步骤"""
        if not self.current_step:
            return
        
        self.current_step.status = status
        
        # 检查缺失模块
        for module in self.current_step.expected_modules:
            if module not in [m.module_name for m in self.current_step.triggered_modules if m.triggered]:
                if module in self.module_registry:
                    if not self.module_registry[module]:
                        self.current_step.warnings.append(f"模块未触发: {module}")
        
        logger.info(f"   ✅ 步骤完成: {status}")
    
    def complete_case(self, status: str = "PASS"):
        """完成用例"""
        if not self.current_case:
            return
        
        self.current_case.status = status
        self.current_case.end_time = datetime.now().isoformat()
        
        # 计算耗时
        start = datetime.fromisoformat(self.current_case.start_time)
        end = datetime.fromisoformat(self.current_case.end_time)
        self.current_case.duration_ms = (end - start).total_seconds() * 1000
        
        # 检查问题
        self._analyze_case_issues()
        
        # 添加到报告
        if self.report:
            self.report.cases.append(self.current_case)
            self.report.total_cases += 1
            if status == "PASS":
                self.report.passed_cases += 1
            elif status == "FAIL":
                self.report.failed_cases += 1
            else:
                self.report.skipped_cases += 1
        
        logger.info(f"🧪 用例完成: {self.current_case.case_id} - {status}")
        
        self.current_case = None
    
    def _analyze_case_issues(self):
        """分析用例问题"""
        if not self.current_case:
            return
        
        # 检查缺失模块
        missing_modules = []
        for module, triggered in self.current_case.modules_coverage.items():
            if not triggered and module in self.current_case.steps[0].expected_modules if self.current_case.steps else []:
                missing_modules.append(module)
        
        if missing_modules:
            self.current_case.issues.append({
                "type": "missing_modules",
                "modules": missing_modules,
                "severity": "high"
            })
        
        # 检查错误
        for step in self.current_case.steps:
            if step.errors:
                self.current_case.issues.append({
                    "type": "step_errors",
                    "step_id": step.step_id,
                    "errors": step.errors,
                    "severity": "high"
                })
    
    def complete_report(self):
        """完成报告"""
        if not self.report:
            return
        
        self.report.end_time = datetime.now().isoformat()
        
        # 计算耗时
        start = datetime.fromisoformat(self.report.start_time)
        end = datetime.fromisoformat(self.report.end_time)
        self.report.duration_seconds = (end - start).total_seconds()
        
        # 生成摘要
        self._generate_summary()
        
        # 生成问题摘要
        self._generate_issues_summary()
        
        # 保存报告
        self._save_report()
        
        # 打印报告
        self._print_report()
        
        logger.info(f"📊 测试报告完成: {self.report.report_id}")
    
    def _generate_summary(self):
        """生成摘要"""
        if not self.report:
            return
        
        success_rate = 0.0
        if self.report.total_cases > 0:
            success_rate = (self.report.passed_cases / self.report.total_cases) * 100
        
        self.report.summary = {
            "total_cases": self.report.total_cases,
            "passed": self.report.passed_cases,
            "failed": self.report.failed_cases,
            "skipped": self.report.skipped_cases,
            "success_rate": success_rate,
            "duration_seconds": self.report.duration_seconds,
            "avg_case_time_ms": 0.0
        }
        
        if self.report.total_cases > 0:
            total_time = sum(case.duration_ms for case in self.report.cases)
            self.report.summary["avg_case_time_ms"] = total_time / self.report.total_cases
    
    def _generate_issues_summary(self):
        """生成问题摘要"""
        if not self.report:
            return
        
        issues_count = {}
        missing_modules_count = {}
        
        for case in self.report.cases:
            for issue in case.issues:
                issue_type = issue.get("type", "unknown")
                issues_count[issue_type] = issues_count.get(issue_type, 0) + 1
                
                if issue_type == "missing_modules":
                    for module in issue.get("modules", []):
                        missing_modules_count[module] = missing_modules_count.get(module, 0) + 1
        
        self.report.issues_summary = {
            "total_issues": sum(issues_count.values()),
            "issues_by_type": issues_count,
            "missing_modules_count": missing_modules_count
        }
    
    def _save_report(self):
        """保存报告"""
        if not self.report:
            return
        
        report_path = self.report_dir / f"{self.report.report_id}.json"
        
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(asdict(self.report), f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 报告已保存: {report_path}")
        
        # 同时保存Markdown版本
        self._save_markdown_report(report_path.with_suffix(".md"))
    
    def _save_markdown_report(self, report_path: Path):
        """保存Markdown报告"""
        if not self.report:
            return
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"# Luna Badge 测试报告: {self.report.report_id}\n\n")
            f.write(f"**测试套件:** {self.report.test_suite}\n\n")
            f.write(f"**执行时间:** {self.report.start_time} ~ {self.report.end_time}\n\n")
            f.write(f"**总耗时:** {self.report.duration_seconds:.2f}秒\n\n")
            
            f.write("---\n\n")
            
            # 摘要
            if self.report.summary:
                f.write("## 📊 测试摘要\n\n")
                f.write(f"- 总用例数: {self.report.summary['total_cases']}\n")
                f.write(f"- ✅ 通过: {self.report.summary['passed']}\n")
                f.write(f"- ❌ 失败: {self.report.summary['failed']}\n")
                f.write(f"- ⏭️  跳过: {self.report.summary['skipped']}\n")
                f.write(f"- 📈 成功率: {self.report.summary['success_rate']:.1f}%\n")
                f.write(f"- ⏱️  平均耗时: {self.report.summary['avg_case_time_ms']:.2f}ms\n\n")
            
            # 问题摘要
            if self.report.issues_summary and self.report.issues_summary['total_issues'] > 0:
                f.write("## 🐛 问题摘要\n\n")
                f.write(f"总问题数: {self.report.issues_summary['total_issues']}\n\n")
                
                if self.report.issues_summary['issues_by_type']:
                    f.write("### 问题类型分布\n\n")
                    for issue_type, count in self.report.issues_summary['issues_by_type'].items():
                        f.write(f"- {issue_type}: {count}\n")
                    f.write("\n")
                
                if self.report.issues_summary['missing_modules_count']:
                    f.write("### 缺失模块统计\n\n")
                    for module, count in sorted(self.report.issues_summary['missing_modules_count'].items(), key=lambda x: x[1], reverse=True):
                        f.write(f"- {module}: {count}次\n")
                    f.write("\n")
            
            # 详细结果
            f.write("## 📋 详细结果\n\n")
            f.write("| 用例ID | 场景 | 状态 | 耗时 | 模块覆盖 | 问题数 |\n")
            f.write("|-------|------|------|------|---------|--------|\n")
            
            for case in self.report.cases:
                modules_cover = f"{sum(case.modules_coverage.values())}/{len(case.modules_coverage)}"
                issues_count = len(case.issues)
                status_emoji = {"PASS": "✅", "FAIL": "❌", "SKIP": "⏭️"}
                emoji = status_emoji.get(case.status, "❓")
                
                f.write(f"| {case.case_id} | {case.scenario} | {emoji} {case.status} | {case.duration_ms:.0f}ms | {modules_cover} | {issues_count} |\n")
            
            f.write("\n")
            
            # 问题详情
            for case in self.report.cases:
                if case.issues:
                    f.write(f"### {case.case_id}: {case.case_name}\n\n")
                    for issue in case.issues:
                        f.write(f"**问题类型:** {issue['type']}\n\n")
                        if 'modules' in issue:
                            f.write(f"**缺失模块:** {', '.join(issue['modules'])}\n\n")
                        if 'errors' in issue:
                            f.write(f"**错误:** {', '.join(issue['errors'])}\n\n")
                        f.write("---\n\n")
        
        logger.info(f"📄 Markdown报告已保存: {report_path}")
    
    def _print_report(self):
        """打印报告"""
        if not self.report:
            return
        
        print("\n" + "=" * 70)
        print("📊 测试报告摘要")
        print("=" * 70)
        
        if self.report.summary:
            print(f"总用例数: {self.report.summary['total_cases']}")
            print(f"✅ 通过: {self.report.summary['passed']}")
            print(f"❌ 失败: {self.report.summary['failed']}")
            print(f"⏭️  跳过: {self.report.summary['skipped']}")
            print(f"📈 成功率: {self.report.summary['success_rate']:.1f}%")
            print(f"⏱️  总耗时: {self.report.duration_seconds:.2f}秒")
        
        if self.report.issues_summary and self.report.issues_summary['total_issues'] > 0:
            print("\n" + "-" * 70)
            print("🐛 问题摘要")
            print("-" * 70)
            print(f"总问题数: {self.report.issues_summary['total_issues']}")
            
            if self.report.issues_summary['missing_modules_count']:
                print("\n缺失模块:")
                for module, count in sorted(self.report.issues_summary['missing_modules_count'].items(), key=lambda x: x[1], reverse=True):
                    print(f"  - {module}: {count}次")
        
        print("\n" + "=" * 70)
    
    def get_tracker_summary(self) -> Dict[str, Any]:
        """获取追踪摘要"""
        if not self.report:
            return {}
        
        return {
            "report_id": self.report.report_id,
            "status": "completed",
            "summary": self.report.summary,
            "issues": self.report.issues_summary
        }


# 全局追踪器实例
_tracker = None


def get_tracker() -> TestTracker:
    """获取全局追踪器"""
    global _tracker
    if _tracker is None:
        _tracker = TestTracker()
    return _tracker


def init_tracker(report_name: str = "luna_badge_test") -> TestTracker:
    """初始化追踪器"""
    global _tracker
    _tracker = TestTracker(report_name=report_name)
    _tracker.start_report()
    return _tracker


if __name__ == "__main__":
    # 示例使用
    tracker = init_tracker()
    
    # 模拟测试用例
    tracker.start_case("A1", "初次到医院寻找挂号", "医院就诊")
    
    tracker.start_step("step1", "voice", "我要挂号", ["Whisper", "Navigator", "TTS"])
    tracker.record_module_trigger("Whisper", success=True)
    tracker.record_module_trigger("Navigator", success=True)
    tracker.record_module_trigger("TTS", success=True)
    tracker.complete_step("PASS")
    
    tracker.complete_case("PASS")
    
    tracker.complete_report()


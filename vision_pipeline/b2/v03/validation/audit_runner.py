# vision_pipeline/b2/v03/validation/audit_runner.py
"""
B2 v0.5 Audit Runner
自动化验收脚本运行器
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Tuple
from collections import defaultdict

# 导入所有规则模块
try:
    from vision_pipeline.b2.v03.validation.rules.s1_gate import get_all_gate_rules
    from vision_pipeline.b2.v03.validation.rules.s2_evidence import get_all_evidence_rules, check_s2_evidence_003
    from vision_pipeline.b2.v03.validation.rules.s3_trigger import get_all_trigger_rules
    from vision_pipeline.b2.v03.validation.rules.s4_impact import get_all_impact_rules
    from vision_pipeline.b2.v03.validation.rules.s5_b2c import get_all_b2c_rules
    from vision_pipeline.b2.v03.validation.rules.s6_trace import check_s6_trace_001, check_s6_timeline_001
    from vision_pipeline.b2.v03.validation.rules.s7_web import get_all_web_rules
    from vision_pipeline.b2.v03.validation.rules.global_rules import get_all_global_rules
except ImportError:
    # 如果导入失败，尝试相对导入
    import sys
    from pathlib import Path
    rules_dir = Path(__file__).parent / "rules"
    sys.path.insert(0, str(rules_dir.parent))
    
    from rules.s1_gate import get_all_gate_rules
    from rules.s2_evidence import get_all_evidence_rules, check_s2_evidence_003
    from rules.s3_trigger import get_all_trigger_rules
    from rules.s4_impact import get_all_impact_rules
    from rules.s5_b2c import get_all_b2c_rules
    from rules.s6_trace import check_s6_trace_001, check_s6_timeline_001
    from rules.s7_web import get_all_web_rules
    from rules.global_rules import get_all_global_rules


class AuditRunner:
    """Audit Runner 主类"""
    
    def __init__(self):
        self.results: List[Dict[str, Any]] = []
        self.stats = {
            "total_checks": 0,
            "passed": 0,
            "failed": 0,
            "warnings": 0
        }
    
    def run(self, trace_path: str, timeline_path: str = None, total_frames: int = None):
        """
        运行所有验收规则
        
        :param trace_path: Trace 文件路径（jsonl）
        :param timeline_path: Timeline 文件路径（可选）
        :param total_frames: 总帧数（可选，用于 S6.TRACE.001）
        """
        print("=" * 70)
        print("B2 v0.5 自动化验收")
        print("=" * 70)
        print(f"Trace 文件: {trace_path}")
        if timeline_path:
            print(f"Timeline 文件: {timeline_path}")
        print()
        
        # 读取 traces
        traces = self._load_traces(trace_path)
        if not traces:
            print("❌ 无法加载 traces")
            return False
        
        print(f"加载了 {len(traces)} 条 trace 记录\n")
        
        # 读取 timeline（如果有）
        timeline = None
        if timeline_path and Path(timeline_path).exists():
            timeline = self._load_timeline(timeline_path)
            if timeline:
                print(f"加载了 {len(timeline)} 条 timeline 记录\n")
        
        # 运行所有规则
        self._run_all_rules(traces, timeline, total_frames)
        
        # 生成报告
        self._print_report()
        
        # 保存报告
        self._save_report()
        
        return self.stats["failed"] == 0
    
    def _load_traces(self, trace_path: str) -> List[Dict[str, Any]]:
        """加载 trace 文件"""
        traces = []
        try:
            with open(trace_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        traces.append(json.loads(line))
            return traces
        except Exception as e:
            print(f"❌ 加载 trace 文件失败: {e}")
            return []
    
    def _load_timeline(self, timeline_path: str) -> List[Dict[str, Any]]:
        """加载 timeline 文件"""
        timeline = []
        try:
            with open(timeline_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        timeline.append(json.loads(line))
            return timeline
        except Exception as e:
            print(f"⚠️  加载 timeline 文件失败: {e}")
            return []
    
    def _run_all_rules(self, traces: List[Dict[str, Any]], timeline: List[Dict[str, Any]] = None, total_frames: int = None):
        """运行所有规则"""
        print("运行验收规则...\n")
        
        # Step 1: Gate
        print("Step 1: Gate")
        for rule_func in get_all_gate_rules():
            self._run_rule_on_traces(rule_func, traces, "S1.GATE")
        
        # Step 2: Evidence
        print("\nStep 2: Evidence")
        for rule_func in get_all_evidence_rules():
            self._run_rule_on_traces(rule_func, traces, "S2.EVIDENCE")
        
        # Evidence 003 需要前一帧
        for i in range(1, len(traces)):
            status, message, evidence = check_s2_evidence_003(traces[i], i, traces[i-1])
            self._record_result("S2.EVIDENCE.003", status, message, evidence, i)
        
        # Step 3: Trigger
        print("\nStep 3: Trigger")
        for rule_func in get_all_trigger_rules():
            self._run_rule_on_traces(rule_func, traces, "S3.TRIGGER")
        
        # Step 4: Impact
        print("\nStep 4: Impact")
        for rule_func in get_all_impact_rules():
            self._run_rule_on_traces(rule_func, traces, "S4.IMPACT")
        
        # Step 5: B → C
        print("\nStep 5: B → C")
        for rule_func in get_all_b2c_rules():
            self._run_rule_on_traces(rule_func, traces, "S5.B2C")
        
        # Step 6: Trace / Timeline
        print("\nStep 6: Trace / Timeline")
        if total_frames is not None:
            status, message, evidence = check_s6_trace_001(traces, total_frames)
            self._record_result("S6.TRACE.001", status, message, evidence)
        
        if timeline:
            status, message, evidence = check_s6_timeline_001(timeline)
            self._record_result("S6.TIMELINE.001", status, message, evidence)
        
        # Step 7: Web
        print("\nStep 7: Web")
        for rule_func in get_all_web_rules():
            self._run_rule_on_traces(rule_func, traces, "S7.WEB")
        
        # Global Rules
        print("\nGlobal Rules")
        for rule_func in get_all_global_rules():
            self._run_rule_on_traces(rule_func, traces, "G.FAIL")
    
    def _run_rule_on_traces(self, rule_func, traces: List[Dict[str, Any]], rule_prefix: str):
        """在 traces 上运行单个规则"""
        rule_name = rule_func.__name__
        for i, trace in enumerate(traces):
            try:
                status, message, evidence = rule_func(trace, i)
                rule_id = f"{rule_prefix}.{rule_name.split('_')[-1]}"
                self._record_result(rule_id, status, message, evidence, i)
            except Exception as e:
                self._record_result(
                    rule_name,
                    "FAIL",
                    f"规则执行异常: {e}",
                    {"trace_id": i, "error": str(e)},
                    i
                )
    
    def _record_result(self, rule_id: str, status: str, message: str, evidence: Dict[str, Any], trace_id: int = None):
        """记录验收结果"""
        result = {
            "rule_id": rule_id,
            "status": status,
            "message": message,
            "evidence": evidence
        }
        if trace_id is not None:
            result["evidence"]["trace_id"] = trace_id
        
        self.results.append(result)
        self.stats["total_checks"] += 1
        
        if status == "PASS":
            self.stats["passed"] += 1
        elif status == "FAIL":
            self.stats["failed"] += 1
            print(f"  ❌ {rule_id}: {message}")
        elif status == "WARN":
            self.stats["warnings"] += 1
            print(f"  ⚠️  {rule_id}: {message}")
    
    def _print_report(self):
        """打印验收报告"""
        print("\n" + "=" * 70)
        print("验收报告")
        print("=" * 70)
        print(f"总检查项: {self.stats['total_checks']}")
        print(f"✅ 通过: {self.stats['passed']}")
        print(f"⚠️  警告: {self.stats['warnings']}")
        print(f"❌ 失败: {self.stats['failed']}")
        print("=" * 70)
        
        if self.stats['failed'] > 0:
            print("\n失败项详情:")
            for result in self.results:
                if result["status"] == "FAIL":
                    print(f"  {result['rule_id']}: {result['message']}")
                    print(f"    证据: {result['evidence']}")
        
        if self.stats['warnings'] > 0:
            print("\n警告项详情:")
            for result in self.results:
                if result["status"] == "WARN":
                    print(f"  {result['rule_id']}: {result['message']}")
    
    def _save_report(self):
        """保存验收报告到 JSON"""
        report = {
            "stats": self.stats,
            "results": self.results
        }
        
        report_path = "b2_audit_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n报告已保存到: {report_path}")


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python audit_runner.py <trace_path> [timeline_path] [total_frames]")
        print("示例: python audit_runner.py traces/b2_runtime_trace_v05.jsonl")
        sys.exit(1)
    
    trace_path = sys.argv[1]
    timeline_path = sys.argv[2] if len(sys.argv) > 2 else None
    total_frames = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    runner = AuditRunner()
    success = runner.run(trace_path, timeline_path, total_frames)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

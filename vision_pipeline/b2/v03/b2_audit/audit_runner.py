# vision_pipeline/b2/v03/b2_audit/audit_runner.py
"""
B2 v0.5 Audit Runner（主入口）
"""

import sys
import os
from pathlib import Path

# 添加当前目录到路径（支持相对导入）
sys.path.insert(0, os.path.dirname(__file__))

from context import AuditContext
from report import AuditReport

# 导入所有规则
from rules.g_failfast import WorldSemanticLeakRule
from rules.s1_gate import (
    GateMustExistRule,
    GateModeValidityRule,
    GateBlockConsistencyRule,
    GateDetailsCompletenessRule
)
from rules.s2_evidence import (
    NoInstantEvidenceRule,
    EvidenceStateValidityRule
)
from rules.s3_trigger import (
    TriggerMustExistRule,
    GateControlsTriggerRule
)
from rules.s4_impact import (
    ImpactEnumValidityRule,
    EnvNoDirectImpactRule,
    ForceAlertThresholdRule
)
from rules.s5_b2c import (
    NoOpNoCommunicationRule,
    ForceAlertCanInterruptRule
)
from rules.s6_trace import TimelineNoNoOpRule
from rules.bc_boundary_rules import get_all_boundary_rules


# 所有规则（按优先级排序：全局规则在前）
RULES = [
    # 全局规则（Fail Fast）
    WorldSemanticLeakRule(),
    
    # Step 1: Gate
    GateMustExistRule(),
    GateModeValidityRule(),
    GateBlockConsistencyRule(),
    GateDetailsCompletenessRule(),
    
    # Step 2: Evidence
    NoInstantEvidenceRule(),
    EvidenceStateValidityRule(),
    
    # Step 3: Trigger
    TriggerMustExistRule(),
    GateControlsTriggerRule(),
    
    # Step 4: Impact
    ImpactEnumValidityRule(),
    EnvNoDirectImpactRule(),
    ForceAlertThresholdRule(),
    
    # Step 5: B → C
    NoOpNoCommunicationRule(),
    ForceAlertCanInterruptRule(),
    
    # Step 6: Trace
    TimelineNoNoOpRule(),
    
    # B/C Boundary Rules (7 assumptions)
] + get_all_boundary_rules()


def run_audit(trace_path: str, timeline_path: str = None) -> AuditReport:
    """
    运行所有验收规则
    
    :param trace_path: Trace 文件路径
    :param timeline_path: Timeline 文件路径（可选）
    :return: AuditReport 对象
    """
    print("=" * 70)
    print("B2 v0.5 自动化验收")
    print("=" * 70)
    print(f"Trace 文件: {trace_path}")
    if timeline_path:
        print(f"Timeline 文件: {timeline_path}")
    print()
    
    # 加载上下文
    ctx = AuditContext(trace_path, timeline_path)
    
    if not ctx.traces:
        print("❌ 无法加载 traces")
        sys.exit(1)
    
    print(f"加载了 {len(ctx.traces)} 条 trace 记录")
    if ctx.timeline:
        print(f"加载了 {len(ctx.timeline)} 条 timeline 记录")
    print()
    
    # 运行所有规则
    report = AuditReport()
    
    print("运行验收规则...\n")
    for rule in RULES:
        try:
            result = rule.check(ctx)
            if result:
                report.add_result(result)
                # Fail Fast：全局规则失败直接停止
                if rule.rule_id.startswith("G.FAIL") and result.get("status") == "FAIL":
                    print(f"⚠️  全局规则失败，停止后续检查: {rule.rule_id}")
                    break
        except Exception as e:
            report.add_result({
                "rule_id": rule.rule_id,
                "status": "FAIL",
                "message": f"规则执行异常: {e}",
                "evidence": {"error": str(e)}
            })
    
    # 生成报告
    report.print_report()
    
    # 保存 JSON 报告
    report_path = report.save_json()
    print(f"报告已保存到: {report_path}\n")
    
    return report


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python audit_runner.py <trace_path> [timeline_path]")
        print("示例: python audit_runner.py traces/b2_runtime_trace_v05.jsonl")
        sys.exit(1)
    
    trace_path = sys.argv[1]
    timeline_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    report = run_audit(trace_path, timeline_path)
    
    sys.exit(0 if not report.has_failures() else 1)


if __name__ == "__main__":
    main()

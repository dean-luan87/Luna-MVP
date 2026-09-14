# vision_pipeline/b2/v03/b2_audit/dcs_runner.py
"""
DCS Runner - 集成 Audit Runner 和 DCS Scorer
"""

import sys
import json
import os
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from context import AuditContext
from audit_runner import run_audit
from dcs_scorer import DCSScorer


def run_dcs(trace_path: str, timeline_path: str = None, manual_scores: dict = None):
    """
    运行 DCS 评分
    
    :param trace_path: Trace 文件路径
    :param timeline_path: Timeline 文件路径（可选）
    :param manual_scores: 人工评分（可选），格式：{"gate": 20, "evidence": 12, ...}
    :return: DCS 评分结果
    """
    print("=" * 70)
    print("B2 v0.5 设计一致性评分（DCS）")
    print("=" * 70)
    
    # 1. 加载上下文
    ctx = AuditContext(trace_path, timeline_path)
    
    # 2. 运行自动化验收
    print("\n步骤 1: 运行自动化验收规则...")
    from audit_runner import RULES
    from report import AuditReport
    
    audit_report = AuditReport()
    for rule in RULES:
        try:
            result = rule.check(ctx)
            if result:
                audit_report.add_result(result)
                # Fail Fast：全局规则失败直接停止
                if rule.rule_id.startswith("G.FAIL") and result.get("status") == "FAIL":
                    print(f"⚠️  全局规则失败，停止后续检查: {rule.rule_id}")
                    break
        except Exception as e:
            audit_report.add_result({
                "rule_id": rule.rule_id,
                "status": "FAIL",
                "message": f"规则执行异常: {e}",
                "evidence": {"error": str(e)}
            })
    
    # 3. 计算 DCS
    print("\n步骤 2: 计算设计一致性评分...")
    scorer = DCSScorer(ctx, audit_report)
    result = scorer.calculate(manual_scores)
    
    # 4. 打印报告
    scorer.print_report(result)
    
    # 5. 保存 JSON 报告
    report_path = "b2_dcs_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"DCS 报告已保存到: {report_path}\n")
    
    return result


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python dcs_runner.py <trace_path> [timeline_path] [manual_scores_json]")
        print("示例: python dcs_runner.py traces/b2_runtime_trace_v05.jsonl")
        print("示例: python dcs_runner.py traces/b2_runtime_trace_v05.jsonl timeline.jsonl '{\"gate\": 20, \"evidence\": 12}'")
        sys.exit(1)
    
    trace_path = sys.argv[1]
    timeline_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # 解析人工评分（如果有）
    manual_scores = None
    if len(sys.argv) > 3:
        try:
            manual_scores = json.loads(sys.argv[3])
        except:
            print("⚠️  人工评分 JSON 解析失败，忽略")
    
    result = run_dcs(trace_path, timeline_path, manual_scores)
    
    # 根据等级退出
    grade = result["grade"]
    if grade == "ROLLBACK":
        sys.exit(2)  # 严重违规
    elif grade == "FAIL":
        sys.exit(1)  # 未通过
    else:
        sys.exit(0)  # 通过


if __name__ == "__main__":
    main()

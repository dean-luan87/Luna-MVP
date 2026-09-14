# vision_pipeline/b2/v03/b2_audit/dcs_history_judge.py
"""
DCS 历史审判工具
用 DCS 回头"审判" v0.1–v0.3 的历史 trace
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from collections import defaultdict

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from context import AuditContext
from dcs_scorer import DCSScorer
from audit_runner import RULES, AuditReport


class DCSHistoryJudge:
    """DCS 历史审判器"""
    
    def __init__(self):
        self.judgment_results = []
    
    def judge_version(self, version: str, trace_path: str, timeline_path: str = None) -> Dict[str, Any]:
        """
        审判单个版本
        
        :param version: 版本号（如 "v0.1", "v0.2"）
        :param trace_path: Trace 文件路径
        :param timeline_path: Timeline 文件路径（可选）
        :return: 审判结果
        """
        print(f"\n{'=' * 70}")
        print(f"审判版本: {version}")
        print(f"{'=' * 70}")
        
        # 加载上下文
        ctx = AuditContext(trace_path, timeline_path)
        if not ctx.traces:
            print(f"❌ 无法加载 traces: {trace_path}")
            return None
        
        print(f"加载了 {len(ctx.traces)} 条 trace 记录")
        
        # 运行自动化验收
        audit_report = AuditReport()
        for rule in RULES:
            try:
                result = rule.check(ctx)
                if result:
                    audit_report.add_result(result)
                    if rule.rule_id.startswith("G.FAIL") and result.get("status") == "FAIL":
                        break
            except Exception as e:
                audit_report.add_result({
                    "rule_id": rule.rule_id,
                    "status": "FAIL",
                    "message": f"规则执行异常: {e}",
                    "evidence": {"error": str(e)}
                })
        
        # 计算 DCS
        scorer = DCSScorer(ctx, audit_report)
        dcs_result = scorer.calculate()
        
        # 分析错误类型分布
        error_distribution = self._analyze_error_distribution(audit_report, ctx)
        
        judgment = {
            "version": version,
            "dcs_score": dcs_result["design_consistency_score"],
            "dcs_grade": dcs_result["grade"],
            "breakdown": dcs_result["breakdown"],
            "fatal_violations": dcs_result["fatal_violations"],
            "warnings": dcs_result["warnings"],
            "error_distribution": error_distribution,
            "trace_count": len(ctx.traces),
            "audit_stats": {
                "total_checks": audit_report.stats["total_checks"],
                "passed": audit_report.stats["passed"],
                "failed": audit_report.stats["failed"],
                "warned": audit_report.stats["warned"]
            }
        }
        
        self.judgment_results.append(judgment)
        
        # 打印结果
        self._print_judgment(judgment)
        
        return judgment
    
    def _analyze_error_distribution(self, audit_report: AuditReport, ctx: AuditContext) -> Dict[str, float]:
        """分析错误类型分布"""
        error_types = defaultdict(int)
        total_errors = 0
        
        # 统计各类错误
        for failure in audit_report.failures:
            rule_id = failure.get("rule_id", "")
            message = failure.get("message", "")
            
            # 分类错误
            if "GATE" in rule_id and "trigger" in message.lower():
                error_types["无 Gate 情况下 Trigger"] += 1
                total_errors += 1
            elif "WORLD" in message or "SCENE" in message:
                error_types["世界描述型 decision"] += 1
                total_errors += 1
            elif "NO_OP" in message and "timeline" in message.lower():
                error_types["NO_OP 污染 timeline"] += 1
                total_errors += 1
            elif "trace" in message.lower() and ("缺失" in message or "缺少" in message):
                error_types["不可追溯"] += 1
                total_errors += 1
            else:
                error_types["其他"] += 1
                total_errors += 1
        
        # 计算百分比
        distribution = {}
        for error_type, count in error_types.items():
            distribution[error_type] = round((count / total_errors * 100) if total_errors > 0 else 0, 1)
        
        return distribution
    
    def _print_judgment(self, judgment: Dict[str, Any]):
        """打印审判结果"""
        version = judgment["version"]
        score = judgment["dcs_score"]
        grade = judgment["dcs_grade"]
        
        # 确定状态 emoji
        if score >= 90:
            emoji = "🟢"
        elif score >= 85:
            emoji = "🟡"
        elif score >= 70:
            emoji = "🟠"
        else:
            emoji = "🔴"
        
        print(f"\n{version} | DCS: {score} {emoji}")
        print(f"等级: {grade}")
        
        breakdown = judgment["breakdown"]
        print(f"\n维度得分:")
        for dim, score in breakdown.items():
            print(f"  {dim:12s}: {score:3d}")
        
        # 错误类型分布
        if judgment["error_distribution"]:
            print(f"\n错误类型分布:")
            for error_type, percentage in judgment["error_distribution"].items():
                print(f"  - {percentage:5.1f}%: {error_type}")
        
        # 关键发现
        print(f"\n关键发现:")
        if breakdown.get("gate", 25) == 0:
            print(f"  ❌ 当时根本没有 Gate，系统是'盲的'")
        if breakdown.get("trace", 15) < 10:
            print(f"  ❌ Trace 可追溯性严重不足")
        if judgment["fatal_violations"]:
            print(f"  ❌ 发现 {len(judgment['fatal_violations'])} 个致命违规")
    
    def compare_versions(self, version_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        对比多个版本
        
        :param version_results: 版本审判结果列表
        :return: 对比结果
        """
        print(f"\n{'=' * 70}")
        print("跨版本对比")
        print(f"{'=' * 70}")
        
        comparison = {
            "versions": [],
            "dcs_trend": [],
            "dimension_trends": defaultdict(list),
            "maturity_analysis": {}
        }
        
        for result in version_results:
            version = result["version"]
            score = result["dcs_score"]
            
            comparison["versions"].append(version)
            comparison["dcs_trend"].append({
                "version": version,
                "score": score,
                "grade": result["dcs_grade"]
            })
            
            # 维度趋势
            for dim, score in result["breakdown"].items():
                comparison["dimension_trends"][dim].append({
                    "version": version,
                    "score": score
                })
        
        # 成熟度分析
        if len(version_results) >= 2:
            first_score = version_results[0]["dcs_score"]
            last_score = version_results[-1]["dcs_score"]
            improvement = last_score - first_score
            
            comparison["maturity_analysis"] = {
                "first_version": version_results[0]["version"],
                "last_version": version_results[-1]["version"],
                "first_score": first_score,
                "last_score": last_score,
                "improvement": improvement,
                "interpretation": self._interpret_maturity(improvement)
            }
        
        # 打印对比
        self._print_comparison(comparison)
        
        return comparison
    
    def _interpret_maturity(self, improvement: float) -> str:
        """解释成熟度变化"""
        if improvement >= 30:
            return "这不是性能提升，这是'人格成熟度'提升"
        elif improvement >= 15:
            return "设计一致性显著改善"
        elif improvement >= 0:
            return "设计一致性略有改善"
        else:
            return "设计一致性下降，需要关注"
    
    def _print_comparison(self, comparison: Dict[str, Any]):
        """打印对比结果"""
        print(f"\n版本对比:")
        for trend in comparison["dcs_trend"]:
            version = trend["version"]
            score = trend["score"]
            grade = trend["grade"]
            
            if score >= 90:
                emoji = "🟢"
            elif score >= 85:
                emoji = "🟡"
            elif score >= 70:
                emoji = "🟠"
            else:
                emoji = "🔴"
            
            print(f"  {version}: DCS {score} {emoji} ({grade})")
        
        if comparison["maturity_analysis"]:
            analysis = comparison["maturity_analysis"]
            print(f"\n成熟度分析:")
            print(f"  {analysis['first_version']} → {analysis['last_version']}")
            print(f"  {analysis['first_score']} → {analysis['last_score']} (提升 {analysis['improvement']:.1f} 分)")
            print(f"  {analysis['interpretation']}")
    
    def save_judgment_report(self, output_path: str = "b2_dcs_history_judgment.json"):
        """保存审判报告"""
        report = {
            "judgments": self.judgment_results,
            "summary": {
                "total_versions": len(self.judgment_results),
                "average_dcs": sum(j["dcs_score"] for j in self.judgment_results) / len(self.judgment_results) if self.judgment_results else 0
            }
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return output_path


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法: python dcs_history_judge.py <version> <trace_path> [timeline_path]")
        print("示例: python dcs_history_judge.py v0.1 traces/v0.1_trace.jsonl")
        print("\n或者对比多个版本:")
        print("  python dcs_history_judge.py compare v0.1:traces/v0.1.jsonl v0.2:traces/v0.2.jsonl v0.3:traces/v0.3.jsonl")
        sys.exit(1)
    
    judge = DCSHistoryJudge()
    
    if sys.argv[1] == "compare":
        # 对比模式
        version_results = []
        for arg in sys.argv[2:]:
            if ":" in arg:
                version, trace_path = arg.split(":", 1)
                result = judge.judge_version(version, trace_path)
                if result:
                    version_results.append(result)
        
        if version_results:
            comparison = judge.compare_versions(version_results)
            judge.save_judgment_report()
    else:
        # 单版本模式
        version = sys.argv[1]
        trace_path = sys.argv[2]
        timeline_path = sys.argv[3] if len(sys.argv) > 3 else None
        
        judge.judge_version(version, trace_path, timeline_path)
        judge.save_judgment_report()


if __name__ == "__main__":
    main()

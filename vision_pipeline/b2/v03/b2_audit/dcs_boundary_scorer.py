# vision_pipeline/b2/v03/b2_audit/dcs_boundary_scorer.py
"""
DCS Boundary Scorer
Maps 7 boundary assumptions to DCS scoring with penalties
"""

from typing import Dict, Any, List
from collections import defaultdict
from context import AuditContext
from report import AuditReport


class DCSBoundaryScorer:
    """DCS 边界评分器"""
    
    # 初始分数
    INITIAL_SCORE = 100
    
    # 扣分等级
    PENALTIES = {
        "LOW": -5,
        "MEDIUM": -10,
        "HIGH": -25,
        "CRITICAL": -50
    }
    
    # 阈值
    THRESHOLDS = {
        "healthy": 85,
        "warning": 70,
        "broken": 0
    }
    
    # 规则映射（7 条裁定 → DCS 规则）
    RULE_MAPPING = {
        "R1": {
            "dimension": "frequency_alignment",
            "penalty": "HIGH",
            "description": "Frequency Mismatch Is Intentional"
        },
        "R2": {
            "dimension": "role_boundary",
            "penalty": "HIGH",
            "description": "B Is System-Awakened, Not Self-Driven"
        },
        "R3": {
            "dimension": "decision_semantics",
            "penalty": "CRITICAL",
            "description": "B Never Confirms Risk, Only Signals It"
        },
        "R4": {
            "dimension": "evolution_direction",
            "penalty": "LOW",
            "description": "Conservative C Is Acceptable"
        },
        "R5": {
            "dimension": "silence_validity",
            "penalty": "MEDIUM",
            "description": "Silence Requires No Immediate Explanation"
        },
        "R6": {
            "dimension": "time_consistency",
            "penalty": "CRITICAL",
            "description": "System Time Is the Only Time"
        },
        "R7": {
            "dimension": "evolution_direction",
            "penalty": "HIGH",
            "description": "B and C Evolve Orthogonally"
        }
    }
    
    def __init__(self, ctx: AuditContext, audit_report: AuditReport):
        """
        初始化边界评分器
        
        :param ctx: AuditContext 对象
        :param audit_report: AuditReport 对象（包含边界规则检查结果）
        """
        self.ctx = ctx
        self.audit_report = audit_report
        self.violations = defaultdict(list)
        self.dimension_scores = {}
    
    def calculate(self) -> Dict[str, Any]:
        """
        计算边界 DCS 分数
        
        :return: 边界 DCS 评分结果
        """
        score = self.INITIAL_SCORE
        
        # 收集边界规则违规
        for failure in self.audit_report.failures:
            rule_id = failure.get("rule_id", "")
            if rule_id.startswith("R"):
                self.violations[rule_id].append(failure)
        
        # 计算各维度分数
        for rule_id, rule_info in self.RULE_MAPPING.items():
            dimension = rule_info["dimension"]
            penalty_level = rule_info["penalty"]
            penalty = self.PENALTIES[penalty_level]
            
            # 计算该维度的扣分
            violation_count = len(self.violations.get(rule_id, []))
            if violation_count > 0:
                dimension_penalty = penalty * min(violation_count, 5)  # 最多扣 5 次
                score += dimension_penalty
                
                self.dimension_scores[dimension] = {
                    "violations": violation_count,
                    "penalty": dimension_penalty,
                    "rule_id": rule_id
                }
            else:
                self.dimension_scores[dimension] = {
                    "violations": 0,
                    "penalty": 0,
                    "rule_id": rule_id
                }
        
        # 确定等级
        if score >= self.THRESHOLDS["healthy"]:
            grade = "HEALTHY"
        elif score >= self.THRESHOLDS["warning"]:
            grade = "WARNING"
        else:
            grade = "BROKEN"
        
        return {
            "boundary_dcs_score": max(0, score),
            "initial_score": self.INITIAL_SCORE,
            "grade": grade,
            "dimensions": dict(self.dimension_scores),
            "violations": {
                rule_id: len(violations)
                for rule_id, violations in self.violations.items()
            },
            "thresholds": self.THRESHOLDS,
            "penalties": self.PENALTIES
        }
    
    def print_report(self, result: Dict[str, Any]):
        """打印边界 DCS 报告"""
        print("\n" + "=" * 70)
        print("B/C Boundary DCS Report")
        print("=" * 70)
        
        score = result["boundary_dcs_score"]
        grade = result["grade"]
        
        print(f"\n边界 DCS 分数: {score} / {result['initial_score']}")
        print(f"等级: {grade}")
        
        print("\n" + "-" * 70)
        print("维度得分:")
        print("-" * 70)
        for dim, info in result["dimensions"].items():
            violations = info["violations"]
            penalty = info["penalty"]
            rule_id = info["rule_id"]
            rule_desc = self.RULE_MAPPING[rule_id]["description"]
            
            if violations > 0:
                print(f"  {dim:20s} {rule_id}: {violations} 违规, 扣分 {penalty}")
                print(f"    {rule_desc}")
            else:
                print(f"  {dim:20s} {rule_id}: ✅ 无违规")
        
        if result["violations"]:
            print("\n" + "-" * 70)
            print("违规汇总:")
            print("-" * 70)
            for rule_id, count in result["violations"].items():
                rule_desc = self.RULE_MAPPING[rule_id]["description"]
                penalty_level = self.RULE_MAPPING[rule_id]["penalty"]
                print(f"  {rule_id}: {count} 次违规 ({penalty_level} 级别)")
                print(f"    {rule_desc}")
        
        print("\n" + "=" * 70)
        if grade == "HEALTHY":
            print("✅ 边界一致性检查通过")
        elif grade == "WARNING":
            print("⚠️  边界一致性警告")
        else:
            print("❌ 边界一致性严重违规")
        print("=" * 70 + "\n")

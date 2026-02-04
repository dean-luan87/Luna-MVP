# vision_pipeline/b2/v03/b2_audit/dcs_scorer.py
"""
设计一致性评分（Design Consistency Score, DCS）
融合自动化规则（A）和人工检查（B）
"""

from typing import Dict, Any, List, Optional
from collections import defaultdict
from context import AuditContext
from report import AuditReport


class DCSScorer:
    """设计一致性评分器"""
    
    # 维度分值
    DIMENSION_WEIGHTS = {
        "gate": 25,
        "evidence": 15,
        "trigger": 15,
        "impact": 20,
        "trace": 15,
        "timeline": 10
    }
    
    # 及格线和强制回滚线
    PASS_THRESHOLD = 85
    ROLLBACK_THRESHOLD = 70
    
    def __init__(self, ctx: AuditContext, audit_report: AuditReport):
        """
        初始化 DCS 评分器
        
        :param ctx: AuditContext 对象
        :param audit_report: AuditReport 对象（包含所有规则检查结果）
        """
        self.ctx = ctx
        self.audit_report = audit_report
        self.breakdown = defaultdict(int)
        self.fatal_violations = []
        self.warnings = []
        
        # 初始化各维度满分
        for dim, weight in self.DIMENSION_WEIGHTS.items():
            self.breakdown[dim] = weight
    
    def calculate(self, manual_scores: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
        """
        计算 DCS 总分
        
        :param manual_scores: 人工评分（可选），格式：{"gate": 20, "evidence": 12, ...}
        :return: DCS 评分结果
        """
        # 1. Gate 合规性（25 分）
        self._score_gate()
        
        # 2. Evidence 生命周期（15 分）
        self._score_evidence()
        
        # 3. Trigger 正当性（15 分）
        self._score_trigger()
        
        # 4. Impact & 干预边界（20 分）
        self._score_impact()
        
        # 5. Trace & 可追溯性（15 分）
        self._score_trace()
        
        # 6. Timeline 克制性（10 分）
        self._score_timeline()
        
        # 应用人工评分（如果有）
        if manual_scores:
            self._apply_manual_scores(manual_scores)
        
        # 计算总分
        total_score = sum(self.breakdown.values())
        
        # 确定等级
        if total_score < self.ROLLBACK_THRESHOLD:
            grade = "ROLLBACK"
        elif total_score < self.PASS_THRESHOLD:
            grade = "FAIL"
        else:
            grade = "PASS"
        
        return {
            "design_consistency_score": total_score,
            "grade": grade,
            "breakdown": dict(self.breakdown),
            "fatal_violations": self.fatal_violations,
            "warnings": self.warnings,
            "thresholds": {
                "pass": self.PASS_THRESHOLD,
                "rollback": self.ROLLBACK_THRESHOLD
            }
        }
    
    def _score_gate(self):
        """Gate 合规性评分（25 分）"""
        score = 25
        
        # 检查自动化规则失败
        for failure in self.audit_report.failures:
            rule_id = failure.get("rule_id", "")
            
            # Gate fail 时仍然 trigger → -25（直接 0 分）
            if rule_id == "S1.GATE.003":
                score = 0
                self.fatal_violations.append({
                    "rule": rule_id,
                    "message": "Gate 挂起但仍触发/通信",
                    "penalty": -25
                })
                break
            
            # Gate 状态未写入 trace → -10
            if rule_id == "S1.GATE.001":
                score -= 10
                self.warnings.append("Gate 状态未写入 trace")
        
        # Gate Mode 合法性
        for failure in self.audit_report.failures:
            if failure.get("rule_id") == "S1.GATE.002":
                score -= 5
                self.warnings.append("Gate Mode 非法值")
                break
        
        self.breakdown["gate"] = max(0, score)
    
    def _score_evidence(self):
        """Evidence 生命周期评分（15 分）"""
        score = 15
        
        # 单帧 CONFIRMED → -10
        for failure in self.audit_report.failures:
            if failure.get("rule_id") == "S2.EVIDENCE.001":
                score -= 10
                self.warnings.append("发现瞬时证据（单帧 CONFIRMED）")
                break
        
        # 检查是否有 DEGRADED / DROPPED 逻辑
        has_lifecycle = False
        for trace in self.ctx.traces:
            evidence_state = trace.get("evidence_state", {})
            for factor_key, evidence in evidence_state.items():
                if isinstance(evidence, dict):
                    state = evidence.get("state")
                    if state in ("DEGRADED", "DROPPED"):
                        has_lifecycle = True
                        break
                if has_lifecycle:
                    break
        
        if not has_lifecycle:
            score -= 5
            self.warnings.append("Evidence DEGRADED/DROPPED 逻辑覆盖率偏低")
        
        self.breakdown["evidence"] = max(0, score)
    
    def _score_trigger(self):
        """Trigger 正当性评分（15 分）"""
        score = 15
        
        # Trigger 但 impact = NO_OP → -15
        trigger_no_op_count = 0
        for trace in self.ctx.traces:
            trigger = trace.get("trigger", {})
            impact_eval = trace.get("impact_eval", {})
            impact = impact_eval.get("impact", "NO_OP")
            
            if trigger.get("triggered") and impact == "NO_OP":
                trigger_no_op_count += 1
        
        if trigger_no_op_count > 0:
            score -= 15
            self.warnings.append(f"发现 {trigger_no_op_count} 次 Trigger 但 impact = NO_OP")
        
        # 连续 trigger 无冷却 → -5
        consecutive_triggers = 0
        max_consecutive = 0
        for trace in self.ctx.traces:
            if trace.get("trigger", {}).get("triggered"):
                consecutive_triggers += 1
                max_consecutive = max(max_consecutive, consecutive_triggers)
            else:
                consecutive_triggers = 0
        
        if max_consecutive > 3:
            score -= 5
            self.warnings.append(f"连续 trigger 无冷却（最多 {max_consecutive} 次）")
        
        self.breakdown["trigger"] = max(0, score)
    
    def _score_impact(self):
        """Impact & 干预边界评分（20 分）"""
        score = 20
        
        # 出现非标准 Impact 枚举 → -20
        for failure in self.audit_report.failures:
            if failure.get("rule_id") == "S4.IMPACT.001":
                score = 0
                self.fatal_violations.append({
                    "rule": "S4.IMPACT.001",
                    "message": "出现非标准 Impact 枚举",
                    "penalty": -20
                })
                break
        
        # ENV 禁止直接影响
        for failure in self.audit_report.failures:
            if failure.get("rule_id") == "S4.IMPACT.002":
                score -= 10
                self.warnings.append("ENV 因子直接产生 impact")
                break
        
        # FORCE_ALERT 权限约束
        for failure in self.audit_report.failures:
            if failure.get("rule_id") == "S4.IMPACT.003":
                score -= 10
                self.warnings.append("FORCE_ALERT 置信度不足")
                break
        
        self.breakdown["impact"] = max(0, score)
    
    def _score_trace(self):
        """Trace & 可追溯性评分（15 分）"""
        score = 15
        
        # 缺少 Gate / Trigger / Impact 任一 → -10
        missing_fields = set()
        for trace in self.ctx.traces[:100]:  # 检查前 100 条
            if "gate_eval" not in trace:
                missing_fields.add("gate_eval")
            if "trigger" not in trace:
                missing_fields.add("trigger")
            if "impact_eval" not in trace:
                missing_fields.add("impact_eval")
        
        if missing_fields:
            score -= 10
            self.warnings.append(f"Trace 缺少字段: {missing_fields}")
        
        # NO_OP 无 reason → -5
        no_op_without_reason = 0
        for trace in self.ctx.traces:
            impact_eval = trace.get("impact_eval", {})
            impact = impact_eval.get("impact", "NO_OP")
            
            if impact == "NO_OP":
                reason = impact_eval.get("reason")
                if not reason:
                    no_op_without_reason += 1
        
        if no_op_without_reason > len(self.ctx.traces) * 0.1:  # 超过 10%
            score -= 5
            self.warnings.append(f"NO_OP 无 reason 比例过高: {no_op_without_reason}/{len(self.ctx.traces)}")
        
        self.breakdown["trace"] = max(0, score)
    
    def _score_timeline(self):
        """Timeline 克制性评分（10 分）"""
        score = 10
        
        # NO_OP 写入 timeline → -10
        for failure in self.audit_report.failures:
            if failure.get("rule_id") == "S6.TIMELINE.001":
                score = 0
                self.warnings.append("Timeline 中发现 NO_OP 条目")
                break
        
        # 高频重复同类事件 → -5
        if self.ctx.timeline:
            event_counts = defaultdict(int)
            for entry in self.ctx.timeline:
                impact = entry.get("impact") or entry.get("impact_eval", {}).get("impact")
                if impact:
                    event_counts[impact] += 1
            
            # 如果某个事件类型超过总数的 30%
            total = len(self.ctx.timeline)
            for event_type, count in event_counts.items():
                if count > total * 0.3 and event_type != "NO_OP":
                    score -= 5
                    self.warnings.append(f"高频重复事件: {event_type} ({count}/{total})")
                    break
        
        self.breakdown["timeline"] = max(0, score)
    
    def _apply_manual_scores(self, manual_scores: Dict[str, int]):
        """
        应用人工评分
        
        :param manual_scores: 人工评分，格式：{"gate": 20, "evidence": 12, ...}
        """
        for dim, manual_score in manual_scores.items():
            if dim in self.breakdown:
                # 人工评分覆盖自动化评分（但不超过满分）
                max_score = self.DIMENSION_WEIGHTS.get(dim, 0)
                self.breakdown[dim] = min(manual_score, max_score)
    
    def print_report(self, result: Dict[str, Any]):
        """打印 DCS 报告"""
        print("\n" + "=" * 70)
        print("设计一致性评分（Design Consistency Score, DCS）")
        print("=" * 70)
        
        score = result["design_consistency_score"]
        grade = result["grade"]
        
        # 使用颜色标记（如果支持）
        if grade == "PASS":
            grade_mark = "✅ PASS"
        elif grade == "FAIL":
            grade_mark = "⚠️  FAIL"
        else:
            grade_mark = "❌ ROLLBACK"
        
        print(f"\n总分: {score} / 100")
        print(f"等级: {grade_mark}")
        print(f"及格线: {result['thresholds']['pass']} 分")
        print(f"强制回滚线: {result['thresholds']['rollback']} 分")
        
        print("\n" + "-" * 70)
        print("维度得分:")
        print("-" * 70)
        for dim, weight in self.DIMENSION_WEIGHTS.items():
            actual_score = result["breakdown"][dim]
            percentage = (actual_score / weight) * 100
            bar = "█" * int(percentage / 5) + "░" * (20 - int(percentage / 5))
            print(f"  {dim:12s} {actual_score:3d} / {weight:3d}  [{bar}] {percentage:.0f}%")
        
        if result["fatal_violations"]:
            print("\n" + "-" * 70)
            print("致命违规:")
            print("-" * 70)
            for violation in result["fatal_violations"]:
                print(f"  ❌ {violation.get('rule')}: {violation.get('message')}")
                print(f"     扣分: {violation.get('penalty')}")
        
        if result["warnings"]:
            print("\n" + "-" * 70)
            print("警告:")
            print("-" * 70)
            for warning in result["warnings"][:10]:  # 只显示前 10 个
                print(f"  ⚠️  {warning}")
        
        print("\n" + "=" * 70)
        if grade == "PASS":
            print("✅ 设计一致性检查通过")
        elif grade == "FAIL":
            print("⚠️  设计一致性检查未通过，需要修复")
        else:
            print("❌ 设计一致性严重违规，建议回滚")
        print("=" * 70 + "\n")

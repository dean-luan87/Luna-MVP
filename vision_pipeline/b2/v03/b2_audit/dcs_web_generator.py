# vision_pipeline/b2/v03/b2_audit/dcs_web_generator.py
"""
DCS Web 可视化数据生成器
将 DCS 评分结果转换为 Web 仪表盘所需的数据格式
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from context import AuditContext
from dcs_scorer import DCSScorer
from audit_runner import RULES, AuditReport


class DCSWebGenerator:
    """DCS Web 数据生成器"""
    
    # 评分等级映射
    GRADE_MAP = {
        "EXCELLENT": {"color": "green", "emoji": "🟢", "min_score": 90},
        "PASS": {"color": "yellow", "emoji": "🟡", "min_score": 85},
        "WARNING": {"color": "orange", "emoji": "🟠", "min_score": 70},
        "FAIL": {"color": "red", "emoji": "🔴", "min_score": 0}
    }
    
    def __init__(self, ctx: AuditContext, dcs_result: Dict[str, Any], audit_report: AuditReport):
        """
        初始化生成器
        
        :param ctx: AuditContext 对象
        :param dcs_result: DCS 评分结果
        :param audit_report: AuditReport 对象
        """
        self.ctx = ctx
        self.dcs_result = dcs_result
        self.audit_report = audit_report
    
    def generate(self) -> Dict[str, Any]:
        """生成 Web 可视化数据"""
        return {
            "dcs_summary": self._generate_summary(),
            "dimensions": self._generate_dimensions(),
            "violations_timeline": self._generate_violations_timeline(),
            "metadata": self._generate_metadata()
        }
    
    def _generate_summary(self) -> Dict[str, Any]:
        """生成顶部摘要"""
        score = self.dcs_result["design_consistency_score"]
        grade = self._get_grade(score)
        grade_info = self.GRADE_MAP[grade]
        
        return {
            "score": score,
            "grade": grade,
            "status_color": grade_info["color"],
            "status_emoji": grade_info["emoji"],
            "fatal_violations_count": len(self.dcs_result["fatal_violations"]),
            "warnings_count": len(self.dcs_result["warnings"]),
            "thresholds": self.dcs_result["thresholds"]
        }
    
    def _get_grade(self, score: float) -> str:
        """根据分数确定等级"""
        if score >= 90:
            return "EXCELLENT"
        elif score >= 85:
            return "PASS"
        elif score >= 70:
            return "WARNING"
        else:
            return "FAIL"
    
    def _generate_dimensions(self) -> Dict[str, Any]:
        """生成维度得分"""
        breakdown = self.dcs_result["breakdown"]
        weights = DCSScorer.DIMENSION_WEIGHTS
        
        dimensions = {}
        for dim, weight in weights.items():
            score = breakdown.get(dim, 0)
            percentage = (score / weight) * 100 if weight > 0 else 0
            
            # 收集扣分项
            deductions = self._get_deductions_for_dimension(dim)
            
            dimensions[dim] = {
                "score": score,
                "max_score": weight,
                "percentage": round(percentage, 1),
                "deductions": deductions,
                "manual_check_ref": f"B.{self._get_manual_check_ref(dim)}"
            }
        
        return dimensions
    
    def _get_deductions_for_dimension(self, dim: str) -> List[Dict[str, Any]]:
        """获取某个维度的扣分项"""
        deductions = []
        
        # 从 audit_report 中查找相关失败项
        for failure in self.audit_report.failures:
            rule_id = failure.get("rule_id", "")
            if self._is_dimension_rule(rule_id, dim):
                evidence = failure.get("evidence", {})
                deductions.append({
                    "rule_id": rule_id,
                    "penalty": self._estimate_penalty(rule_id, dim),
                    "reason": failure.get("message", ""),
                    "evidence": evidence
                })
        
        return deductions
    
    def _is_dimension_rule(self, rule_id: str, dim: str) -> bool:
        """判断规则是否属于某个维度"""
        dim_prefix_map = {
            "gate": "S1.GATE",
            "evidence": "S2.EVIDENCE",
            "trigger": "S3.TRIGGER",
            "impact": "S4.IMPACT",
            "trace": "S6.TRACE",
            "timeline": "S6.TIMELINE"
        }
        prefix = dim_prefix_map.get(dim, "")
        return rule_id.startswith(prefix)
    
    def _estimate_penalty(self, rule_id: str, dim: str) -> int:
        """估算扣分数值"""
        # 根据规则 ID 和维度估算扣分
        if "GATE.003" in rule_id:  # Gate fail 仍 trigger
            return -25
        elif "GATE.001" in rule_id:  # Gate 未写入
            return -10
        elif "EVIDENCE.001" in rule_id:  # 单帧 CONFIRMED
            return -10
        elif "TRIGGER" in rule_id and "NO_OP" in rule_id:
            return -15
        elif "IMPACT.001" in rule_id:  # 非标准 Impact
            return -20
        elif "TIMELINE.001" in rule_id:  # NO_OP 写入 timeline
            return -10
        else:
            return -5  # 默认扣分
    
    def _get_manual_check_ref(self, dim: str) -> str:
        """获取人工检查条目编号"""
        ref_map = {
            "gate": "1",
            "evidence": "2",
            "trigger": "3",
            "impact": "4",
            "trace": "5",
            "timeline": "6"
        }
        return ref_map.get(dim, "?")
    
    def _generate_violations_timeline(self) -> List[Dict[str, Any]]:
        """生成违规时间线"""
        timeline = []
        
        # 从 audit_report 中提取违规事件
        violation_id = 0
        for failure in self.audit_report.failures:
            violation_id += 1
            evidence = failure.get("evidence", {})
            trace_index = evidence.get("trace_index")
            
            # 获取对应 trace
            trace = None
            if trace_index is not None and trace_index < len(self.ctx.traces):
                trace = self.ctx.traces[trace_index]
            
            if trace:
                time_info = trace.get("time", {})
                violation_event = {
                    "violation_id": f"V{violation_id:04d}",
                    "rule_id": failure.get("rule_id", ""),
                    "severity": "fatal" if failure.get("status") == "FAIL" else "warning",
                    "message": failure.get("message", ""),
                    "time": {
                        "ts": time_info.get("ts", 0),
                        "human_time": time_info.get("human_time", "00:00.00"),
                        "frame_id": time_info.get("frame_id", 0)
                    },
                    "frame_info": {
                        "frame_id": time_info.get("frame_id", 0),
                        "human_time": time_info.get("human_time", "00:00.00"),
                        "fps": time_info.get("fps", 30.0)
                    },
                    "context": {
                        "impact": trace.get("impact_eval", {}).get("impact", "NO_OP"),
                        "decision": trace.get("impact_eval", {}).get("decision_level", ""),
                        "gate_mode": trace.get("gate_eval", {}).get("mode", ""),
                        "human_explanation": self._get_human_explanation(trace)
                    },
                    "trace_ref": {
                        "trace_index": trace_index,
                        "frame_id": time_info.get("frame_id", 0),
                        "human_time": time_info.get("human_time", "00:00.00")
                    }
                }
                timeline.append(violation_event)
        
        # 按时间排序
        timeline.sort(key=lambda x: x["time"]["ts"])
        
        return timeline
    
    def _get_human_explanation(self, trace: Dict[str, Any]) -> str:
        """获取人类可读解释"""
        impact_eval = trace.get("impact_eval", {})
        impact = impact_eval.get("impact", "NO_OP")
        reason = impact_eval.get("reason", "")
        
        if impact == "NO_OP":
            return f"B 在此帧认为有变化，但该变化不会影响 C 的行为。原因: {reason}"
        else:
            return f"B 判断 impact = {impact}。原因: {reason}"
    
    def _generate_metadata(self) -> Dict[str, Any]:
        """生成元数据"""
        return {
            "trace_file": self.ctx.trace_path,
            "timeline_file": self.ctx.timeline_path,
            "total_frames": len(self.ctx.traces),
            "duration_seconds": self._estimate_duration(),
            "generated_at": datetime.now().isoformat()
        }
    
    def _estimate_duration(self) -> float:
        """估算总时长"""
        if not self.ctx.traces:
            return 0.0
        
        first_time = self.ctx.traces[0].get("time", {}).get("ts", 0)
        last_time = self.ctx.traces[-1].get("time", {}).get("ts", 0)
        return last_time - first_time if last_time > first_time else 0.0
    
    def save(self, output_path: str = "b2_dcs_web_data.json"):
        """保存 Web 数据到文件"""
        data = self.generate()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return output_path

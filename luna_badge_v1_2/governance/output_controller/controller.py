"""
Model Output Controller

模型输出治理的中心控制器。

v1.5 定位：治理器，不是智能体
- 所有决策：规则化、确定性、可配置
- 不引入学习、不引入自适应
"""

from collections import deque
from dataclasses import asdict
import time
from typing import List, Dict, Any, Optional
from .normalizer import OutputNormalizer
from .validator import OutputValidator
from .conflict_detector import ConflictDetector
from .arbiter import OutputArbiter
from .authority import resolve_authority
from .ability_matrix import AbilityMask, AuthorityLevel, AUTHORITY_ABILITY_MATRIX
from .distortion_report import DistortionReport
from .authority_hysteresis import apply_authority_hysteresis
from .bc_c_coordinator import BCAction, decide_bc_c_cooperation
from ..instinct_controller.c_controller import CController
from ..invariants import (
    assert_bc_decision_not_from_risk,
    assert_bc_snapshot_invariants,
    assert_bc_snapshot_risk_invariants,
    assert_risk_not_lowering_authority,
    assert_risk_not_used_for_decision,
)
from .debug_view import build_debug_view
from ..risk_center import RiskCenter, build_world_snapshot
from ..risk_center.vo import evaluate_vo
from ..risk_center.interfaces.envelope import evaluate_envelope
from ..risk_center.interfaces.bus import EnvelopeBus


def build_ability_mask(authority: AuthorityLevel) -> AbilityMask:
    return AUTHORITY_ABILITY_MATRIX[authority]


def _default_distortion_report() -> DistortionReport:
    return DistortionReport(
        distorted=False,
        severity="LOW",
        reason_codes=[],
        recommended_action="NONE",
    )


def evaluate_distortion(history: List[Dict[str, Any]], window_size: int) -> DistortionReport:
    if not history:
        return _default_distortion_report()

    window = history[-window_size:]
    reason_codes: List[str] = []

    # D-01: 能力空转
    if all(
        (s.get("authority") or {}).get("effective") in {"A4", "A5"}
        and s.get("abilities", {}).get("allow_output") is False
        and s.get("abilities", {}).get("allow_arbitration") is True
        for s in window
    ):
        reason_codes.append("D-01_EMPTY_CAPABILITY_LOOP")

    # D-02: Gate 长期兜底
    if all(s.get("gate") == "BLOCK" for s in window):
        reason_codes.append("D-02_GATE_BLOCKED_STREAK")

    # D-03: Authority 震荡
    authority_series = [(s.get("authority") or {}).get("effective") for s in window]
    if len(authority_series) >= 3:
        changes = sum(
            1 for idx in range(1, len(authority_series))
            if authority_series[idx] != authority_series[idx - 1]
        )
        if changes >= 2 and all(a in {"A2", "A3", "A4"} for a in authority_series):
            reason_codes.append("D-03_AUTHORITY_OSCILLATION")

    if not reason_codes:
        return _default_distortion_report()

    severity = "MEDIUM" if "D-03_AUTHORITY_OSCILLATION" in reason_codes else "HIGH"
    return DistortionReport(
        distorted=True,
        severity=severity,
        reason_codes=reason_codes,
        recommended_action="OBSERVE_ONLY",
    )


def hard_gate(arbitration_result: Dict[str, Any], system_snapshot: dict) -> Dict[str, Any]:
    if not isinstance(system_snapshot, dict):
        return arbitration_result

    control_distortion = str(system_snapshot.get("control_distortion", "")).upper()
    hardware = str(system_snapshot.get("hardware_state") or system_snapshot.get("hardware", "")).upper()
    calibration = str(system_snapshot.get("calibration_state") or system_snapshot.get("calibration", "")).upper()
    system_mode = str(system_snapshot.get("system_mode", "")).upper()

    if (
        control_distortion in {"FAIL_SAFE", "TRUE"}
        or hardware in {"FAULT", "FAILED"}
        or calibration in {"FAILED", "NOT_READY"}
        or system_mode == "FAIL_SAFE"
    ):
        gated = dict(arbitration_result)
        gated["action"] = "fallback"
        gated["selected_result"] = None
        gated["reason"] = arbitration_result.get("reason", "")
        gated["fallback_plan"] = "hard_gate_blocked"
        return gated

    return arbitration_result


    


class ModelOutputController:
    """
    模型输出控制器
    
    职责：
    - 接收多个模型输出
    - 协调归一化、验证、冲突检测、仲裁
    - 返回系统可执行结果（符合 decision_schema.json）
    
    关键原则：
    - TaskChain 永远不直接信任模型输出，只信任 MOC 的决策结果
    """
    
    def __init__(self, metrics_collector=None, trace_id=None):
        """
        初始化控制器
        
        依赖：
        - Normalizer: 输出标准化
        - Validator: 输出合法性校验
        - ConflictDetector: 冲突检测
        - Arbiter: 仲裁决策
        - metrics_collector: 指标收集器（可选）
        - trace_id: 跟踪 ID（可选）
        """
        self.normalizer = OutputNormalizer()
        self.validator = OutputValidator()
        self.conflict_detector = ConflictDetector()
        self.arbiter = OutputArbiter()
        self.metrics_collector = metrics_collector
        self.trace_id = trace_id or (metrics_collector.new_trace_id() if metrics_collector else None)
        self._bc_snapshot_history = deque(maxlen=5)
        self._authority_history = deque(maxlen=50)
        self._c = CController()
        self._risk = RiskCenter()
    def process(
        self,
        task_domain: str,
        model_outputs: List[Dict[str, Any]],
        system_snapshot: dict,
    ) -> Dict[str, Any]:
        """
        主流程：raw_outputs -> decision_schema
        
        Args:
            task_domain: 任务领域（如 "navigation", "safety", "inquiry"）
            model_outputs: 模型输出列表，每个元素必须包含：
                {
                    "model_id": str,
                    "model_version": Optional[str],
                    "result" | "data" | "output": Any,  # 原始输出数据
                    "confidence": Optional[float],
                    "meta": Optional[Dict]
                }
            
        Returns:
            符合 decision_schema.json 的决策结果：
            {
                "decision": "commit" | "fallback" | "abort",
                "selected_result": Optional[Dict],
                "reason": str,
                "used_model": Optional[Dict],
                "confidence": None,
                "fallback_plan": Optional[str],
                "decision_trace": Dict
            }
        """
        # 0. Authority (入口第一步)
        now_ts = time.time()
        raw_authority = resolve_authority(system_snapshot)
        history_snapshot = list(self._bc_snapshot_history)
        pre_distortion = evaluate_distortion(history_snapshot, window_size=3)
        # 1. C 决策（本能层，先于仲裁）
        c_decision = self._c.decide(system_snapshot)

        # 2. Risk Center（只读信号）
        world_snapshot = build_world_snapshot(system_snapshot)
        risk_signal = self._risk.evaluate(system_snapshot)
        vo_projection = evaluate_vo(world_snapshot)
        authority_risk_context = {
            "risk_present": risk_signal.present,
            "risk_level": risk_signal.level,
        }
        envelope_signal = evaluate_envelope(system_snapshot, {"risk": risk_signal})

        final_authority = apply_authority_hysteresis(
            raw_authority=raw_authority,
            authority_history=list(self._authority_history),
            distortion_report=pre_distortion,
            now_ts=now_ts,
            risk_context=authority_risk_context,
        )
        abilities = build_ability_mask(final_authority)
        assert_risk_not_lowering_authority(raw_authority, final_authority, risk_signal.present)

        # 3. C ↔ BC 协同裁决
        coop = decide_bc_c_cooperation(
            authority=final_authority,
            c_decision=c_decision,
        )

        # 4. 归一化所有输出
        normalized = []
        for output in model_outputs:
            try:
                n = self.normalizer.normalize(task_domain, output)
                normalized.append(n)
            except Exception as e:
                # 归一化失败，跳过该输出
                continue
        
        # 5. 验证输出有效性
        valid_outputs = []
        for n in normalized:
            is_valid, reason = self.validator.validate(n)
            if is_valid:
                valid_outputs.append(n)
            # v1.5: 无效输出直接丢弃，不记录到 trace（简化处理）

        # 6. 入口裁剪（AbilityMask + C 协同）
        b_candidates = valid_outputs if (abilities.allow_b_input and coop.allow_execute_b) else []

        # 7. 检测冲突
        conflicts = self.conflict_detector.detect(b_candidates)

        # 8. 仲裁决策（不读 Authority）
        if coop.bc_action == BCAction.EXECUTE and abilities.allow_arbitration:
            arbitration_result = self.arbiter.arbitrate(task_domain, b_candidates, conflicts)
        else:
            if coop.bc_action == BCAction.FORCE_STOP:
                reason = "c_force_stop"
            elif coop.bc_action == BCAction.HOLD:
                reason = "c_hold"
            elif coop.bc_action == BCAction.REQUEST_TAKEOVER:
                reason = "c_request_takeover"
            else:
                reason = "coop_fallback" if coop.bc_action == BCAction.FALLBACK else "arbitration_disabled"
            arbitration_result = {"action": "fallback", "selected_output": None, "reason": reason}

        # 9. Hard Gate（兜底，不读 Authority）
        gated_result = hard_gate(arbitration_result, system_snapshot)

        # 10. 组装 decision_schema
        gate_blocked = (
            gated_result.get("action") == "fallback"
            and gated_result.get("fallback_plan") == "hard_gate_blocked"
        )
        decision = gated_result["action"]
        selected_output = gated_result.get("selected_output")
        if not abilities.allow_output:
            decision = "fallback"
            selected_output = None
            gated_result = dict(gated_result)
            if not gate_blocked:
                gated_result["fallback_plan"] = "ability_output_disabled"
        
        # 构建决策结果
        authority_blocked_by = None
        if final_authority != raw_authority:
            if pre_distortion.distorted:
                authority_blocked_by = "DISTORTION"
            else:
                last_effective = (
                    AuthorityLevel(self._authority_history[-1]["effective"])
                    if self._authority_history
                    else raw_authority
                )
                if risk_signal.risk_present and final_authority == last_effective:
                    authority_blocked_by = "RISK"
                else:
                    authority_blocked_by = "HYSTERESIS"

        if self._authority_history and self._authority_history[-1]["effective"] == final_authority.value:
            authority_since = self._authority_history[-1]["since"]
        else:
            authority_since = now_ts

        distortion_report = pre_distortion
        bc_snapshot = {
            "authority": {
                "raw": raw_authority.value,
                "effective": final_authority.value,
                "blocked_by": authority_blocked_by,
                "since": authority_since,
            },
            "abilities": asdict(abilities),
            "used_candidates": [o.get("model_id") for o in (selected_output and [selected_output] or [])],
            "shaping_applied": [],
            "override_used": False,
            "arbitration": arbitration_result.get("action"),
            "gate": "BLOCK" if gate_blocked else "PASS",
            "c_decision": coop.c_decision,
            "bc_action": coop.bc_action.value,
            "can_recover": coop.can_recover,
            "risk": {
                "present": risk_signal.present,
                "level": risk_signal.level,
                "type": risk_signal.type,
                "time_to_risk": risk_signal.time_to_event,
                "vo": {
                    "time_to_risk": vo_projection.time_to_risk,
                    "min_distance": vo_projection.min_distance,
                    "level": vo_projection.level,
                    "schema_version": vo_projection.schema_version,
                },
            },
            "distortion": asdict(distortion_report),
            "envelope": {
                "status": envelope_signal.status.value,
                "reasons": list(envelope_signal.reasons),
                "confidence": envelope_signal.confidence,
                "timestamp": envelope_signal.timestamp,
            },
            "threshold_version_id": None,
            "rollout_state": None,
            "envelope_bus": {
                "signals": [
                    {
                        "status": envelope_signal.status.value,
                        "reasons": list(envelope_signal.reasons),
                        "confidence": envelope_signal.confidence,
                        "timestamp": envelope_signal.timestamp,
                    }
                ]
            },
        }
        debug_view_input = {
            "authority": bc_snapshot["authority"],
            "abilities": bc_snapshot["abilities"],
            "gate": bc_snapshot["gate"],
            "c_decision": bc_snapshot["c_decision"],
            "bc_action": bc_snapshot["bc_action"],
            "risk": bc_snapshot["risk"],
            "distortion": bc_snapshot.get("distortion", {}),
            "envelope": bc_snapshot.get("envelope", {}),
            "threshold_version_id": bc_snapshot["threshold_version_id"],
            "rollout_state": bc_snapshot["rollout_state"],
        }
        from .debug_view import assert_debug_view_input
        assert_debug_view_input(debug_view_input)
        bc_snapshot["debug_view"] = build_debug_view(
            raw_authority=raw_authority,
            effective_authority=final_authority,
            blocked_by=authority_blocked_by,
            authority_since=authority_since,
            risk_signal=risk_signal,
            risk_vo=bc_snapshot["risk"].get("vo"),
            gate_blocked=gate_blocked,
            abilities=abilities,
            attempting_recovery=raw_authority != final_authority,
            distortion_distorted=distortion_report.distorted,
            envelope_signal=bc_snapshot.get("envelope", {}),
        )
        self._authority_history.append(
            {
                "ts": now_ts,
                "raw": raw_authority.value,
                "effective": final_authority.value,
                "since": authority_since,
            }
        )
        self._bc_snapshot_history.append(bc_snapshot)
        assert_bc_snapshot_invariants(bc_snapshot)
        assert_bc_snapshot_risk_invariants(bc_snapshot)

        result = {
            "decision": decision,
            "selected_result": selected_output.get("data") if selected_output else None,
            "reason": gated_result.get("reason", arbitration_result.get("reason")),
            "used_model": {
                "model_id": selected_output.get("model_id") if selected_output else None,
                "version": selected_output.get("model_version") if selected_output else None
            } if selected_output else None,
            "confidence": None,  # v1.5 暂不使用
            "fallback_plan": gated_result.get("fallback_plan") or ("default_fallback" if decision == "fallback" else None),
            "decision_trace": {
                "task_domain": task_domain,
                "rules_applied": [
                    "normalize_all_outputs",
                    "validate_outputs",
                    "detect_conflicts",
                    "arbitrate_by_priority"
                ],
                "conflicts_detected": conflicts,
                "valid_outputs_count": len(valid_outputs),
                "total_outputs_count": len(model_outputs),
                "bc_snapshot": bc_snapshot
            }
        }

        assert_bc_decision_not_from_risk(result.get("decision_trace", {}))
        assert_risk_not_used_for_decision(result)
        
        # 6. 记录 MOC 决策事件（打点）
        if self.metrics_collector and self.trace_id:
            self.metrics_collector.trace(
                trace_id=self.trace_id,
                task_domain=task_domain,
                node_id="moc",
                event="moc_decision",
                payload={
                    "decision": decision,
                    "used_model": result["used_model"],
                    "conflicts_count": len(conflicts),
                    "valid_outputs_count": len(valid_outputs),
                    "reason": arbitration_result["reason"]
                }
            )
        
        return result






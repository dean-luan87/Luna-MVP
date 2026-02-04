from typing import Any, Dict

from c.input_adapter import build_c_input
from c.layers.hard_safety import evaluate as eval_l1
from c.layers.environment import evaluate as eval_l2
from c.layers.uncertainty import evaluate as eval_l3
from c.types import CDecision, CResult

def decide(system_snapshot: Dict[str, Any]) -> CResult:
    assert isinstance(system_snapshot, dict)

    c_input = build_c_input(system_snapshot)
    for evaluator in (eval_l1, eval_l2, eval_l3):
        result = evaluator(c_input)
        if result is not None:
            return result

    return CResult(
        decision=CDecision.PASS,
        reason_code="NO_RISK",
        layer="NONE",
        facts={},
    )

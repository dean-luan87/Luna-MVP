from typing import Dict

from dynamic_view.entity import ObservedEntity
from c_adapter.types import CDecision


class CAdapter:
    """
    C Adapter v0：
    - 只读 stable world state
    - 不维护历史
    """

    def decide(self, stable_world: Dict[str, ObservedEntity]) -> Dict[str, CDecision]:
        decisions: Dict[str, CDecision] = {}

        for eid, ent in stable_world.items():
            if "traffic_light" in eid:
                decisions[eid] = CDecision.STOP
            elif "elevator" in eid:
                decisions[eid] = CDecision.PASS
            else:
                decisions[eid] = CDecision.PASS

        return decisions

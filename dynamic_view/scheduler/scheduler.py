from typing import Dict, List, Optional

from .contract import ObservationContract, ObservationPolicy
from .policy import merge_policies


class ObservationScheduler:
    """
    Scheduler v1：
    - 管理 ObservationContract
    - 为 entity 生成有效观察策略
    """

    def __init__(self):
        self._contracts: Dict[str, ObservationContract] = {}

    def register(self, contract: ObservationContract):
        self._contracts[contract.contract_id] = contract

    def revoke(self, contract_id: str):
        if contract_id in self._contracts:
            del self._contracts[contract_id]

    def policies_for_entity(self, entity_id: str) -> List[ObservationContract]:
        res = []
        for c in self._contracts.values():
            if c.entity_id is None:
                res.append(c)
            elif c.entity_id == entity_id:
                res.append(c)
        return res

    def effective_policy(self, entity_id: str) -> Optional[ObservationPolicy]:
        policies = [c.policy for c in self.policies_for_entity(entity_id)]
        if not policies:
            return None
        return merge_policies(policies)

from typing import Dict

from .types import ObservationContract


class ObservationScheduler:
    def __init__(self):
        self.active_contracts: Dict[str, ObservationContract] = {}

    def request(self, key: str, contract: ObservationContract):
        self.active_contracts[key] = contract

    def revoke(self, key: str):
        self.active_contracts.pop(key, None)

    def list_active(self):
        return list(self.active_contracts.values())

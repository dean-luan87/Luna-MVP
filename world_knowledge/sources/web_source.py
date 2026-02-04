import time
from typing import List

from world_knowledge.schema import ObservationSignal
from world_knowledge.profile import EnvironmentProfile


class WebSearchSource:
    """
    Untrusted: produces ObservationSignal only.
    Real search integration will be added later.
    """

    def search(self, query: str, profile: EnvironmentProfile) -> List[ObservationSignal]:
        return [
            ObservationSignal(
                signal_type="web_snippet",
                payload={"query": query, "snippets": []},
                provider="web_stub",
                ts=time.time(),
            )
        ]

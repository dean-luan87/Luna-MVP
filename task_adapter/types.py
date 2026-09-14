from dataclasses import dataclass
from enum import Enum

from dynamic_view.types import ObservationState


class TaskAction(Enum):
    ANNOUNCE = "announce"
    GUIDE = "guide"
    NONE = "none"


@dataclass
class TaskTrigger:
    entity_id: str
    on_state: ObservationState
    action: TaskAction
    message: str

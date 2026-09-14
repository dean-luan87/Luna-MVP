from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class EnvironmentProfile:
    """Environment profile for region/scene/device/user routing."""

    region_code: str
    scene: str
    device_caps: Dict[str, Any]
    user_prefs: Optional[Dict[str, Any]] = None

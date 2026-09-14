from __future__ import annotations

from typing import Any, Dict

from map_d0.context import MapContext


def attach_map_context(world_snapshot: Dict[str, Any], map_context: MapContext) -> Dict[str, Any]:
    """
    Sidecar attach: write into reference only.
    """
    ws = dict(world_snapshot) if world_snapshot is not None else {}
    ref = dict(ws.get("reference", {}))
    ref["map_context"] = map_context.as_dict()
    ws["reference"] = ref
    return ws

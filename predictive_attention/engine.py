from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any

from .context import PalContext
from .schema import AttentionHint, PathStackState
from .path.interface import PathManager
from .roi.interface import RoiPredictor


@dataclass
class PalOutput:
    paths: PathStackState
    hints: List[AttentionHint]
    debug: Dict[str, Any]


class PredictiveAttentionEngine:
    def __init__(
        self,
        path_manager: PathManager,
        roi_predictor: RoiPredictor,
        enabled: bool = False,
    ):
        self._path_manager = path_manager
        self._roi_predictor = roi_predictor
        self._enabled = enabled

    def run(self, ctx: PalContext) -> PalOutput:
        paths = self._path_manager.update(ctx)
        if not self._enabled:
            return PalOutput(paths=paths, hints=[], debug={"enabled": False})
        hints = self._roi_predictor.propose(ctx, paths)
        return PalOutput(
            paths=paths,
            hints=hints,
            debug={"enabled": True, "hint_count": len(hints)},
        )

    def set_enabled(self, enabled: bool) -> None:
        self._enabled = enabled

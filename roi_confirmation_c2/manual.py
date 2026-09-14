from __future__ import annotations

import time

from roi_confirmation_c2.events import ROIManualEvent
from roi_confirmation_c2.schema import ROIDefaultEntry
from roi_confirmation_c2.registry import ROIDefaultRegistry


class ROIManualConfirmer:
    """
    人工确认接口：
    - 只写 registry
    - 只产 event
    - 不做任何判断
    """

    def confirm(
        self,
        registry: ROIDefaultRegistry,
        roi_kind: str,
        actor: str,
        reason: dict,
        version: str = "c2.1-manual",
    ) -> ROIManualEvent:
        entry = ROIDefaultEntry(
            roi_kind=roi_kind,
            mode="MANUAL",
            version=version,
            reason=reason,
        )
        registry.upsert(entry)

        return ROIManualEvent(
            roi_kind=roi_kind,
            action="CONFIRM",
            actor=actor,
            reason=reason,
            timestamp=time.time(),
        )

    def reject(
        self,
        roi_kind: str,
        actor: str,
        reason: dict,
    ) -> ROIManualEvent:
        return ROIManualEvent(
            roi_kind=roi_kind,
            action="REJECT",
            actor=actor,
            reason=reason,
            timestamp=time.time(),
        )

    def revoke(
        self,
        registry: ROIDefaultRegistry,
        roi_kind: str,
        actor: str,
        reason: dict,
    ) -> ROIManualEvent:
        registry.remove(roi_kind)

        return ROIManualEvent(
            roi_kind=roi_kind,
            action="REVOKE",
            actor=actor,
            reason=reason,
            timestamp=time.time(),
        )

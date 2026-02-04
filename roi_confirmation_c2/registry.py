from __future__ import annotations

from typing import Dict

from roi_confirmation_c2.schema import ROIDefaultEntry


class ROIDefaultRegistry:
    """
    v0：内存注册表，可随时替换为文件 / DB
    """

    def __init__(self):
        self._items: Dict[str, ROIDefaultEntry] = {}

    def upsert(self, entry: ROIDefaultEntry):
        self._items[entry.roi_kind] = entry

    def remove(self, roi_kind: str):
        self._items.pop(roi_kind, None)

    def all(self) -> Dict[str, ROIDefaultEntry]:
        return dict(self._items)

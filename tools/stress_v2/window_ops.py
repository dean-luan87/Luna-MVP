# tools/stress_v2/window_ops.py
from __future__ import annotations

from typing import List, Tuple

Window = Tuple[int, int]  # (start, end) inclusive


def expand_window(w: Window, left: int, right: int, lo: int, hi: int) -> Window:
    s, e = w
    s2 = max(lo, s - left)
    e2 = min(hi, e + right)
    return (s2, e2)


def merge_overlaps(windows: List[Window]) -> List[Window]:
    if not windows:
        return []
    windows = sorted(windows, key=lambda x: (x[0], x[1]))
    merged: List[Window] = [windows[0]]
    for s, e in windows[1:]:
        ms, me = merged[-1]
        if s <= me + 1:
            merged[-1] = (ms, max(me, e))
        else:
            merged.append((s, e))
    return merged

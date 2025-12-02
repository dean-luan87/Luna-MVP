"""
Tile Enhancer Module (v1.3.0)

局部关键区增强模块
"""

from .enhancer import TileEnhancer
from .config import (
    TILE_ROWS,
    TILE_COLS,
    BRIGHTNESS_THRESHOLD,
    CONTRAST_THRESHOLD,
    NOISE_THRESHOLD,
)

__all__ = [
    "TileEnhancer",
    "TILE_ROWS",
    "TILE_COLS",
    "BRIGHTNESS_THRESHOLD",
    "CONTRAST_THRESHOLD",
    "NOISE_THRESHOLD",
]










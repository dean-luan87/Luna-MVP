"""
视觉输出模块 (v1.2.0)
将视觉结果打包成返回格式（JSON / event），供 routes 调用
"""

from .visual_packager import VisualPackager
from .visual_serializer import VisualSerializer
from .visual_event_mapper import VisualEventMapper

__all__ = [
    'VisualPackager',
    'VisualSerializer',
    'VisualEventMapper'
]




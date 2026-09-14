"""
ModelOCR capabilities package.

Hard boundary reminder:
- raw-text only
- no downstream integration
- no runtime execution enablement
"""

from .macos_vision_ocr_adapter_v0 import MacOSVisionOCRAdapterV0
from .paddleocr_adapter_v0 import PaddleOCRAdapterV0
from .rapidocr_adapter_v0 import RapidOCRAdapterV0

__all__ = ["MacOSVisionOCRAdapterV0", "PaddleOCRAdapterV0", "RapidOCRAdapterV0"]

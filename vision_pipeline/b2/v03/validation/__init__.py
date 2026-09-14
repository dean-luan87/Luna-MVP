# vision_pipeline/b2/v03/validation/__init__.py
"""
B2 v0.5 自动化验收模块
"""

from vision_pipeline.b2.v03.validation.b2_v05_validation import (
    B2V05Validator,
    ValidationResult
)

__all__ = ["B2V05Validator", "ValidationResult"]

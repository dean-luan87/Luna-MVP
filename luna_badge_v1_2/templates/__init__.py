"""
Task Template Library for Luna Badge v1.4.0
"""

from .hospital_templates import HOSPITAL_TEMPLATES
from .mall_templates import MALL_TEMPLATES
from .subway_templates import SUBWAY_TEMPLATES
from .gov_templates import GOV_TEMPLATES

TEMPLATE_LIBRARY = {
    "HospitalHall": HOSPITAL_TEMPLATES,
    "MallIndoor": MALL_TEMPLATES,
    "SubwayStation": SUBWAY_TEMPLATES,
    "GovServiceHall": GOV_TEMPLATES,
}

__all__ = [
    "HOSPITAL_TEMPLATES",
    "MALL_TEMPLATES",
    "SUBWAY_TEMPLATES",
    "GOV_TEMPLATES",
    "TEMPLATE_LIBRARY",
]











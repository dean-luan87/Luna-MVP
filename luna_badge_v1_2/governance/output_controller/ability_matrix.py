from dataclasses import dataclass
from enum import Enum


class AuthorityLevel(str, Enum):
    A1 = "A1"
    A2 = "A2"
    A3 = "A3"
    A4 = "A4"
    A5 = "A5"


@dataclass(frozen=True)
class AbilityMask:
    allow_b_input: bool
    allow_c_input: bool
    allow_arbitration: bool
    allow_shaping: bool
    allow_output: bool
    allow_voice: bool


AUTHORITY_ABILITY_MATRIX = {
    AuthorityLevel.A1: AbilityMask(
        allow_b_input=True,
        allow_c_input=False,
        allow_arbitration=True,
        allow_shaping=False,
        allow_output=True,
        allow_voice=True,
    ),
    AuthorityLevel.A2: AbilityMask(
        allow_b_input=True,
        allow_c_input=False,
        allow_arbitration=True,
        allow_shaping=False,
        allow_output=True,
        allow_voice=False,
    ),
    AuthorityLevel.A3: AbilityMask(
        allow_b_input=False,
        allow_c_input=False,
        allow_arbitration=True,
        allow_shaping=False,
        allow_output=False,
        allow_voice=False,
    ),
    AuthorityLevel.A4: AbilityMask(
        allow_b_input=False,
        allow_c_input=False,
        allow_arbitration=True,
        allow_shaping=False,
        allow_output=False,
        allow_voice=False,
    ),
    AuthorityLevel.A5: AbilityMask(
        allow_b_input=False,
        allow_c_input=False,
        allow_arbitration=False,
        allow_shaping=False,
        allow_output=False,
        allow_voice=False,
    ),
}

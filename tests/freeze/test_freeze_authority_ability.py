from luna_badge_v1_2.governance.output_controller.ability_matrix import AUTHORITY_ABILITY_MATRIX, AuthorityLevel
from luna_badge_v1_2.governance.output_controller.controller import build_ability_mask


def test_authority_ability_matrix_exact():
    for level in AuthorityLevel:
        assert build_ability_mask(level) == AUTHORITY_ABILITY_MATRIX[level]

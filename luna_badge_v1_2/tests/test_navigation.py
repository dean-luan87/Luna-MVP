from core.scene_output import SceneState
from capabilities.navigation_logic import NavigationEngine


def test_navigation_engine_decide():
    engine = NavigationEngine()
    scene_state = SceneState(
        timestamp=0.0,
        objects=[{"class": "obstacle"}],
        depth_info=None,
        walkable_zone=None,
        raw_frame=None,
    )
    engine.update(scene_state)
    text = engine.decide()
    assert isinstance(text, str)
    assert len(text) > 0


























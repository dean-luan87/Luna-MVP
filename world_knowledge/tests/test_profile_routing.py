from world_knowledge.profile import EnvironmentProfile


def test_environment_profile_fields():
    profile = EnvironmentProfile(
        region_code="CN-GD-GZ",
        scene="outdoor_crosswalk",
        device_caps={"net": True, "gps": True},
        user_prefs={"pace": "conservative"},
    )
    assert profile.region_code == "CN-GD-GZ"
    assert profile.scene == "outdoor_crosswalk"
    assert profile.device_caps["net"] is True
    assert profile.user_prefs["pace"] == "conservative"

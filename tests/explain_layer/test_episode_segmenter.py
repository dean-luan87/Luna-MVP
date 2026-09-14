from luna_badge_v1_2.governance.explain_layer.episode_segmenter import segment_episodes


def test_episode_segmentation_min_timeline():
    episodes = segment_episodes([{"acceleration": "INCREASING"}])
    assert episodes == ["BUILD_UP", "CRITICAL"]


def test_episode_segmentation_empty():
    episodes = segment_episodes([])
    assert episodes == ["SAFE"]

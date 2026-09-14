from dynamic_view.attention import AttentionManager, AttentionWindow


def test_attention_ttl_expires():
    m = AttentionManager()
    m.set([AttentionWindow(area_type="platform", hint="test", ttl_frames=2)])
    assert len(m.get()) == 1
    m.tick()
    assert len(m.get()) == 1
    m.tick()
    assert len(m.get()) == 0

from map_d0 import MapContext, attach_map_context


def test_attach_map_context_reference_only():
    ws = {"facts": {"vision": {"entities": []}}}
    ctx = MapContext(
        city_id="shanghai",
        available_layers=["L1"],
        structural_anchors=["road"],
        active_zone_radius_m=500,
        confidence=0.8,
    )

    out = attach_map_context(ws, ctx)
    assert out["facts"] == ws["facts"]
    assert "reference" in out
    assert out["reference"]["map_context"]["city_id"] == "shanghai"

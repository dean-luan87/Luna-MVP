import time

from dynamic_view.engine import ObservationEngine
from dynamic_view.binder.simple import SimpleBinder
from dynamic_view.descriptors import EntityDescriptor
from dynamic_view.types import ObservationState


def test_ingest_descriptor_creates_entity_and_stabilizes():
    binder = SimpleBinder()
    eng = ObservationEngine(binder=binder)
    t0 = time.time()

    d = EntityDescriptor(kind="elevator", signature="sig_elevator_A")
    eid = eng.ingest_descriptor(d, t0)
    assert eid is not None
    assert eid in eng.entities

    eng.tick(t0)
    assert eng.entities[eid].state == ObservationState.APPEARED

    eng.tick(t0 + 0.1)
    assert eng.entities[eid].state == ObservationState.STABLE


def test_same_signature_maps_to_same_entity_id():
    binder = SimpleBinder()
    eng = ObservationEngine(binder=binder)
    t0 = time.time()

    d1 = EntityDescriptor(kind="cat", signature="sig_cat_001")
    eid1 = eng.ingest_descriptor(d1, t0)

    d2 = EntityDescriptor(kind="cat", signature="sig_cat_001")
    eid2 = eng.ingest_descriptor(d2, t0 + 0.2)

    assert eid1 == eid2
    assert eid1 in eng.entities


def test_descriptor_without_signature_creates_new_entity_id():
    binder = SimpleBinder()
    eng = ObservationEngine(binder=binder)
    t0 = time.time()

    d1 = EntityDescriptor(kind="traffic_light", signature=None)
    d2 = EntityDescriptor(kind="traffic_light", signature=None)

    eid1 = eng.ingest_descriptor(d1, t0)
    eid2 = eng.ingest_descriptor(d2, t0 + 0.1)

    assert eid1 is not None and eid2 is not None
    assert eid1 != eid2

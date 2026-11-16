"""Deterministic telemetry storage-policy tests (TEL-001..020 baseline)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from telemetry.models import TelemetryPoint
from telemetry.storage import ingest_event, subscribe_observer

BASE = datetime(2026, 11, 13, 10, 0, 0, tzinfo=UTC)


def _ingest(
    attribute,
    value,
    i=0,
    *,
    value_type="number",
    agent=None,
    history_enabled=True,
    source_event_id="",
    sequence=None,
    **kw,
):
    return ingest_event(
        tenant_id=str(attribute.tenant_id),
        project_id=str(attribute.project_id) if attribute.project_id else None,
        asset_id=str(attribute.asset_id),
        attribute_id=str(attribute.id),
        value=value,
        value_type=value_type,
        observed_at=BASE + timedelta(seconds=i),
        source_event_id=source_event_id,
        sequence=sequence,
        agent_default_policy=agent,
        history_enabled=history_enabled,
        history_override=attribute.history_policy_override,
        **kw,
    )


def _history(attribute):
    return [p.typed_value for p in TelemetryPoint.objects.filter(attribute_id=attribute.id).order_by("ts")]


def test_tel001_on_change_same_value_stores_once(attribute_factory):
    attr = attribute_factory("temp")
    agent = {"mode": "on_change", "compare": {"absolute_epsilon": 0}}
    results = [_ingest(attr, 42, i=i, agent=agent) for i in range(1000)]
    received = sum(r.received for r in results)
    accepted = sum(r.accepted for r in results)
    filtered_equal = sum(r.filtered_equal for r in results)
    assert received == 1000
    assert accepted == 1
    assert filtered_equal == 999
    assert len(_history(attr)) == 1
    assert _history(attr) == [42.0]


def test_tel002_on_change_sequence(attribute_factory):
    attr = attribute_factory("pressure")
    agent = {"mode": "on_change", "compare": {"absolute_epsilon": 0}}
    for i, v in enumerate([1, 1, 2, 2, 3, 3]):
        _ingest(attr, v, i=i, agent=agent)
    assert _history(attr) == [1.0, 2.0, 3.0]


def test_tel003_boolean_transitions(attribute_factory):
    attr = attribute_factory("state", value_type="boolean")
    agent = {"mode": "on_change", "compare": {}}
    for i, v in enumerate([False, False, True, False]):
        _ingest(attr, v, i=i, value_type="boolean", agent=agent)
    assert _history(attr) == [False, True, False]


def test_tel004_epsilon_absolute(attribute_factory):
    attr = attribute_factory("temp")
    agent = {"mode": "on_change", "compare": {"absolute_epsilon": 0.1}}
    for i, v in enumerate([20.0, 20.05, 20.09, 20.2]):
        _ingest(attr, v, i=i, agent=agent)
    assert _history(attr) == [20.0, 20.2]


def test_tel005_attribute_override_beats_agent_default(attribute_factory):
    attr_inherit = attribute_factory("inherit")
    attr_override = attribute_factory(
        "override", history_policy_override={"max_samples": {"count": 5, "window": "PT1H"}}
    )
    agent = {"mode": "on_change", "max_samples": {"count": 2, "window": "PT1H"}}
    for i in range(100):
        _ingest(attr_inherit, float(i), i=i, agent=agent)
        _ingest(attr_override, float(i), i=i, agent=agent)
    assert len(_history(attr_inherit)) == 2
    assert len(_history(attr_override)) == 5


def test_tel006_quota_hard_cap(attribute_factory):
    attr = attribute_factory("cap")
    agent = {"mode": "on_change", "max_samples": {"count": 3, "window": "PT1H"}}
    results = [_ingest(attr, float(i), i=i, agent=agent) for i in range(1000)]
    accepted = sum(r.accepted for r in results)
    filtered_quota = sum(r.filtered_quota for r in results)
    assert accepted == 3
    assert filtered_quota == 997
    assert len(_history(attr)) == 3


def test_tel007_two_windows(attribute_factory):
    attr = attribute_factory("windowed")
    agent = {"mode": "on_change", "max_samples": {"count": 2, "window": "PT1H"}}
    # 4 events at end of hour 0, 4 at start of hour 1.
    for i in range(4):
        _ingest(attr, float(i), i=i, agent=agent)
    late = BASE + timedelta(hours=1)
    for j in range(4):
        ingest_event(
            tenant_id=str(attr.tenant_id),
            project_id=str(attr.project_id) if attr.project_id else None,
            asset_id=str(attr.asset_id),
            attribute_id=str(attr.id),
            value=float(10 + j),
            value_type="number",
            observed_at=late + timedelta(seconds=j),
            agent_default_policy=agent,
            history_enabled=True,
        )
    points = TelemetryPoint.objects.filter(attribute_id=attr.id).order_by("ts")
    first_window = [p for p in points if p.ts < late]
    second_window = [p for p in points if p.ts >= late]
    assert len(first_window) == 2
    assert len(second_window) == 2


def test_tel008_history_disabled_still_rules_and_current(attribute_factory):
    attr = attribute_factory("nohist", history_enabled=False)
    seen = []

    def observer(event):
        seen.append(event["value"])

    subscribe_observer(observer)
    for i in range(10):
        _ingest(attr, float(i), i=i, history_enabled=False)
    assert len(_history(attr)) == 0
    assert len(seen) == 10
    from telemetry.models import AttributeCurrent

    current = AttributeCurrent.objects.get(attribute_id=attr.id)
    assert current.typed_value == 9.0


def test_tel010_dedupe_replay(attribute_factory):
    attr = attribute_factory("replay")
    agent = {"mode": "on_change", "compare": {"absolute_epsilon": 0}}
    r1 = _ingest(attr, 42, i=0, agent=agent, source_event_id="evt-1")
    r2 = _ingest(attr, 42, i=0, agent=agent, source_event_id="evt-1")
    assert r1.accepted == 1
    assert r2.duplicate == 1
    assert len(_history(attr)) == 1


def test_tel013_invalid_numeric(attribute_factory):
    attr = attribute_factory("invalid")
    agent = {"mode": "on_change", "compare": {"absolute_epsilon": 0}}
    for i, v in enumerate([None, float("nan"), float("inf"), 5.0]):
        r = _ingest(attr, v, i=i, agent=agent)
        if v in (None, float("nan"), float("inf")):
            assert r.invalid == 1
    assert len(_history(attr)) == 1
    assert _history(attr) == [5.0]
    from telemetry.models import AttributeCurrent

    current = AttributeCurrent.objects.get(attribute_id=attr.id)
    assert current.typed_value == 5.0
    assert current.quality == "good"


def test_tel020_no_nodered_needed(attribute_factory):
    # Direct ingest (the only path) works with no Node-RED service involved.
    attr = attribute_factory("direct")
    agent = {"mode": "on_change", "max_samples": {"count": 60, "window": "PT1H"}}
    results = [_ingest(attr, 7, i=i, agent=agent) for i in range(10)]
    assert sum(r.accepted for r in results) == 1
    assert len(_history(attr)) == 1

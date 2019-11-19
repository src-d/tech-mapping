import tm


def test_make_snapshots():
    base = tm._utc_iso("2013-01-01")
    lower = tm._utc_iso("2013-01-01")
    upper = tm._utc_iso("2013-02-01")
    period = tm._timedelta_days(7)
    assert [
        tm._utc_iso("2013-01-01"),
        tm._utc_iso("2013-01-08"),
        tm._utc_iso("2013-01-15"),
        tm._utc_iso("2013-01-22"),
        tm._utc_iso("2013-01-29"),
    ] == tm.make_snapshots(lower, upper, base, period)


def test_make_snapshots_middle():
    base = tm._utc_iso("2013-01-01")
    lower = tm._utc_iso("2013-01-06")
    upper = tm._utc_iso("2013-01-24")
    period = tm._timedelta_days(7)
    assert [
        tm._utc_iso("2013-01-08"),
        tm._utc_iso("2013-01-15"),
        tm._utc_iso("2013-01-22"),
    ] == tm.make_snapshots(lower, upper, base, period)


def test_snapshot_tracker():
    base = tm._utc_iso("2013-01-01")
    lower = tm._utc_iso("2013-01-06")
    upper = tm._utc_iso("2013-01-24")
    period = tm._timedelta_days(7)
    snapshots = tm.make_snapshots(lower, upper, base, period)
    # assert [
    #     tm._utc_iso("2013-01-08"),
    #     tm._utc_iso("2013-01-15"),
    #     tm._utc_iso("2013-01-22"),
    # ] == snapshots
    tracker = tm._SnapshotTracker(snapshots)
    assert not tracker.snapshots_for_date(tm._utc_iso("2013-01-24"))
    assert tracker.snapshots_for_date(tm._utc_iso("2013-01-21")) == [
        tm._utc_iso("2013-01-22")
    ]
    assert tracker.snapshots_for_date(tm._utc_iso("2013-01-07")) == [
        tm._utc_iso("2013-01-15"),
        tm._utc_iso("2013-01-08"),
    ]

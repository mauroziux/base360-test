from datetime import timezone
from decimal import Decimal

import pytest

from app.services.reservations import _month_bounds_utc, calculate_monthly_revenue


def test_month_bounds_use_property_timezone():
    start, end = _month_bounds_utc(3, 2024, "Europe/Paris")

    # March 1 at midnight in Paris is Feb 29 23:00 UTC; the end also reflects
    # the DST change that occurs during the month.
    assert start == start.replace(tzinfo=timezone.utc)
    assert end == end.replace(tzinfo=timezone.utc)
    assert start.isoformat() == "2024-02-29T23:00:00+00:00"
    assert end.isoformat() == "2024-03-31T22:00:00+00:00"


def test_month_bounds_reject_invalid_month():
    with pytest.raises(ValueError):
        _month_bounds_utc(13, 2024, "UTC")


@pytest.mark.asyncio
async def test_monthly_revenue_uses_tenant_and_local_month_bounds():
    calls = []

    class Result:
        def __init__(self, row=None, total=None):
            self.row = row
            self.total = total

        def fetchone(self):
            return self.row

        def scalar_one(self):
            return self.total

    class Session:
        async def execute(self, query, params):
            calls.append((str(query), params))
            if len(calls) == 1:
                return Result(row=type("Property", (), {"timezone": "Europe/Paris"})())
            return Result(total=Decimal("1250.000"))

    total = await calculate_monthly_revenue(
        "prop-001", 3, 2024, db_session=Session(), tenant_id="tenant-a"
    )

    assert total == Decimal("1250.000")
    assert calls[0][1] == {"property_id": "prop-001", "tenant_id": "tenant-a"}
    assert calls[1][1]["tenant_id"] == "tenant-a"
    assert calls[1][1]["start_date"].isoformat() == "2024-02-29T23:00:00+00:00"
    assert calls[1][1]["end_date"].isoformat() == "2024-03-31T22:00:00+00:00"

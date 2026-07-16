from decimal import Decimal

import pytest

from app.api.v1 import dashboard


@pytest.mark.asyncio
async def test_dashboard_rounds_revenue_to_cents(monkeypatch):
    async def summary(property_id, tenant_id):
        return {
            "property_id": property_id,
            "tenant_id": tenant_id,
            "total": "10.999",
            "currency": "USD",
            "count": 2,
        }

    monkeypatch.setattr(dashboard, "get_revenue_summary", summary)
    result = await dashboard.get_dashboard_summary(
        "prop-001", current_user=type("User", (), {"tenant_id": "tenant-a"})()
    )

    assert result["total_revenue"] == Decimal("11.00")
    assert isinstance(result["total_revenue"], Decimal)


@pytest.mark.asyncio
async def test_dashboard_rounds_half_cent_away_from_zero(monkeypatch):
    async def summary(property_id, tenant_id):
        return {
            "property_id": property_id,
            "tenant_id": tenant_id,
            "total": "10.005",
            "currency": "USD",
            "count": 1,
        }

    monkeypatch.setattr(dashboard, "get_revenue_summary", summary)
    result = await dashboard.get_dashboard_summary(
        "prop-001", current_user=type("User", (), {"tenant_id": "tenant-a"})()
    )

    assert result["total_revenue"] == Decimal("10.01")

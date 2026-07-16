import pytest

from app.core import database_pool
from app.services.reservations import calculate_total_revenue


@pytest.mark.asyncio
async def test_database_fallback_is_scoped_by_tenant(monkeypatch):
    class BrokenDatabasePool:
        async def initialize(self):
            raise RuntimeError("database unavailable")

    monkeypatch.setattr(database_pool, "DatabasePool", BrokenDatabasePool)

    sunset = await calculate_total_revenue("prop-001", "tenant-a")
    ocean = await calculate_total_revenue("prop-001", "tenant-b")

    assert sunset["total"] == "1000.00"
    assert sunset["tenant_id"] == "tenant-a"
    assert ocean["total"] == "0.00"
    assert ocean["tenant_id"] == "tenant-b"

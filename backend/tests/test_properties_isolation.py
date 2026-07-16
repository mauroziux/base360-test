import pytest

from app.core import database_pool
from app.services.properties import get_tenant_properties


@pytest.mark.asyncio
async def test_property_fallback_is_scoped_by_tenant(monkeypatch):
    class BrokenDatabasePool:
        async def initialize(self):
            raise RuntimeError("database unavailable")

    monkeypatch.setattr(database_pool, "DatabasePool", BrokenDatabasePool)

    sunset = await get_tenant_properties("tenant-a")
    ocean = await get_tenant_properties("tenant-b")

    assert [property["id"] for property in sunset] == ["prop-001", "prop-002", "prop-003"]
    assert sunset[0]["name"] == "Beach House Alpha"
    assert [property["id"] for property in ocean] == ["prop-001", "prop-004", "prop-005"]
    assert ocean[0]["name"] == "Mountain Lodge Beta"

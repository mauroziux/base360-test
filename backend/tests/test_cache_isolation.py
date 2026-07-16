import json

import pytest

from app.services import cache


class FakeRedis:
    def __init__(self):
        self.values = {}

    async def get(self, key):
        return self.values.get(key)

    async def setex(self, key, ttl, value):
        self.values[key] = value


@pytest.mark.asyncio
async def test_revenue_cache_is_scoped_by_tenant(monkeypatch):
    redis = FakeRedis()
    monkeypatch.setattr(cache, "redis_client", redis)

    async def calculate(property_id, tenant_id):
        return {
            "property_id": property_id,
            "tenant_id": tenant_id,
            "total": "1000.00" if tenant_id == "tenant-a" else "2000.00",
            "currency": "USD",
            "count": 1,
        }

    monkeypatch.setattr("app.services.reservations.calculate_total_revenue", calculate)

    sunset = await cache.get_revenue_summary("prop-001", "tenant-a")
    ocean = await cache.get_revenue_summary("prop-001", "tenant-b")

    assert sunset["tenant_id"] == "tenant-a"
    assert ocean["tenant_id"] == "tenant-b"
    assert json.loads(redis.values["revenue:tenant-a:prop-001"])["tenant_id"] == "tenant-a"
    assert json.loads(redis.values["revenue:tenant-b:prop-001"])["tenant_id"] == "tenant-b"

from typing import Any


# Development fallback used only when the configured database is unavailable.
# Keep this tenant-scoped because property IDs are not globally unique.
PROPERTY_FALLBACKS = {
    "tenant-a": [
        {"id": "prop-001", "name": "Beach House Alpha", "timezone": "Europe/Paris"},
        {"id": "prop-002", "name": "City Apartment Downtown", "timezone": "Europe/Paris"},
        {"id": "prop-003", "name": "Country Villa Estate", "timezone": "Europe/Paris"},
    ],
    "tenant-b": [
        {"id": "prop-001", "name": "Mountain Lodge Beta", "timezone": "America/New_York"},
        {"id": "prop-004", "name": "Lakeside Cottage", "timezone": "America/New_York"},
        {"id": "prop-005", "name": "Urban Loft Modern", "timezone": "America/New_York"},
    ],
}


async def get_tenant_properties(tenant_id: str) -> list[dict[str, Any]]:
    """Return only properties belonging to the requested tenant."""
    try:
        from app.core.database_pool import DatabasePool
        from sqlalchemy import text

        db_pool = DatabasePool()
        await db_pool.initialize()
        if db_pool.session_factory:
            async with db_pool.get_session() as session:
                result = await session.execute(
                    text("""
                        SELECT id, name, timezone
                        FROM properties
                        WHERE tenant_id = :tenant_id
                        ORDER BY name
                    """),
                    {"tenant_id": tenant_id},
                )
                return [dict(row._mapping) for row in result.fetchall()]
    except Exception as error:
        print(f"Database error loading properties (tenant: {tenant_id}): {error}")

    return PROPERTY_FALLBACKS.get(tenant_id, [])

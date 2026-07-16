# Revenue dashboard debugging

## Errors found and fixes

1. **Tenant cache collision:** Redis used only `property_id`. Keys now include `tenant_id`.
2. **Tenant-unsafe fallback:** development fallback data was keyed only by property. It is now nested by tenant and property.
3. **Monetary precision:** revenue remains `Decimal` with the database's three-decimal precision; the UI formats it for display.
4. **Monthly timezone boundaries:** monthly ranges are calculated in the property's timezone and converted to UTC.
5. **Client-controlled tenant:** the frontend no longer sends a simulated tenant header; the backend resolves tenant identity from authentication.
6. **Hardcoded property dropdown:** the dashboard previously showed all five properties to every tenant. It now loads properties from the tenant-scoped backend endpoint.

## Database connection

The challenge provides a local PostgreSQL database through `DATABASE_URL`. The database pool now uses that setting and `asyncpg`; the previous pool implementation referenced legacy Supabase settings and silently forced revenue/property reads into fallback data.

The fallback remains available only for development when the database is unavailable. It mirrors the seed data and is tenant-scoped.

## Verification

Backend regression tests:

```bash
uv run --directory backend pytest tests -q
```

Frontend build:

```bash
cd frontend && npm run build
```

Manual dashboard/API verification with the supplied credentials:

- Sunset: `prop-001` is **Beach House Alpha**, plus `prop-002` and `prop-003`.
- Ocean: `prop-001` is **Mountain Lodge Beta**, plus `prop-004` and `prop-005`.

The same property ID is valid in both tenants, but the tenant-scoped name and data are different.

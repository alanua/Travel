# Adapter Library

Provider-specific adapters are added on demand for real planning work, validated on bounded routes, and retained for reuse.

## Required adapter metadata

```text
provider
country_or_region
coverage
modes
official_status
authentication
licence
rate_limits
schedule_support
realtime_support
fare_support
disruption_support
accessibility_support
last_validation
known_failures
fallbacks
data_quality
```

## Required behaviour

- Preserve source provenance and retrieval time.
- Distinguish scheduled, live, cached, estimated, and simulated data.
- Return `UNKNOWN` for missing evidence.
- Never expose secret values in logs or normalized records.
- Never send private route, family, document, budget, or watchlist data upstream unless the provider request strictly requires a bounded route query.
- Keep provider-specific payloads behind the adapter boundary.

## Planned first families

```text
Germany: national rail, VBB/BVG, regional transport unions
Poland: national/intercity, regional rail, city networks
Netherlands: national rail and local transit
France: national rail and regional/urban networks
Austria, Czechia, Denmark, Sweden, and other countries as routes require
Generic: GTFS, GTFS-Realtime, SIRI, NeTEx, GBFS
```

Provider names and implementation status belong in the registry only after source and licence review.

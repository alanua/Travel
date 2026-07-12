# Situational Intelligence

Travel consumes shared Skeleton Situational Intelligence. It does not own a universal OSINT, weather, disaster or risk platform.

Source architecture:

- `alanua/Skeleton#1545` — bounded WorldMonitor research and pilot boundary;
- `alanua/Skeleton#1750` — shared capability model.

## Flow

```text
public external observations
→ bounded provider adapter
→ provenance and freshness validation
→ normalized Situational Intelligence signal
→ Travel risk projection
→ proposal or status update
```

## WorldMonitor role

WorldMonitor may be used only as an optional read-only sensor for public signals such as:

- conflict and unrest;
- disasters, wildfire and severe weather;
- infrastructure and aviation disruption;
- GNSS interference, airspace and NOTAM context;
- public advisories;
- indicative market or transport signals where provenance is available.

It is not authority, not a universal proxy, not an executor and not a private-memory writer.

## Required validation

Every result must retain, where available:

- upstream version or reviewed commit;
- original provider attribution;
- source timestamp and retrieval timestamp;
- freshness state;
- stale, cached or fallback state;
- real, demo or simulated state;
- source tier and confidence;
- query scope and result hash.

AI summaries and derived risk scores are observations, not verified source facts. Material conclusions require corroboration from appropriate primary or official sources.

## Privacy boundary

No private traveller information may be sent upstream, including:

- live or home location;
- private route candidates or watchlists;
- documents, identity or family context;
- bookings, tickets or private calendars;
- personal risk tolerance or decision state.

Public queries must be bounded to general place, time, source and event filters.

## Travel projection

Travel maps normalized signals to domain effects such as:

```text
NO_MATERIAL_IMPACT
INFORMATIONAL
ROUTE_RECHECK
SCHEDULE_RECHECK
RISK_RISING
TEMPORARILY_DOWNGRADED
ACTION_BLOCKED
```

A signal never books, cancels, contacts, writes canon or sends an alert by itself. It may create a typed proposal governed by shared notification and approval policy.

## Separate official adapters

A broad situational source does not replace official transport, airport, meteorological, civil-protection, advisory or operator sources. Travel retains separate adapters for route-specific authority and live operations.

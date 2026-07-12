# Provider Registry

The registry contains public-safe provider metadata only. It records reviewed source identity, coverage, licence, authentication class, freshness expectations, capability support, simulation risk, and validation status.

It must not contain API keys, personal route history, private price observations, bookings, tickets, watchlists, or document data.

Provider states:

```text
DISCOVERED
SOURCE_REVIEW
PROTOTYPE
VALIDATED
ACTIVE
DEGRADED
RETIRED
```

A provider becomes `VALIDATED` only after bounded tests against current official evidence and known route cases. Unsupported or stale capabilities remain explicit rather than inferred.

# Travel

Public-safe code, contracts, provider metadata, and reusable adapters for the Travel opportunity-planning and logistics module.

## Purpose

Travel supports worldwide opportunity discovery, route planning, full-cost comparison, multimodal logistics, and live journey monitoring. Provider-specific adapters are added when a real planning need appears, validated on bounded routes, and then retained for reuse.

## Public/private boundary

This repository may contain:

- generic architecture and contracts;
- reusable transport, accommodation, climate, event, safety, and price-observation adapters;
- public provider identifiers, licences, coverage notes, and synthetic fixtures;
- tests built from synthetic or public-safe data.

This repository must not contain:

- personal travel history, preferences, budgets, watchlists, rankings, or route candidates;
- passport, visa, residence, family, booking, ticket, payment, or location-history data;
- API keys, credentials, cookies, tokens, document numbers, or secret values;
- private price observations or derived personal decision records.

Private context belongs behind the Skeleton Memory Gate. Secrets belong in the approved secret store and are referenced only by typed secret references.

## Initial structure

```text
PROJECT_MANIFEST.yaml
adapters/
contracts/
docs/
registry/
tests/
```

## Adapter lifecycle

```text
REQUIRED_FOR_TRIP
→ SOURCE_RESEARCH
→ PROTOTYPE
→ VALIDATED_FOR_ROUTE
→ ACTIVE_FOR_TRIP
→ REUSABLE_ADAPTER
→ MAINTAINED
→ DEGRADED | RETIRED
```

No booking, payment, reservation, cancellation, contact, or subscription change is performed without explicit approval.

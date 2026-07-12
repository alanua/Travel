# Privacy, Authority and Secrets

Travel follows the Skeleton public/private/secret separation.

Source architecture:

- `alanua/Skeleton#1748` — Travel privacy boundary;
- `alanua/Skeleton#1761` — provider-neutral Secret Store Gate;
- `alanua/Skeleton#1750` — shared authority and composition model.

## Public repository

Allowed:

- generic architecture and deterministic code;
- provider-neutral contracts;
- public source identifiers, coverage and licences;
- synthetic fixtures;
- public-safe tests and aggregate benchmark results.

Forbidden:

- personal history, preferences, budgets, watchlists or rankings;
- route candidates, private opportunity maps or decision records;
- raw location tracks or live/home locations;
- passports, visas, residence data or document identifiers;
- bookings, tickets, emails, PDFs, payment data or private calendars;
- private price history or personalized model outputs;
- credentials, cookies, tokens, secret values or vault exports.

## Private MemoryGateway

Private canonical records are written only through the approved Skeleton MemoryGateway boundary.

Examples:

- traveller and party references;
- private constraints and preferences;
- visited-place and trip history;
- watchlists and rankings;
- private route candidates and decisions;
- personal scoring weights;
- private price observations and derived analysis;
- document-status references.

A chat statement or public commit is not a canonical private write. Canonical state requires a successful private write and read-back through the approved bridge.

## Private artifact storage

Raw scans, PDFs, tickets, booking confirmations, source snapshots and other sensitive files belong in an approved encrypted artifact store. Memory records contain bounded references and metadata, not copied file contents.

## Secret Store Gate

Travel modules receive typed opaque references only:

```text
Travel module or adapter
→ SecretReference
→ Skeleton Secret Store Gate
→ approved provider adapter
→ process-time injection
```

Secret values must never appear in GitHub, prompts, logs, issue comments, MemoryGateway records, CI output or agent-visible responses.

The domain cannot enumerate a vault or obtain whole-vault access. Each machine identity and module receives least-privilege access to only the approved reference and purpose.

## Authority levels

- `READ_ONLY` — search, retrieve, parse, normalize and monitor;
- `PROPOSAL` — shortlist, alert, recheck or booking-order proposal;
- `APPROVED_MUTATION` — a separately registered operation after explicit authorization.

Research and monitoring create options, never purchase intent.

No automatic path may:

- book or reserve;
- submit passenger or contact information;
- pay or change a subscription;
- cancel a booking;
- contact an operator, property or authority;
- publish private information;
- promote an observation directly into canon.

## Receipts and redaction

Operational receipts contain only metadata required for audit:

- module and operation;
- provider and secret reference ID;
- timestamp and outcome;
- evidence or result hash;
- failure category.

Receipts never contain secret values, private payloads, document numbers or full external responses.

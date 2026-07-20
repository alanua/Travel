# Travel Trip Page Pipeline

Travel creates and refreshes private trip pages through the universal Skeleton Page Pipeline. A normal page instance is data, not a code change: it does not require a GitHub issue, branch or pull request.

## Commands

```bash
python -m travel_page build --manifest /private/trips/milan-2026.yaml
python -m travel_page publish --manifest /private/trips/milan-2026.yaml
python -m travel_page publish --manifest /private/trips/milan-2026.yaml --mode update_owned
```

The wrapper `python scripts/publish_trip_page.py ...` is equivalent.

## Flow

```text
private Travel manifest
→ normalize to trip-page schema 1.1
→ verify licensed image metadata
→ render from web/trip-page
→ inline private trip data into the rendered package
→ Skeleton Page Pipeline
→ deterministic validation and hashing
→ encrypted GitHub Pages / Tailscale / filesystem backend
→ live verification
→ private receipt
→ idempotent Calendar connector action/outbox
```

Travel never implements backend deployment itself. It registers `travel_trip_v1` as a Skeleton renderer and `travel_calendar_v1` as a post-verification action.

## Private manifest

A compact manifest contains `schema_version`, `trip_id`, `title`, `locale`, `publication_profile_id`, `publication_mode`, route, practical data and either date windows, itinerary or a `trip_data_ref` conforming to `web/trip-page/schema/trip-page.schema.json`.

For encrypted GitHub Pages use private backend options such as a checked-out publication repository, HTTPS base URL, `git_mode: commit_push` and `verification_mode: https`. Private manifests, normalized trip data, event references and keys stay outside Git. Temporary normalized data and asset manifests are mode `0600` and removed after the Skeleton call.

## Images

Every used image must have `asset_url`, source page, author, licence, retrieval date, subject and alt text. Approved sources are Wikimedia Commons and Unsplash-compatible sources; another source requires `operator_approved: true`. Missing or unlicensed metadata blocks the build.

The renderer uses the existing Travel template with a five-image hero, up to eight gallery images, image-led daily cards, route, stays, activities, cost and practical sections. The private trip JSON is embedded into the staging package and encrypted by Skeleton before publication.

## Calendar action

Only after successful verification, `travel_calendar_v1` receives the private URL and declared event references. It creates an idempotent private request under `~/.local/share/travel/calendar-outbox/` or calls an approved bridge from `TRAVEL_CALENDAR_BRIDGE_COMMAND` using JSON on stdin.

The connector contract preserves event title, dates, transparency, visibility, attendees and reminders; writes one unbroken URL with the matching date selector; never creates or duplicates events; never adds Google Meet; and performs no mutation before publication verification.

## Milan migration

Milan is an `update_owned` migration. Its private manifest must use the stable `milan-2026` route, existing key through Skeleton private state or a mode-`0600` migration key file, and the three current date selectors. After a verified generated revision, the Milan-only enhancement injection can be removed separately.

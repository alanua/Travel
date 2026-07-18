# Canonical Travel trip page

Dependency-light static renderer for Travel candidate, planned and in-trip pages.

## Local preview

```bash
cd web/trip-page
python3 -m http.server 8080
```

Open `http://localhost:8080/`. Supply another dataset with `?data=path/to/trip.json`.

## Runtime boundary

The public repository stores only the generic template, schema and synthetic fixture. Real trip data, personal names, private prices, calendar IDs and private hostnames are supplied only through the private runtime publication path. The page performs no booking, payment or contact action.

# MapDrop City Poster Spec

Compiled 2026-10-12 from WORKFLOW.md and pipeline/batch_render.py.

## Format

| Item | Spec |
|---|---|
| Size | A3 |
| Resolution | 300 dpi, print-ready PDF |
| Preview | 1200 x 1600 PNG |
| Data | Live OpenStreetMap via maptoposter |
| Credit | "© OpenStreetMap contributors" on every poster and listing (ODbL) |

## Styles (3 per city)

| MapDrop name | maptoposter theme | Use |
|---|---|---|
| clean | warm_beige | Minimal, expected bestseller |
| dark | noir | Premium, high contrast |
| vibrant | sunset | Colourful, gift market |

Also available: blueprint, ocean, midnight_blue, pastel_dream, japanese_ink, copper_patina, neon_cyberpunk.

## File names

| File | Pattern | Example |
|---|---|---|
| PDF | `[city-slug]-[theme]-A3-300dpi.pdf` | `sydney-clean-A3-300dpi.pdf` |
| Preview | `[city-slug]-[theme]-preview-1200x1600.png` | `sydney-clean-preview-1200x1600.png` |
| Listing | `[city-slug]-listing.md` | `sydney-listing.md` |

## Quality gates (9.5/10 minimum)

| Check | Pass | Fail action |
|---|---|---|
| PDF opens | Yes | Re-render |
| Roads and water visible | Yes | Re-render |
| File size | Over 100 KB | Re-render (blank tile) |
| Correct city | Yes | Re-render (geocode error) |
| Preview clear | Yes | Re-render |
| Listing title | Under 140 characters | Rewrite |
| Listing tags | 13 unique | Rewrite |
| Copy | Passed humanizer | Rewrite |

## Known issue

`batch_render.py` still has a `DASH_REPO` path pointing at business-idea-dash (CortexOS only). Geo must repoint it to `clawanthonyzed/mapdrop` before the first batch run.

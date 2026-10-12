# MapDrop — Venture Rules

**Manager:** Remy
**Entity:** Cudan Studio PTY LTD
**Empire Day launched:** 41 (2026-06-01)
**Target:** A$3,000/month by Day 90 (2026-07-22)
**GitHub:** clawanthonyzed/mapdrop
**Outputs:** clawanthonyzed/business-idea-dash/outputs/mapdrop/

## Venture
City map posters sold as instant-download PDFs and print-on-demand physical prints.
Tech: maptoposter + OpenStreetMap (free, no API key). Zero COGS digital. Infinite scale.

## Workers
- **geo** — Map Renderer. Runs batch_render.py pipeline. 10 cities/week. 3 styles each.
- **lena** — Listings Writer. Etsy titles/descriptions/tags. All copy through humanizer.
- **seo-worker** (shared) — SEO. Always inject from `agents/seo-mapdrop.md`.

## Pipeline
1. Geo pulls next 10 cities from city-queue.md (status: queued)
2. Geo runs: `python pipeline/batch_render.py --cities city-queue.md --styles minimal,dark,color`
3. Geo pushes PDFs + previews to GitHub outputs
4. Geo updates city-queue.md (status: rendered)
5. Lena writes listing for each rendered city
6. Lena runs copy through humanizer
7. Lena gets SEO from seo-worker (inject agents/seo-mapdrop.md context)
8. Lena saves listing text to outputs/listings/
9. Remy reports weekly revenue to Anthony

## Channels
- Etsy (primary): single-city digital downloads
- Gumroad: bundle packs (5-city, 10-city)
- LemonSqueezy: monthly subscription (City Drop — 2 cities/month)

## Pricing (pending market research — placeholder)
| Product | Price |
|---------|-------|
| Single city PDF | A$8.95 |
| 5-city pack | A$24.95 |
| 10-city pack | A$39.95 |
| Physical A3 print | A$34.95 |
| Monthly sub | A$14.95/mo |

## Rules
- All output to GitHub — no local-only files
- Revenue through Cudan Studio — never Anthony personally
- QC minimum 9.5/10 — reject and rework below threshold
- Never create paid accounts without explicit Anthony instruction
- Gumroad + LemonSqueezy + Etsy for ALL digital products
- SEO every listing before publish — no exceptions
- All copy through humanizer before publish

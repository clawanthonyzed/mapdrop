# MapDrop — Business Plan

**Entity:** Cudan Studio PTY LTD
**Manager:** Remy
**Empire Day:** 41 (launched 2026-06-01)
**Target:** A$3,000/month by Day 90 (2026-07-22)

---

## Problem
People want high-quality city map prints for homes, gifts, offices. Most Etsy sellers charge $5-20 for PDFs but use low-res, outdated, or unattractive maps. Physical print services are slow and expensive.

## Solution
Instant-download city map posters generated from live OpenStreetMap data via maptoposter. Beautiful, print-ready, 300dpi. Three style variants per city. Infinite scalability — any city on earth, zero marginal cost for digital.

## Product Line

| Product | Format | Price | Channel |
|---------|--------|-------|---------|
| Single city PDF (3 styles) | Digital download | A$8.95 | Etsy, Gumroad |
| 5-city pack | Digital bundle | A$24.95 | Etsy, Gumroad |
| 10-city pack | Digital bundle | A$39.95 | Gumroad |
| A3 physical print | Print-on-demand (Printify) | A$34.95 | Etsy |
| Monthly city drop | Subscription (2 new cities/mo) | A$14.95/mo | LemonSqueezy |

## Revenue Model

**Month 1 target: A$500**
- 50 single-city sales @ A$8.95 = A$447
- 2 bundle sales @ A$24.95 = A$50
- Etsy fees (~10%): -A$50
- Net: ~A$450

**Month 2 target: A$1,500**
- 100 cities in catalog
- SEO traffic building
- First physical print orders

**Month 3 target: A$3,000**
- 200 cities in catalog
- 10+ subscription members
- Bundle sales accelerating

## Channels

### Etsy (Primary)
- Largest map print buyer audience
- SEO-optimized titles + 13 tags per listing
- Etsy ads: $0 spend (organic only per empire rules)
- Goal: 100+ active listings by Day 60

### Gumroad
- Bundle packs + city collections
- Email list capture
- No platform algorithm dependency

### LemonSqueezy
- Subscription product: "City Drop" (2 new cities/month)
- Recurring revenue base

## Tech Stack
- **maptoposter** — map generation (Python, OSM, free)
- **OpenStreetMap** — data source (free, no API key)
- **Printify** — print-on-demand fulfillment (physical only)
- **Etsy** — primary marketplace
- **Gumroad** — secondary marketplace
- **LemonSqueezy** — subscription

## Competitive Advantage
1. Zero COGS on digital — 100% margin
2. Any city on earth — competitors are catalog-limited
3. 3 style variants — more SKUs per city
4. Automated pipeline — geo can render 50 cities/day
5. OSM data updates — always current maps

## Milestones

| Day | Milestone |
|-----|-----------|
| 41 (today) | Repo live, agents created, maptoposter installed |
| 45 | 10 cities rendered, Etsy shop open, first 10 listings live |
| 55 | 50 cities in catalog, Gumroad bundles live |
| 65 | 100 cities, first physical print via Printify |
| 75 | LemonSqueezy subscription live |
| 90 | 200 cities, A$3,000/month run rate |

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Low Etsy traffic early | SEO-optimized listings, keyword research via seo-worker |
| Map quality issues | Geo QC checks all outputs, 3 variants = more chances |
| Competition | Style differentiation, faster catalog growth, better SEO |
| OSM data gaps (small cities) | Stick to top 200 cities; flag gaps |

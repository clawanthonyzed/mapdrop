# MapDrop — Execution Workflow

**Manager:** Remy
**Cadence:** Weekly sprints

---

## Step 0: Activation (one-time, before any batch work)

### 0a — Install maptoposter on server (Geo)
```bash
cd /opt/openclaw/mapdrop
git clone https://github.com/originalankur/maptoposter
cd maptoposter && pip install -r requirements.txt
python create_map_poster.py --list-themes   # confirm themes load
```

### 0b — Smoke test (Geo — MUST PASS before batch)
```bash
cd /opt/openclaw/mapdrop/mapdrop-repo
python pipeline/batch_render.py --smoke-test
```
Expected output: `Smoke test PASSED — pipeline ready for batch`
If FAILED: check maptoposter install, OSMnx, geocoding, ImageMagick.

### 0c — Dry run (Geo)
```bash
python pipeline/batch_render.py --limit 3 --dry-run
```
Confirms queue parsing and file naming before any real renders.

### 0d — Verify outputs (Geo)
After first real render:
- Open at least 2 PDFs — visually confirm map loads, roads visible, no blank tiles
- Confirm file size >100KB
- Confirm GitHub push succeeded

Only proceed to batch after all 4 steps pass.

---

## Week 1 — Launch Sprint (Days 41-48)

### Step 1: Render Tier 1 cities (Geo)
```bash
python pipeline/batch_render.py --limit 10
```
Cities: Sydney, Melbourne, Perth, Brisbane, London, New York, Paris, Tokyo, Barcelona, Amsterdam
Output: 30 files (10 cities × 3 themes: clean, dark, vibrant)

### Step 2: Open Etsy shop (Anthony — 15 min)
- Shop name: MapDrop (or MapDropAU if taken)
- Connect Cudan Studio bank account
- Category: Digital downloads / Art & Collectibles
- Return policy: Digital — no refunds (Etsy standard)
- Location: Perth, WA, Australia

### Step 3: Write first 10 listings (Lena)
For each Tier 1 city:
1. Pull PNG preview from GitHub outputs/mapdrop/previews/
2. Get SEO from seo-worker (inject agents/seo-mapdrop.md)
3. Write title, description, 13 tags using SEO output
4. Run all copy through humanizer
5. Save to: business-idea-dash/outputs/mapdrop/listings/[city-slug]-listing.md
6. Price: A$8.95 per listing (all 3 themes in one listing, 3 preview images)

### Step 4: Upload to Etsy (Lena)
- Upload 10 listings manually (API OAuth needed for automation — pending)
- Attach PDF files to each listing
- Set instant download flag
- Publish all 10

### Step 5: Set up Gumroad (Remy drafts → Anthony creates account)
- 5-city pack: A$24.95
- 10-city pack: A$39.95
- Buyer chooses cities from catalog list in product description

---

## Weekly Recurring Workflow

### Monday — Render Sprint (Geo)
1. Pull next 10 cities from city-queue.md (status: queued)
2. Run: `python pipeline/batch_render.py --limit 10`
3. QC all outputs visually (open 3 random PDFs)
4. Update city-queue.md statuses
5. Push to GitHub

### Tuesday — Listings Sprint (Lena)
1. Pull new city renders from GitHub
2. Get SEO from seo-worker for each city
3. Write + humanize all listings
4. Save to GitHub outputs/listings/
5. Upload to Etsy

### Wednesday — SEO Review (Remy → seo-worker)
1. Check Etsy Views and Favourites on top 10 listings
2. Flag any listing with <20 views after 7 days
3. seo-worker rewrites underperforming titles/tags
4. Update listings on Etsy

### Friday — Revenue Report (Remy → Anthony)
```
Week [N] Revenue Report:
- Etsy sales: [count] @ A$[total]
- Gumroad sales: [count] @ A$[total]
- Top city: [city]
- Top theme: [theme]
- New cities added: [count]
- Catalog size: [total] cities
- Next week target: [goal]
```

---

## Gumroad Setup (Week 1, Remy drafts)

Products:
1. "Any 5 City Map Pack" — A$24.95 (buyer lists cities in checkout note)
2. "Any 10 City Map Pack" — A$39.95

Process: Anthony receives order → Remy generates custom PDFs → delivers via Gumroad

---

## LemonSqueezy Subscription (Week 6)

Product: "City Drop Membership" — A$14.95/month
- 2 new city PDFs delivered each month (all 3 themes)
- Early access to new cities before Etsy
- Setup: Anthony creates LemonSqueezy account, Remy configures product

---

## Physical Prints via Printify (Week 8)

1. Anthony creates Printify account (free)
2. Remy configures A3 print product
3. Upload map PNGs as print files
4. Connect Printify → Etsy listing variant
5. Set price: A$34.95 (Printify ~A$12 cost)

---

## Quality Control Gates

Every output must score 9.5/10:

| Check | Pass | Fail |
|-------|------|------|
| PDF opens | Yes | Re-render |
| Map visible (roads, water) | Yes | Re-render |
| File size | >100KB | Re-render (blank tile) |
| City correct | Yes | Re-render (geocode error) |
| PNG preview clear | Yes | Re-render |
| Listing title | <140 chars | Rewrite |
| Listing tags | 13 unique tags | Rewrite |
| Copy humanized | Passed | Run through humanizer |

---

## File Naming Convention

```
PDFs:    [city-slug]-[theme]-A3-300dpi.pdf
         sydney-clean-A3-300dpi.pdf

Preview: [city-slug]-[theme]-preview-1200x1600.png
         sydney-clean-preview-1200x1600.png

Listing: [city-slug]-listing.md
         sydney-listing.md
```

---

## Theme Reference

| Our Name | maptoposter Theme | Use Case |
|----------|-------------------|----------|
| clean | warm_beige | Minimal, bestseller |
| dark | noir | Premium, high-contrast |
| vibrant | sunset | Colourful, gift market |

Other available: blueprint, ocean, midnight_blue, pastel_dream, japanese_ink, copper_patina, neon_cyberpunk

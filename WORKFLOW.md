# MapDrop — Execution Workflow

**Manager:** Remy
**Cadence:** Weekly sprints

---

## Week 1 — Launch Sprint (Days 41-48)

### Step 1: Infrastructure (Remy + Geo)
- [ ] Clone maptoposter to `/opt/openclaw/mapdrop/maptoposter/` on server
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Test render: Sydney minimal style → confirm PDF output
- [ ] Set up GitHub outputs folder: `business-idea-dash/outputs/mapdrop/`
- [ ] Create `/outputs/mapdrop/pdfs/`, `/outputs/mapdrop/previews/`, `/outputs/mapdrop/listings/`

### Step 2: Tier 1 City Batch (Geo)
Render all 10 Tier 1 cities × 3 styles = 30 PDFs
- Sydney, Melbourne, Perth, Brisbane, London, New York, Paris, Tokyo, Barcelona, Amsterdam
- Output: PDF (A3, 300dpi) + PNG preview (1200×1600)
- Push all to GitHub outputs

### Step 3: Open Etsy Shop (Anthony — 15 min manual task)
- Shop name: MapDrop
- Category: Digital downloads / Art prints
- Location: Perth, WA, Australia
- Payment: Cudan Studio bank account

### Step 4: Write First 10 Listings (Lena)
- One listing per Tier 1 city (all 3 styles in one listing, different photos)
- Title, description, 13 tags, A$8.95 price
- All copy through humanizer
- SEO titles via seo-worker (inject: "MapDrop, Etsy city map posters, digital download, OSM")
- Save listing text to: `business-idea-dash/outputs/mapdrop/listings/`

### Step 5: Launch
- Upload 10 listings to Etsy
- Set up Gumroad account (Remy to draft, Anthony approves and creates)
- Post first 5-city bundle on Gumroad

---

## Weekly Recurring Workflow

### Every Monday — Render Sprint (Geo)
1. Pull next 10 cities from city-queue.md
2. Render 3 styles per city (30 renders total)
3. QC check all outputs
4. Push to GitHub

### Every Tuesday — Listings Sprint (Lena)
1. Pull new city PDFs from GitHub
2. Write listing for each city
3. Humanize all copy
4. SEO optimize all titles/tags
5. Upload to Etsy

### Every Wednesday — SEO Review (seo-worker via Remy)
1. Check Etsy search ranking for top 10 listings
2. Update underperforming titles/tags
3. Research new keyword opportunities

### Every Friday — Revenue Report (Remy → Anthony)
1. Total sales this week
2. Top-performing cities/styles
3. New cities queued
4. Any issues flagged

---

## Etsy Shop Setup Checklist (Anthony — one-time)

- [ ] Create Etsy shop "MapDrop" (or "MapDropAU" if taken)
- [ ] Connect Cudan Studio bank account for payments
- [ ] Set shop announcement: "Instant-download city map prints. Any city. Beautiful quality."
- [ ] Set return policy: Digital downloads — no refunds (Etsy standard)
- [ ] Upload shop banner (Geo to design — dark map style)
- [ ] Add 10 listings from Lena's first batch

---

## Gumroad Setup (Remy drafts, Anthony approves)

Products to create:
1. "City 5-Pack" — A$24.95 (buyer chooses 5 cities from catalog)
2. "City 10-Pack" — A$39.95 (buyer chooses 10 cities)
3. Individual city packs (auto-add as catalog grows)

---

## LemonSqueezy Subscription (Week 6)

Product: "City Drop Membership"
- A$14.95/month
- 2 new city map PDFs delivered monthly
- All 3 styles included
- Early access to new cities

---

## Quality Control

Every output must score 9.5/10 minimum:
- PDF: clean render, no blank tiles, roads visible, correct city, proper DPI
- Preview: high-contrast, shows map detail, looks premium
- Listing: compelling title, keyword-rich, accurate description
- Below 9.5 = reject and re-render/rewrite

---

## File Naming Convention

```
PDFs:    [city-slug]-[style]-A3-300dpi.pdf
         sydney-minimal-A3-300dpi.pdf

Preview: [city-slug]-[style]-preview-1200x1600.png
         sydney-minimal-preview-1200x1600.png

Listing: [city-slug]-listing.md
         sydney-listing.md
```

---

## City Queue Management

File: `city-queue.md` in repo root
Columns: City | Country | Status | Rendered | Listed | Sales

Statuses: queued → rendering → QC → listed → selling

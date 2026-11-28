# MapDrop: town shortlist and personalised map product plan (Round 8)

Owner: Remy (MapDrop manager). Prepared 2026-11-28. Status: PLAN and DRAFT. Nothing is published, no shop is open, nothing is spent.
All money in Australian dollars (A$). US dollar fees converted at the Reserve Bank of Australia rate of 27 Nov 2026 (A$1.5013 per US$1, from `/opt/openclaw/logs/fx_aud.json`).

Anthony's decisions this plan follows:
1. No plain big-city posters, unless zoomed right in on one street area.
2. Target smaller towns and suburbs with enough people to buy.
3. The main product is a personalised map of any town, suburb or address.
4. Sell on our own digital product site with Lemon Squeezy as the merchant of record (takes cards and PayPal). Etsy is not first.

---

## Part 1. Twenty towns and suburbs, scored

**Population sources**
- Towns: ABS estimated resident population, June 2025, by Significant Urban Area (SUA). Source: [ABS Regional population, latest release](https://www.abs.gov.au/statistics/people/population/regional-population/latest-release). Figures were read from the table on [Wikipedia: List of cities in Australia by population](https://en.wikipedia.org/wiki/List_of_cities_in_Australia_by_population), which cites that ABS release. Check the ABS data cube before quoting any figure publicly.
- Fremantle (a suburb, not an SUA): [ABS 2021 Census QuickStats, Fremantle SAL50522](https://abs.gov.au/census/find-census-data/quickstats/2021/SAL50522), 9,251 people.

**Scores (1 to 5 each, total out of 20)**
- Identity: how strongly locals and visitors attach to the place (coast, river, heritage, holiday town).
- Buyers: residents plus holiday visitors and people who grew up there and moved away.
- Map look: how good the shape looks inside a 1.5 to 3 km circle (water edge, jetty, river bends, harbour).
- OSM detail: expected OpenStreetMap street and water detail. This is an estimate; the playbook's preview render is the real test and a town that renders thin is dropped.

| # | Place | State | Population | Source | Identity | Buyers | Map look | OSM detail | Total |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Fremantle (suburb) | WA | 9,251 (2021 Census) | QuickStats SAL50522 | 5 | 5 | 5 | 5 | **20** |
| 2 | Byron Bay | NSW | 11,482 | ABS SUA 2025 | 5 | 5 | 4 | 4 | **18** |
| 3 | Port Macquarie | NSW | 53,369 | ABS SUA 2025 | 4 | 5 | 5 | 4 | **18** |
| 4 | Albany | WA | 38,287 | ABS SUA 2025 | 4 | 4 | 5 | 4 | **17** |
| 5 | Echuca-Moama (Murray River) | VIC/NSW | 23,393 | ABS SUA 2025 | 5 | 4 | 4 | 4 | **17** |
| 6 | Nelson Bay | NSW | 29,024 | ABS SUA 2025 | 4 | 4 | 5 | 4 | **17** |
| 7 | Busselton | WA | 46,023 | ABS SUA 2025 | 4 | 4 | 4 | 4 | **16** |
| 8 | Victor Harbor-Goolwa | SA | 30,900 | ABS SUA 2025 | 4 | 4 | 4 | 4 | **16** |
| 9 | Broome | WA | 16,506 | ABS SUA 2025 | 5 | 3 | 4 | 3 | **15** |
| 10 | Geraldton | WA | 42,104 | ABS SUA 2025 | 3 | 4 | 4 | 4 | **15** |
| 11 | Ballina | NSW | 48,465 | ABS SUA 2025 | 3 | 4 | 4 | 4 | **15** |
| 12 | Forster-Tuncurry | NSW | 21,272 | ABS SUA 2025 | 3 | 3 | 5 | 4 | **15** |
| 13 | Batemans Bay | NSW | 17,849 | ABS SUA 2025 | 3 | 3 | 5 | 4 | **15** |
| 14 | Warrnambool | VIC | 36,689 | ABS SUA 2025 | 3 | 4 | 4 | 4 | **15** |
| 15 | Airlie Beach-Cannonvale | QLD | 16,597 | ABS SUA 2025 | 4 | 4 | 4 | 3 | **15** |
| 16 | Esperance | WA | 12,580 | ABS SUA 2025 | 4 | 3 | 4 | 3 | **14** |
| 17 | Port Lincoln | SA | 17,064 | ABS SUA 2025 | 3 | 3 | 4 | 3 | **13** |
| 18 | Yeppoon | QLD | 22,522 | ABS SUA 2025 | 3 | 3 | 4 | 3 | **13** |
| 19 | Mudgee (wine town, inland) | NSW | 12,965 | ABS SUA 2025 | 4 | 3 | 2 | 4 | **13** |
| 20 | Castlemaine (heritage, inland) | VIC | 11,640 | ABS SUA 2025 | 4 | 3 | 2 | 4 | **13** |

**Launch first (5):** Fremantle, Byron Bay, Port Macquarie, Albany, Echuca-Moama.
Why: the top scores, a mix of states (WA, NSW, VIC), and three different map shapes (harbour and ocean, river mouth, river bends), so the catalogue shows the range of what the personalised product can do. Fremantle is already rendered in four styles this round. Nelson Bay is the first reserve.

---

## Part 2. Personalised product plan

### 2.1 Customer flow
```
Type a town, suburb or address  ->  pick a style (4)  ->  pick a size (A4 / A3 / both)
   ->  see a preview  ->  pay (Lemon Squeezy: card or PayPal)  ->  download link by email and on the order page
```
1. **Type:** search box. Towns in the catalogue show a ready preview at once. Anything else is geocoded (turned into a map point).
2. **Pick style:** Clean (beige), Night (black), Blueprint (blue), Terracotta (warm). See the Fremantle set rendered this round.
3. **Pick size:** A4 and A3 PNG at 300 dots per inch, plus a print-ready PDF. A2 prints well from the A3 file at about 210 dots per inch (fine for a poster seen from a step back); a native A2 file needs a small renderer change because the renderer caps the canvas at 20 inches.
4. **Preview:** catalogue towns show instantly. Custom places show the nearest catalogue preview in the chosen style with the customer's own title text, plus the note "your exact map is drawn after payment, usually within 30 minutes". This avoids free renders for every visitor, which the server cannot afford.
5. **Pay:** Lemon Squeezy checkout. The place, point, radius, title, style and size ride along as custom checkout data (`checkout[custom][lat]=...` and so on; they come back in the webhook as `meta.custom_data`).
6. **Get the file:** Lemon Squeezy sends an `order_created` webhook to our server. The server checks the signature, queues the render, renders, checks the file (pixel size, file size, not blank), uploads it, and emails a download link. The order page shows the same link when ready.

### 2.2 What we build (two layers)
| Layer | What it is | How it delivers | Build effort |
|---|---|---|---|
| A. Town catalogue | Pre-rendered posters for the launch 5, then the full 20, in 4 styles | Lemon Squeezy's own digital file delivery (one product per town, one variant per style). Fully automatic, no server work per sale | Small: render, upload, write copy |
| B. Custom request | Any town, suburb or address, own title line | Webhook to a render queue on the server, then emailed link | Medium: one web page, one webhook receiver, one queue worker |

Start with Layer A (it can sell with no new code), then Layer B. The queue worker is the new script this round: `pipeline/render_on_request.py` (one render at a time, refuses when memory is low, writes the file and a 900 px preview, prints pass or fail checks).

Parts for Layer B:
- **Store page:** a small static site (the empire already deploys static sites on Vercel). Search box, style and size buttons, preview image, buy button that opens the Lemon Squeezy checkout link with custom data.
- **Geocoding:** OpenStreetMap Nominatim is free but its usage policy allows at most 1 request a second and no heavy commercial use. Fine for launch volume; switch to a paid geocoder only if orders grow (Anthony decides, Einstein gate).
- **Webhook receiver:** a small endpoint behind the existing nginx on the server. It checks the Lemon Squeezy `X-Signature` header (HMAC with the webhook secret) and writes one job row.
- **Queue worker:** a systemd service that takes one job at a time and runs `render_on_request.py`.
- **File hosting:** a private bucket with links that expire (for example Cloudflare R2 free tier). Not GitHub: customer files are private.
- **Email:** Resend free tier (3,000 a month) for the download email. Sending to customers needs Anthony's sign-off before go-live.

### 2.3 Turnaround and server limits (measured this round)
Measured on 28 Nov 2026, Fremantle, 2.5 km radius, A3 at 300 dots per inch (3537 x 4992 pixels, about 3.5 MB PNG):

| Run | Wall time | Peak memory |
|---|---|---|
| First style of a new place (downloads OpenStreetMap data) | 17 min 38 s (an earlier 0.7 km run took 9 min 42 s) | 0.63 GB |
| Each further style of the same place (cached data) | 19 to 29 s | 0.58 GB |

- Almost all the first-render time is waiting on the free public Overpass map-data service (and its fallback mirrors), not the server's processor.
- Memory: well under 1 GB per render; the shared 8 GB server usually has 1.5 to 2.5 GB free. So **one render at a time**, and the script refuses to start below 1.2 GB free (2 x the measured peak).
- Promise to customers: catalogue towns download instantly. Custom places: "usually within 30 minutes, always within 24 hours". The 24 hours covers a busy queue or an Overpass outage.
- Capacity: about 3 new places an hour, or about 120 extra styles an hour of places already cached. Far above launch volume. The public Overpass service is a shared free resource, so at volume we pre-download data per town (catalogue) or run our own map-data copy for Australia (a server cost Anthony would decide on).

### 2.4 Lemon Squeezy fit
- Lemon Squeezy is the merchant of record: it collects GST and overseas sales taxes and pays out to us.
- Fee: 5% plus US$0.50 (about A$0.75) per sale; Lemon Squeezy says sales outside the US may carry small extra fees. [Lemon Squeezy pricing](https://www.lemonsqueezy.com/pricing)
- Catalogue products use Lemon Squeezy file delivery directly.
- Custom products use checkout custom data and the `order_created` webhook. [Passing custom data](https://docs.lemonsqueezy.com/help/checkout/passing-custom-data)
- Anthony opens the Lemon Squeezy store (his account). No agent creates it.

### 2.5 Prices (recommendation, Anthony confirms)
Evidence from the last round (Etsy Australia, 26 Nov 2026): plain digital city maps A$9 to A$15; a "Custom Map Print of Any Location" at A$12.36 with 36.4k reviews; printed A3 A$45 to A$60; printed A2 A$65 to A$85. Sources are listed in the [Perth listing draft](https://github.com/clawanthonyzed/mapdrop/blob/main/outputs/drafts/20261126-perth-listing-DRAFT.md).

| Product | Recommended price | Fee to Lemon Squeezy | We keep (before income tax) | Reasoning |
|---|---|---|---|---|
| Catalogue town, digital, 1 style (A4 + A3 PNG and PDF) | **A$15** | A$1.50 | A$13.50 | Top of the A$9 to A$15 digital range; town maps are rarer than city maps and include real coast and river detail |
| Personalised, digital, any place, own title, 1 style | **A$19** | A$1.70 | A$17.30 | A$4 to A$7 above the cheapest custom-map listings, because the customer sees the style first and gets the file the same day; still an easy gift price |
| Personalised, all 4 styles | **A$29** | A$2.20 | A$26.80 | Bundle lifts the average order; extra styles cost us only cached re-renders |
| Printed A3 (later) | A$55 | not set | not set | Inside the A$45 to A$60 market. Needs a print partner quote first; the print cost is not in the repo |
| Printed A2 (later) | A$79 | not set | not set | Inside the A$65 to A$85 market; same print quote needed |

Fees worked: 5% of the price plus A$0.75 (US$0.50 at A$1.5013), before any extra overseas fee.

**Recommendation for Anthony to confirm:** launch digital only at A$15 (catalogue), A$19 (personalised), A$29 (all 4 styles). Add print later once a print partner quote is in.

### 2.6 What only Anthony can do
1. Confirm the three prices (or change them).
2. Open the Lemon Squeezy store under his account and add the payout bank account.
3. Approve the store site going live and the download email wording.

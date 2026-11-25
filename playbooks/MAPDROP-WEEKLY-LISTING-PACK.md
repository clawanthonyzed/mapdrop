# PLAYBOOK: MAPDROP WEEKLY LISTING PACK

**Venture:** mapdrop | **Owner:** remy | **Version:** 1 | **Last clean run:** never
**Standard:** a Haiku model must be able to run this with no other context and pass QC 10/10.

## 1. Trigger
Every Monday (Perth time), and whenever Anthony says "do the next MapDrop city". One run prepares ONE city: it picks the next city in the queue, checks whether the poster renderer can run on this server, and writes a DRAFT Etsy listing pack for that city. The first dollar for MapDrop needs three things: a rendered poster, listing copy, and Anthony's Etsy shop. This playbook makes the listing copy every week and tells the truth about the renderer. It never publishes, never spends, never opens an account.

## Step 0: Read lessons (mandatory)
Run on the server (from a laptop wrap it: `ssh root@46.250.244.248 "timeout 100 bash -lc '...'"`):
```
cat > /tmp/mapdrop-env.sh <<'EOF'
V=mapdrop; A=haiku-mapdrop
VD=/opt/openclaw/business/config/workspace/production/mapdrop
PB=$VD/playbooks/MAPDROP-WEEKLY-LISTING-PACK.md
DATE=$(TZ=Australia/Perth date +%Y%m%d); TASK=mapdrop-weekly-$DATE; W=/tmp/mapdrop-wk-$DATE
mkdir -p $W $VD/outputs/drafts
qc() { python3 /opt/openclaw/toolbox/scripts/step_qc.py --file "$1" --venture $V --agent $A --task $TASK --step "$2" --playbook $PB --no-links --require-lessons-read --tier haiku "${@:3}"; }
sv() { python3 /opt/openclaw/toolbox/scripts/step_save.py --venture $V --agent $A --task $TASK --step "$1" --kind step --title "$2" --file "$3"; }
EOF
. /tmp/mapdrop-env.sh
python3 /opt/openclaw/toolbox/scripts/lesson_capture.py read --playbook MAPDROP-WEEKLY-LISTING-PACK --task $TASK
```
Paste the printed lessons at the top of every worker prompt under "LESSONS (obey these)". Every later step starts with `. /tmp/mapdrop-env.sh`.

## 2. Inputs
- Queue: `/opt/openclaw/business/config/workspace/production/mapdrop/outputs/city-queue.md` (read only here).
- Spec: `/opt/openclaw/business/config/workspace/production/mapdrop/outputs/specs/POSTER-SPEC.md` (sizes, three styles, credit line, listing rules).
- Renderer: `/opt/openclaw/business/config/workspace/production/mapdrop/outputs/templates/batch_render.py` (needs the maptoposter folder and the osmnx package; neither is installed on 2026-11-25).
- Output folder: `/opt/openclaw/business/config/workspace/production/mapdrop/outputs/drafts/`.
- Price: not set. Anthony has not given a price, so every draft says so. Never invent one.

## 3. Steps

### Step 1. Pick the next queued city
- **Do:**
```
. /tmp/mapdrop-env.sh
python3 - > $W/s1-city.txt <<'EOF'
import re, datetime
rows = [l for l in open("/opt/openclaw/business/config/workspace/production/mapdrop/outputs/city-queue.md") if l.startswith("|")]
q = [[c.strip() for c in l.strip().strip("|").split("|")] for l in rows]
q = [r for r in q if len(r) >= 3 and r[2] == "queued"]
c = q[0]
print("MapDrop weekly step 1: next queued city")
print("checked_at=" + datetime.datetime.now().isoformat(timespec="seconds"))
print("rule=this check only reads files and changes nothing. A FAIL line means fix only the listed items and rerun this step.")
print("source=outputs/city-queue.md, first row whose Status is queued")
print("city=" + c[0])
print("country=" + c[1])
print("slug=" + re.sub(r"[^a-z]+", "-", c[0].lower()).strip("-"))
print("queued_rows=" + str(len(q)))
print("rule=the queue file is only read in this playbook, its Status column is never changed here")
EOF
```
- **Output file:** `/tmp/mapdrop-wk-DATE/s1-city.txt` (DATE is the Perth date as 8 digits, set by the env file).
- **Pass checks:** `qc $W/s1-city.txt 1 --min-chars 250 --require '^city=[A-Z]' --require '^slug=[a-z-]+$' --require '^queued_rows=[0-9]+$'`
- **Save:** `sv 1 "MapDrop weekly: city picked" $W/s1-city.txt`

### Step 2. Check whether the renderer can run
- **Do:**
```
. /tmp/mapdrop-env.sh
python3 - > $W/s2-render.txt <<'EOF'
import importlib.util, os, datetime
VD = "/opt/openclaw/business/config/workspace/production/mapdrop"
checks = [
 ("osmnx package", importlib.util.find_spec("osmnx") is not None),
 ("geopandas package", importlib.util.find_spec("geopandas") is not None),
 ("maptoposter folder", os.path.isdir("/opt/openclaw/mapdrop/maptoposter")),
 ("batch_render.py", os.path.isfile(VD + "/outputs/templates/batch_render.py")),
]
print("MapDrop weekly step 2: render readiness (read only, nothing is installed)")
print("checked_at=" + datetime.datetime.now().isoformat(timespec="seconds"))
print("rule=this check only reads files and changes nothing. A FAIL line means fix only the listed items and rerun this step.")
for n, ok in checks:
    print("check " + n + " = " + ("OK" if ok else "MISSING"))
ready = all(ok for _, ok in checks)
print("render_status=" + ("READY" if ready else "BLOCKED"))
print("note=" + ("all four parts present" if ready else "a missing part means no poster file can be made this week, the draft listing says so"))
print("rule=this playbook never installs packages, the manager decides on an install and states its size first")
EOF
```
- **Output file:** `/tmp/mapdrop-wk-DATE/s2-render.txt`
- **Pass checks:** `qc $W/s2-render.txt 2 --min-chars 300 --require '^render_status=(READY|BLOCKED)$' --require '^check osmnx package = (OK|MISSING)$'`
- **Save:** `sv 2 "MapDrop weekly: render readiness" $W/s2-render.txt`

### Step 3. Write the DRAFT listing file
- **Do:** write the file `$VD/outputs/drafts/DATE-SLUG-listing-DRAFT.md` (DATE and SLUG from step 1) with exactly this shape. The model fills the lines in plain English from the city name only. No claim about the city beyond its name and country.
```
# DRAFT (not published): MapDrop listing for CITYNAME
Status: DRAFT ONLY, nothing is published or posted
Render status: copy the render_status value from step 2, READY or BLOCKED
Price: not set by Anthony yet
## Title
One line, under 140 characters, starts with the city name, says custom map poster, A3 digital download.
## Tags
1. to 13. one tag per line, 13 different tags, each 20 characters or fewer.
## Description
150 to 250 words. Name the three styles: clean, dark, vibrant. Say A3 size, 300 dpi print file, digital download. Include the exact line: Map data © OpenStreetMap contributors.
If Render status is BLOCKED, add the line: Preview images are added when the poster is rendered.
## Open items for Anthony
One bullet per open item (price, Etsy shop, render install if BLOCKED).
```
- **Output file:** `/opt/openclaw/business/config/workspace/production/mapdrop/outputs/drafts/DATE-SLUG-listing-DRAFT.md`
- **Pass checks:** see step 4 (the checker runs first, then QC).
- **Save:** done in step 5.

### Step 4. Check the draft with the checker, then QC it
- **Do:**
```
. /tmp/mapdrop-env.sh
D=$(ls -t $VD/outputs/drafts/*-listing-DRAFT.md | head -1)
python3 - "$D" > $W/s4-check.txt <<'EOF'
import re, sys, datetime
t = open(sys.argv[1], encoding="utf-8").read()
fails = []
title = t.split("## Title")[1].split("##")[0].strip().splitlines()[0] if "## Title" in t else ""
tags = [re.sub(r"^\d+\.\s*", "", l).strip() for l in t.split("## Tags")[1].split("##")[0].splitlines() if re.match(r"^\d+\.", l.strip())] if "## Tags" in t else []
if not title or len(title) >= 140: fails.append("title missing or 140 characters or more")
if len(tags) != 13: fails.append("tags found: " + str(len(tags)) + ", need 13")
if len(set(x.lower() for x in tags)) != len(tags): fails.append("tags are not all different")
if any(len(x) > 20 for x in tags): fails.append("a tag is longer than 20 characters")
if "Map data © OpenStreetMap contributors." not in t: fails.append("OpenStreetMap credit line missing")
if "Price: not set by Anthony yet" not in t: fails.append("price line missing or invented")
if not re.search(r"^Render status: (READY|BLOCKED)", t, re.M): fails.append("render status line missing")
for w in ("clean", "dark", "vibrant"):
    if w not in t.lower(): fails.append("style not named: " + w)
words = len(t.split("## Description")[1].split("##")[0].split()) if "## Description" in t else 0
if not 150 <= words <= 250: fails.append("description words " + str(words) + ", need 150 to 250")
print("MapDrop weekly step 4: listing checker")
print("checked_at=" + datetime.datetime.now().isoformat(timespec="seconds"))
print("rule=this check only reads files and changes nothing. A FAIL line means fix only the listed items and rerun this step.")
print("title_chars=" + str(len(title)) + " tags=" + str(len(tags)) + " description_words=" + str(words))
print("CHECK: PASS" if not fails else "CHECK: FAIL " + "; ".join(fails))
EOF
cat $W/s4-check.txt
```
- **Output files:** `/tmp/mapdrop-wk-DATE/s4-check.txt` and the draft itself.
- **Pass checks:** `qc $W/s4-check.txt 4 --min-chars 220 --require '^CHECK: PASS$'` then `qc "$D" 4 --min-chars 900 --require '^## Open items for Anthony' --forbid '\bpublished on\b'`. On CHECK: FAIL, fix only the listed items in the draft and rerun this step.
- **Save:** `sv 4 "MapDrop weekly: checker result" $W/s4-check.txt`

### Step 5. Save the draft
- **Do:** `sv 5 "MapDrop weekly: DRAFT listing pack" "$D"` and print the draft path.
- **Output file:** the draft under `outputs/drafts/`.
- **Pass checks:** the save exits 0 (it verifies the second brain, knowledge graph and central memory).
- **Save:** this is the save.

## 4. Worked example
Step 2 output when the renderer is missing:
```
MapDrop weekly step 2: render readiness (read only, nothing is installed)
checked_at=2026-11-25T14:20:00
check osmnx package = MISSING
check geopandas package = MISSING
check maptoposter folder = MISSING
check batch_render.py = OK
render_status=BLOCKED
```
The draft then carries `Render status: BLOCKED` and the preview line.

## 5. Final deliverable
One DRAFT file per week in `mapdrop/outputs/drafts/`. Nothing is posted. When Anthony opens the Etsy shop and sets a price, the manager updates the price line and the renderer install is done first. Commit to the public MapDrop repo only after Anthony approves the text.

## 6. Escalate to Anthony only if
Money (Etsy fees, any paid tool), accounts (the Etsy shop is his), the price (owner-only fact), legal (map data licence question beyond the standard credit line).

## 7. Hard stops
Never post to Etsy or any site. Never install paid tools. Never state a render exists when step 2 says BLOCKED. Map data credit line stays on every listing (ODbL). Never change the queue Status column in this playbook. AUD only.

## Lessons learned
(lesson_capture.py promote adds lines here. One line per lesson, with its id. The manager rewrites the failing step, not only this list.)
- 2026-11-25 first Haiku run: step_qc.py rejects any file under 200 characters, so short checker outputs failed. Every checker now prints a fixed rule= line (built into the steps above).
- 2026-11-25 empire-wide: Never leave unfinished placeholder markers such as slots in brackets, braces or angle brackets in a deliverable. (seen in Cudan, DataForge and empire work)
- 2026-11-25 empire-wide: Always make sure every link in a deliverable is a real address that opens, never a template stub such as a date slot or a host variable. (seen in Cudan, DataForge and empire work)

## Credit rule (2026-11-21)
Anthony: sessions must last the full 5 hours. The big model plans and reviews once; each step of this playbook runs on a background Haiku subagent (model haiku) with the step QC script. Never run builds, scans, scrapes or bulk edits on the main model. Keep outputs short (tail, grep, counts). One artifact per round, edited not rewritten. Tell Anthony before starting a job that would use more than half a session.

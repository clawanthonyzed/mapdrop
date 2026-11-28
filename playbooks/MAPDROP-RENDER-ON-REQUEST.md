# PLAYBOOK: MAPDROP RENDER A TOWN ON REQUEST

**Venture:** mapdrop | **Owner:** remy | **Version:** 1 | **Written:** 2026-11-28 (Round 8) | **Last clean run:** 2026-11-28 (Fremantle test, see Worked example)
**Standard:** a Haiku model must be able to run this with no other context and pass QC 10/10.

## 1. Trigger
- Anthony or Remy says "render PLACE" (a town, suburb or address), or
- a paid custom order arrives (later, once the Lemon Squeezy webhook is live), or
- a catalogue town from `outputs/plans/20261128-town-shortlist-and-personalised-plan.md` needs its 4 styles.
One run = one place. It renders a small preview first, checks it, then the full A3 in the chosen style; every A3 run also writes an A4 file (resized from the A3) and a 900 px preview. It never publishes, never sends, never spends.

## Step 0: Read lessons (mandatory)
Run on the server. From a laptop wrap each block: `ssh root@46.250.244.248 "timeout 1900 bash -lc '...'"` (renders can take up to 30 minutes).
```
cat > /tmp/mapdrop-req-env.sh <<'EOF'
V=mapdrop; A=haiku-mapdrop
REPO=/opt/openclaw/repos/mapdrop
PB=$REPO/playbooks/MAPDROP-RENDER-ON-REQUEST.md
PY=/opt/openclaw/business/production/mapdrop/renderer/.venv/bin/python
RR="$PY $REPO/pipeline/render_on_request.py"
DATE=$(TZ=Australia/Perth date +%Y%m%d); TASK=mapdrop-request-$DATE; W=/tmp/mapdrop-req-$DATE
mkdir -p $W
qc() { python3 /opt/openclaw/toolbox/scripts/step_qc.py --file "$1" --venture $V --agent $A --task $TASK --step "$2" --playbook $PB --no-links --require-lessons-read --tier haiku "${@:3}"; }
sv() { python3 /opt/openclaw/toolbox/scripts/step_save.py --venture $V --agent $A --task $TASK --step "$1" --kind step --title "$2" --file "$3"; }
EOF
. /tmp/mapdrop-req-env.sh
python3 /opt/openclaw/toolbox/scripts/lesson_capture.py read --playbook MAPDROP-RENDER-ON-REQUEST --task $TASK
```
Paste the printed lessons at the top of every worker prompt under "LESSONS (obey these)". Every later step starts with `. /tmp/mapdrop-req-env.sh`.

## 2. Inputs
| Input | Example | Rule |
|---|---|---|
| ORDER | `fremantle-catalogue` | lower case letters, digits and dashes only; becomes the folder name |
| TITLE | `Fremantle` | the big name on the poster |
| SUBTITLE | `Western Australia` | second line; state for towns, the customer's words for custom orders |
| LAT, LON | `-32.0560`, `115.7530` | decimal degrees; south latitudes are negative. If only a place name is known use `--place "Town, State, Australia"` instead. For a coastal town put the point a little inland so about a third of the poster is water |
| RADIUS | `2500` | real metres from the point to the poster's short edge (the script converts it for the renderer). Town centre 1500 to 3000. One street 500 to 1000. Never above 4000 (memory) |
| STYLE | `clean` | one of: clean, night, blueprint, terracotta (also ocean, ink) |
| SIZE | `A3` | always A3 for the real file (the A4 file is made from it automatically). PREVIEW (half of A3) is only for the step 2 check |

Script: `/opt/openclaw/repos/mapdrop/pipeline/render_on_request.py` (one render at a time through a lock file; refuses when free memory is under 1,200 MB (override with MAPDROP_MIN_FREE_MB); 30 minute hard stop). Output folder: `/opt/openclaw/repos/mapdrop/outputs/orders/ORDER/`.

## 3. Steps

### Step 1. Check the server can take a render
- **Do:**
```
. /tmp/mapdrop-req-env.sh
{ echo "MapDrop request step 1: server check (read only)"
  echo "checked_at=$(date -Is)"
  echo "rule=this check only reads the server state. A FAIL line means wait 10 minutes and rerun this step, never kill another job."
  echo "free_memory_mb=$(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo)"
  echo "renders_running=$(pgrep -fc '[c]reate_map_poster.py' || true)"
  echo "disk_free_gb=$(df -BG --output=avail / | tail -1 | tr -dc 0-9)"
  echo "renderer_python=$(test -x $PY && echo OK || echo MISSING)"
  echo "script=$(test -f $REPO/pipeline/render_on_request.py && echo OK || echo MISSING)"
} > $W/s1-server.txt
```
- **Output file:** `$W/s1-server.txt`
- **Pass checks:** `qc $W/s1-server.txt 1 --min-chars 250 --require '^renders_running=0$' --require '^renderer_python=OK$' --require '^script=OK$'` and by eye: free_memory_mb at least 1200, disk_free_gb at least 5.
- **Save:** `sv 1 "MapDrop request: server check" $W/s1-server.txt`

### Step 2. Quick preview render (checks the place has enough map detail)
- **Do (fill the values from Inputs):**
```
. /tmp/mapdrop-req-env.sh
$RR --order-id ORDER --title "TITLE" --subtitle "SUBTITLE" --lat LAT --lon LON --radius RADIUS --style clean --size PREVIEW > $W/s2-preview.txt 2>&1; echo "exit=$?" >> $W/s2-preview.txt
echo "rule=PREVIEW size is a quick check only and is never sold; result=PASS means the place has enough streets and water to sell" >> $W/s2-preview.txt
```
- **Output file:** `$W/s2-preview.txt` plus `outputs/orders/ORDER/*-clean-PREVIEW-preview-900.jpg`
- **Pass checks:** `qc $W/s2-preview.txt 2 --min-chars 250 --require '^result=PASS$' --require '^exit=0$'`. Then the reviewing model opens the 900 px JPG and confirms: streets fill the circle, water (if any) is blue or dark, the title is spelled right. If streets are sparse, raise RADIUS by 500 and rerun this step once; if still sparse, stop and report "not enough OpenStreetMap detail".
- **If exit=2 (REFUSED):** another render or low memory. Wait 10 minutes, rerun. Never kill another render.
- **Save:** `sv 2 "MapDrop request: preview check" $W/s2-preview.txt`

### Step 3. Full render in the chosen style and size
- **Do:**
```
. /tmp/mapdrop-req-env.sh
$RR --order-id ORDER --title "TITLE" --subtitle "SUBTITLE" --lat LAT --lon LON --radius RADIUS --style STYLE --size A3 > $W/s3-full.txt 2>&1; echo "exit=$?" >> $W/s3-full.txt
echo "rule=full files are 300 dpi; the map data is cached from step 2 so this run is faster" >> $W/s3-full.txt
```
For a catalogue town, repeat step 3 for each of clean, night, blueprint, terracotta (one at a time, never in parallel).
- **Output file:** `$W/s3-full.txt`, `outputs/orders/ORDER/TITLE-STYLE-A3-300dpi.png`, `TITLE-STYLE-A4-300dpi.png` and `TITLE-STYLE-A3-preview-900.jpg` (TITLE in lower case, spaces as dashes)
- **Pass checks:** `qc $W/s3-full.txt 3 --min-chars 300 --require '^result=PASS$' --require '^exit=0$' --require 'pixels=3[0-9]{3}x4[0-9]{3}' --require '^check a4_pixels=2480x3508$'`. Reviewer opens the 900 px JPG once.
- **Save:** `sv 3 "MapDrop request: full render" $W/s3-full.txt`

### Step 4. Store the file
- **Catalogue towns (public samples):** copy the A3 PNG to `outputs/mapdrop/posters/TOWN-STYLE-A3-300dpi.png`, then
```
cd $REPO && git add outputs/mapdrop/posters/ && git commit -m "feat(mapdrop): TOWN posters" && git push && gh api repos/clawanthonyzed/mapdrop/contents/outputs/mapdrop/posters --jq '.[].name' > $W/s4-store.txt
echo "rule=a file counts as stored only when its name appears in this GitHub listing" >> $W/s4-store.txt
```
- **Customer orders:** customer files are private. Leave them in `outputs/orders/` (that folder is git-ignored) until the private file store is live. Never push a customer order to GitHub.
- **Pass checks:** `qc $W/s4-store.txt 4 --min-chars 150 --require 'TOWN-STYLE-A3-300dpi.png'` (catalogue only).
- **Save:** `sv 4 "MapDrop request: stored" $W/s4-store.txt`

## 4. Worked example (Fremantle, 2026-11-28)
Inputs: ORDER=fremantle-catalogue, TITLE=Fremantle, SUBTITLE=Western Australia, LAT=-32.0560, LON=115.7530, RADIUS=2500.
Result lines from the test run are recorded in the Round 8 result file. Four styles were rendered at A3: clean, night, blueprint, terracotta, and pushed to `outputs/mapdrop/posters/fremantle-*-A3-300dpi.png`.

## 5. Final deliverable
For a catalogue town: 4 A3 PNG files on GitHub plus 900 px previews. For a custom order: the PNG files in the order folder, ready for the delivery step (private link and email, which is not built yet and needs Anthony's sign-off).

## 6. Escalate to Anthony only if
Money (a bigger server, a paid geocoder, file storage beyond free tiers), accounts (Lemon Squeezy is his), customer contact (refund or wording), legal (a map data question beyond the OpenStreetMap credit line).

## 7. Hard stops
- One render at a time. Never run two. Never kill another job's render.
- RADIUS never above 4000 metres (memory).
- Geocoding goes through OpenStreetMap Nominatim: at most 1 lookup a second, never bulk lookups, never a scraper.
- Never publish, list, post or email anything. Never push a customer's order or address to GitHub.
- Keep the credit line "Map data © OpenStreetMap contributors (ODbL)" on every listing.
- AUD only for any price mentioned. No price is final until Anthony confirms it.

## Lessons learned
(lesson_capture.py promote adds lines here. One line per lesson, with its id.)
- 2026-11-28 Round 8: create_map_poster.py must run with its own folder as the working directory, or it fails with "No themes found". render_on_request.py sets this itself; never call the renderer from another folder.
- 2026-11-28 Round 8: the first render of a new place spends most of its time downloading OpenStreetMap data (water features are slowest). Repeat styles of the same place reuse the cache, so always render all styles of one place back to back.
- 2026-11-28 Round 8: the renderer's --distance is NOT the visible radius. It shows only distance x (long side / short side) / 4 metres from the centre, so --distance 2000 gave a 700 m view of Fremantle with no coast. render_on_request.py takes the real radius and converts it; never call the renderer with a raw distance.
- 2026-11-25 empire-wide: Never leave unfinished placeholder markers in a deliverable. Never give a link that does not open.

## Credit rule (2026-11-21)
Anthony: sessions must last the full 5 hours. The big model plans and reviews once; each step of this playbook runs on a background Haiku subagent (model haiku) with the step QC script. Never run builds, scans, scrapes or bulk edits on the main model. Keep outputs short (tail, grep, counts). One artifact per round, edited not rewritten. Tell Anthony before starting a job that would use more than half a session.

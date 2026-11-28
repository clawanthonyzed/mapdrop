#!/usr/bin/env python3
"""MapDrop: render ONE personalised town, suburb or address poster on request.

Safe wrapper around maptoposter/create_map_poster.py for the 8 GB shared server:
- one render at a time (file lock), refuses to start below the free-memory floor
- named sizes (A4, A3) and named styles (clean, night, blueprint, terracotta, ocean, ink)
- writes the full-size PNG plus a 900 px wide JPG preview into one order folder
- prints key=value check lines so step_qc.py can verify the run

Usage (on the server):
  /opt/openclaw/business/production/mapdrop/renderer/.venv/bin/python \
    /opt/openclaw/repos/mapdrop/pipeline/render_on_request.py \
    --order-id test-fremantle --title Fremantle --subtitle "Western Australia" \
    --lat -32.0540 --lon 115.7500 --radius 2000 --style clean --size A3

  --place "Busselton, Western Australia" can replace --lat/--lon (geocoded by the
  renderer through OpenStreetMap Nominatim: keep to 1 lookup per second, never bulk).
Exit codes: 0 rendered and checked, 1 render or check failed, 2 refused (busy or low memory).
"""
import argparse
import datetime
import fcntl
import glob
import os
import shutil
import subprocess
import sys
import time

RENDERER = "/opt/openclaw/business/production/mapdrop/renderer"
MAPTOPOSTER = os.path.join(RENDERER, "maptoposter")
PYTHON = os.path.join(RENDERER, ".venv", "bin", "python")
ORDERS = "/opt/openclaw/repos/mapdrop/outputs/orders"
LOCK = "/tmp/mapdrop-render.lock"
MIN_FREE_MB = int(os.environ.get("MAPDROP_MIN_FREE_MB", "1200"))  # A3 town render peaked at 0.63 GB (Fremantle 2026-11-28); 2x headroom
TIMEOUT_S = 1800            # 30 minutes hard stop per render

STYLES = {                  # product name -> maptoposter theme file
    "clean": "warm_beige",
    "night": "noir",
    "blueprint": "blueprint",
    "terracotta": "terracotta",
    "ocean": "ocean",
    "ink": "japanese_ink",
}
SIZES = {                   # inches (width, height); PNG is saved at 300 dpi
    "A3": (11.69, 16.54),   # every A3 run also writes an A4 file, resized from the A3 (sharper than a separate A4 render)
    "PREVIEW": (11.69 / 2, 16.54 / 2),  # quick check; exactly half of A3 so the map data cache is shared
}
A4_PIXELS = (2480, 3508)    # A4 at 300 dpi


def free_mb():
    with open("/proc/meminfo") as f:
        info = {l.split(":")[0]: int(l.split()[1]) for l in f}
    return info.get("MemAvailable", 0) // 1024


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--order-id", required=True)
    ap.add_argument("--title", required=True, help="Big name on the poster, for example the town")
    ap.add_argument("--subtitle", default="Australia", help="Second line, for example the state")
    ap.add_argument("--lat")
    ap.add_argument("--lon")
    ap.add_argument("--place", help="Free text place to geocode when lat/lon are not given")
    ap.add_argument("--radius", type=int, default=2500,
                    help="real metres from the centre to the poster's short edge (town 1500 to 3000, one street 500 to 1000)")
    ap.add_argument("--style", choices=sorted(STYLES), default="clean")
    ap.add_argument("--size", choices=sorted(SIZES), default="A3")
    a = ap.parse_args()

    if not (a.lat and a.lon) and not a.place:
        print("result=FAIL reason=give --lat and --lon, or --place")
        return 1
    if not 400 <= a.radius <= 4000:
        print("result=FAIL reason=radius must be 400 to 4000 metres")
        return 1

    lock = open(LOCK, "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("result=REFUSED reason=another MapDrop render is running, try again later")
        return 2
    mem = free_mb()
    print(f"check free_memory_mb={mem} floor={MIN_FREE_MB}")
    if mem < MIN_FREE_MB:
        print("result=REFUSED reason=not enough free memory, try again later")
        return 2

    out_dir = os.path.join(ORDERS, a.order_id)
    os.makedirs(out_dir, exist_ok=True)
    w, h = SIZES[a.size]
    theme = STYLES[a.style]
    city_arg = a.place.split(",")[0].strip() if a.place else a.title
    country_arg = a.place.split(",", 1)[1].strip() if a.place and "," in a.place else "Australia"
    # maptoposter shows only distance * (long side / short side) / 4 metres from the centre,
    # so convert the real radius the customer wants into the renderer's --distance value.
    # PREVIEW is exactly half of A3, so both give the same --distance and the same renderer cache keys:
    # the preview run downloads the map data once and the A3 run reuses it.
    distance = int(round(a.radius * 4 / (16.54 / 11.69)))

    print(f"check radius_m={a.radius} renderer_distance={distance}")
    cmd = [PYTHON, "create_map_poster.py", "--city", city_arg, "--country", country_arg,
           "--display-city", a.title, "--display-country", a.subtitle,
           "--distance", str(distance), "--width", str(w), "--height", str(h), "--theme", theme]
    if a.lat and a.lon:
        cmd += ["--latitude", str(a.lat), "--longitude", str(a.lon)]

    before = set(glob.glob(os.path.join(MAPTOPOSTER, "posters", "*.png")))
    t0 = time.time()
    log_path = os.path.join(out_dir, f"render-{a.style}-{a.size}.log")
    with open(log_path, "w") as log:
        try:
            rc = subprocess.run(cmd, cwd=MAPTOPOSTER, stdout=log, stderr=subprocess.STDOUT,
                                timeout=TIMEOUT_S).returncode
        except subprocess.TimeoutExpired:
            rc = 124
    secs = int(time.time() - t0)
    new = sorted(set(glob.glob(os.path.join(MAPTOPOSTER, "posters", "*.png"))) - before)
    print(f"check render_exit_code={rc}")
    print(f"check render_seconds={secs}")
    if rc != 0 or not new:
        print(f"result=FAIL reason=renderer failed, see {log_path}")
        return 1

    slug = a.title.lower().replace(" ", "-")
    final = os.path.join(out_dir, f"{slug}-{a.style}-{a.size}-300dpi.png")
    shutil.move(new[-1], final)
    size_kb = os.path.getsize(final) // 1024

    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(final)
    px_w, px_h = im.size
    colours = len(im.convert("RGB").resize((200, 280)).getcolors(200 * 280) or [])
    prev = im.convert("RGB")
    prev.thumbnail((900, 900 * px_h // px_w))
    preview = final.replace("-300dpi.png", "-preview-900.jpg")
    prev.save(preview, "JPEG", quality=85)
    if a.size == "A3":
        a4 = final.replace("-A3-300dpi.png", "-A4-300dpi.png")
        im.resize(A4_PIXELS, Image.LANCZOS).save(a4, dpi=(300, 300))
        print(f"a4_png={a4}")
        print(f"check a4_pixels={A4_PIXELS[0]}x{A4_PIXELS[1]}")

    ok_size = size_kb >= 300
    ok_px = px_w >= int(w * 300 * 0.9)
    ok_colours = colours >= 20          # a blank or one-colour poster has very few colours
    print(f"check file_kb={size_kb} pass={ok_size}")
    print(f"check pixels={px_w}x{px_h} pass={ok_px}")
    print(f"check distinct_colours_sample={colours} pass={ok_colours}")
    print(f"final_png={final}")
    print(f"preview_jpg={preview}")
    print(f"rendered_at={datetime.datetime.now().isoformat(timespec='seconds')}")
    print("rule=map data from OpenStreetMap contributors (ODbL); credit line stays on every listing")
    if ok_size and ok_px and ok_colours:
        print("result=PASS")
        return 0
    print("result=FAIL reason=output check failed, look at the preview before anything else")
    return 1


if __name__ == "__main__":
    sys.exit(main())

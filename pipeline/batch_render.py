#!/usr/bin/env python3
"""
MapDrop Batch Renderer — Geo's production pipeline.
Reads city-queue.md, renders queued cities via maptoposter, pushes to GitHub outputs.

Install:
    cd /opt/openclaw/mapdrop
    git clone https://github.com/originalankur/maptoposter
    cd maptoposter && pip install -r requirements.txt

Smoke test first:
    python pipeline/batch_render.py --smoke-test

Production run:
    python pipeline/batch_render.py --limit 10
"""

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT    = Path(__file__).parent.parent
QUEUE_FILE   = REPO_ROOT / "city-queue.md"
MAPTOPOSTER  = Path("/opt/openclaw/mapdrop/maptoposter")
OUTPUT_PDF   = Path("/opt/openclaw/outputs/mapdrop/pdfs")
OUTPUT_PNG   = Path("/opt/openclaw/outputs/mapdrop/previews")
DASH_REPO    = Path("/opt/openclaw/repos/business-idea-dash")
QUALITY_MIN_KB = 100  # renders smaller than this are blank/broken

# Themes mapped to our product names
# Run `python create_map_poster.py --list-themes` to see all available
THEMES = {
    "clean":   "warm_beige",   # white/neutral — bestseller
    "dark":    "noir",         # black bg, high contrast — premium
    "vibrant": "sunset",       # colour — gift market
}


def parse_queue(queue_file: Path) -> list[dict]:
    cities = []
    with open(queue_file) as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|") or "City" in line or "---" in line:
                continue
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 3 and parts[2].strip() == "queued":
                cities.append({"city": parts[0], "country": parts[1]})
    return cities


def update_queue_status(city_name: str, new_status: str):
    content = QUEUE_FILE.read_text()
    lines = []
    for line in content.splitlines():
        if f"| {city_name} |" in line:
            parts = line.split("|")
            parts[3] = f" {new_status} "
            line = "|".join(parts)
        lines.append(line)
    QUEUE_FILE.write_text("\n".join(lines))


def city_slug(city: str) -> str:
    return city.lower().replace(" ", "-").replace(",", "")


def render_city(city: str, country: str, theme_key: str, dry_run: bool = False) -> Path | None:
    theme_val = THEMES[theme_key]
    slug = city_slug(city)
    pdf_name = f"{slug}-{theme_key}-A3-300dpi.pdf"
    pdf_out  = OUTPUT_PDF / pdf_name

    if dry_run:
        print(f"  [DRY] {city}, {country} / {theme_key} ({theme_val}) → {pdf_name}")
        return pdf_out

    OUTPUT_PDF.mkdir(parents=True, exist_ok=True)
    OUTPUT_PNG.mkdir(parents=True, exist_ok=True)

    # Render PNG via maptoposter
    cmd = [
        sys.executable, str(MAPTOPOSTER / "create_map_poster.py"),
        "--city", city,
        "--country", country,
        "--theme", theme_val,
        "--width", "12",    # 12 × 16 in = ~A3 at 300dpi
        "--height", "16",
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=180, cwd=MAPTOPOSTER
        )
        if result.returncode != 0:
            print(f"  ERROR {city}/{theme_key}: {result.stderr[:300]}")
            return None
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT {city}/{theme_key} >180s")
        return None
    except FileNotFoundError:
        print(f"  ERROR: create_map_poster.py not found at {MAPTOPOSTER}")
        print(f"  Run: git clone https://github.com/originalankur/maptoposter {MAPTOPOSTER}")
        return None

    # Locate the output PNG (saved to maptoposter/posters/ with timestamp)
    poster_dir = MAPTOPOSTER / "posters"
    pngs = sorted(poster_dir.glob(f"{city.lower()}*{theme_val}*.png"))
    if not pngs:
        # Fallback: newest PNG in posters/
        all_pngs = sorted(poster_dir.glob("*.png"), key=os.path.getmtime, reverse=True)
        pngs = all_pngs[:1]

    if not pngs:
        print(f"  ERROR: no PNG output found for {city}/{theme_key}")
        return None

    src_png = pngs[-1]
    png_name = f"{slug}-{theme_key}-preview-1200x1600.png"
    png_dest = OUTPUT_PNG / png_name
    shutil.copy2(src_png, png_dest)

    # Convert PNG → PDF via ImageMagick
    try:
        subprocess.run(
            ["convert", str(png_dest), "-density", "300", str(pdf_out)],
            check=True, timeout=60
        )
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"  WARN: PDF convert failed ({e}) — PNG saved, PDF skipped")
        return png_dest  # return PNG path so QC can still check

    print(f"  OK: {pdf_name}")
    return pdf_out


def qc_check(path: Path) -> bool:
    if not path or not path.exists():
        print(f"  QC FAIL: file missing")
        return False
    size_kb = path.stat().st_size / 1024
    if size_kb < QUALITY_MIN_KB:
        print(f"  QC FAIL: {path.name} only {size_kb:.0f}KB — likely blank render")
        return False
    return True


def smoke_test() -> bool:
    """Activation test — render Sydney/clean, verify output before batch run."""
    print("=== SMOKE TEST: Sydney, Australia (clean theme) ===")
    out = render_city("Sydney", "Australia", "clean", dry_run=False)
    passed = qc_check(out)
    if passed:
        print("Smoke test PASSED — pipeline ready for batch")
    else:
        print("Smoke test FAILED — fix maptoposter before running batch")
    return passed


def push_to_github(files: list[Path]):
    if not DASH_REPO.exists():
        subprocess.run(
            ["git", "clone",
             "https://github.com/clawanthonyzed/business-idea-dash.git",
             str(DASH_REPO)],
            check=True, timeout=60
        )

    for src in files:
        if not src or not src.exists():
            continue
        if "preview" in src.name or src.suffix == ".png":
            dest = DASH_REPO / "outputs" / "mapdrop" / "previews" / src.name
        else:
            dest = DASH_REPO / "outputs" / "mapdrop" / "pdfs" / src.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

    subprocess.run(["git", "add", "outputs/mapdrop/"], cwd=DASH_REPO, check=True)
    diff = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=DASH_REPO)
    if diff.returncode != 0:
        subprocess.run(
            ["git", "commit", "-m",
             f"feat(mapdrop): add {len(files)} rendered city maps"],
            cwd=DASH_REPO, check=True
        )
        subprocess.run(["git", "push"], cwd=DASH_REPO, check=True)
        print(f"Pushed {len(files)} files to GitHub")
    else:
        print("No new files to push")


def main():
    parser = argparse.ArgumentParser(description="MapDrop batch city map renderer")
    parser.add_argument("--limit", type=int, default=10, help="Max cities per run")
    parser.add_argument("--themes", default="clean,dark,vibrant",
                        help="Comma-separated theme keys to render")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--smoke-test", action="store_true",
                        help="Run activation smoke test only — renders Sydney/clean")
    args = parser.parse_args()

    if args.smoke_test:
        ok = smoke_test()
        sys.exit(0 if ok else 1)

    themes = [t.strip() for t in args.themes.split(",") if t.strip() in THEMES]
    cities = parse_queue(QUEUE_FILE)[:args.limit]

    if not cities:
        print("No queued cities. Update city-queue.md.")
        return

    print(f"Rendering {len(cities)} cities × {len(themes)} themes "
          f"= {len(cities)*len(themes)} maps")

    all_outputs = []
    for row in cities:
        city, country = row["city"], row["country"]
        print(f"\n[{city}, {country}]")
        city_outputs, failed = [], False

        for theme_key in themes:
            out = render_city(city, country, theme_key, dry_run=args.dry_run)
            if qc_check(out):
                city_outputs.append(out)
            else:
                failed = True

        status = "rendered" if not failed and len(city_outputs) == len(themes) else "error"
        update_queue_status(city, status)

        if status == "rendered":
            all_outputs.extend(city_outputs)
            print(f"  {city} — {len(city_outputs)} files OK")
        else:
            print(f"  {city} — FAILED (partial: {len(city_outputs)}/{len(themes)})")

    if not args.dry_run and all_outputs:
        push_to_github(all_outputs)

    print(f"\nDone. {len(all_outputs)} files rendered.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""MapDrop water-layer patch for maptoposter/create_map_poster.py (idempotent)."""
import sys
from pathlib import Path

p = Path(sys.argv[1])
src = p.read_text()
if "MAPDROP_WATER_PATCH" in src:
    print("already patched")
    sys.exit(0)

helper = '''

# MAPDROP_WATER_PATCH: sea from OSM coastlines, rivers as lines, more inland water tags
def build_sea_polygons(point, dist, crs):
    """Build sea polygons inside the map box from natural=coastline ways.

    OSM coastline ways run with land on the LEFT and water on the RIGHT.
    The box is cut into faces by the coastline; each face is voted sea or land
    by probe points offset to either side of every coastline segment.
    """
    from shapely.geometry import box as _box, LineString, MultiLineString
    from shapely.ops import unary_union, polygonize
    from shapely import STRtree
    import geopandas as gpd

    coast = fetch_features(point, dist * 1.6, tags={"natural": "coastline"}, name="coastline")
    if coast is None or coast.empty:
        return None
    coast = coast[coast.geometry.type.isin(["LineString", "MultiLineString"])]
    if coast.empty:
        return None
    coast = coast.to_crs(crs)
    c = gpd.GeoSeries([Point(point[1], point[0])], crs="EPSG:4326").to_crs(crs).iloc[0]
    d = dist * 1.15
    frame = _box(c.x - d, c.y - d, c.x + d, c.y + d)

    lines = []
    for geom in coast.geometry:
        parts = geom.geoms if isinstance(geom, MultiLineString) else [geom]
        lines.extend(parts)
    if not lines:
        return None
    noded = unary_union([frame.boundary] + [l for l in lines if l.intersects(frame)])
    faces = [f for f in polygonize(noded) if f.within(frame.buffer(1))]
    if not faces:
        return None

    probes, signs = [], []
    off = 3.0
    for l in lines:
        if not l.intersects(frame):
            continue
        coords = list(l.coords)
        step = max(1, len(coords) // 400)
        for i in range(0, len(coords) - 1, step):
            (x1, y1), (x2, y2) = coords[i][:2], coords[i + 1][:2]
            dx, dy = x2 - x1, y2 - y1
            n = (dx * dx + dy * dy) ** 0.5
            if n < 1e-6:
                continue
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            rx, ry = dy / n * off, -dx / n * off
            probes.append(Point(mx + rx, my + ry)); signs.append(1)   # right = water
            probes.append(Point(mx - rx, my - ry)); signs.append(-1)  # left = land
    if not probes:
        return None
    tree = STRtree(faces)
    pidx, fidx = tree.query(probes, predicate="within")
    votes = [0] * len(faces)
    for pi, fi in zip(pidx, fidx):
        votes[fi] += signs[pi]
    sea = [f for f, v in zip(faces, votes) if v > 0]
    if not sea:
        return None
    return gpd.GeoDataFrame(geometry=sea, crs=crs)

'''

anchor = "\ndef create_poster("
assert anchor in src
src = src.replace(anchor, helper + anchor, 1)

old_tags = 'tags={"natural": ["water", "bay", "strait"], "waterway": "riverbank"},\n            name="water",'
new_tags = ('tags={"natural": ["water", "bay", "strait"], "waterway": "riverbank",'
            ' "landuse": ["reservoir", "basin"]},\n            name="water_v2",')
assert old_tags in src
src = src.replace(old_tags, new_tags, 1)

old_plot = "            water_polys.plot(ax=ax, facecolor=THEME['water'], edgecolor='none', zorder=0.5)\n"
new_plot = old_plot + '''
    # MAPDROP_WATER_PATCH: sea polygons and river lines
    try:
        sea = build_sea_polygons(point, compensated_dist, g_proj.graph['crs'])
        if sea is not None and not sea.empty:
            sea.plot(ax=ax, facecolor=THEME['water'], edgecolor='none', zorder=0.45)
            print(f"✓ Sea polygons: {len(sea)}")
    except Exception as e:
        print(f"WARN sea build failed: {e}")
    try:
        rivers = fetch_features(point, compensated_dist,
                                tags={"waterway": ["river", "canal"]}, name="rivers")
        if rivers is not None and not rivers.empty:
            rl = rivers[rivers.geometry.type.isin(["LineString", "MultiLineString"])]
            if not rl.empty:
                rl.to_crs(g_proj.graph['crs']).plot(ax=ax, color=THEME['water'],
                                                    linewidth=1.6, zorder=0.55)
    except Exception as e:
        print(f"WARN rivers failed: {e}")
'''
assert old_plot in src
src = src.replace(old_plot, new_plot, 1)

# wetland should not be water-coloured if it is a big swamp? keep: most AU wetlands read as water.
p.write_text(src)
print("patched")

"""
parse_content.py

Reads everything under "User Input/" and turns it into plain Python data:
- portfolio entries (builds + events, photos + YouTube-highlight entries)
- product entries (3d-printed, spare-deals, used-blasters)
- brand entries

Also builds the case-insensitive keyword index that cross-links all of the
above (build <-> product <-> brand <-> gallery filter).

This module has NO knowledge of HTML — it just returns clean data structures.
render_dynamic.py consumes this to actually build the pages.
"""

import os
import re
import glob

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "User Input")


def slugify(name):
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def parse_txt(path):
    """Parses a simple 'Key: value' txt file. Multi-line values (Breakdown)
    are supported by treating any non-'Key:' line as a continuation of the
    previous key's value."""
    fields = {}
    last_key = None
    if not os.path.exists(path):
        return fields
    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.rstrip("\r\n")
            if not line.strip():
                # a blank line inside a Breakdown is a paragraph break
                if last_key == "Breakdown" and not fields[last_key].endswith("\n\n"):
                    fields[last_key] = fields[last_key].rstrip("\n") + "\n\n"
                continue
            m = re.match(r"^([A-Za-z][A-Za-z0-9 ]*):\s*(.*)$", line)
            if m and m.group(1).strip() in KNOWN_KEYS:
                key = m.group(1).strip()
                fields[key] = m.group(2).strip()
                last_key = key
            elif last_key == "Captions":
                fields[last_key] += "\n" + line.strip()
            elif last_key == "Breakdown":
                cur = fields[last_key]
                fields[last_key] = cur + (line.strip() if cur.endswith("\n\n") else "\n" + line.strip())
            elif last_key:
                fields[last_key] += " " + line.strip()
    return fields


KNOWN_KEYS = {
    "Title", "Description", "Breakdown", "Type", "Location", "Keywords",
    "YouTube", "Hover Start", "Highlight Length", "Captions", "Ask About", "Ask Prefill", "Brand", "Status", "Price", "Supplier Link", "Priority", "Series",
}


def parse_captions(raw):
    """Captions field -> {number: text}. One caption per line, e.g.
         1: Front view with the suppressor fitted
         Image 2: Close-up of the hop-up
       "image", "photo" and "pic" before the number are allowed; the separator
       can be : . ) or -. A line with no number carries on the previous caption."""
    out, last = {}, None
    for line in (raw or "").split("\n"):
        line = line.strip()
        if not line:
            continue
        m = re.match(r"^(?:image|photo|pic)?[ _]*(\d+)\s*[:.)\-]\s*(.*)$", line, re.I)
        if m:
            last = int(m.group(1))
            out[last] = m.group(2).strip()
        elif last is not None:
            out[last] = (out[last] + " " + line).strip()
    return {k: v for k, v in out.items() if v}


def parse_length(raw, default=20):
    """Highlight Length: "60", "60s", "1:00" -> seconds. Blank/invalid -> default (20)."""
    raw = (raw or "").strip().lower().rstrip("s").strip()
    if not raw:
        return default
    try:
        if ":" in raw:
            sec = 0
            for x in raw.split(":"):
                sec = sec * 60 + int(x)
        else:
            sec = int(float(raw))
    except ValueError:
        return default
    return min(max(sec, 5), 600)


def parse_priority(raw):
    """'Priority: 1' -> 1.0. Blank, missing or non-numeric -> None (unranked)."""
    if raw is None:
        return None
    try:
        return float(str(raw).strip())
    except ValueError:
        return None


def series_key(entry):
    return (entry.get("series") or "").strip().lower()


def group_series(entries):
    """Keep entries that share a Series name next to each other. The group sits where its first
    member would have been, and members keep their own order. Entries with no Series are untouched."""
    out, done = [], set()
    for e in entries:
        k = series_key(e)
        if not k:
            out.append(e)
        elif k not in done:
            done.add(k)
            out.extend(x for x in entries if series_key(x) == k)
    return out


def priority_sort_key(entry):
    """Lowest Priority number first. Entries with no Priority come after all
    numbered ones. Ties (and all unranked entries) fall back to A-Z by title."""
    pr = entry.get("priority")
    return (pr is None, pr if pr is not None else 0, entry["title"].lower())


def parse_keywords_field(raw):
    """'flash-bang (1:32), 3d-printed (0:45), cqb-loadout' ->
    [{'kw': 'flash-bang', 'ts': '1:32'}, {'kw': '3d-printed', 'ts': '0:45'},
     {'kw': 'cqb-loadout', 'ts': None}]"""
    if not raw:
        return []
    out = []
    for chunk in raw.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        m = re.match(r"^(.*?)\s*\(([\d:]+)\)\s*$", chunk)
        if m:
            out.append({"kw": m.group(1).strip(), "ts": m.group(2).strip()})
        else:
            out.append({"kw": chunk, "ts": None})
    return out


def timestamp_to_seconds(ts):
    if not ts:
        return None
    parts = [int(p) for p in ts.split(":")]
    secs = 0
    for p in parts:
        secs = secs * 60 + p
    return secs


def group_numbered_files(files, base_stem):
    """Given a list of filenames and a base stem (e.g. 'flash-bang-carry'),
    returns them ordered: exact match first, then '<stem> 2', '<stem> 3'...
    Gaps are fine, non-numbered/unrelated files are ignored."""
    exact = None
    numbered = []
    for f in files:
        stem, ext = os.path.splitext(os.path.basename(f))
        if stem == base_stem:
            exact = f
        else:
            m = re.match(r"^" + re.escape(base_stem) + r"[ _](\d+)$", stem)
            if m:
                numbered.append((int(m.group(1)), f))
    numbered.sort(key=lambda t: t[0])
    result = []
    if exact:
        result.append(exact)
    result.extend(f for _, f in numbered)
    return result


IMG_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def parse_portfolio():
    folder = os.path.join(ROOT, "portfolio")
    if not os.path.isdir(folder):
        return []
    txt_files = glob.glob(os.path.join(folder, "*.txt"))
    all_files = [f for f in os.listdir(folder) if f != "README.md"]
    entries = []
    for txt_path in txt_files:
        stem = os.path.splitext(os.path.basename(txt_path))[0]
        fields = parse_txt(txt_path)
        if not fields.get("Title"):
            continue
        matching_imgs = [
            f for f in all_files
            if os.path.splitext(f)[1].lower() in IMG_EXTS
            and (os.path.splitext(f)[0] == stem
                 or re.match(r"^" + re.escape(stem) + r"[ _]\d+$", os.path.splitext(f)[0]))
        ]
        images = group_numbered_files(matching_imgs, stem)
        if not images and fields.get("YouTube"):
            # No picture supplied: use the video's own YouTube thumbnail
            ym = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{6,})", fields.get("YouTube"))
            if ym:
                images = [f"https://i.ytimg.com/vi/{ym.group(1)}/maxresdefault.jpg"]
        entries.append({
            "slug": slugify(stem),
            "raw_name": stem,
            "title": fields.get("Title", stem),
            "description": fields.get("Description", ""),
            "breakdown": fields.get("Breakdown", ""),
            "type": fields.get("Type", "Build"),
            "location": fields.get("Location", ""),
            "keywords": parse_keywords_field(fields.get("Keywords", "")),
            "images": images,
            "captions": parse_captions(fields.get("Captions", "")),
            "ask_about": (fields.get("Ask About") or "").strip(),
            "ask_prefill": (fields.get("Ask Prefill") or "").strip(),
            "youtube": fields.get("YouTube") or None,
            "hover_start": fields.get("Hover Start") or None,
            "highlight_length": parse_length(fields.get("Highlight Length")),
            "priority": parse_priority(fields.get("Priority")),
            "series": (fields.get("Series") or "").strip(),
        })
    entries.sort(key=priority_sort_key)
    entries = group_series(entries)
    return entries


def parse_product_folder(section_path, section_name):
    if not os.path.isdir(section_path):
        return []
    entries = []
    for item_name in sorted(os.listdir(section_path)):
        item_path = os.path.join(section_path, item_name)
        if not os.path.isdir(item_path):
            continue
        info_path = os.path.join(item_path, "info.txt")
        if not os.path.exists(info_path):
            continue
        fields = parse_txt(info_path)
        if not fields.get("Title"):
            continue
        images = sorted([
            f for f in os.listdir(item_path)
            if os.path.splitext(f)[1].lower() in IMG_EXTS
        ])
        # main thumbnail = file matching folder name, else first alphabetically
        stem_match = [f for f in images if os.path.splitext(f)[0] == item_name]
        ordered = group_numbered_files(images, item_name) if stem_match else images
        entries.append({
            "slug": slugify(item_name),
            "raw_name": item_name,
            "section": section_name,
            "title": fields.get("Title", item_name),
            "description": fields.get("Description", ""),
            "brand": fields.get("Brand", ""),
            "status": fields.get("Status", ""),
            "price": fields.get("Price", ""),
            "keywords": parse_keywords_field(fields.get("Keywords", "")),
            "images": ordered,
            "folder": item_path,
            "priority": parse_priority(fields.get("Priority")),
            "series": (fields.get("Series") or "").strip(),
        })
    entries.sort(key=priority_sort_key)
    entries = group_series(entries)
    return entries


def parse_products():
    return {
        "3d-printed": parse_product_folder(
            os.path.join(ROOT, "products", "3d-printed"), "3d-printed"),
        "spare-deals": parse_product_folder(
            os.path.join(ROOT, "products", "store", "spare-deals"), "spare-deals"),
        "used-blasters": parse_product_folder(
            os.path.join(ROOT, "products", "store", "used-blasters"), "used-blasters"),
    }


def parse_brands():
    folder = os.path.join(ROOT, "brands")
    if not os.path.isdir(folder):
        return []
    txt_files = glob.glob(os.path.join(folder, "*.txt"))
    all_files = [f for f in os.listdir(folder) if f != "README.md"]
    entries = []
    for txt_path in txt_files:
        stem = os.path.splitext(os.path.basename(txt_path))[0]
        fields = parse_txt(txt_path)
        if not fields.get("Title"):
            continue
        matching_imgs = [
            f for f in all_files
            if os.path.splitext(f)[1].lower() in IMG_EXTS
            and (os.path.splitext(f)[0] == stem
                 or re.match(r"^" + re.escape(stem) + r"[ _]\d+$", os.path.splitext(f)[0]))
        ]
        images = group_numbered_files(matching_imgs, stem)
        entries.append({
            "slug": slugify(stem),
            "raw_name": stem,
            "title": fields.get("Title", stem),
            "description": fields.get("Description", ""),
            "keywords": [k["kw"] for k in parse_keywords_field(fields.get("Keywords", ""))],
            "supplier_link": fields.get("Supplier Link", ""),
            "logo": images[0] if images else None,
            "priority": parse_priority(fields.get("Priority")),
            "series": (fields.get("Series") or "").strip(),
        })
    entries.sort(key=priority_sort_key)
    entries = group_series(entries)
    return entries


def build_keyword_index(products):
    """lowercased keyword -> list of product dicts (across all sections)"""
    index = {}
    for section_products in products.values():
        for p in section_products:
            for k in p["keywords"]:
                kw_lower = k["kw"].lower()
                index.setdefault(kw_lower, []).append(p)
    return index


def build_brand_lookup(brands):
    """lowercased brand title -> brand dict"""
    return {b["title"].lower(): b for b in brands}


def resolve_build_brands(portfolio_entry, kw_index, brand_lookup):
    """For a portfolio entry, find matched products (by keyword), group by
    brand, skip brands with no logo. Returns:
    [{'brand': brand_dict, 'products': [product_dict, ...]}, ...]"""
    matched_products = {}
    for k in portfolio_entry["keywords"]:
        kw_lower = k["kw"].lower()
        for p in kw_index.get(kw_lower, []):
            matched_products[(p["section"], p["slug"])] = p

    by_brand = {}
    for p in matched_products.values():
        brand_name = p.get("brand", "")
        if not brand_name:
            continue
        brand = brand_lookup.get(brand_name.lower())
        if not brand or not brand.get("logo"):
            continue  # skip brands with no matching entry or no logo
        by_brand.setdefault(brand["slug"], {"brand": brand, "products": []})
        by_brand[brand["slug"]]["products"].append(p)

    return list(by_brand.values())


def resolve_product_examples(product, portfolio):
    """For a product, find portfolio entries (builds/events) that share any
    of its keywords — used for the 'See Examples' button."""
    product_kws = {k["kw"].lower() for k in product["keywords"]}
    matches = []
    for entry in portfolio:
        entry_kws = {k["kw"].lower() for k in entry["keywords"]}
        if product_kws & entry_kws:
            matches.append(entry)
    return matches


TYPE_TO_CATEGORY = {
    "build": "builds", "builds": "builds",
    "event": "events", "events": "events",
    "tech tip": "tech-tips", "tech tips": "tech-tips", "tech-tip": "tech-tips", "tech-tips": "tech-tips", "techtips": "tech-tips",
    "review": "reviews", "reviews": "reviews",
}


def category_for(type_text):
    return TYPE_TO_CATEGORY.get(re.sub(r"\s+", " ", (type_text or "").strip().lower()))


def assign_categories(portfolio):
    """Keep only entries whose Type matches Builds / Events / Tech Tips / Reviews."""
    kept = []
    for e in portfolio:
        cat = category_for(e["type"])
        if cat is None:
            print(f"  ! Not posted: '{e['raw_name']}' has Type '{e['type']}' "
                  f"(use Build, Event, Tech Tip or Review)")
            continue
        e["category"] = cat
        kept.append(e)
    return kept


def load_all():
    portfolio = assign_categories(parse_portfolio())
    products = parse_products()
    brands = parse_brands()
    kw_index = build_keyword_index(products)
    brand_lookup = build_brand_lookup(brands)
    return {
        "portfolio": portfolio,
        "products": products,
        "brands": brands,
        "kw_index": kw_index,
        "brand_lookup": brand_lookup,
    }


if __name__ == "__main__":
    data = load_all()
    print(f"Portfolio entries: {len(data['portfolio'])}")
    for e in data["portfolio"]:
        print(f"  - [{e['type']}] {e['title']} ({len(e['images'])} images, "
              f"youtube={'yes' if e['youtube'] else 'no'})")
    for section, items in data["products"].items():
        print(f"Products / {section}: {len(items)}")
        for p in items:
            print(f"  - {p['title']} (brand={p['brand'] or 'none'})")
    print(f"Brands: {len(data['brands'])}")
    for b in data["brands"]:
        print(f"  - {b['title']} (logo={'yes' if b['logo'] else 'no'})")

    print("\n--- Cross-link test ---")
    for entry in data["portfolio"]:
        groups = resolve_build_brands(entry, data["kw_index"], data["brand_lookup"])
        if groups:
            print(f"{entry['title']} matches:")
            for g in groups:
                names = ", ".join(p["title"] for p in g["products"])
                print(f"  -> {g['brand']['title']}: {names}")

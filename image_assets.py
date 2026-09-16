"""
image_assets.py

Reads "User Input/image-assets/assets.txt" and turns each heading into a
named hero/banner image with independent desktop and mobile positioning.
Used by build_site2.py to generate the <img> tag + matching CSS rule for
each named location — falling back to sensible defaults if a location
isn't defined in the txt file yet.

--------------------------------------------------------------------------
assets.txt format
--------------------------------------------------------------------------
## Homepage Hero
Image: hero-home.jpg

#Desktop
Scale: 100%
Alignment: top-left
Opacity: 100
Nudge: 0px 0px

#Mobile
Scale: 80%
Alignment: top
Opacity: 100
Nudge: 0px -20px

- `Image` sits once, under the `##` heading, shared by both devices.
- `#Desktop` and `#Mobile` each carry their own Scale/Alignment/Opacity/
  Nudge. If `#Mobile` is left out entirely, mobile just uses the desktop
  values. If `#Mobile` is present but only sets SOME fields, the rest
  fall back to the matching desktop value (not to the hard-coded
  defaults) — so you only need to specify what's actually different on
  mobile.
- "Mobile" means the same thing it means everywhere else on this site:
  screens at or under 900px wide (the same breakpoint the nav switches
  on), so hero images stay visually consistent with the rest of the
  layout's responsive behaviour.

--------------------------------------------------------------------------
Scale / Alignment / Nudge behaviour (per device)
--------------------------------------------------------------------------
  - The image ALWAYS fills its box completely at Scale: 100% (blank =
    100%). There's no "contain"-style option that leaves empty space on
    its own — if you want empty space, dial Scale below 100% on purpose.
  - Alignment is the anchor point that stays put — it never moves, no
    matter how much you scale up or down; only the edges away from it
    move. Nine options: center, top, bottom, left, right, top-left,
    top-right, bottom-left, bottom-right.
  - Scale is a plain percentage. 100% = fills the box exactly (old
    "cover"). Above 100% zooms in further, pivoting on the anchor
    (crops more). Below 100% zooms out from the anchor and will reveal
    empty space around the image on the sides away from the anchor.
  - Nudge is the one thing that can move the anchor's exact position —
    it shifts the image by a literal pixel amount on top of everything
    above, and stays a fixed pixel offset regardless of Scale.
"""

import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "User Input", "image-assets")
MOBILE_BREAKPOINT = 900  # matches the site's existing nav breakpoint

# alignment_key -> (object-position, transform-origin)
ALIGNMENT_MAP = {
    "center":       ("center center", "50% 50%"),
    "top":          ("center top",    "50% 0%"),
    "bottom":       ("center bottom", "50% 100%"),
    "left":         ("left center",   "0% 50%"),
    "right":        ("right center",  "100% 50%"),
    "top-left":     ("left top",      "0% 0%"),
    "top-right":    ("right top",     "100% 0%"),
    "bottom-left":  ("left bottom",   "0% 100%"),
    "bottom-right": ("right bottom",  "100% 100%"),
}


def parse_assets():
    """Returns {location_name: {"shared": {...}, "desktop": {...}, "mobile": {...}}}"""
    path = os.path.join(ROOT, "assets.txt")
    locations = {}
    if not os.path.exists(path):
        return locations

    current = None
    section = "shared"
    with open(path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.rstrip("\n").strip()
            if not line:
                continue

            heading2 = re.match(r"^##\s*(.+)$", line)
            if heading2:
                current = heading2.group(1).strip()
                locations[current] = {"shared": {}, "desktop": {}, "mobile": {}}
                section = "shared"
                continue

            heading1 = re.match(r"^#\s*(.+)$", line)
            if heading1 and current:
                label = heading1.group(1).strip().lower()
                if label.startswith("desktop"):
                    section = "desktop"
                elif label.startswith("mobile"):
                    section = "mobile"
                else:
                    section = "shared"
                continue

            kv = re.match(r"^([A-Za-z]+):\s*(.*)$", line)
            if kv and current:
                locations[current][section][kv.group(1).strip()] = kv.group(2).strip()
    return locations


def _parse_nudge(raw):
    if not raw:
        return (0, 0)
    m = re.match(r"^(-?\d+)px\s+(-?\d+)px$", raw.strip())
    if not m:
        return (0, 0)
    return (int(m.group(1)), int(m.group(2)))


def _normalize_alignment(raw):
    """Accepts 'top-left', 'top left', 'Top_Left', etc. Falls back to
    'center' for anything blank or unrecognised."""
    if not raw:
        return "center"
    key = raw.strip().lower().replace(" ", "-").replace("_", "-")
    return key if key in ALIGNMENT_MAP else "center"


def _parse_scale_percent(raw):
    """Blank -> 100. Accepts '100', '100%', '120 %', etc. Anything
    unparseable or <= 0 also falls back to 100."""
    if not raw:
        return 100.0
    s = raw.strip().replace("%", "").strip()
    try:
        val = float(s)
    except ValueError:
        return 100.0
    return val if val > 0 else 100.0


def _style_string(raw, default_alignment, default_opacity):
    alignment_key = _normalize_alignment(raw.get("Alignment", default_alignment))
    opacity = raw.get("Opacity", str(default_opacity))
    scale_pct = _parse_scale_percent(raw.get("Scale", ""))
    nx, ny = _parse_nudge(raw.get("Nudge", "0px 0px"))

    object_position, transform_origin = ALIGNMENT_MAP[alignment_key]
    scale_factor = scale_pct / 100.0

    parts = [
        "object-fit:cover",
        f"object-position:{object_position}",
        f"transform-origin:{transform_origin}",
    ]

    transform_bits = []
    if nx or ny:
        transform_bits.append(f"translate({nx}px, {ny}px)")
    if scale_factor != 1.0:
        transform_bits.append(f"scale({scale_factor})")
    if transform_bits:
        parts.append(f"transform:{' '.join(transform_bits)}")

    try:
        opacity_val = float(opacity) / 100
    except (ValueError, TypeError):
        opacity_val = 1.0
    if opacity_val != 1.0:
        parts.append(f"opacity:{opacity_val}")

    return "; ".join(parts)


def class_name_for(location_name):
    slug = re.sub(r"[^a-z0-9]+", "-", location_name.lower()).strip("-")
    return f"hero-photo-{slug}"


def resolve(location_name, default_file, default_alignment="center", default_opacity=100):
    """Returns (image_path, css_class, css_rule_block).

    - image_path: the <img src="..."> value.
    - css_class: put this class on the <img> tag.
    - css_rule_block: CSS text (selector + braces included) to drop into
      the page's stylesheet once. Contains the desktop rule for the
      class, plus a @media (max-width: 900px) override if mobile values
      actually differ from desktop.
    """
    locations = parse_assets()
    entry = locations.get(location_name)
    css_class = class_name_for(location_name)

    if not entry or not entry.get("shared", {}).get("Image"):
        image_path = default_file
        desktop_raw = {}
        mobile_raw = {}
    else:
        image_path = f"User Input/image-assets/{entry['shared']['Image']}"
        desktop_raw = dict(entry.get("desktop", {}))
        mobile_raw = dict(desktop_raw)
        mobile_raw.update(entry.get("mobile", {}))

    desktop_css = _style_string(desktop_raw, default_alignment, default_opacity)
    mobile_css = _style_string(mobile_raw, default_alignment, default_opacity)

    # Selector is "img.<class>" (tag+class), matching the specificity of
    # the base ".hero img" / ".page-banner img" rules — a plain class-only
    # selector would be LESS specific than those and could lose regardless
    # of source order, since inline styles no longer do this job for us.
    block = f"img.{css_class}{{ {desktop_css}; }}\n"
    if mobile_css != desktop_css:
        block += f"@media (max-width: {MOBILE_BREAKPOINT}px){{ img.{css_class}{{ {mobile_css}; }} }}\n"

    return image_path, css_class, block


if __name__ == "__main__":
    print(parse_assets())
    print(resolve("Homepage Hero", "images/hero.jpg"))
    print(resolve("Nonexistent Location", "images/fallback.jpg"))

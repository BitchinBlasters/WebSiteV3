"""
render_dynamic.py

Turns parse_content.py's data into HTML. build_site2.py imports the
functions here to splice dynamic sections (gallery grid, product cards,
brand cards) into its existing pages, and to write the individual
build/event detail pages as separate files.
"""

import os
import parse_content

UI_PATH = "User Input"  # relative path prefix used in generated <img src="">


def img_src(entry_or_folder_rel, filename):
    return f"{UI_PATH}/{entry_or_folder_rel}/{filename}"


def portfolio_img_src(filename):
    return f"{UI_PATH}/portfolio/{filename}"


def product_img_src(section, raw_name, filename):
    subpath = {"3d-printed": "products/3d-printed",
               "spare-deals": "products/store/spare-deals",
               "used-blasters": "products/store/used-blasters"}[section]
    return f"{UI_PATH}/{subpath}/{raw_name}/{filename}"


def brand_img_src(filename):
    return f"{UI_PATH}/brands/{filename}"


# ---------------------------------------------------------------------------
# GALLERY GRID (build-gallery.html)
# ---------------------------------------------------------------------------

def gallery_card(entry):
    kw_list = ",".join(k["kw"].lower() for k in entry["keywords"])
    thumb = portfolio_img_src(entry["images"][0]) if entry["images"] else ""
    type_badge = entry["type"]

    if entry["youtube"]:
        yt_id = extract_youtube_id(entry["youtube"])
        hover_start_sec = parse_content.timestamp_to_seconds(entry["hover_start"]) or 0
        return f'''    <a class="gallery-item gallery-video-card" href="builds/{entry['slug']}.html"
       data-keywords="{kw_list}" data-yt-id="{yt_id}" data-hover-start="{hover_start_sec}">
      <img src="{thumb}" alt="{entry['title']}">
      <span class="gallery-type-badge">{type_badge} &middot; Video</span>
      <span class="play-overlay" aria-hidden="true">{PLAY_SVG_INLINE}</span>
      <div class="gallery-cap"><strong>{entry['title']}</strong><br>{entry['description']}</div>
    </a>'''
    return f'''    <a class="gallery-item" href="builds/{entry['slug']}.html" data-keywords="{kw_list}">
      <img src="{thumb}" alt="{entry['title']}">
      <span class="gallery-type-badge">{type_badge}</span>
      <div class="gallery-cap"><strong>{entry['title']}</strong><br>{entry['description']}</div>
    </a>'''


PLAY_SVG_INLINE = '<svg viewBox="0 0 24 24" width="28" height="28" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>'


def extract_youtube_id(url):
    import re
    m = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{6,})", url)
    return m.group(1) if m else ""


def gallery_grid_html(portfolio):
    if not portfolio:
        return '<div class="wrap"><p style="color:var(--text-dim);">No builds or events uploaded yet.</p></div>'
    cards = "\n".join(gallery_card(e) for e in portfolio)
    return f'<div class="gallery-grid" id="dynamic-gallery">\n{cards}\n  </div>'


# ---------------------------------------------------------------------------
# PRODUCT CARDS (3d-printing.html / store.html)
# ---------------------------------------------------------------------------

def product_card(product, portfolio, show_status=False, show_price=False):
    thumb = product_img_src(product["section"], product["raw_name"], product["images"][0]) if product["images"] else ""
    examples = parse_content.resolve_product_examples(product, portfolio)
    kw_list = ",".join(k["kw"].lower() for k in product["keywords"])

    meta_line = ""
    if show_status and product.get("status"):
        cls = "status-in-stock" if product["status"].lower() == "in stock" else "status-print-to-order"
        meta_line = f'<span class="product-status {cls}">{product["status"]}</span>'
    if show_price and product.get("price"):
        meta_line += f'<span class="product-price">{product["price"]}</span>'

    examples_btn = ""
    if examples and kw_list:
        first_kw = kw_list.split(",")[0]
        examples_btn = f'<a class="btn small" href="build-gallery.html?keyword={first_kw}">See Examples</a>'

    return f'''    <div class="card product-card" data-keywords="{kw_list}">
      <img src="{thumb}" alt="{product['title']}">
      <div class="card-body">
        <h3>{product['title']}</h3>
        <p>{product['description']}</p>
        <div class="product-meta">{meta_line}</div>
        {examples_btn}
      </div>
    </div>'''


def products_grid_html(products, portfolio, show_status=False, show_price=False):
    if not products:
        return '<p style="color:var(--text-dim);">Nothing listed here yet.</p>'
    cards = "\n".join(product_card(p, portfolio, show_status, show_price) for p in products)
    return f'<div class="card-row cols-3">\n{cards}\n  </div>'


# ---------------------------------------------------------------------------
# BRAND CARDS (brands.html)
# ---------------------------------------------------------------------------

def brand_card(brand, all_products):
    if not brand.get("logo"):
        return ""  # no logo = skip entirely, per spec
    logo = brand_img_src(brand["logo"])
    brand_products = []
    for section_products in all_products.values():
        for p in section_products:
            if p.get("brand", "").lower() == brand["title"].lower():
                brand_products.append(p)

    submenu = ""
    if brand_products:
        items = "\n".join(
            f'<a href="{_product_link(p)}">{p["title"]}</a>' for p in brand_products
        )
        submenu = f'<div class="brand-submenu">{items}</div>'

    link = brand.get("supplier_link") or "#"
    return f'''    <div class="brand-tile">
      <a href="{link}" target="_blank" rel="noopener" class="brand-logo-link">
        <img src="{logo}" alt="{brand['title']}">
      </a>
      {submenu}
    </div>'''


def _product_link(product):
    anchor_map = {"3d-printed": "3d-printing.html", "spare-deals": "store.html", "used-blasters": "store.html"}
    return f'{anchor_map.get(product["section"], "#")}#{product["slug"]}'


def brands_grid_html(brands, products):
    cards = [brand_card(b, products) for b in brands]
    cards = [c for c in cards if c]
    if not cards:
        return '<p style="color:var(--text-dim);">No brand logos uploaded yet.</p>'
    return f'<div class="brand-grid">\n{"".join(cards)}\n  </div>'


# ---------------------------------------------------------------------------
# BUILD / EVENT DETAIL PAGES
# ---------------------------------------------------------------------------

def keyword_buttons_html(entry, kw_index):
    """Buttons under a build's breakdown linking to matched products directly
    (not grouped by brand — that's the separate brand-logo section)."""
    seen = set()
    buttons = []
    for k in entry["keywords"]:
        kw_lower = k["kw"].lower()
        for p in kw_index.get(kw_lower, []):
            key = (p["section"], p["slug"])
            if key in seen:
                continue
            seen.add(key)
            buttons.append(f'<a class="btn small" href="{_product_link(p)}">{p["title"]}</a>')
    if not buttons:
        return ""
    return f'<div class="keyword-product-buttons">{"".join(buttons)}</div>'


def brand_section_html(entry, kw_index, brand_lookup):
    groups = parse_content.resolve_build_brands(entry, kw_index, brand_lookup)
    if not groups:
        return ""
    tiles = []
    for g in groups:
        brand = g["brand"]
        logo = brand_img_src(brand["logo"])
        items = "\n".join(
            f'<a href="{_product_link(p)}">{p["title"]}</a>' for p in g["products"]
        )
        link = brand.get("supplier_link") or "#"
        tiles.append(f'''    <div class="brand-tile">
      <a href="{link}" target="_blank" rel="noopener" class="brand-logo-link">
        <img src="{logo}" alt="{brand['title']}">
      </a>
      <div class="brand-submenu">{items}</div>
    </div>''')
    return f'''<div class="section-head" style="margin-top:40px;">
      <span class="kicker">Featured in this build</span>
      <h3>Brands</h3>
    </div>
    <div class="brand-grid">
{"".join(tiles)}
    </div>'''


def video_block_html(entry):
    if not entry["youtube"]:
        return ""
    yt_id = extract_youtube_id(entry["youtube"])
    hover_start_sec = parse_content.timestamp_to_seconds(entry["hover_start"]) or 0
    kw_timestamps = [
        {"label": k["kw"], "sec": parse_content.timestamp_to_seconds(k["ts"])}
        for k in entry["keywords"] if k["ts"]
    ]
    jump_buttons = "".join(
        f'<button class="btn small keyword-jump-btn" data-seek="{kt["sec"]}">{kt["label"]} ({entry["hover_start"] if False else ""}{_fmt_ts(kt["sec"])})</button>'
        for kt in kw_timestamps
    )
    return f'''<div class="video-highlight-player" data-yt-id="{yt_id}" data-start="{hover_start_sec}" id="detail-video">
      <div class="video-highlight-frame"></div>
      <div class="video-pause-overlay" hidden>
        <div class="video-pause-buttons">
          <a class="btn primary" href="https://youtube.com/watch?v={yt_id}" target="_blank" rel="noopener">Watch in Full</a>
          <a class="btn" href="#products-used">Buy Products</a>
        </div>
        <a class="video-channel-link" href="{{CHANNEL_URL}}" target="_blank" rel="noopener">
          <span class="video-channel-name">{{CHANNEL_NAME}}</span>
        </a>
      </div>
    </div>
    <div class="video-jump-row">{jump_buttons}</div>'''


def _fmt_ts(seconds):
    if seconds is None:
        return ""
    m, s = divmod(int(seconds), 60)
    return f"{m}:{s:02d}"


def detail_page_body(entry, kw_index, brand_lookup):
    gallery_imgs = "\n".join(
        f'<div class="gallery-item"><img src="{portfolio_img_src(img)}" alt="{entry["title"]}"></div>'
        for img in entry["images"][1:]  # first image already shown as hero/video
    )
    location_line = f'<p class="kicker">{entry["location"]}</p>' if entry.get("location") else ""
    hero_media = video_block_html(entry) if entry["youtube"] else (
        f'<img src="{portfolio_img_src(entry["images"][0])}" alt="{entry["title"]}" class="detail-hero-img">'
        if entry["images"] else ""
    )

    kw_buttons = keyword_buttons_html(entry, kw_index)
    brand_section = brand_section_html(entry, kw_index, brand_lookup) if entry["type"] == "Build" else ""

    return f'''<section class="page-banner" style="min-height:180px;">
  <div class="page-banner-content">
    <span class="kicker">{entry['type']}</span>
    <h1>{entry['title']}</h1>
    {location_line}
  </div>
</section>
<section>
  <div class="wrap">
    <div class="detail-hero">{hero_media}</div>
    <div class="detail-breakdown">
      <p>{entry['breakdown'] or entry['description']}</p>
    </div>
    <div id="products-used">{kw_buttons}</div>
    {gallery_imgs and f'<div class="gallery-grid" style="margin-top:32px;">{gallery_imgs}</div>'}
    {brand_section}
    <p style="margin-top:40px;"><a href="../build-gallery.html" class="btn">&larr; Back to Gallery</a></p>
  </div>
</section>'''


def write_detail_pages(output_dir, page_fn, data):
    """page_fn: build_site2.page(title, description, active, body) -> full html string.
    Writes one file per portfolio entry into output_dir/builds/<slug>.html"""
    builds_dir = os.path.join(output_dir, "builds")
    os.makedirs(builds_dir, exist_ok=True)
    for entry in data["portfolio"]:
        body = detail_page_body(entry, data["kw_index"], data["brand_lookup"])
        # detail pages live one level deeper (builds/), so relative asset
        # paths need "../" — patch that in for nav/logo/footer links.
        html = page_fn(f"{entry['title']} — Bitchin' Blasters", entry["description"],
                        "build-gallery", body)
        html = _fix_relative_paths(html)
        with open(os.path.join(builds_dir, f"{entry['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(html)


GALLERY_FILTER_SCRIPT = """
  // ---- Gallery keyword filter (?keyword=xxx) ----
  (function() {
    const params = new URLSearchParams(window.location.search);
    const kw = (params.get('keyword') || '').toLowerCase();
    if (!kw) return;
    document.querySelectorAll('#dynamic-gallery .gallery-item').forEach(item => {
      const kws = (item.dataset.keywords || '').split(',');
      if (!kws.includes(kw)) item.style.display = 'none';
    });
  })();
"""

VIDEO_SYSTEM_SCRIPT = """
  // ---- Shared YouTube highlight-clip system ----
  const HIGHLIGHT_DURATION = 20; // seconds, fixed site-wide, not configurable per video

  let ytAPIReady = false;
  let ytAPIQueue = [];
  function loadYouTubeAPI(cb) {
    if (ytAPIReady && window.YT && window.YT.Player) { cb(); return; }
    ytAPIQueue.push(cb);
    if (document.getElementById('youtube-iframe-api')) return;
    const tag = document.createElement('script');
    tag.id = 'youtube-iframe-api';
    tag.src = 'https://www.youtube.com/iframe_api';
    document.head.appendChild(tag);
    window.onYouTubeIframeAPIReady = function() {
      ytAPIReady = true;
      ytAPIQueue.forEach(f => f());
      ytAPIQueue = [];
    };
  }

  function attachHighlightPlayer(mountEl, ytId, startSec, options) {
    options = options || {};
    let player = null;
    let capTimer = null;

    function clearCap() { if (capTimer) { clearTimeout(capTimer); capTimer = null; } }

    function armCap() {
      clearCap();
      capTimer = setTimeout(() => {
        if (player && player.pauseVideo) player.pauseVideo();
        if (options.onCap) options.onCap();
      }, HIGHLIGHT_DURATION * 1000);
    }

    function create(muted) {
      const div = document.createElement('div');
      mountEl.appendChild(div);
      player = new YT.Player(div, {
        videoId: ytId,
        playerVars: {
          start: startSec, autoplay: 1, controls: muted ? 0 : 1,
          modestbranding: 1, rel: 0, playsinline: 1
        },
        events: {
          onReady: (e) => {
            if (muted) { e.target.mute(); } else { e.target.unMute(); }
            e.target.playVideo();
            armCap();
            if (!muted && options.onUnmutedReady) {
              // Detect blocked autoplay: if still paused shortly after play(),
              // the browser blocked unmuted autoplay and needs a real click.
              setTimeout(() => {
                if (player.getPlayerState && player.getPlayerState() !== 1) {
                  options.onUnmutedReady(player);
                }
              }, 600);
            }
          }
        }
      });
    }

    function seekTo(sec) {
      if (!player || !player.seekTo) return;
      player.seekTo(sec, true);
      player.playVideo();
      if (options.onResume) options.onResume();
      armCap();
    }

    function destroy() {
      clearCap();
      if (player && player.destroy) player.destroy();
      player = null;
      mountEl.innerHTML = '';
    }

    return { create, seekTo, destroy, getPlayer: () => player };
  }

  // ---- Gallery grid: muted hover preview on video cards ----
  document.querySelectorAll('.gallery-item[data-yt-id]').forEach(card => {
    const ytId = card.dataset.ytId;
    const startSec = parseInt(card.dataset.hoverStart || '0', 10);
    let ctrl = null;
    let mount = null;
    if (window.matchMedia && window.matchMedia('(hover: none)').matches) return; // skip touch devices
    card.addEventListener('mouseenter', () => {
      loadYouTubeAPI(() => {
        mount = document.createElement('div');
        mount.style.cssText = 'position:absolute;inset:0;z-index:1;pointer-events:none;';
        card.appendChild(mount);
        ctrl = attachHighlightPlayer(mount, ytId, startSec, {});
        ctrl.create(true);
      });
    });
    card.addEventListener('mouseleave', () => {
      if (ctrl) { ctrl.destroy(); ctrl = null; }
      if (mount) { mount.remove(); mount = null; }
    });
  });

  // ---- Build/event detail page: full unmuted highlight player ----
  document.querySelectorAll('.video-highlight-player').forEach(playerBlock => {
    const ytId = playerBlock.dataset.ytId;
    const startSec = parseInt(playerBlock.dataset.start || '0', 10);
    const frame = playerBlock.querySelector('.video-highlight-frame');
    const overlay = playerBlock.querySelector('.video-pause-overlay');

    const ctrl = attachHighlightPlayer(frame, ytId, startSec, {
      onCap: () => { if (overlay) overlay.hidden = false; },
      onResume: () => { if (overlay) overlay.hidden = true; },
      onUnmutedReady: (player) => {
        // Autoplay-with-sound was blocked by the browser — show a simple
        // click-to-play button in place of the frame (a real click always
        // satisfies autoplay-with-sound policies).
        const btn = document.createElement('button');
        btn.className = 'btn primary';
        btn.style.cssText = 'position:absolute;inset:0;margin:auto;width:180px;height:52px;z-index:4;';
        btn.textContent = 'Play';
        frame.appendChild(btn);
        btn.addEventListener('click', () => {
          player.unMute();
          player.playVideo();
          btn.remove();
        });
      }
    });
    loadYouTubeAPI(() => ctrl.create(false));

    playerBlock.parentElement.querySelectorAll('.keyword-jump-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const sec = parseInt(btn.dataset.seek, 10);
        ctrl.seekTo(sec);
      });
    });
  });
"""


def _fix_relative_paths(html):
    """Detail pages are one folder deeper than the site root, so every
    relative link/asset path needs a '../' prefix. Absolute URLs (http/https)
    and already-relative '../' paths are left untouched."""
    import re
    def repl(m):
        attr, val = m.group(1), m.group(2)
        if val.startswith(("http://", "https://", "mailto:", "#", "../")):
            return m.group(0)
        return f'{attr}="../{val}"'
    return re.sub(r'(src|href)="([^"]+)"', repl, html)

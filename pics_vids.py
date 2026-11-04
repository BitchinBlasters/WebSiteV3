"""
pics_vids.py

Builds the "Pics & Vids" page (build-gallery.html):
  - a pinned header with the page title, jump links, All/Photos/Videos filter and a search button
  - four sections (Builds, Events, Tech Tips, Reviews), each with its own 300px banner and a
    sideways-scrolling carousel of cards
  - photos and videos alternate (photo, video, photo, video ...); Priority orders each kind
  - a section with nothing in it shows "Content coming soon"

render_dynamic.gallery_card() makes each card, so hover previews and detail-page links are unchanged.
"""

import html
import re

import render_dynamic

SECTIONS = [
    ("builds", "Builds", "Builds Hero", "Finished builds, start to finish."),
    ("events", "Events", "Events Hero", "Skirmish days, meetups and time on the field."),
    ("tech-tips", "Tech Tips", "Tech Tips Hero", "Know-how from the bench."),
    ("reviews", "Reviews", "Reviews Hero", "Straight talk on parts and gear."),
]

SEARCH_SVG = ('<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" '
              'stroke="currentColor" stroke-width="2.6" stroke-linecap="round">'
              '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 L21 21"/></svg>')
CLOSE_SVG = ('<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" '
             'stroke="currentColor" stroke-width="2.6" stroke-linecap="round"><path d="M5 5 L19 19 M19 5 L5 19"/></svg>')
TRI_LEFT = '<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path d="M17 4 L6 12 L17 20 Z" fill="currentColor"/></svg>'
TRI_RIGHT = '<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true"><path d="M7 4 L18 12 L7 20 Z" fill="currentColor"/></svg>'


def _units(entries):
    """Entries that share a Series stay together as one unit; everything else is a unit of one."""
    units, seen = [], set()
    for e in entries:
        k = (e.get("series") or "").strip().lower()
        if not k:
            units.append([e])
        elif k not in seen:
            seen.add(k)
            units.append([x for x in entries if (x.get("series") or "").strip().lower() == k])
    return units


def interleave(entries):
    """photo, video, photo, video ... Order within each kind is whatever came in (already by Priority).
    Entries sharing a Series name sit side by side, and count as one step in the pattern.
    Leftovers of the longer kind simply continue at the end."""
    photos = _units([e for e in entries if not e["youtube"]])
    videos = _units([e for e in entries if e["youtube"]])
    out = []
    for i in range(max(len(photos), len(videos))):
        if i < len(photos):
            out.extend(photos[i])
        if i < len(videos):
            out.extend(videos[i])
    return out


def _slide(entry):
    kind = "video" if entry["youtube"] else "photo"
    kws = " ".join(k["kw"] for k in entry["keywords"])
    search = html.escape(f'{entry["title"]} {entry["description"]} {kws} {entry["type"]}'.lower(), quote=True)
    card = render_dynamic.gallery_card(entry)
    m = re.search(r'\s*<div class="gallery-cap">(.*?)</div>', card, re.S)
    cap = m.group(1) if m else ""
    card = card.replace(m.group(0), "") if m else card
    card = re.sub(r'\s*<span class="gallery-type-badge">.*?</span>', '', card, flags=re.S)
    cap = cap.replace("<br>", "</strong><span>", 1) + "</span>" if "<br>" in cap else cap
    cap = cap.replace("</strong></strong>", "</strong>")
    return (f'<div class="pv-slide" data-kind="{kind}" data-search="{search}">\n'
            f'{card}\n<a class="pv-cap" href="builds/{entry["slug"]}.html">{cap}</a>\n</div>')


def _filter_buttons(aria):
    return (f'<div class="pv-filter" role="group" aria-label="{aria}">'
            '<button type="button" class="btn pv-fbtn on" data-kind="all">All</button>'
            '<button type="button" class="btn pv-fbtn" data-kind="photo">Photos</button>'
            '<button type="button" class="btn pv-fbtn" data-kind="video">Videos</button>'
            '</div>')


def _section(sec, entries, hero):
    sid, label, _loc, blurb = sec
    img_path, img_class = hero
    mine = interleave([e for e in entries if e["category"] == sid])
    slides = "\n".join(_slide(e) for e in mine)
    return f'''<section class="pv-section" id="{sid}" data-section="{sid}">
  <div class="page-banner pv-banner">
    <img class="{img_class}" src="{img_path}" alt="">
    <div class="page-banner-content">
      <h2><button type="button" class="pv-title-btn" data-cat="{sid}" title="Show only {label}">{label}</button></h2>
      <p>{blurb}</p>
    </div>
    <button type="button" class="btn pv-sbtn pv-banner-x" aria-label="Show all categories" hidden>{CLOSE_SVG}</button>
  </div>
  <div class="wrap pv-wrap">
    <div class="pv-carousel"{' hidden' if not mine else ''}>
      <button type="button" class="btn pv-arrow pv-prev" aria-label="Previous">{TRI_LEFT}</button>
      <div class="pv-track" tabindex="0">
{slides}
      </div>
      <button type="button" class="btn pv-arrow pv-next" aria-label="Next">{TRI_RIGHT}</button>
      <div class="pv-counter" aria-live="polite"></div>
      <div class="pv-bar">
        <button type="button" class="btn pv-bar-btn pv-bar-prev" aria-label="Scroll left">{TRI_LEFT}</button>
        <div class="pv-bar-track"><div class="pv-bar-thumb"></div></div>
        <button type="button" class="btn pv-bar-btn pv-bar-next" aria-label="Scroll right">{TRI_RIGHT}</button>
      </div>
    </div>
    <p class="pv-empty"{'' if not mine else ' hidden'}>Content coming soon</p>
  </div>
</section>'''


def body_html(portfolio, header_hero, section_heroes):
    """header_hero: (img_path, css_class); section_heroes: list of (img_path, css_class), one per SECTIONS entry."""
    hp, hc = header_hero
    jumps = "".join(f'<button type="button" class="btn pv-jump" data-cat="{sid}" aria-pressed="false">{label}</button>' for sid, label, _l, _b in SECTIONS)
    sections = "\n\n".join(_section(s, portfolio, h) for s, h in zip(SECTIONS, section_heroes))
    return f'''<div class="pv-header" id="pv-header">
  <div class="pv-inner pv-header-inner">
    <div class="pv-main">
      <div class="pv-title"><h1>Gallery</h1><p>Builds, events, tech tips and reviews.</p></div>
      <nav class="pv-jumps" aria-label="Jump to a section">{jumps}</nav>
      <div class="pv-controls">
        {_filter_buttons("Show everywhere")}
        <button type="button" class="btn pv-sbtn" id="pv-search-open" aria-label="Search">{SEARCH_SVG}<span class="pv-tip">Search</span></button>
      </div>
    </div>
    <div class="pv-searchbar">
      <input type="search" id="pv-q" placeholder="Search pics &amp; vids" autocomplete="off" aria-label="Search pics and vids">
      <button type="button" class="btn pv-sbtn" id="pv-search-close" aria-label="Close search">{CLOSE_SVG}</button>
    </div>
  </div>
</div>

{sections}'''


CSS = """
  /* ---------- PICS & VIDS PAGE ---------- */
  .pv-header [hidden], .pv-section [hidden], .pv-section[hidden]{ display:none !important; }
  .pv-inner{ max-width:var(--wrap); margin:0 auto; padding:0 24px; width:100%; }
  .pv-header{
    position:sticky; top:var(--pv-nav, 0px); z-index:90;
    height:98px; background:linear-gradient(100deg,#0a110a,#050805); border-bottom:2px solid var(--lime);
    box-shadow:0 6px 20px rgba(0,0,0,.5);
  }
  .pv-header > img{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; filter:saturate(.8); }
  .pv-header::after{ content:""; position:absolute; inset:0; background:linear-gradient(100deg, rgba(5,8,5,.94) 8%, rgba(5,8,5,.72) 60%, rgba(5,8,5,.6) 100%); }
  .pv-header-inner{ position:relative; z-index:2; height:100%; }
  .pv-main{ height:100%; display:grid; grid-template-columns:1fr auto; grid-template-rows:auto auto; row-gap:8px; align-content:center; column-gap:24px; align-items:center; }
  .pv-title{ grid-column:1; grid-row:1 / 3; align-self:center; }
  .pv-title h1{ font-size:clamp(30px,4.2vw,48px); line-height:1.05; }
  .pv-title p{ margin-top:6px; font-size:14px; color:var(--text-dim); }
  .pv-jumps{ grid-column:2; grid-row:1; display:flex; gap:8px; justify-self:end; align-self:center; }
  .pv-controls{ grid-column:2; grid-row:2; display:flex; gap:8px; justify-self:end; align-items:center; }
  /* All Pics & Vids buttons are the site's .btn (clipped corners, glow, bolding text). These tweak size only. */
  .pv-jump, .pv-fbtn, .pv-sbtn, .pv-bar-btn, .pv-arrow{ --pc:11px; font-family:inherit; }
  .pv-jump::before, .pv-fbtn::before, .pv-sbtn::before, .pv-bar-btn::before, .pv-arrow::before{
    clip-path:polygon(var(--pc) 0, 100% 0, 100% calc(100% - var(--pc)), calc(100% - var(--pc)) 100%, 0 100%, 0 var(--pc)); }
  .pv-jump::after, .pv-fbtn::after, .pv-sbtn::after, .pv-bar-btn::after, .pv-arrow::after{
    clip-path:polygon(calc(var(--pc) * .916) 0, 100% 0, 100% calc(100% - var(--pc) * .916), calc(100% - var(--pc) * .916) 100%, 0 100%, 0 calc(var(--pc) * .916)); }
  .pv-jump{ height:30px; padding:0 14px; font-size:11px; justify-content:center; white-space:nowrap; --pc:9px; }
  .pv-filter{ display:flex; gap:8px; }
  .pv-fbtn{ height:36px; padding:0 15px; font-size:11.5px; }
  .pv-sbtn{ width:36px; height:36px; padding:0; justify-content:center; flex:none; --pc:9px; }
  .pv-fbtn.on, .pv-sbtn.on, .pv-jump.on{ color:#08110a; font-weight:900; }
  .pv-fbtn.on::before, .pv-jump.on::before{ background:var(--lime); }
  .pv-fbtn.on::after, .pv-jump.on::after{
    background-image:
      radial-gradient(ellipse at center, rgba(42,255,0,1) 0%, rgba(42,255,0,0.65) 45%, rgba(42,255,0,0.25) 75%, rgba(42,255,0,0) 100%),
      repeating-linear-gradient(0deg, rgba(42,255,0,.055) 0px, rgba(42,255,0,.055) 1px, transparent 1px, transparent 3px); }
  .pv-tip{ position:absolute; top:calc(100% + 8px); right:0; padding:5px 9px; font-size:11px; font-weight:800; letter-spacing:.05em; text-transform:uppercase;
    color:#08110a; background:var(--lime); white-space:nowrap; opacity:0; pointer-events:none; transition:opacity .15s ease; z-index:5;
    clip-path:polygon(6px 0, 100% 0, 100% calc(100% - 6px), calc(100% - 6px) 100%, 0 100%, 0 6px); }
  .pv-sbtn:hover .pv-tip{ opacity:1; }
  .pv-searchbar{ display:none; height:100%; align-items:center; gap:8px; }
  .pv-searchbar input{ flex:1; max-width:560px; height:40px; padding:0 14px; font-size:16px; color:var(--text); background:rgba(5,8,5,.9); border:1px solid var(--lime); border-radius:0; }
  .pv-searchbar input:focus{ outline:2px solid var(--lime); }
  .pv-header.searching .pv-main{ display:none; }
  .pv-header.searching .pv-searchbar{ display:flex; }

  .pv-section{ padding:0; border-bottom:none; scroll-margin-top:var(--pv-stack, 150px); }
  .pv-banner{ height:104px; min-height:104px; }
  .pv-title-btn{ font:inherit; color:inherit; letter-spacing:inherit; text-transform:inherit; background:none; border:0; padding:0; cursor:pointer; text-align:left; }
  .pv-title-btn:hover, .pv-title-btn:focus-visible{ color:var(--lime); text-shadow:0 0 14px rgba(42,255,0,.55); }
  .pv-banner-x{ position:absolute; top:10px; right:max(14px, calc((100% - var(--wrap)) / 2 + 24px)); z-index:4; width:32px; height:32px; padding:0; justify-content:center; --pc:8px; }
  .pv-banner .page-banner-content{ padding:24px; }
  .pv-banner-filters{ position:absolute; left:0; right:0; top:50%; transform:translateY(-50%); z-index:3; }
  .pv-inner-banner{ display:flex; justify-content:flex-end; }
  .pv-banner-controls{ display:flex; gap:8px; align-items:center; }
  .pv-banner-search{ display:none; align-items:center; gap:8px; width:100%; max-width:420px; }
  .pv-banner-search input{ flex:1; min-width:0; height:36px; padding:0 12px; font-size:16px; color:var(--text); background:rgba(5,8,5,.9); border:1px solid var(--lime); border-radius:0; }
  .pv-banner-search input:focus{ outline:2px solid var(--lime); }
  .pv-banner-filters.searching .pv-sec-open{ display:none; }
  .pv-banner-filters.searching .pv-banner-search{ display:flex; }
  .pv-inner-banner{ align-items:center; gap:8px; }
  .pv-banner-search{ order:-1; width:auto; flex:0 1 300px; }

  .pv-wrap{ padding-top:26px; padding-bottom:46px; }
  .pv-carousel{ position:relative; }
  .pv-track{ display:flex; gap:14px; overflow-x:auto; scroll-snap-type:x proximity; scrollbar-width:none; -webkit-overflow-scrolling:touch; }
  .pv-track::-webkit-scrollbar{ display:none; }
  .pv-slide{ flex:0 0 calc((100% - 3 * 14px) / 4); scroll-snap-align:start; min-width:0; }
  .pv-slide .gallery-item{ aspect-ratio:4/3; display:block; }
  .pv-cap{ display:block; padding:10px 2px 0; color:var(--text); text-decoration:none; }
  .pv-cap strong{ display:block; font-size:14px; line-height:1.3; font-weight:700; display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
  .pv-cap span{ display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; text-overflow:ellipsis; margin-top:3px; font-size:12px; line-height:1.4; color:var(--text-dim); }
  .pv-cap:hover strong{ color:var(--lime); }
  .pv-arrow{ display:none; }
  .pv-counter{ display:none; }
  .pv-bar{ display:flex; align-items:center; gap:8px; margin-top:14px; }
  .pv-bar.inactive{ visibility:hidden; }
  .pv-bar-btn{ width:30px; height:24px; padding:0; justify-content:center; flex:none; color:var(--lime); --pc:7px; }
  .pv-bar-btn:hover:not(:disabled){ color:#08110a; }
  .pv-bar-btn:disabled{ opacity:.3; cursor:default; }
  .pv-bar-track{ position:relative; flex:1; height:10px; background:var(--panel); border:1px solid var(--line); cursor:pointer; }
  .pv-bar-thumb{ position:absolute; left:0; top:0; bottom:0; background:var(--lime); opacity:.85; cursor:grab; touch-action:none; }
  .pv-bar-thumb:active{ cursor:grabbing; }

  /* one category showing: vertical tile grid instead of a carousel */
  .pv-section.pv-grid .pv-track{ display:grid; grid-template-columns:repeat(4, minmax(0,1fr)); gap:14px; overflow:visible; scroll-snap-type:none; }
  .pv-section.pv-grid .pv-slide{ flex:none; width:auto; }
  .pv-section.pv-grid .pv-bar, .pv-section.pv-grid .pv-arrow, .pv-section.pv-grid .pv-counter{ display:none !important; }
  .pv-empty{ padding:46px 0; text-align:center; font-size:15px; letter-spacing:.08em; text-transform:uppercase; color:var(--text-dim); border:1px dashed var(--line); }

  @media (hover:none){ .pv-slide .gallery-cap{ opacity:1; } }
  /* touch screens keep :hover after a tap, so un-selected buttons must not stay lit */
  @media (hover:none){
    .pv-jump:not(.on):hover, .pv-fbtn:not(.on):hover, .pv-sbtn:not(.on):hover{ transform:none; font-weight:700; color:var(--text); }
    .pv-jump:not(.on):hover::before, .pv-fbtn:not(.on):hover::before, .pv-sbtn:not(.on):hover::before{ background:rgba(42,255,0,.4); }
    .pv-jump:not(.on):hover::after, .pv-fbtn:not(.on):hover::after, .pv-sbtn:not(.on):hover::after{
      background-image:repeating-linear-gradient(0deg, rgba(42,255,0,.055) 0px, rgba(42,255,0,.055) 1px, transparent 1px, transparent 3px); }
  }

  @media (max-width: 900px){
    .pv-header{ top:0; height:72px; overflow:hidden; }
    .pv-inner{ padding:0 12px; }
    .pv-main{ grid-template-columns:1fr auto; grid-template-rows:auto auto; align-content:center; column-gap:10px; row-gap:0; }
    .pv-title{ grid-column:1; grid-row:1; align-self:end; padding-bottom:5px; }
    .pv-title h1{ font-size:21px; }
    .pv-title p{ display:none; }
    .pv-controls{ grid-column:1; grid-row:2; justify-self:start; align-self:start; padding-bottom:0; gap:5px; }
    .pv-fbtn{ height:26px; padding:0 8px; font-size:9.5px; --pc:7px; }
    .pv-filter{ gap:5px; }
    .pv-sbtn{ height:26px; width:26px; --pc:7px; }
    .pv-tip{ display:none; }
    .pv-jumps{ grid-column:2; grid-row:1 / 3; align-self:center; justify-self:end; padding:0; display:grid; grid-template-columns:repeat(2, 66px); grid-template-rows:repeat(2, 26px); gap:4px; }
    .pv-jump{ height:26px; padding:0 2px; font-size:9.5px; --pc:7px; }
    .pv-banner{ height:auto; min-height:70px; padding:12px 0; flex-direction:column; align-items:stretch; justify-content:center; gap:10px; }
    .pv-banner .page-banner-content{ padding:0 20px; }
    .pv-banner .page-banner-content h2{ font-size:24px; line-height:1.1; }
    .pv-banner .page-banner-content p{ margin-top:4px; font-size:13px; }
    .pv-banner .page-banner-content .kicker{ margin-bottom:4px; }
    .pv-inner-banner{ justify-content:flex-start; }
    .pv-inner-banner{ flex-wrap:wrap; justify-content:flex-start; }
    .pv-banner-search{ flex:1 0 100%; max-width:none; }
    .pv-banner-search input{ height:26px; }
    .pv-banner-x{ top:8px; right:12px; width:28px; height:28px; --pc:7px; }
    .pv-inner-banner{ padding:0 20px; }
    .pv-wrap{ padding:18px 0 34px; }
    .pv-wrap.wrap{ padding-left:0; padding-right:0; }
    .pv-track{ gap:8px; padding:0 10px; scroll-padding:0 10px; scroll-snap-type:x mandatory; }
    .pv-slide{ flex:0 0 calc((100% - 8px - 20px) / 2); }
    .pv-slide .gallery-item{ aspect-ratio:4/3; }
    .pv-bar{ display:none; }
    .pv-arrow{ display:flex; position:absolute; top:calc(50% - 22px); z-index:4; width:34px; height:46px; justify-content:center;
      color:var(--lime); padding:0; --pc:9px; }
    .pv-arrow:hover:not(:disabled){ color:#08110a; }
    .pv-prev{ left:6px; } .pv-next{ right:6px; }
    .pv-arrow:disabled{ opacity:.25; }
    .pv-counter{ display:block; text-align:center; margin-top:10px; font-size:12px; letter-spacing:.08em; text-transform:uppercase; color:var(--text-dim); }
    .pv-empty{ margin:0 12px; }
    .pv-searchbar input{ max-width:none; }
    .pv-cap span{ font-size:11.5px; }
    .pv-cap{ padding:8px 2px 0; }
    .pv-section.pv-grid .pv-wrap{ padding-left:10px; padding-right:10px; }
    .pv-section.pv-grid .pv-track{ grid-template-columns:repeat(2, minmax(0,1fr)); gap:8px; scroll-snap-type:none; }
  }
"""


SCRIPT = r"""
  // ---- Pics & Vids: layout, filters, search, carousels ----
  (function(){
    const header = document.getElementById('pv-header');
    if (!header) return;
    const nav = document.querySelector('header.nav');
    const mq = window.matchMedia('(max-width: 900px)');
    const root = document.documentElement;

    function layout(){
      const navH = (!mq.matches && nav) ? nav.getBoundingClientRect().height : 0;
      root.style.setProperty('--pv-nav', navH + 'px');
      root.style.setProperty('--pv-stack', (navH + header.offsetHeight) + 'px');
    }
    layout();
    window.addEventListener('resize', layout);
    window.addEventListener('load', layout);

    // ---- carousels ----
    function Carousel(sec){
      const track = sec.querySelector('.pv-track');
      const bar = sec.querySelector('.pv-bar');
      const barTrack = sec.querySelector('.pv-bar-track');
      const thumb = sec.querySelector('.pv-bar-thumb');
      const counter = sec.querySelector('.pv-counter');
      const prevs = sec.querySelectorAll('.pv-prev, .pv-bar-prev');
      const nexts = sec.querySelectorAll('.pv-next, .pv-bar-next');
      const visible = function(){ return Array.prototype.slice.call(track.querySelectorAll('.pv-slide:not([hidden])')); };
      const gap = function(){ return parseFloat(getComputedStyle(track).columnGap) || 0; };

      function update(){
        const max = track.scrollWidth - track.clientWidth;
        bar.classList.toggle('inactive', max <= 2);
        const tw = barTrack.clientWidth;
        const tl = Math.max(40, tw * (track.clientWidth / Math.max(1, track.scrollWidth)));
        thumb.style.width = Math.min(tl, tw) + 'px';
        const ratio = max > 0 ? track.scrollLeft / max : 0;
        thumb.style.transform = 'translateX(' + (ratio * Math.max(0, tw - tl)) + 'px)';
        const list = visible();
        let idx = 0;
        if (list.length) {
          const w = list[0].offsetWidth + gap();
          idx = Math.min(list.length - 1, Math.round(track.scrollLeft / Math.max(1, w)));
        }
        counter.textContent = list.length ? (idx + 1) + ' of ' + list.length : '';
        prevs.forEach(function(b){ b.disabled = track.scrollLeft <= 2; });
        nexts.forEach(function(b){ b.disabled = track.scrollLeft >= max - 2; });
      }
      function step(dir){
        const list = visible();
        const w = list.length ? list[0].offsetWidth + gap() : track.clientWidth;
        const amount = mq.matches ? w * 2 : track.clientWidth * 0.8;
        track.scrollBy({ left: dir * amount, behavior: 'smooth' });
      }
      prevs.forEach(function(b){ b.addEventListener('click', function(){ step(-1); }); });
      nexts.forEach(function(b){ b.addEventListener('click', function(){ step(1); }); });
      track.addEventListener('scroll', function(){ window.requestAnimationFrame(update); });
      window.addEventListener('resize', update);

      // drag the bar thumb, or click the bar to jump
      let drag = null;
      thumb.addEventListener('pointerdown', function(e){
        e.preventDefault(); e.stopPropagation();
        thumb.setPointerCapture(e.pointerId);
        drag = { x: e.clientX, left: track.scrollLeft };
      });
      thumb.addEventListener('pointermove', function(e){
        if (!drag) return;
        const max = track.scrollWidth - track.clientWidth;
        const room = barTrack.clientWidth - thumb.offsetWidth;
        if (room > 0) track.scrollLeft = drag.left + (e.clientX - drag.x) * (max / room);
      });
      function endDrag(){ drag = null; }
      thumb.addEventListener('pointerup', endDrag);
      thumb.addEventListener('pointercancel', endDrag);
      barTrack.addEventListener('click', function(e){
        if (e.target === thumb) return;
        const r = barTrack.getBoundingClientRect();
        const ratio = (e.clientX - r.left) / Math.max(1, r.width);
        track.scrollTo({ left: ratio * (track.scrollWidth - track.clientWidth), behavior: 'smooth' });
      });

      return { reset: function(){ track.scrollLeft = 0; update(); }, update: update };
    }

    // ---- filters + search ----
    // One shared state: which category is selected (null = all), photo/video filter, search text.
    const sections = Array.prototype.slice.call(document.querySelectorAll('.pv-section'));
    const catBtns = Array.prototype.slice.call(header.querySelectorAll('.pv-jump'));
    const qBox = document.getElementById('pv-q');
    const state = { cat: null, kind: 'all', q: '', secOpen: null };
    sections.forEach(function(s){ s._pv = Carousel(s); });

    function apply(){
      const q = state.q;
      const res = sections.map(function(s){
        const id = s.dataset.section;
        const slides = Array.prototype.slice.call(s.querySelectorAll('.pv-slide'));
        let shown = 0;
        slides.forEach(function(sl){
          const ok = (state.kind === 'all' || sl.dataset.kind === state.kind) && (!q || sl.dataset.search.indexOf(q) !== -1);
          sl.hidden = !ok;
          if (ok) shown++;
        });
        return { s: s, id: id, total: slides.length, shown: shown };
      });
      const filtering = state.kind !== 'all' || !!q;
      let vis = res.filter(function(r){ return state.cat ? r.id === state.cat : (!filtering || r.shown > 0); });
      if (!state.cat && filtering && vis.length === 0) vis = res;   // nothing matches anywhere: show all with "No matches"
      const single = vis.length === 1;
      const lone = single ? vis[0].id : null;

      res.forEach(function(r){
        const s = r.s;
        const on = vis.indexOf(r) !== -1;
        s.hidden = !on;
        s.classList.toggle('pv-grid', on && (!!state.cat || single));
        s.querySelector('.pv-banner-x').hidden = state.cat !== r.id;
        const empty = s.querySelector('.pv-empty');
        const car = s.querySelector('.pv-carousel');
        if (r.shown === 0) {
          empty.textContent = (r.total && (q || state.kind !== 'all')) ? 'No matches' : 'Content coming soon';
          empty.hidden = false; car.hidden = true;
        } else { empty.hidden = true; car.hidden = false; }
        if (on) s._pv.reset();
      });
      catBtns.forEach(function(b){ b.classList.toggle('on', b.dataset.cat === state.cat); b.setAttribute('aria-pressed', b.classList.contains('on') ? 'true' : 'false'); });
      header.querySelectorAll('.pv-controls .pv-fbtn').forEach(function(b){ b.classList.toggle('on', b.dataset.kind === state.kind); });
      layout();
      try { history.replaceState(null, '', state.cat ? '#' + state.cat : window.location.pathname + window.location.search); } catch (e) {}
    }

    function scrollToTop(){
      const first = sections.filter(function(s){ return !s.hidden; })[0];
      if (!first) return;
      const y = first.getBoundingClientRect().top + window.pageYOffset - (parseFloat(getComputedStyle(root).getPropertyValue('--pv-stack')) || 0);
      window.scrollTo({ top: Math.max(0, y), behavior: 'auto' });
    }

    // header category buttons: toggle one category on/off (never hidden)
    catBtns.forEach(function(b){
      b.addEventListener('click', function(){
        const id = b.dataset.cat;
        state.cat = (state.cat === id) ? null : id;
        apply();
        scrollToTop();
      });
    });
    // header filter buttons: filter whatever is showing (a selected category stays selected)
    header.querySelectorAll('.pv-controls .pv-fbtn').forEach(function(b){
      b.addEventListener('click', function(){ state.kind = (state.kind === b.dataset.kind) ? 'all' : b.dataset.kind; apply(); scrollToTop(); });
    });
    // banner title toggles its category; the X brings the rest back
    sections.forEach(function(s){
      const id = s.dataset.section;
      s.querySelector('.pv-title-btn').addEventListener('click', function(){ state.cat = (state.cat === id) ? null : id; apply(); scrollToTop(); });
      s.querySelector('.pv-banner-x').addEventListener('click', function(){ state.cat = null; apply(); scrollToTop(); });
    });

    // header search (keeps whatever category is selected)
    function openSearch(){ header.classList.add('searching'); qBox.focus(); layout(); }
    function closeSearch(){ header.classList.remove('searching'); qBox.value = ''; state.q = ''; apply(); }
    document.getElementById('pv-search-open').addEventListener('click', openSearch);
    document.getElementById('pv-search-close').addEventListener('click', closeSearch);
    qBox.addEventListener('input', function(){ state.q = qBox.value.trim().toLowerCase(); apply(); });
    qBox.addEventListener('keydown', function(e){ if (e.key === 'Escape') closeSearch(); });

    // links from product pages (?keyword=xxx) open with that word searched
    const kw = (new URLSearchParams(window.location.search).get('keyword') || '').toLowerCase();
    if (kw) { qBox.value = kw; state.q = kw; header.classList.add('searching'); }

    // menu links (build-gallery.html#builds etc.) behave exactly like pressing that category button
    const ids = sections.map(function(s){ return s.dataset.section; });
    function fromHash(){
      const h = decodeURIComponent(window.location.hash.slice(1));
      if (ids.indexOf(h) === -1) return false;
      state.cat = h; apply(); scrollToTop(); return true;
    }
    window.addEventListener('hashchange', fromHash);
    if (ids.indexOf(decodeURIComponent(window.location.hash.slice(1))) !== -1) state.cat = decodeURIComponent(window.location.hash.slice(1));
    apply();
    if (state.cat) { scrollToTop(); window.addEventListener('load', scrollToTop); }
  })();
"""

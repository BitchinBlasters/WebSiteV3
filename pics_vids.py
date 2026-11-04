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
    return (f'<div class="pv-slide" data-kind="{kind}" data-search="{search}">\n'
            f'{render_dynamic.gallery_card(entry)}\n</div>')


def _filter_buttons(aria):
    return (f'<div class="pv-filter" role="group" aria-label="{aria}">'
            '<button type="button" class="pv-fbtn on" data-kind="all">All</button>'
            '<button type="button" class="pv-fbtn" data-kind="photo">Photos</button>'
            '<button type="button" class="pv-fbtn" data-kind="video">Videos</button>'
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
      <span class="kicker">Pics &amp; Vids</span>
      <h2>{label}</h2>
      <p>{blurb}</p>
    </div>
    <div class="pv-banner-filters"><div class="pv-inner pv-inner-banner">
      <div class="pv-banner-controls">{_filter_buttons(f"Show in {label}")}<button type="button" class="pv-sbtn pv-sec-open" aria-label="Search {label}" data-tip="Search">{SEARCH_SVG}</button></div>
      <div class="pv-banner-search"><input type="search" class="pv-sec-q" placeholder="Search {label.lower()}" autocomplete="off" aria-label="Search {label}"><button type="button" class="pv-sbtn pv-sec-close" aria-label="Close search">{CLOSE_SVG}</button></div>
    </div></div>
  </div>
  <div class="wrap pv-wrap">
    <div class="pv-carousel"{' hidden' if not mine else ''}>
      <button type="button" class="pv-arrow pv-prev" aria-label="Previous">{TRI_LEFT}</button>
      <div class="pv-track" tabindex="0">
{slides}
      </div>
      <button type="button" class="pv-arrow pv-next" aria-label="Next">{TRI_RIGHT}</button>
      <div class="pv-counter" aria-live="polite"></div>
      <div class="pv-bar">
        <button type="button" class="pv-bar-btn pv-bar-prev" aria-label="Scroll left">{TRI_LEFT}</button>
        <div class="pv-bar-track"><div class="pv-bar-thumb"></div></div>
        <button type="button" class="pv-bar-btn pv-bar-next" aria-label="Scroll right">{TRI_RIGHT}</button>
      </div>
    </div>
    <p class="pv-empty"{'' if not mine else ' hidden'}>Content coming soon</p>
  </div>
</section>'''


def body_html(portfolio, header_hero, section_heroes):
    """header_hero: (img_path, css_class); section_heroes: list of (img_path, css_class), one per SECTIONS entry."""
    hp, hc = header_hero
    jumps = "".join(f'<a class="pv-jump" href="#{sid}">{label}</a>' for sid, label, _l, _b in SECTIONS)
    sections = "\n\n".join(_section(s, portfolio, h) for s, h in zip(SECTIONS, section_heroes))
    return f'''<div class="pv-header" id="pv-header">
  <img class="{hc}" src="{hp}" alt="">
  <div class="pv-inner pv-header-inner">
    <div class="pv-main">
      <div class="pv-title"><h1>Pics &amp; Vids</h1><p>Builds, events, tech tips and reviews.</p></div>
      <nav class="pv-jumps" aria-label="Jump to a section">{jumps}</nav>
      <div class="pv-controls">
        {_filter_buttons("Show everywhere")}
        <button type="button" class="pv-sbtn" id="pv-search-open" aria-label="Search" data-tip="Search">{SEARCH_SVG}</button>
      </div>
    </div>
    <div class="pv-searchbar">
      <input type="search" id="pv-q" placeholder="Search pics &amp; vids" autocomplete="off" aria-label="Search pics and vids">
      <button type="button" class="pv-sbtn" id="pv-search-close" aria-label="Close search">{CLOSE_SVG}</button>
    </div>
  </div>
</div>

{sections}'''


CSS = """
  /* ---------- PICS & VIDS PAGE ---------- */
  .pv-header [hidden], .pv-section [hidden]{ display:none !important; }
  .pv-inner{ max-width:var(--wrap); margin:0 auto; padding:0 24px; width:100%; }
  .pv-header{
    position:sticky; top:var(--pv-nav, 0px); z-index:90;
    height:150px; background:#050805; border-bottom:2px solid var(--lime);
    box-shadow:0 6px 20px rgba(0,0,0,.5);
  }
  .pv-header > img{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; filter:saturate(.8); }
  .pv-header::after{ content:""; position:absolute; inset:0; background:linear-gradient(100deg, rgba(5,8,5,.94) 8%, rgba(5,8,5,.72) 60%, rgba(5,8,5,.6) 100%); }
  .pv-header-inner{ position:relative; z-index:2; height:100%; }
  .pv-main{ height:100%; display:grid; grid-template-columns:1fr auto; grid-template-rows:1fr auto 1fr; column-gap:24px; align-items:center; }
  .pv-title{ grid-column:1; grid-row:1 / 4; align-self:center; }
  .pv-title h1{ font-size:clamp(30px,4.2vw,48px); line-height:1.05; }
  .pv-title p{ margin-top:6px; font-size:14px; color:var(--text-dim); }
  .pv-jumps{ grid-column:2; grid-row:1; display:flex; gap:8px; justify-self:end; align-self:end; padding-bottom:7px; }
  .pv-controls{ grid-column:2; grid-row:2; display:flex; gap:8px; justify-self:end; align-items:center; }
  .pv-jump{ display:inline-flex; align-items:center; justify-content:center; height:30px; padding:0 14px; font-size:11px; font-weight:800;
    letter-spacing:.05em; text-transform:uppercase; color:#08110a; background:var(--lime); border:1px solid var(--lime); white-space:nowrap; }
  .pv-jump:hover{ background:#fff; border-color:#fff; }
  .pv-filter{ display:flex; gap:6px; }
  .pv-fbtn, .pv-sbtn{ height:36px; font:inherit; font-size:11.5px; font-weight:800; letter-spacing:.05em; text-transform:uppercase; cursor:pointer;
    color:var(--text); background:rgba(8,12,8,.85); border:1px solid var(--lime); }
  .pv-fbtn{ padding:0 15px; }
  .pv-fbtn:hover, .pv-sbtn:hover{ background:rgba(42,255,0,.18); }
  .pv-fbtn.on{ background:var(--lime); color:#08110a; }
  .pv-sbtn{ position:relative; width:36px; display:inline-flex; align-items:center; justify-content:center; padding:0; flex:none; }
  .pv-sbtn[data-tip]::after{ content:attr(data-tip); position:absolute; top:calc(100% + 8px); right:0; padding:5px 9px; font-size:11px; font-weight:800;
    letter-spacing:.05em; text-transform:uppercase; color:#08110a; background:var(--lime); white-space:nowrap; opacity:0; pointer-events:none; transition:opacity .15s ease; }
  .pv-sbtn[data-tip]:hover::after{ opacity:1; }
  .pv-header.hide-filters .pv-controls{ display:none; }
  .pv-searchbar{ display:none; height:100%; align-items:center; gap:8px; }
  .pv-searchbar input{ flex:1; max-width:560px; height:40px; padding:0 14px; font-size:16px; color:var(--text); background:rgba(5,8,5,.9); border:1px solid var(--lime); border-radius:0; }
  .pv-searchbar input:focus{ outline:2px solid var(--lime); }
  .pv-header.searching .pv-main{ display:none; }
  .pv-header.searching .pv-searchbar{ display:flex; }

  .pv-section{ padding:0; border-bottom:none; scroll-margin-top:var(--pv-stack, 150px); }
  .pv-banner{ height:300px; min-height:300px; }
  .pv-banner .page-banner-content{ padding:24px; }
  .pv-banner-filters{ position:absolute; left:0; right:0; bottom:18px; z-index:3; }
  .pv-inner-banner{ display:flex; justify-content:flex-end; }
  .pv-banner-controls{ display:flex; gap:8px; align-items:center; }
  .pv-banner-search{ display:none; align-items:center; gap:8px; width:100%; max-width:420px; }
  .pv-banner-search input{ flex:1; min-width:0; height:36px; padding:0 12px; font-size:16px; color:var(--text); background:rgba(5,8,5,.9); border:1px solid var(--lime); border-radius:0; }
  .pv-banner-search input:focus{ outline:2px solid var(--lime); }
  .pv-banner-filters.searching .pv-sec-open{ display:none; }
  .pv-banner-filters.searching .pv-banner-search{ display:flex; }
  .pv-inner-banner{ align-items:center; gap:8px; }
  .pv-banner-search{ order:-1; width:auto; flex:0 1 300px; }
  body.pv-master-on .pv-banner-filters{ display:none; }

  .pv-wrap{ padding-top:26px; padding-bottom:46px; }
  .pv-carousel{ position:relative; }
  .pv-track{ display:flex; gap:14px; overflow-x:auto; scroll-snap-type:x proximity; scrollbar-width:none; -webkit-overflow-scrolling:touch; }
  .pv-track::-webkit-scrollbar{ display:none; }
  .pv-slide{ flex:0 0 calc((100% - 3 * 14px) / 3.4); scroll-snap-align:start; min-width:0; }
  .pv-slide .gallery-item{ aspect-ratio:4/3; display:block; }
  .pv-arrow{ display:none; }
  .pv-counter{ display:none; }
  .pv-bar{ display:flex; align-items:center; gap:8px; margin-top:14px; }
  .pv-bar.inactive{ visibility:hidden; }
  .pv-bar-btn{ width:26px; height:22px; display:inline-flex; align-items:center; justify-content:center; color:var(--lime); background:transparent; border:1px solid var(--line); cursor:pointer; padding:0; flex:none; }
  .pv-bar-btn:hover:not(:disabled){ border-color:var(--lime); background:rgba(42,255,0,.12); }
  .pv-bar-btn:disabled{ opacity:.3; cursor:default; }
  .pv-bar-track{ position:relative; flex:1; height:10px; background:var(--panel); border:1px solid var(--line); cursor:pointer; }
  .pv-bar-thumb{ position:absolute; left:0; top:0; bottom:0; background:var(--lime); opacity:.85; cursor:grab; touch-action:none; }
  .pv-bar-thumb:active{ cursor:grabbing; }
  .pv-empty{ padding:46px 0; text-align:center; font-size:15px; letter-spacing:.08em; text-transform:uppercase; color:var(--text-dim); border:1px dashed var(--line); }

  @media (hover:none){ .pv-slide .gallery-cap{ opacity:1; } }

  @media (max-width: 900px){
    .pv-header{ top:0; height:90px; overflow:hidden; }
    .pv-inner{ padding:0 12px; }
    .pv-main{ grid-template-columns:1fr auto; grid-template-rows:1fr auto; column-gap:10px; row-gap:0; }
    .pv-title{ grid-column:1; grid-row:1; align-self:end; padding-bottom:5px; }
    .pv-title h1{ font-size:21px; }
    .pv-title p{ display:none; }
    .pv-controls{ grid-column:1; grid-row:2; justify-self:start; align-self:start; padding-bottom:0; gap:5px; }
    .pv-fbtn{ height:28px; padding:0 8px; font-size:9.5px; }
    .pv-sbtn{ height:28px; width:28px; }
    .pv-sbtn[data-tip]::after{ display:none; }
    .pv-jumps{ grid-column:2; grid-row:1 / 3; align-self:center; justify-self:end; padding:0; display:grid; grid-template-columns:repeat(2, 66px); grid-template-rows:repeat(2, 34px); gap:4px; }
    .pv-jump{ height:34px; padding:0 2px; font-size:9.5px; }
    .pv-banner{ height:300px; }
    .pv-inner-banner{ justify-content:flex-start; }
    .pv-inner-banner{ flex-wrap:wrap; justify-content:flex-start; }
    .pv-banner-search{ flex:1 0 100%; max-width:none; }
    .pv-banner-search input{ height:28px; }
    .pv-banner-filters{ bottom:14px; }
    .pv-wrap{ padding:18px 0 34px; }
    .pv-wrap.wrap{ padding-left:0; padding-right:0; }
    .pv-track{ gap:0; scroll-snap-type:x mandatory; }
    .pv-slide{ flex:0 0 100%; }
    .pv-slide .gallery-item{ aspect-ratio:4/3; }
    .pv-bar{ display:none; }
    .pv-arrow{ display:flex; position:absolute; top:calc(50% - 22px); z-index:4; width:34px; height:46px; align-items:center; justify-content:center;
      color:var(--lime); background:rgba(5,8,5,.7); border:1px solid var(--lime); padding:0; cursor:pointer; }
    .pv-prev{ left:6px; } .pv-next{ right:6px; }
    .pv-arrow:disabled{ opacity:.25; }
    .pv-counter{ display:block; text-align:center; margin-top:10px; font-size:12px; letter-spacing:.08em; text-transform:uppercase; color:var(--text-dim); }
    .pv-empty{ margin:0 12px; }
    .pv-searchbar input{ max-width:none; }
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
        const amount = mq.matches ? w : track.clientWidth * 0.8;
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
    const sections = Array.prototype.slice.call(document.querySelectorAll('.pv-section'));
    const state = { master: 'all', sec: {}, secq: {}, secopen: {}, q: '' };
    sections.forEach(function(s){ const id = s.dataset.section; state.sec[id] = 'all'; state.secq[id] = ''; state.secopen[id] = false; s._pv = Carousel(s); });

    function apply(){
      const anySec = sections.some(function(s){ const id = s.dataset.section; return state.sec[id] !== 'all' || state.secopen[id]; });
      if (anySec && state.q) { state.q = ''; qBox.value = ''; header.classList.remove('searching'); }
      header.classList.toggle('hide-filters', anySec);
      document.body.classList.toggle('pv-master-on', state.master !== 'all');
      header.querySelectorAll('.pv-fbtn').forEach(function(b){ b.classList.toggle('on', b.dataset.kind === state.master); });
      sections.forEach(function(s){
        const id = s.dataset.section;
        const kind = state.master !== 'all' ? state.master : state.sec[id];
        const q = state.secopen[id] ? state.secq[id] : state.q;
        s.querySelector('.pv-banner-filters').classList.toggle('searching', state.secopen[id]);
        s.querySelectorAll('.pv-banner-filters .pv-fbtn').forEach(function(b){ b.classList.toggle('on', b.dataset.kind === state.sec[id]); });
        const slides = Array.prototype.slice.call(s.querySelectorAll('.pv-slide'));
        let shown = 0;
        slides.forEach(function(sl){
          const ok = (kind === 'all' || sl.dataset.kind === kind) && (!q || sl.dataset.search.indexOf(q) !== -1);
          sl.hidden = !ok;
          if (ok) shown++;
        });
        const empty = s.querySelector('.pv-empty');
        const car = s.querySelector('.pv-carousel');
        if (shown === 0) {
          empty.textContent = (slides.length && q) ? 'No matches' : 'Content coming soon';
          empty.hidden = false; car.hidden = true;
        } else { empty.hidden = true; car.hidden = false; }
        s._pv.reset();
      });
    }

    header.querySelectorAll('.pv-fbtn').forEach(function(b){
      b.addEventListener('click', function(){
        const k = b.dataset.kind;
        state.master = (state.master === k) ? 'all' : k;
        if (state.master !== 'all') sections.forEach(function(s){ const id = s.dataset.section; state.sec[id] = 'all'; state.secopen[id] = false; state.secq[id] = ''; s.querySelector('.pv-sec-q').value = ''; });
        apply();
      });
    });
    sections.forEach(function(s){
      const id = s.dataset.section;
      s.querySelectorAll('.pv-banner-filters .pv-fbtn').forEach(function(b){
        b.addEventListener('click', function(){
          const k = b.dataset.kind;
          state.sec[id] = (state.sec[id] === k) ? 'all' : k;
          apply();
        });
      });
    });

    sections.forEach(function(s){
      const id = s.dataset.section;
      const box = s.querySelector('.pv-sec-q');
      s.querySelector('.pv-sec-open').addEventListener('click', function(){ state.secopen[id] = true; apply(); box.focus(); });
      function close(){ state.secopen[id] = false; state.secq[id] = ''; box.value = ''; apply(); }
      s.querySelector('.pv-sec-close').addEventListener('click', close);
      box.addEventListener('input', function(){ state.secq[id] = box.value.trim().toLowerCase(); apply(); });
      box.addEventListener('keydown', function(e){ if (e.key === 'Escape') close(); });
    });

    const qBox = document.getElementById('pv-q');
    function openSearch(){ header.classList.add('searching'); qBox.focus(); layout(); }
    function closeSearch(){ header.classList.remove('searching'); qBox.value = ''; state.q = ''; apply(); layout(); }
    document.getElementById('pv-search-open').addEventListener('click', openSearch);
    document.getElementById('pv-search-close').addEventListener('click', closeSearch);
    qBox.addEventListener('input', function(){ state.q = qBox.value.trim().toLowerCase(); apply(); });
    qBox.addEventListener('keydown', function(e){ if (e.key === 'Escape') closeSearch(); });

    // links from product pages (?keyword=xxx) open with that word searched
    const kw = (new URLSearchParams(window.location.search).get('keyword') || '').toLowerCase();
    if (kw) { qBox.value = kw; state.q = kw; header.classList.add('searching'); }
    apply();
  })();
"""

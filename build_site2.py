import base64, os

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "images")

def datauri(fname, mime):
    with open(os.path.join(IMG, fname), "rb") as f:
        b = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b}"

HERO = "images/hero.jpg"
GAL1 = "images/gallery-1.jpg"
GAL2 = "images/gallery-2.jpg"
SIG = "images/signature.jpg"
LOGO = "images/logo-lime-matched.png"
CARBON = datauri("carbon-ref2-proc.jpg", "image/jpeg")
FOOTER_TEXTURE = datauri("carbon-ref1-proc.jpg", "image/jpeg")
GRAIN = datauri("grain.png", "image/png")

CONTACT_EMAIL = "b1tch1nblasters@gmail.com"
INSTAGRAM_URL = "https://www.instagram.com/bitchinblasters"
YOUTUBE_URL = "https://www.youtube.com/@BitchinBlasters"
FACEBOOK_URL = "https://facebook.com/b1tch1nblasters"
AMAZON_URL = "https://www.amazon.com.au/"

# ---------------------------------------------------------------------------
# SHARED CSS
# ---------------------------------------------------------------------------
CSS = """
  :root{
    --ink:#0c0f0a;
    --panel:#12160f;
    --line:#2b3324;
    --line-soft:#1f2519;
    --text:#ece8db;
    --text-dim:#9a9c88;
    --lime:#2AFF00;
    --lime-dim:#1ecb00;
    --tan:#c9ac7f;
    --wrap: 1160px;
    --nav-h: 104px;
  }
  *{box-sizing:border-box; margin:0; padding:0;}
  html{scroll-behavior:smooth;}
  body{
    background:var(--ink); color:var(--text);
    font-family:'Inter', system-ui, sans-serif; font-size:16px; line-height:1.6;
    -webkit-font-smoothing:antialiased;
  }
  img{max-width:100%; display:block;}
  a{color:inherit; text-decoration:none;}
  ul{list-style:none;}
  button, input, select, textarea{font-family:inherit; font-size:inherit; color:inherit;}
  h1,h2,h3,.display{
    font-family:'Big Shoulders Display', sans-serif; font-weight:800;
    letter-spacing:0.01em; line-height:1; text-transform:uppercase;
  }
  .wrap{max-width:var(--wrap); margin:0 auto; padding:0 24px;}
  :focus-visible{ outline:2px solid var(--lime); outline-offset:3px; }

  /* ---------- NAV (carbon banner + tile mega-menu) ---------- */
  header.nav{
    position:sticky; top:0; z-index:100;
    min-height:var(--nav-h);
    background-color:#0a0a0a;
    background-image:
      linear-gradient(180deg, rgba(0,0,0,0.1), rgba(0,0,0,0.5)),
      url('__CARBON__');
    background-size:cover;
    background-repeat:no-repeat;
    background-position:center;
    border-bottom:2px solid var(--lime);
    box-shadow:0 6px 24px rgba(0,0,0,0.55);
  }
  .nav-wrap{
    display:flex; align-items:center; justify-content:space-between;
    min-height:var(--nav-h); gap:10px; flex-wrap:wrap; padding:5px 24px;
  }
  .brand{ display:flex; align-items:center; }
  .brand-logo{ height:130px; width:auto; display:block; }

  @property --edge {
    syntax: '<percentage>';
    inherits: false;
    initial-value: 19%;
  }
  @property --edge-m {
    syntax: '<percentage>';
    inherits: false;
    initial-value: 81%;
  }
  @property --bedge {
    syntax: '<percentage>';
    inherits: false;
    initial-value: 19%;
  }
  @property --bedge-m {
    syntax: '<percentage>';
    inherits: false;
    initial-value: 81%;
  }

  .nav-tiles{ display:flex; align-items:flex-end; gap:24px; align-self:flex-end; flex-wrap:nowrap; justify-content:flex-end; }
  .nav-tile{ position:relative; }
  .tile-label{
    position:relative; display:inline-block; white-space:nowrap;
    color:#08110a;
    font-weight:800; font-size:11.5px; letter-spacing:.05em; text-transform:uppercase;
    padding:10px 15px 8px;
    box-shadow:0 6px 14px rgba(0,0,0,.5);
  }
  .tile-border{
    position:absolute; inset:0; z-index:0;
    background: var(--lime);
    clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
  }
  .tile-inner{
    position:absolute; inset:2px; z-index:1;
    overflow:hidden;
    clip-path: polygon(8.83px 0, 100% 0, 100% calc(100% - 8.83px), calc(100% - 8.83px) 100%, 0 100%, 0 8.83px);
  }
  .tile-gradient{
    position:absolute; inset:0;
    --edge: 19%;
    --edge-m: 81%;
    background-image: linear-gradient(135deg,
      #050805 0%,
      #050805 2%,
      #1c7a00 6%,
      #2AFF00 var(--edge),
      #2AFF00 var(--edge-m),
      #1c7a00 94%,
      #050805 98%,
      #050805 100%);
    transition: --edge .45s ease, --edge-m .45s ease;
  }
  .tile-glow{
    position:absolute; inset: 7px 12px; z-index:1;
    background: radial-gradient(ellipse at center, rgba(255,255,255,1) 0%, rgba(255,255,255,0.65) 45%, rgba(255,255,255,0.25) 75%, rgba(255,255,255,0) 100%);
    border-radius: 999px;
    pointer-events:none;
    opacity:0;
    transition: opacity .3s ease;
  }
  .nav-tile:hover .tile-glow,
  .tile-label.tile-current .tile-glow,
  .tile-label.tile-open .tile-glow{
    opacity:1;
  }
  .tile-text{
    position:relative; z-index:2;
    display:inline-block;
    transform: scale(1);
    font-weight:800;
    transition: transform .45s ease, font-weight .15s ease;
  }
  .nav-tile:hover .tile-gradient,
  .tile-label.tile-current .tile-gradient,
  .tile-label.tile-open .tile-gradient{
    --edge: 11.5%;
    --edge-m: 88.5%;
  }
  .nav-tile:hover .tile-text,
  .tile-label.tile-current .tile-text,
  .tile-label.tile-open .tile-text{
    transform: scale(1.07);
    font-weight:900;
  }
  .nav-tile:active .tile-text{
    font-weight:900;
  }

  /* ---------- DROPDOWN (Splinter-Cell style panel) ---------- */
  .tile-sub{
    position:absolute; top:100%; right:0; width:max-content; max-width:90vw; margin-top:6px;
    opacity:0; visibility:hidden; transform:translateY(-6px);
    transition:opacity .18s ease, transform .18s ease, visibility .18s;
    z-index:50;
  }
  .nav-tile:hover .tile-sub{ opacity:1; visibility:visible; transform:translateY(0); }
  .tile-sub.tile-sub-open{ opacity:1; visibility:visible; transform:translateY(0); }
  .tile-sub-border{
    position:absolute; inset:0; z-index:0;
    background: rgba(42,255,0,.4);
    clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
  }
  .tile-sub-inner{
    position:relative; z-index:1;
    margin:1.5px; padding:10px;
    display:flex; flex-direction:column; gap:10px;
    background:#0a0d08;
    clip-path: polygon(9.12px 0, 100% 0, 100% calc(100% - 9.12px), calc(100% - 9.12px) 100%, 0 100%, 0 9.12px);
    overflow:hidden;
  }
  .tile-sub-inner::before{
    content:""; position:absolute; inset:0; z-index:0;
    background-image:url('__GRAIN__');
    background-size:96px 96px;
    opacity:.055; mix-blend-mode:screen; pointer-events:none;
  }
  .tile-sub-inner::after{
    content:""; position:absolute; inset:0; z-index:0; pointer-events:none;
    background-image:repeating-linear-gradient(0deg, rgba(42,255,0,.055) 0px, rgba(42,255,0,.055) 1px, transparent 1px, transparent 3px);
  }
  .sub-link{
    position:relative; display:block; z-index:1;
    padding:4px 14px;
    font-size:13px; color:var(--text-dim); white-space:nowrap;
    text-decoration:none;
    transition:color .15s ease;
  }
  .sub-link-border{
    position:absolute; inset:0; z-index:0;
    background: rgba(42,255,0,.4);
    clip-path: polygon(6px 0, 100% 0, 100% calc(100% - 6px), calc(100% - 6px) 100%, 0 100%, 0 6px);
    transition:background .15s ease;
  }
  .sub-link-fill{
    position:absolute; inset:1px; z-index:0;
    background-color:#0a0d08;
    clip-path: polygon(5.41px 0, 100% 0, 100% calc(100% - 5.41px), calc(100% - 5.41px) 100%, 0 100%, 0 5.41px);
    transition:background-color .15s ease, background-image .3s ease;
  }
  .sub-link-text{
    position:relative; z-index:2;
    font-weight:600;
    transition:font-weight .15s ease;
  }
  .sub-link:hover .sub-link-fill{
    background-color:rgba(42,255,0,.06);
    background-image: radial-gradient(ellipse at center, rgba(42,255,0,1) 0%, rgba(42,255,0,0.65) 45%, rgba(42,255,0,0.25) 75%, rgba(42,255,0,0) 100%);
  }
  .sub-link:hover{ color:#08110a; }
  .sub-link:hover .sub-link-text{ font-weight:800; }
  .sub-link:active .sub-link-text{ font-weight:800; }
  .sub-link:hover .sub-link-border{ background:var(--lime); }

  /* ---------- BUTTONS ---------- */
  .btn{
    position:relative; overflow:visible; isolation:isolate;
    display:inline-flex; align-items:center; gap:8px; padding:14px 26px;
    font-weight:700; font-size:14px; letter-spacing:0.04em; text-transform:uppercase;
    border:none; cursor:pointer; background:transparent; color:var(--text);
    transition:transform .15s ease, color .15s ease, font-weight .15s ease;
  }
  .btn:hover{ transform:translateY(-1px); font-weight:900; }
  .btn:active{ font-weight:900; }
  .btn:not(.primary):hover{ color:#08110a; }
  .btn::before{
    content:""; position:absolute; inset:0; z-index:-2; pointer-events:none;
    background:rgba(42,255,0,.4);
    clip-path: polygon(14px 0, 100% 0, 100% calc(100% - 14px), calc(100% - 14px) 100%, 0 100%, 0 14px);
    transition:background .2s ease;
  }
  .btn:hover::before{ background:var(--lime); }
  .btn.primary::before{ background:var(--lime); }
  .btn::after{
    content:""; position:absolute; inset:2px; z-index:-1; pointer-events:none;
    clip-path: polygon(12.83px 0, 100% 0, 100% calc(100% - 12.83px), calc(100% - 12.83px) 100%, 0 100%, 0 12.83px);
  }
  .btn:not(.primary)::after{
    background-color:#0a0d08;
    background-image:
      repeating-linear-gradient(0deg, rgba(42,255,0,.055) 0px, rgba(42,255,0,.055) 1px, transparent 1px, transparent 3px);
    transition: background-image .3s ease;
  }
  .btn:not(.primary):hover::after{
    background-image:
      radial-gradient(ellipse at center, rgba(42,255,0,1) 0%, rgba(42,255,0,0.65) 45%, rgba(42,255,0,0.25) 75%, rgba(42,255,0,0) 100%),
      repeating-linear-gradient(0deg, rgba(42,255,0,.055) 0px, rgba(42,255,0,.055) 1px, transparent 1px, transparent 3px);
  }
  .btn.primary{
    color:#0c0f0a;
    --bedge: 19%;
    --bedge-m: 81%;
  }
  .btn.primary::after{
    background-image:
      linear-gradient(135deg,
      #050805 0%,
      #050805 2%,
      #1c7a00 6%,
      #2AFF00 var(--bedge),
      #2AFF00 var(--bedge-m),
      #1c7a00 94%,
      #050805 98%,
      #050805 100%);
    transition: --bedge .45s ease, --bedge-m .45s ease, background-image .3s ease;
  }
  .btn.primary:hover::after{
    --bedge: 11.5%;
    --bedge-m: 88.5%;
    background-image:
      radial-gradient(ellipse at center, rgba(255,255,255,1) 0%, rgba(255,255,255,0.65) 45%, rgba(255,255,255,0.25) 75%, rgba(255,255,255,0) 100%),
      linear-gradient(135deg,
      #050805 0%,
      #050805 2%,
      #1c7a00 6%,
      #2AFF00 var(--bedge),
      #2AFF00 var(--bedge-m),
      #1c7a00 94%,
      #050805 98%,
      #050805 100%);
  }
  .btn.block{ width:100%; justify-content:center; }
  .btn:disabled{ opacity:0.45; cursor:not-allowed; transform:none; }

  /* ---------- HERO (home only) ---------- */
  .hero{ position:relative; min-height:82svh; display:flex; align-items:flex-end; background:#000; overflow:hidden; }
  .hero img{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:left top; filter:saturate(0.9) contrast(1.05); }
  .hero::after{ content:""; position:absolute; inset:0;
    background:linear-gradient(180deg, rgba(8,10,6,0.4) 0%, rgba(8,10,6,0.15) 30%, rgba(8,10,6,0.55) 68%, rgba(8,10,6,0.96) 100%); }
  .hero-content{ position:relative; z-index:2; padding:0 24px 72px; max-width:var(--wrap); margin:0 auto; width:100%; }
  .hero-content .kicker{ display:inline-block; color:var(--lime); font-weight:600; font-size:13px; letter-spacing:0.14em; text-transform:uppercase; margin-bottom:18px; border-left:2px solid var(--lime); padding-left:10px; }
  .hero-content h1{ font-size:clamp(46px, 9vw, 108px); max-width:14ch; }
  .hero-content .tagline{ margin-top:20px; font-size:clamp(16px,2.2vw,20px); color:var(--text); max-width:44ch; font-weight:500; }
  .hero-actions{ display:flex; flex-wrap:wrap; gap:14px; margin-top:34px; }

  /* ---------- PAGE BANNER (sub-pages) ---------- */
  .page-banner{ position:relative; min-height:260px; display:flex; align-items:center; overflow:hidden; background:#000; }
  .page-banner img{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; filter:saturate(0.85) contrast(1.05); }
  .page-banner::after{ content:""; position:absolute; inset:0; background:linear-gradient(100deg, rgba(8,10,6,0.92) 10%, rgba(8,10,6,0.55) 55%, rgba(8,10,6,0.35) 100%); }
  .page-banner-content{ position:relative; z-index:2; padding:56px 24px; max-width:var(--wrap); margin:0 auto; width:100%; }
  .page-banner-content .kicker{ display:inline-block; color:var(--lime); font-weight:600; font-size:12px; letter-spacing:0.14em; text-transform:uppercase; margin-bottom:14px; border-left:2px solid var(--lime); padding-left:10px; }
  .page-banner-content h1{ font-size:clamp(34px,6vw,60px); }
  .page-banner-content p{ margin-top:14px; color:var(--text); opacity:.85; max-width:48ch; font-size:16px; }

  /* ---------- SECTION SCAFFOLD ---------- */
  section{ padding:100px 0; border-bottom:1px solid var(--line-soft); }
  section.tight{ padding:70px 0; }
  section:last-of-type{ border-bottom:none; }
  .section-head{ max-width:640px; margin-bottom:50px; }
  .section-head h2{ font-size:clamp(30px,5vw,48px); }
  .section-head .kicker{ display:block; color:var(--lime); font-weight:600; font-size:12.5px; letter-spacing:.12em; text-transform:uppercase; margin-bottom:10px; }
  .section-head p{ color:var(--text-dim); margin-top:16px; font-size:17px; max-width:52ch; }

  /* ---------- MINI BLOCKS (Who / Why / How) ---------- */
  .kicker{ display:inline-block; color:var(--lime); font-weight:600; font-size:12px; letter-spacing:.12em; text-transform:uppercase; margin-bottom:8px; }
  .mini-block{ margin-bottom:30px; }
  .mini-block h3{ font-size:21px; margin:4px 0 10px; text-transform:none; font-weight:700; letter-spacing:0; }
  .mini-block p{ color:var(--text-dim); font-size:16px; max-width:52ch; }
  .mini-block p strong{ color:var(--text); font-weight:600; }

  /* ---------- TEXT + CARDS (equal-height split) ---------- */
  .split{ display:grid; grid-template-columns: 1.1fr 0.9fr; gap:64px; align-items:stretch; }
  .split .copy p{ color:var(--text-dim); font-size:17px; margin-bottom:18px; max-width:52ch; }
  .split .copy p strong{ color:var(--text); font-weight:600; }
  .card-stack{ display:flex; flex-direction:column; gap:16px; height:100%; }
  .promise{
    flex:1; display:flex; flex-direction:column; justify-content:center;
    border:1px solid var(--line); padding:28px; background:var(--panel);
    clip-path: polygon(14px 0, 100% 0, 100% calc(100% - 14px), calc(100% - 14px) 100%, 0 100%, 0 14px);
  }
  .promise .num{ color:var(--lime); font-weight:700; font-size:13px; letter-spacing:.08em; }
  .promise h3{ font-size:24px; margin:10px 0 12px; text-transform:none; font-weight:700; letter-spacing:0; }
  .promise p{ color:var(--text-dim); font-size:15px; }

  /* ---------- SIGNATURE BAND ---------- */
  .signature{ position:relative; padding:0; border-bottom:1px solid var(--line-soft); }
  .signature-inner{ position:relative; min-height:420px; display:flex; align-items:center; }
  .signature img{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; object-position:60% 55%; }
  .signature::after{ content:""; position:absolute; inset:0; background:linear-gradient(90deg, rgba(8,10,6,0.94) 0%, rgba(8,10,6,0.72) 32%, rgba(8,10,6,0.15) 62%, rgba(8,10,6,0.35) 100%); }
  .signature-text{ position:relative; z-index:2; padding:60px 24px; margin:0 auto; width:100%; max-width:var(--wrap); }
  .signature-text .tag{ color:var(--tan); font-weight:600; font-size:13px; letter-spacing:.12em; text-transform:uppercase; }
  .signature-text h2{ font-size:clamp(28px,4vw,44px); margin:14px 0 16px; max-width:12ch; }
  .signature-text p{ color:var(--text); opacity:0.85; max-width:38ch; font-size:16px; }

  /* ---------- GALLERY ---------- */
  .gallery-grid{ display:grid; grid-template-columns: repeat(3, 1fr); gap:2px; background:var(--line-soft); }
  .gallery-item{ position:relative; overflow:hidden; aspect-ratio: 3/4; background:#000; }
  .gallery-item.wide{ aspect-ratio:16/10; grid-column:span 3; }
  .gallery-item img{ width:100%; height:100%; object-fit:cover; transition:transform .5s ease; }
  .gallery-item:hover img{ transform:scale(1.05); }
  .gallery-cap{ position:absolute; left:0; right:0; bottom:0; padding:16px;
    background:linear-gradient(0deg, rgba(0,0,0,0.75), transparent); font-size:13px; color:var(--text-dim);
    opacity:0; transition:opacity .25s ease; }
  .gallery-item:hover .gallery-cap{ opacity:1; }
  .gallery-credit{ margin-top:18px; font-size:13px; color:var(--text-dim); }

  .video-grid{ display:grid; grid-template-columns:repeat(2,1fr); gap:2px; background:var(--line-soft); }
  .video-card{ position:relative; background:var(--ink); overflow:hidden; }
  .video-thumb-link{ position:relative; display:block; }
  .video-thumb-link img{ width:100%; display:block; }
  .play-overlay{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; background:rgba(0,0,0,.15); transition:background .2s ease; }
  .video-thumb-link:hover .play-overlay{ background:rgba(0,0,0,.35); }
  .play-overlay svg{ width:60px; height:42px; filter:drop-shadow(0 4px 10px rgba(0,0,0,.6)); transition:transform .15s ease; }
  .video-thumb-link:hover .play-overlay svg{ transform:scale(1.08); }
  .video-caption{ padding:16px 18px; background:var(--panel); font-size:14px; color:var(--text-dim); }

  /* ---------- CARDS (2/3 up, generic) ---------- */
  .card-row{ display:grid; gap:24px; align-items:stretch; }
  .card-row.cols-2{ grid-template-columns:repeat(2,1fr); }
  .card-row.cols-3{ grid-template-columns:repeat(3,1fr); }
  .info-card{ display:flex; flex-direction:column; border:1px solid var(--line); background:var(--panel); padding:32px;
    clip-path: polygon(14px 0, 100% 0, 100% calc(100% - 14px), calc(100% - 14px) 100%, 0 100%, 0 14px); }
  .info-card .status{ font-size:12px; font-weight:700; letter-spacing:.1em; text-transform:uppercase; color:var(--lime); }
  .info-card h3{ font-size:22px; margin:10px 0 12px; text-transform:none; font-weight:700; letter-spacing:0; }
  .info-card p{ color:var(--text-dim); font-size:15px; margin-bottom:20px; flex:1; }

  .stl-links{ display:grid; grid-template-columns:repeat(4, 1fr); gap:14px; margin-top:32px; }
  .stl-link{ border:1px solid var(--line); background:var(--ink); padding:20px; display:flex; flex-direction:column; gap:6px;
    transition:border-color .15s ease, transform .15s ease; }
  .stl-link:hover{ border-color:var(--lime); transform:translateY(-2px); }
  .stl-link .name{ font-family:'Big Shoulders Display'; font-weight:700; font-size:18px; text-transform:uppercase; }
  .stl-link .desc{ font-size:13px; color:var(--text-dim); }

  /* ---------- FORMS ---------- */
  .field{ margin-bottom:20px; }
  .field label{ display:block; font-size:13px; font-weight:600; letter-spacing:.04em; text-transform:uppercase; color:var(--text-dim); margin-bottom:8px; }
  .field input, .field select, .field textarea{ width:100%; background:var(--ink); border:1px solid var(--line); color:var(--text); padding:12px 14px; border-radius:2px; }
  .field textarea{ min-height:110px; resize:vertical; }
  .field-row{ display:grid; grid-template-columns:1fr 1fr; gap:20px; }
  .form-panel{ border:1px solid var(--line); padding:40px; background:var(--panel); max-width:640px; }
  .choice-grid{ display:grid; grid-template-columns:repeat(auto-fit, minmax(190px,1fr)); gap:10px; margin-bottom:8px; }
  .choice{ border:1px solid var(--line); padding:14px 16px; cursor:pointer; font-size:14px; background:var(--ink);
    transition:border-color .15s ease, background .15s ease; user-select:none; }
  .choice:hover{ border-color:var(--tan); }
  .choice.selected{ border-color:var(--lime); background:rgba(42,255,0,.08); color:var(--text); }
  .choice input{ display:none; }
  .step{ margin-bottom:30px; }
  .step-label{ display:flex; align-items:baseline; gap:10px; margin-bottom:14px; }
  .step-label .n{ color:var(--lime); font-family:'Big Shoulders Display'; font-weight:800; font-size:22px; }
  .step-label h4{ font-size:14px; letter-spacing:.05em; text-transform:uppercase; color:var(--text); font-weight:700; }

  /* ---------- SHOP / GENERIC BANNER ---------- */
  .promo-banner{ border:1px solid var(--line); background:var(--panel); padding:48px;
    display:flex; justify-content:space-between; align-items:center; gap:32px; flex-wrap:wrap;
    clip-path: polygon(18px 0, 100% 0, 100% calc(100% - 18px), calc(100% - 18px) 100%, 0 100%, 0 18px); }
  .promo-banner h3{ font-size:26px; margin-bottom:10px; text-transform:none; letter-spacing:0; }
  .promo-banner p{ color:var(--text-dim); max-width:46ch; }
  .placeholder-note{ margin-top:14px; font-size:12.5px; color:var(--tan); font-style:italic; }

  /* ---------- FOOTER ---------- */
  footer{ position:relative; padding:20px 0 15px; border-top:1px solid var(--line-soft); background:var(--ink); overflow:hidden; }
  footer::before{
    content:""; position:absolute; inset:0; z-index:0; pointer-events:none;
    background-image:url('__FOOTER_TEXTURE__');
    background-size:130%; background-position:center; background-repeat:no-repeat;
    opacity:.5;
  }
  footer > .wrap{ position:relative; z-index:1; }

  .foot-row{ display:flex; align-items:flex-start; justify-content:space-between; gap:32px; padding:0 40px; }

  .foot-left{ display:flex; flex-direction:column; align-items:flex-start; }
  .foot-brand-logo{ height:56px; width:auto; }
  .foot-est{ margin-top:8px; font-size:12px; color:var(--text-dim); }

  .foot-mid{ display:flex; flex-direction:column; align-items:flex-start; }
  .foot-follow-label{
    font-size:12px; color:var(--text-dim); text-transform:uppercase; letter-spacing:.06em; font-weight:600;
    margin-bottom:8px;
  }
  .foot-social{ display:flex; gap:14px; }
  .foot-social a{ width:44px; height:44px; border:1px solid var(--line); display:flex; align-items:center; justify-content:center; }
  .foot-social a:hover{ border-color:var(--lime); color:var(--lime); }
  .foot-social svg{ width:22px; height:22px; fill:currentColor; }

  .foot-right{ display:flex; flex-direction:column; align-items:flex-end; text-align:right; }
  .foot-terms{ font-size:12px; }
  .foot-terms a:hover{ color:var(--lime); }
  .foot-email{ margin-top:8px; font-size:12px; color:var(--text-dim); }
  .foot-email a{ color:var(--text-dim); }
  .foot-email a:hover{ color:var(--lime); }

  /* ---------- BACK TO TOP ---------- */
  .totop{ position:fixed; left:22px; bottom:22px; z-index:90; width:44px; height:44px; border:1px solid var(--line);
    background:var(--panel); color:var(--text); display:flex; align-items:center; justify-content:center;
    opacity:0; pointer-events:none; transition:opacity .25s ease; cursor:pointer; }
  .totop.show{ opacity:1; pointer-events:auto; }
  .totop:hover{ border-color:var(--lime); color:var(--lime); }

  /* ---------- RESPONSIVE ---------- */
  @media (max-width: 900px){
    :root{ --nav-h:auto; }
    header.nav{ position:static; }
    .brand-logo{ height:104px; }
    .nav-wrap{ justify-content:center; padding:16px 20px; }
    .brand{ width:100%; justify-content:center; margin-bottom:6px; }
    .nav-tiles{
      display:grid; grid-template-columns:repeat(3, 1fr); width:100%;
      align-self:auto; gap:6px;
    }
    .nav-tile{ display:flex; justify-content:stretch; }
    .tile-label{ font-size:9px; padding:8px 6px 7px; width:100%; text-align:center; white-space:normal; line-height:1.25; }
    .tile-glow{ inset: 4px 6px; }
    .tile-sub{
      position:absolute; top:100%; left:0;
      width:max-content; max-width:80vw;
      opacity:0; visibility:hidden; pointer-events:none;
      transition:opacity .18s ease, visibility .18s ease;
    }
    .nav-tile:nth-child(3n) .tile-sub{
      left:auto; right:0;
    }
    .tile-sub.tile-sub-open{
      opacity:1; visibility:visible; pointer-events:auto;
    }
    .nav-tile:hover .tile-sub{ opacity:0; visibility:hidden; }
    .nav-tile:hover .tile-sub.tile-sub-open{ opacity:1; visibility:visible; }
    .split{ grid-template-columns:1fr; }
    .field-row{ grid-template-columns:1fr; }
    .gallery-grid{ grid-template-columns:1fr 1fr; }
    .video-grid{ grid-template-columns:1fr; }
    .card-row.cols-2, .card-row.cols-3{ grid-template-columns:1fr; }
    .stl-links{ grid-template-columns:1fr 1fr; }
    section{ padding:70px 0; }
    .form-panel{ padding:26px; }
    .promo-banner{ padding:32px; }

    /* ---------- FOOTER (mobile) ---------- */
    .foot-row{ position:relative; flex-wrap:wrap; align-items:flex-start; justify-content:space-between; gap:19px 0; text-align:left; padding:0; }
    .foot-left{ display:flex; flex-direction:column; align-items:center; text-align:center; position:absolute; left:0; top:16px; }
    .foot-mid{ position:absolute; top:-3px; right:0; align-items:flex-start; text-align:left; }
    .foot-right{ flex-basis:100%; align-items:center; text-align:center; order:3; margin-top:116px; }
    .foot-email{ margin-top:4px; }
    .foot-social{
      display:grid;
      grid-template-columns:repeat(2, 44px);
      grid-template-rows:repeat(2, 44px);
      gap:14px;
    }
    .foot-social a:nth-child(1){ grid-column:1; grid-row:1; }
    .foot-social a:nth-child(2){ grid-column:2; grid-row:1; }
    .foot-social a:nth-child(3){ grid-column:2; grid-row:2; }
  }
  @media (max-width: 420px){
    .tile-label{ font-size:7.5px; padding:7px 5px 6px; }
    .nav-tiles{ gap:5px; }
  }
  @media (prefers-reduced-motion: reduce){ html{ scroll-behavior:auto; } *{ transition:none !important; } }

  /* ---------- DYNAMIC CONTENT SYSTEM ---------- */
  .gallery-type-badge{ position:absolute; top:10px; left:10px; z-index:2; background:rgba(8,10,6,.75); color:var(--lime);
    font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.06em; padding:4px 8px; border:1px solid var(--line); }
  .gallery-video-card .play-overlay{ z-index:2; }
  .card-row.cols-3{ grid-template-columns:repeat(3, 1fr); }
  .product-card{ background:var(--panel); border:1px solid var(--line); overflow:hidden; display:flex; flex-direction:column; }
  .product-card img{ width:100%; aspect-ratio:4/3; object-fit:cover; }
  .product-card .card-body{ padding:18px; display:flex; flex-direction:column; gap:10px; flex:1; }
  .product-card h3{ font-size:16px; }
  .product-card p{ font-size:14px; color:var(--text-dim); flex:1; }
  .product-meta{ display:flex; gap:10px; flex-wrap:wrap; }
  .product-status{ font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:.05em; padding:3px 8px; border:1px solid var(--line); }
  .status-in-stock{ color:var(--lime); border-color:var(--lime-dim); }
  .status-print-to-order{ color:var(--tan); }
  .product-price{ font-size:14px; color:var(--text); font-weight:700; }
  .keyword-product-buttons{ display:flex; flex-wrap:wrap; gap:10px; margin-top:20px; }

  .brand-grid{ display:flex; flex-wrap:wrap; gap:24px; margin-top:20px; }
  .brand-tile{ position:relative; }
  .brand-logo-link{ display:flex; align-items:center; justify-content:center; width:120px; height:80px;
    border:1px solid var(--line); background:var(--panel); padding:14px; }
  .brand-logo-link img{ max-width:100%; max-height:100%; object-fit:contain; }
  .brand-submenu{ position:absolute; top:100%; left:0; z-index:10; margin-top:8px; min-width:180px;
    background:var(--panel); border:1px solid var(--line); padding:8px; display:flex; flex-direction:column; gap:4px;
    opacity:0; visibility:hidden; transform:translateY(-6px); transition:opacity .2s ease, transform .2s ease; }
  .brand-tile:hover .brand-submenu{ opacity:1; visibility:visible; transform:translateY(0); }
  .brand-submenu a{ font-size:13px; color:var(--text-dim); padding:6px 8px; }
  .brand-submenu a:hover{ color:var(--lime); background:rgba(42,255,0,.06); }

  .detail-hero{ margin-top:32px; }
  .detail-hero-img{ width:100%; max-height:520px; object-fit:cover; }
  .detail-breakdown{ margin-top:24px; max-width:70ch; }
  .detail-breakdown p{ color:var(--text-dim); font-size:16px; line-height:1.7; }

  .video-highlight-player{ position:relative; width:100%; aspect-ratio:16/9; background:#000; overflow:hidden; }
  .video-highlight-frame{ position:absolute; inset:0; }
  .video-highlight-frame iframe{ width:100%; height:100%; border:0; }
  .video-pause-overlay{ position:absolute; inset:0; z-index:3; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:18px;
    background:rgba(8,10,6,.55); backdrop-filter:blur(6px); }
  .video-pause-buttons{ display:flex; gap:14px; }
  .video-channel-link{ display:flex; align-items:center; gap:10px; color:var(--text); }
  .video-channel-name{ font-size:13px; font-weight:600; }
  .video-jump-row{ display:flex; flex-wrap:wrap; gap:10px; margin-top:14px; }
  .gallery-item[data-yt-id]{ cursor:pointer; }
""".replace("__CARBON__", CARBON).replace("__GRAIN__", GRAIN).replace("__FOOTER_TEXTURE__", FOOTER_TEXTURE)

HEAD_LINKS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">"""

IG_ICON = """<svg viewBox="0 0 24 24"><path d="M12 2.2c3.2 0 3.58.01 4.85.07 1.17.05 1.97.24 2.43.4a4.9 4.9 0 0 1 1.77 1.15 4.9 4.9 0 0 1 1.15 1.77c.16.46.35 1.26.4 2.43.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.24 1.97-.4 2.43a4.9 4.9 0 0 1-1.15 1.77 4.9 4.9 0 0 1-1.77 1.15c-.46.16-1.26.35-2.43.4-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.97-.24-2.43-.4a4.9 4.9 0 0 1-1.77-1.15 4.9 4.9 0 0 1-1.15-1.77c-.16-.46-.35-1.26-.4-2.43C2.21 15.58 2.2 15.2 2.2 12s.01-3.58.07-4.85c.05-1.17.24-1.97.4-2.43a4.9 4.9 0 0 1 1.15-1.77A4.9 4.9 0 0 1 5.59 1.8c.46-.16 1.26-.35 2.43-.4C9.29 1.34 9.67 1.33 12 1.33Zm0 1.98c-3.17 0-3.52.01-4.76.07-1.02.05-1.57.21-1.94.35-.49.19-.84.42-1.2.79-.37.36-.6.71-.79 1.2-.14.37-.3.92-.35 1.94-.06 1.24-.07 1.59-.07 4.76s.01 3.52.07 4.76c.05 1.02.21 1.57.35 1.94.19.49.42.84.79 1.2.36.37.71.6 1.2.79.37.14.92.3 1.94.35 1.24.06 1.59.07 4.76.07s3.52-.01 4.76-.07c1.02-.05 1.57-.21 1.94-.35.49-.19.84-.42 1.2-.79.37-.36.6-.71.79-1.2.14-.37.3-.92.35-1.94.06-1.24.07-1.59.07-4.76s-.01-3.52-.07-4.76c-.05-1.02-.21-1.57-.35-1.94a3.1 3.1 0 0 0-.79-1.2 3.1 3.1 0 0 0-1.2-.79c-.37-.14-.92-.3-1.94-.35-1.24-.06-1.59-.07-4.76-.07Zm0 3.37a5.45 5.45 0 1 1 0 10.9 5.45 5.45 0 0 1 0-10.9Zm0 1.98a3.47 3.47 0 1 0 0 6.94 3.47 3.47 0 0 0 0-6.94Zm5.66-2.2a1.27 1.27 0 1 1 0 2.55 1.27 1.27 0 0 1 0-2.55Z"/></svg>"""
YT_ICON = """<svg viewBox="0 0 24 24"><path d="M22.5 6.98a2.78 2.78 0 0 0-1.96-1.97C18.88 4.5 12 4.5 12 4.5s-6.88 0-8.54.51a2.78 2.78 0 0 0-1.96 1.97A29 29 0 0 0 1 12a29 29 0 0 0 .5 5.02 2.78 2.78 0 0 0 1.96 1.97C5.12 19.5 12 19.5 12 19.5s6.88 0 8.54-.51a2.78 2.78 0 0 0 1.96-1.97A29 29 0 0 0 23 12a29 29 0 0 0-.5-5.02ZM9.75 15.02V8.98L15.5 12l-5.75 3.02Z"/></svg>"""
FB_ICON = """<svg viewBox="0 0 24 24"><path d="M13.5 22v-8.4h2.82l.42-3.28H13.5V8.24c0-.95.26-1.6 1.63-1.6h1.74V3.72C16.56 3.65 15.55 3.56 14.36 3.56c-2.48 0-4.18 1.51-4.18 4.29v2.47H7.34v3.28h2.84V22h3.32Z"/></svg>"""
PLAY_SVG = """<svg viewBox="0 0 68 48"><path d="M66.5 7.7c-.8-2.9-2.6-5.2-4.9-6C57.1 0 34 0 34 0S10.9 0 6.4 1.7c-2.3.8-4.1 3.1-4.9 6C0 12.3 0 24 0 24s0 11.7 1.5 16.3c.8 2.9 2.6 5.2 4.9 6C10.9 48 34 48 34 48s23.1 0 27.6-1.7c2.3-.8 4.1-3.1 4.9-6C68 35.7 68 24 68 24s0-11.7-1.5-16.3z" fill="#ff0000"/><path d="M45 24 27 14v20z" fill="#fff"/></svg>"""

NAV_SECTIONS = [
    ("who-we-are.html", "who-we-are", "Who We Are", [
        ("Why We Build", "why-we-build"),
        ("Professional History", "professional-history"),
        ("Our Promise", "our-promise"),
    ]),
    ("your-build.html", "your-build", "Your Build", [
        ("Dream Build", "dream-build"),
        ("Level Up My Blaster", "level-up"),
        ("Other Enquiries", "other-enquiries"),
    ]),
    ("3d-printing.html", "3d-printing", "3D Printing", [
        ("In Stock", "in-stock"),
        ("Print to Order", "print-to-order"),
        ("Request a Print", "request-a-print"),
    ]),
    ("store.html", "store", "Store", [
        ("Amazon for Consumables", "amazon-consumables"),
        ("Spare Deals", "spare-deals"),
        ("Used Blasters", "used-blasters"),
    ]),
    ("build-gallery.html", "build-gallery", "Build Gallery", [
        ("The Builds", "the-builds"),
        ("In Play", "in-play"),
        ("Videos", "videos"),
    ]),
    ("brands.html", "brands", "Brands We Endorse", [
        ("Recommended Parts", "recommended-parts"),
        ("Trusted Suppliers", "trusted-suppliers"),
        ("Brands We Stand By", "brands-we-stand-by"),
    ]),
]

def nav(active):
    tiles = []
    for href, key, label, subs in NAV_SECTIONS:
        current = " tile-current" if active == key else ""
        sub_links = "\n".join(
            f'      <a href="{href}#{anchor}" class="sub-link">'
            f'<span class="sub-link-border"></span>'
            f'<span class="sub-link-fill"></span>'
            f'<span class="sub-link-text">{sub_label}</span>'
            f'</a>'
            for sub_label, anchor in subs
        )
        tiles.append(f'''  <div class="nav-tile">
    <a href="{href}" class="tile-label{current}">
      <span class="tile-border"></span>
      <span class="tile-inner"><span class="tile-gradient"></span></span>
      <span class="tile-glow"></span>
      <span class="tile-text">{label}</span>
    </a>
    <div class="tile-sub">
      <span class="tile-sub-border"></span>
      <div class="tile-sub-inner">
{sub_links}
      </div>
    </div>
  </div>''')
    tiles_html = "\n".join(tiles)
    return f"""<header class="nav">
  <div class="nav-wrap">
    <a href="index.html" class="brand"><img src="{LOGO}" alt="Bitchin' Blasters logo" class="brand-logo"></a>
    <nav class="nav-tiles" aria-label="Main">
{tiles_html}
    </nav>
  </div>
</header>"""

def footer():
    return f"""<footer id="contact">
  <div class="wrap">
    <div class="foot-row">
      <div class="foot-left">
        <img src="{LOGO}" alt="Bitchin' Blasters logo" class="foot-brand-logo">
        <div class="foot-est">est. 2025</div>
      </div>
      <div class="foot-mid">
        <div class="foot-follow-label">Follow</div>
        <div class="foot-social">
          <a href="{INSTAGRAM_URL}" target="_blank" rel="noopener" aria-label="Instagram">{IG_ICON}</a>
          <a href="{YOUTUBE_URL}" target="_blank" rel="noopener" aria-label="YouTube">{YT_ICON}</a>
          <a href="{FACEBOOK_URL}" target="_blank" rel="noopener" aria-label="Facebook">{FB_ICON}</a>
        </div>
      </div>
      <div class="foot-right">
        <div class="foot-terms"><a href="terms.html">Terms &amp; Conditions</a></div>
        <div class="foot-email"><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></div>
      </div>
    </div>
  </div>
</footer>"""

BASE_SCRIPT = """
  const totop = document.getElementById('totop');
  window.addEventListener('scroll', () => { totop.classList.toggle('show', window.scrollY > 600); });
  totop.addEventListener('click', () => window.scrollTo({top:0, behavior:'smooth'}));

  // ---- Mobile nav-tile dropdown: first tap opens, second tap on the same tile navigates ----
  function isMobileNav(){ return window.matchMedia('(max-width: 900px)').matches; }

  function closeAllTiles(){
    document.querySelectorAll('.tile-label.tile-open').forEach(t => t.classList.remove('tile-open'));
    document.querySelectorAll('.tile-sub.tile-sub-open').forEach(s => s.classList.remove('tile-sub-open'));
  }

  document.querySelectorAll('.nav-tile').forEach((navTile, index) => {
    const label = navTile.querySelector('.tile-label');
    const sub = navTile.querySelector('.tile-sub');

    label.addEventListener('click', (e) => {
      if (!isMobileNav()) return; // desktop keeps normal hover + click-through behavior

      const alreadyOpen = label.classList.contains('tile-open');

      if (alreadyOpen) {
        // second tap on an already-open tile: let it navigate normally
        closeAllTiles();
        return;
      }

      // first tap: open this one, close any other open tile, don't navigate yet
      e.preventDefault();
      closeAllTiles();
      label.classList.add('tile-open');
      sub.classList.add('tile-sub-open');
    });

    sub.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => closeAllTiles());
    });
  });

  document.addEventListener('click', (e) => {
    if (!isMobileNav()) return;
    if (!e.target.closest('.nav-tile')) closeAllTiles();
  });

  // ---- Desktop nav-tile dropdown: opens on hover, then stays locked open ----
  // (ignores the mouse leaving) until another tile opens or the page is scrolled 50%.
  document.querySelectorAll('.nav-tile').forEach((navTile) => {
    navTile.addEventListener('mouseenter', () => {
      if (isMobileNav()) return;
      closeAllTiles();
      navTile.querySelector('.tile-label').classList.add('tile-open');
      navTile.querySelector('.tile-sub').classList.add('tile-sub-open');
    });
  });

  window.addEventListener('scroll', () => {
    if (isMobileNav()) return;
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const pct = scrollable > 0 ? (window.scrollY / scrollable) : 0;
    if (pct >= 0.5) closeAllTiles();
  });
"""

def page(title, description, active, body, extra_script=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
{HEAD_LINKS}
<style>{CSS}</style>
</head>
<body>
{nav(active)}
<main>
{body}
</main>
{footer()}
<button class="totop" id="totop" aria-label="Back to top">&#8593;</button>
<script>
{BASE_SCRIPT}
{extra_script}
</script>
</body>
</html>"""

# ---------------------------------------------------------------------------
# SHARED SNIPPETS
# ---------------------------------------------------------------------------

def choice_grid_script():
    return """
  document.querySelectorAll('.choice-grid').forEach(group => {
    const multi = group.dataset.multi === 'true';
    group.querySelectorAll('.choice').forEach(choice => {
      choice.addEventListener('click', () => {
        const input = choice.querySelector('input');
        if (!multi) {
          group.querySelectorAll('.choice').forEach(c => c.classList.remove('selected'));
          input.checked = true;
          choice.classList.add('selected');
        } else {
          input.checked = !input.checked;
          choice.classList.toggle('selected', input.checked);
        }
      });
    });
  });
"""

def mailto_button_script(btn_id, field_ids, subject_js, var_prefix):
    field_lines = [f"      {fid.replace('-','_')}: document.getElementById('{fid}').value || 'Not given'" for fid in field_ids]
    fields_js = ",\n".join(field_lines)
    return f"""
  document.getElementById('{btn_id}').addEventListener('click', () => {{
    const {var_prefix} = {{
{fields_js}
    }};
    const body = Object.entries({var_prefix}).map(([k,v]) => k + ': ' + v).join('\\n');
    window.location.href = `mailto:{CONTACT_EMAIL}?subject=${{encodeURIComponent({subject_js})}}&body=${{encodeURIComponent(body)}}`;
  }});
"""

# ---------------------------------------------------------------------------
# PAGE CONTENT: INDEX (landing — hero + approach teaser ONLY)
# ---------------------------------------------------------------------------
import image_assets
import render_dynamic
import parse_content

# Collects one CSS rule block per named hero/banner location (desktop rule
# + optional @media mobile override). Joined into the shared CSS string
# once, further down, before any page() call happens.
_HERO_CSS_BLOCKS = []


def _hero(location_name, default_file, default_alignment="center"):
    img_path, css_class, css_block = image_assets.resolve(location_name, default_file, default_alignment=default_alignment)
    _HERO_CSS_BLOCKS.append(css_block)
    return img_path, css_class


HOME_HERO_IMG, HOME_HERO_CLASS = _hero("Homepage Hero", HERO, default_alignment="top-left")
CONTENT = parse_content.load_all()

INDEX_BODY = f"""<section class="hero" id="top">
  <img class="{HOME_HERO_CLASS}" src="{HOME_HERO_IMG}" alt="Custom gel blaster build in a ghillie hood, raised mid-game in the trees">
  <div class="hero-content">
    <span class="kicker">Queensland &middot; Custom builds &amp; upgrades</span>
    <h1>Bitchin' Blasters</h1>
    <p class="tagline">Built to how you play — not to how I think you should. Every build is a one-off, shaped around your loadout and your game.</p>
    <div class="hero-actions">
      <a href="your-build.html#dream-build" class="btn primary">Start a Build</a>
      <a href="build-gallery.html" class="btn">See Work</a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <h2>No template.<br>No house style.</h2>
      <p>Every build starts with how you actually play — your role, your field, your habits — not with a spec sheet I think looks impressive. Bring your own blaster for an upgrade, or start from nothing. One-off and bespoke means exactly that: no two builds leave the bench the same.</p>
    </div>
  </div>
</section>"""

# ---------------------------------------------------------------------------
# PAGE CONTENT: HOW WE ARE
# ---------------------------------------------------------------------------
WHO_WE_ARE_HERO_IMG, WHO_WE_ARE_HERO_CLASS = _hero("Who We Are Hero", HERO)
HOW_WE_ARE_BODY = f"""<section class="page-banner">
  <img class="{WHO_WE_ARE_HERO_CLASS}" src="{WHO_WE_ARE_HERO_IMG}" alt="Ghillie-wrapped custom build in the field">
  <div class="page-banner-content">
    <span class="kicker">Who we are</span>
    <h1>Built to how you play</h1>
    <p>Not to how I think you should. Every build is a one-off, shaped around your loadout and your game.</p>
  </div>
</section>

<section id="why-we-build">
  <div class="wrap split">
    <div class="copy">
      <div class="mini-block">
        <span class="kicker">Who</span>
        <h3>One builder, no house style</h3>
        <p>Bitchin' Blasters is a one-person operation — no workshop full of staff, no house style, just builds shaped around how you actually play. It started as tinkering with my own gear, and turned into building for other players who wanted the same thing: something matched to their role, their field, their habits, not a shelf model with someone else's idea of "best" baked in.</p>
      </div>
      <div class="mini-block">
        <span class="kicker">Why</span>
        <h3>Built to how you play</h3>
        <p><strong>Every build starts with how you actually play</strong> — your role, your field, your habits — not with a spec sheet I think looks impressive. If you run CQB and need something light and fast, that's what you get. If you sit back and support, that's what you get.</p>
      </div>
      <div class="mini-block" style="margin-bottom:0;">
        <span class="kicker">How</span>
        <h3>No template. No house style.</h3>
        <p>Bring your own blaster for an upgrade, or start from nothing. Either way, the build is shaped around your outcome, not mine. One-off and bespoke means exactly that: no two builds leave the bench the same.</p>
      </div>
    </div>
    <div class="card-stack">
      <div class="promise">
        <div class="num">01</div>
        <h3>Built around your playstyle</h3>
        <p>Role, field conditions and habits come first. The parts list follows from that.</p>
      </div>
      <div class="promise">
        <div class="num">02</div>
        <h3>Carbon fibre, wherever it fits</h3>
        <p>The signature habit on every build — light, stiff, and it's how you'll spot one of mine on the field.</p>
      </div>
    </div>
  </div>
</section>

<section id="professional-history">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Professional history</span>
      <h2>The background</h2>
      <p>This is where your story goes — how you got into building, what led you to go bespoke, any milestones, past work, or experience worth mentioning. Drop your own background in here.</p>
      <p class="placeholder-note">Placeholder section — replace with your real history before this goes live.</p>
    </div>
  </div>
</section>

<section id="our-promise" style="border-bottom:none;">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Our promise</span>
      <h2>What you can count on</h2>
    </div>
    <div class="card-row cols-3">
      <div class="info-card">
        <h3>Built around your playstyle</h3>
        <p>Role, field conditions and habits come first. The parts list follows from that, not the other way round.</p>
      </div>
      <div class="info-card">
        <h3>Bring your own, or start fresh</h3>
        <p>Upgrade what you've already got, or commission a full build from scratch — same process either way.</p>
      </div>
      <div class="info-card">
        <h3>One-off, on purpose</h3>
        <p>Bespoke builds only. If it's been done before, it wasn't done for you.</p>
      </div>
    </div>
  </div>
</section>

<section class="signature" style="border-bottom:none; padding:0;">
  <div class="signature-inner">
    <img src="{SIG}" alt="Close-up of a carbon fibre outer barrel on a custom gel blaster build">
    <div class="signature-text">
      <span class="tag">The tell</span>
      <h2>Carbon fibre outers, wherever the build allows it</h2>
      <p>It's the small habit that carries across every build — light, stiff, and it's how you'll spot one of mine on the field before you spot me.</p>
    </div>
  </div>
</section>"""

# ---------------------------------------------------------------------------
# PAGE CONTENT: YOUR BUILD
# ---------------------------------------------------------------------------
YOUR_BUILD_HERO_IMG, YOUR_BUILD_HERO_CLASS = _hero("Your Build Hero", SIG)
YOUR_BUILD_BODY = f"""<section class="page-banner">
  <img class="{YOUR_BUILD_HERO_CLASS}" src="{YOUR_BUILD_HERO_IMG}" alt="Custom build with carbon fibre outer barrel">
  <div class="page-banner-content">
    <span class="kicker">Your build</span>
    <h1>Commission a build</h1>
    <p>Dream build, an upgrade, or just a question — pick the one that fits.</p>
  </div>
</section>

<section id="dream-build">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Dream build</span>
      <h2>Start from scratch</h2>
      <p>Step through it and I'll get a clear picture of what you're after before we talk price.</p>
    </div>
    <div class="form-panel">
      <div class="step">
        <div class="step-label"><span class="n">01</span><h4>How you play</h4></div>
        <div class="choice-grid" data-group="db-role" data-multi="false">
          <label class="choice"><input type="radio" name="db-role"><span>CQB &amp; rapid fire</span></label>
          <label class="choice"><input type="radio" name="db-role"><span>Long-range support / DMR</span></label>
          <label class="choice"><input type="radio" name="db-role"><span>Sniper &amp; stealth</span></label>
          <label class="choice"><input type="radio" name="db-role"><span>All-rounder</span></label>
          <label class="choice"><input type="radio" name="db-role"><span>Just want it to look incredible</span></label>
        </div>
      </div>
      <div class="step">
        <div class="step-label"><span class="n">02</span><h4>Priorities</h4></div>
        <div class="choice-grid" data-group="db-priority" data-multi="true">
          <label class="choice"><input type="checkbox"><span>Range &amp; accuracy</span></label>
          <label class="choice"><input type="checkbox"><span>Rate of fire</span></label>
          <label class="choice"><input type="checkbox"><span>Low sound signature</span></label>
          <label class="choice"><input type="checkbox"><span>Reliability in the field</span></label>
          <label class="choice"><input type="checkbox"><span>Looks &amp; finish</span></label>
          <label class="choice"><input type="checkbox"><span>Weight &amp; handling</span></label>
        </div>
      </div>
      <div class="step">
        <div class="step-label"><span class="n">03</span><h4>Extras to consider</h4></div>
        <div class="choice-grid" data-group="db-extras" data-multi="true">
          <label class="choice"><input type="checkbox"><span>Carbon fibre outer barrel</span></label>
          <label class="choice"><input type="checkbox"><span>Suppressor cover</span></label>
          <label class="choice"><input type="checkbox"><span>Ghillie wrap</span></label>
          <label class="choice"><input type="checkbox"><span>Custom cerakote / paint</span></label>
          <label class="choice"><input type="checkbox"><span>Hop-up tuning</span></label>
        </div>
      </div>
      <div class="field-row">
        <div class="field"><label for="db-name">Name</label><input type="text" id="db-name" placeholder="Your name"></div>
        <div class="field"><label for="db-contact">Email or phone</label><input type="text" id="db-contact" placeholder="Best way to reach you"></div>
      </div>
      <div class="field"><label for="db-notes">Anything else?</label><textarea id="db-notes" placeholder="Budget, timeframe, whatever's on your mind"></textarea></div>
      <div style="display:flex; gap:12px; flex-wrap:wrap; align-items:center;">
        <button class="btn primary" id="db-generate">Generate Request</button>
        <button class="btn" id="db-email" style="display:none;">Email This Request</button>
        <span class="copy-note" id="db-note" style="font-size:13px; color:var(--lime); opacity:0; transition:opacity .2s;">Ready to send</span>
      </div>
      <div class="summary-box" id="db-summary" style="display:none; margin-top:22px; border:1px solid var(--line); background:var(--ink); padding:20px; font-size:14px; color:var(--text-dim); white-space:pre-wrap;"></div>
    </div>
  </div>
</section>

<section id="level-up">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Level up my blaster</span>
      <h2>Upgrade what you've got</h2>
      <p>Tell me what you're running and what you want it to do better.</p>
    </div>
    <div class="form-panel">
      <div class="field-row">
        <div class="field"><label for="lu-name">Name</label><input type="text" id="lu-name" placeholder="Your name"></div>
        <div class="field"><label for="lu-contact">Email or phone</label><input type="text" id="lu-contact" placeholder="Best way to reach you"></div>
      </div>
      <div class="field"><label for="lu-current">What have you got?</label><input type="text" id="lu-current" placeholder="Make / model / current setup"></div>
      <div class="field"><label for="lu-message">What do you want improved?</label><textarea id="lu-message" placeholder="Range, sound, looks, reliability..."></textarea></div>
      <button class="btn primary" id="lu-send">Email This Request</button>
    </div>
  </div>
</section>

<section id="other-enquiries" style="border-bottom:none;">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Other enquiries</span>
      <h2>Anything else</h2>
      <p>Questions, parts, general chat — send it through.</p>
    </div>
    <div class="form-panel">
      <div class="field-row">
        <div class="field"><label for="oe-name">Name</label><input type="text" id="oe-name" placeholder="Your name"></div>
        <div class="field"><label for="oe-contact">Email or phone</label><input type="text" id="oe-contact" placeholder="Best way to reach you"></div>
      </div>
      <div class="field"><label for="oe-message">Message</label><textarea id="oe-message" placeholder="What's on your mind"></textarea></div>
      <button class="btn primary" id="oe-send">Email This Enquiry</button>
    </div>
  </div>
</section>"""

YOUR_BUILD_SCRIPT = choice_grid_script() + f"""
  function selected(groupName){{
    const group = document.querySelector(`.choice-grid[data-group="${{groupName}}"]`);
    const labels = [];
    group.querySelectorAll('.choice.selected span').forEach(s => labels.push(s.textContent));
    return labels;
  }}
  let dbSummary = '';
  document.getElementById('db-generate').addEventListener('click', () => {{
    const role = selected('db-role')[0] || 'Not specified';
    const priorities = selected('db-priority');
    const extras = selected('db-extras');
    const name = document.getElementById('db-name').value || 'Not given';
    const contact = document.getElementById('db-contact').value || 'Not given';
    const notes = document.getElementById('db-notes').value || 'None';
    dbSummary = `DREAM BUILD REQUEST\\n\\nName: ${{name}}\\nContact: ${{contact}}\\n\\nPlaystyle: ${{role}}\\nPriorities: ${{priorities.length ? priorities.join(', ') : 'Not specified'}}\\nExtras: ${{extras.length ? extras.join(', ') : 'None selected'}}\\n\\nNotes: ${{notes}}`;
    document.getElementById('db-summary').textContent = dbSummary;
    document.getElementById('db-summary').style.display = 'block';
    document.getElementById('db-email').style.display = 'inline-flex';
  }});
  document.getElementById('db-email').addEventListener('click', () => {{
    window.location.href = `mailto:{CONTACT_EMAIL}?subject=${{encodeURIComponent('Dream Build request')}}&body=${{encodeURIComponent(dbSummary)}}`;
  }});
""" + mailto_button_script("lu-send", ["lu-name", "lu-contact", "lu-current", "lu-message"], "'Level Up My Blaster'", "luData") \
   + mailto_button_script("oe-send", ["oe-name", "oe-contact", "oe-message"], "'General enquiry'", "oeData")

# ---------------------------------------------------------------------------
# PAGE CONTENT: 3D PRINTING
# ---------------------------------------------------------------------------
PRINTING_HERO_IMG, PRINTING_HERO_CLASS = _hero("3D Printing Hero", GAL2)
PRINTING_BODY = f"""<section class="page-banner">
  <img class="{PRINTING_HERO_CLASS}" src="{PRINTING_HERO_IMG}" alt="Custom build detail, close on hardware">
  <div class="page-banner-content">
    <span class="kicker">3D printing</span>
    <h1>3D printed parts</h1>
    <p>Grips, mounts, covers and small fixtures — some kept in stock, the rest printed to order.</p>
  </div>
</section>

<section id="in-stock">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">In stock</span>
      <h2>Ready to ship</h2>
      <p>Parts that get asked for often enough to keep printed and on the shelf. Ask what's currently in stock and I'll confirm availability and turnaround.</p>
    </div>
    {render_dynamic.products_grid_html([p for p in CONTENT['products']['3d-printed'] if p['status'].lower() == 'in stock'], CONTENT['portfolio'], show_status=True)}
    <a href="your-build.html#other-enquiries" class="btn primary" style="margin-top:24px;">Ask What's In Stock</a>
  </div>
</section>

<section id="print-to-order">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Print to order</span>
      <h2>Built when you order it</h2>
      <p>Anything outside the in-stock range gets printed to order. Turnaround depends on size and complexity.</p>
    </div>
    {render_dynamic.products_grid_html([p for p in CONTENT['products']['3d-printed'] if p['status'].lower() == 'print to order'], CONTENT['portfolio'], show_status=True)}
    <a href="your-build.html#other-enquiries" class="btn primary" style="margin-top:24px;">Request a Print</a>
  </div>
</section>

<section id="request-a-print" style="border-bottom:none;">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Request a print &amp; find the files</span>
      <h2>Sourcing your own files</h2>
      <p>STL is the standard file format most 3D-printable designs are shared in. If you've got a specific part or accessory in mind, these are good places to start looking — bring me the file and I'll print it.</p>
    </div>
    <div class="stl-links">
      <a href="https://cults3d.com/" target="_blank" rel="noopener" class="stl-link">
        <span class="name">Cults3D</span><span class="desc">Marketplace of free &amp; paid STL files</span>
      </a>
      <a href="https://www.yeggi.com/" target="_blank" rel="noopener" class="stl-link">
        <span class="name">Yeggi</span><span class="desc">Search engine across STL sites</span>
      </a>
      <a href="https://www.thingiverse.com/" target="_blank" rel="noopener" class="stl-link">
        <span class="name">Thingiverse</span><span class="desc">Long-running free STL community</span>
      </a>
      <a href="https://www.printables.com/" target="_blank" rel="noopener" class="stl-link">
        <span class="name">Printables</span><span class="desc">Prusa's free model library</span>
      </a>
    </div>
  </div>
</section>"""

# ---------------------------------------------------------------------------
# PAGE CONTENT: STORE
# ---------------------------------------------------------------------------
STORE_HERO_IMG, STORE_HERO_CLASS = _hero("Store Hero", GAL2)
STORE_BODY = f"""<section class="page-banner">
  <img class="{STORE_HERO_CLASS}" src="{STORE_HERO_IMG}" alt="Field-ready custom build">
  <div class="page-banner-content">
    <span class="kicker">Store</span>
    <h1>Gel balls, deals &amp; more</h1>
    <p>Consumables, spares, and the occasional used build.</p>
  </div>
</section>

<section id="amazon-consumables">
  <div class="wrap">
    <div class="promo-banner">
      <div>
        <h3>Amazon for consumables</h3>
        <p>Gel balls and hop-ups, sourced direct and sold through the Amazon storefront for fast, straightforward ordering.</p>
      </div>
      <a href="{AMAZON_URL}" target="_blank" rel="noopener" class="btn primary">Shop on Amazon</a>
    </div>
  </div>
</section>

<section id="spare-deals">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Spare deals</span>
      <h2>Clearance &amp; discounted spares</h2>
      <p>Keep an eye here for discounted spares and clearance parts as they come up.</p>
    </div>
    {render_dynamic.products_grid_html(CONTENT['products']['spare-deals'], CONTENT['portfolio'], show_price=True)}
  </div>
</section>

<section id="used-blasters" style="border-bottom:none;">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Used blasters</span>
      <h2>Trade-ins &amp; second-hand builds</h2>
      <p>Trade-ins and used builds occasionally available — enquire to see what's currently on hand.</p>
    </div>
    {render_dynamic.products_grid_html(CONTENT['products']['used-blasters'], CONTENT['portfolio'], show_price=True)}
    <a href="your-build.html#other-enquiries" class="btn primary" style="margin-top:24px;">Enquire</a>
  </div>
</section>"""

# ---------------------------------------------------------------------------
# PAGE CONTENT: BUILD GALLERY
# ---------------------------------------------------------------------------
GALLERY_HERO_IMG, GALLERY_HERO_CLASS = _hero("Build Gallery Hero", GAL1)
GALLERY_BODY = f"""<section class="page-banner">
  <img class="{GALLERY_HERO_CLASS}" src="{GALLERY_HERO_IMG}" alt="Custom build aimed down carbon fibre outer barrel">
  <div class="page-banner-content">
    <span class="kicker">Build gallery</span>
    <h1>Builds in the field</h1>
    <p>Not studio shots — builds doing the job they were made for.</p>
  </div>
</section>

<section id="the-builds">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">The builds</span>
      <h2>Builds &amp; events</h2>
      <p>Photos and video highlights, side by side. Click anything to see the full story, products used, and related brands.</p>
    </div>
  </div>
  <div class="wrap">
    {render_dynamic.gallery_grid_html(CONTENT['portfolio'])}
  </div>
</section>

<section id="in-play" style="border-bottom:none;">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">In play</span>
      <h2>On the field</h2>
      <p>Photographed at Donnybrook Gel Ballers, Queensland.</p>
    </div>
  </div>
  <div class="gallery-grid">
    <div class="gallery-item">
      <img src="{HERO}" alt="Ghillie-wrapped custom build moving through pine forest">
      <div class="gallery-cap">Ghillie-wrapped build, moving through cover</div>
    </div>
    <div class="gallery-item">
      <img src="{GAL1}" alt="Custom build aimed down carbon fibre outer barrel, forest game day">
      <div class="gallery-cap">On the line — carbon fibre outer, suppressor cover</div>
    </div>
    <div class="gallery-item">
      <img src="{GAL2}" alt="Close-up on custom build red dot and suppressor from cover">
      <div class="gallery-cap">Holding position, red dot up</div>
    </div>
  </div>
  <div class="wrap">
    <p class="gallery-credit">Photography: Solutions Photography, at Donnybrook Gel Ballers, Queensland.</p>
  </div>
</section>"""

# ---------------------------------------------------------------------------
# PAGE CONTENT: BRANDS WE ENDORSE
# ---------------------------------------------------------------------------
BRANDS_HERO_IMG, BRANDS_HERO_CLASS = _hero("Brands Hero", GAL1)
BRANDS_BODY = f"""<section class="page-banner">
  <img class="{BRANDS_HERO_CLASS}" src="{BRANDS_HERO_IMG}" alt="Custom build detail">
  <div class="page-banner-content">
    <span class="kicker">Brands we endorse</span>
    <h1>Parts, suppliers &amp; brands</h1>
    <p>The names behind the builds.</p>
  </div>
</section>

<section id="recommended-parts">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Recommended parts</span>
      <h2>What goes in the builds</h2>
      <p>This is where you can list specific parts and manufacturers you personally recommend, with notes on why.</p>
      <p class="placeholder-note">Placeholder section — add your real recommended parts here.</p>
    </div>
  </div>
</section>

<section id="trusted-suppliers">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Trusted suppliers</span>
      <h2>Who I source from</h2>
      <p>List the suppliers you trust and buy from regularly, with a line on what they're good for.</p>
      <p class="placeholder-note">Placeholder section — add your real suppliers here.</p>
    </div>
  </div>
</section>

<section id="brands-we-stand-by" style="border-bottom:none;">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Brands we stand by</span>
      <h2>Backed by experience</h2>
      <p>Hover a logo to see which of their products show up in the builds. Click through to shop, or click a product to see it in the gallery.</p>
    </div>
    {render_dynamic.brands_grid_html(CONTENT['brands'], CONTENT['products'])}
  </div>
</section>"""

# ---------------------------------------------------------------------------
# PAGE CONTENT: TERMS (footer link only, not in nav)
# ---------------------------------------------------------------------------
TERMS_BODY = """<section class="page-banner" style="min-height:180px;">
  <div class="page-banner-content">
    <h1>Terms &amp; Conditions</h1>
  </div>
</section>

<section>
  <div class="wrap" style="max-width:820px;">
    <div class="section-head">
      <h2>Orders &amp; Commissions</h2>
      <p>Placeholder terms — replace with your actual policies on deposits, lead times, and order changes before publishing.</p>
    </div>
    <div class="section-head">
      <h2>Returns &amp; Warranty</h2>
      <p>Placeholder terms — outline your real returns, warranty, and repair policy here.</p>
    </div>
    <div class="section-head" style="margin-bottom:0;">
      <h2>Liability</h2>
      <p>Placeholder terms — this page is a starting template only and hasn't been reviewed for legal accuracy. Get it checked before relying on it.</p>
    </div>
  </div>
</section>"""

# All hero/banner locations have now been resolved above, so their CSS
# rule blocks are appended to the shared stylesheet once, here — before
# any page() call embeds CSS into an actual HTML page.
CSS = CSS + "\n" + "\n".join(_HERO_CSS_BLOCKS)

# ---------------------------------------------------------------------------
# WRITE FILES
# ---------------------------------------------------------------------------
pages = {
    "index.html": page("Bitchin' Blasters — Custom Gel Blaster Builds, Queensland",
                        "One-off custom gel blaster builds and upgrades, built to how you play. Queensland-based.",
                        "home", INDEX_BODY),
    "who-we-are.html": page("Who We Are — Bitchin' Blasters",
                             "Why we build, our background, and what you can count on with every Bitchin' Blasters build.",
                             "who-we-are", HOW_WE_ARE_BODY),
    "your-build.html": page("Your Build — Bitchin' Blasters",
                             "Commission a dream build, upgrade your own blaster, or send a general enquiry.",
                             "your-build", YOUR_BUILD_BODY, YOUR_BUILD_SCRIPT),
    "3d-printing.html": page("3D Printing — Bitchin' Blasters",
                              "In-stock and print-to-order 3D printed parts, plus where to find STL files.",
                              "3d-printing", PRINTING_BODY),
    "store.html": page("Store — Bitchin' Blasters",
                        "Gel balls and hop-ups, spare part deals, and used blasters.",
                        "store", STORE_BODY),
    "build-gallery.html": page("Build Gallery — Bitchin' Blasters",
                                "Custom gel blaster builds, in-play action shots, and videos.",
                                "build-gallery", GALLERY_BODY,
                                render_dynamic.GALLERY_FILTER_SCRIPT + render_dynamic.VIDEO_SYSTEM_SCRIPT),
    "brands.html": page("Brands We Endorse — Bitchin' Blasters",
                         "Recommended parts, trusted suppliers, and the brands behind the builds.",
                         "brands", BRANDS_BODY),
    "terms.html": page("Terms & Conditions — Bitchin' Blasters",
                        "Terms and conditions for Bitchin' Blasters.",
                        "", TERMS_BODY),
}

for fname, content in pages.items():
    with open(os.path.join(BASE, fname), "w", encoding="utf-8") as f:
        f.write(content)
    print(fname, len(content))

render_dynamic.write_detail_pages(
    BASE,
    lambda title, desc, active, body: page(title, desc, active, body, render_dynamic.VIDEO_SYSTEM_SCRIPT),
    CONTENT
)
print(f"detail pages: {len(CONTENT['portfolio'])}")

print("DONE")

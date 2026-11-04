"""
sale_banner.py

Reads "User Input/sale-banner/sale-banner.txt" and produces:
  - a popup shown on the home page after a delay (default 60 seconds)
  - a banner shown at the top of the Store page

Both come from the same text file, so changing the sale means editing one file.
If Enabled is "no" (or the Title is blank) neither one appears.
"""

import html
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "User Input", "sale-banner")

KEYS = ("Enabled", "Popup", "Title", "Description", "Button", "Link", "Delay")


def load():
    """Returns a dict (title, description, button, link, delay) or None if switched off."""
    path = os.path.join(ROOT, "sale-banner.txt")
    if not os.path.exists(path):
        return None
    fields = {}
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            m = re.match(r"^(" + "|".join(KEYS) + r"):\s*(.*)$", raw.strip())
            if m:
                fields[m.group(1)] = m.group(2).strip()

    if fields.get("Enabled", "yes").lower() not in ("yes", "y", "true", "on", "1"):
        return None
    title = fields.get("Title", "")
    if not title:
        return None
    try:
        delay = max(0, int(float(fields.get("Delay", "60"))))
    except ValueError:
        delay = 60
    link = fields.get("Link", "")
    if link and not re.match(r"^[a-z][a-z0-9+.-]*:", link, re.I):
        link = "https://" + link  # allow pasting a link without https://
    return {
        "title": title,
        "description": fields.get("Description", ""),
        "button": fields.get("Button", "") or "View the Sale",
        "link": link,
        "delay": delay,
        "popup": fields.get("Popup", "yes").lower() in ("yes", "y", "true", "on", "1"),
    }


def _button(sale, extra_class="btn primary", close_popup=False):
    if not sale["link"]:
        return ""
    attrs = ' data-sale-close' if close_popup else ""
    return (f'<a href="{html.escape(sale["link"], quote=True)}" target="_blank" rel="noopener" '
            f'class="{extra_class}"{attrs}>{html.escape(sale["button"])}</a>')


def popup_html(sale):
    if not sale or not sale.get("popup", True):
        return ""
    desc = f'<p>{html.escape(sale["description"])}</p>' if sale["description"] else ""
    return f'''<div class="sale-popup" id="sale-popup" role="dialog" aria-modal="true" aria-labelledby="sale-popup-title">
  <div class="sale-popup-panel">
    <button type="button" class="sale-popup-close" id="sale-popup-close" aria-label="Close this pop-up">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5 L19 19 M19 5 L5 19" /></svg>
    </button>
    <span class="kicker">Sale on now</span>
    <h2 id="sale-popup-title">{html.escape(sale["title"])}</h2>
    {desc}
    {_button(sale, "btn primary", close_popup=True)}
  </div>
</div>'''


def popup_script(sale):
    if not sale or not sale.get("popup", True):
        return ""
    return """
  // ---- Sale pop-up: opens once per visit, after the delay set in sale-banner.txt ----
  (function(){
    const popup = document.getElementById('sale-popup');
    if (!popup) return;
    const KEY = 'bb-sale-popup-closed';
    function alreadyClosed(){ try { return sessionStorage.getItem(KEY) === '1'; } catch(e) { return false; } }
    function remember(){ try { sessionStorage.setItem(KEY, '1'); } catch(e) {} }
    function closePopup(){ popup.classList.remove('open'); remember(); }
    if (alreadyClosed()) return;
    setTimeout(function(){
      popup.classList.add('open');
      document.getElementById('sale-popup-close').focus();
    }, %d);
    document.getElementById('sale-popup-close').addEventListener('click', closePopup);
    popup.addEventListener('click', function(e){ if (e.target === popup) closePopup(); });
    popup.querySelectorAll('[data-sale-close]').forEach(function(el){ el.addEventListener('click', closePopup); });
    document.addEventListener('keydown', function(e){ if (e.key === 'Escape') closePopup(); });
  })();
""" % (sale["delay"] * 1000)


def store_banner_html(sale):
    if not sale:
        return ""
    desc = f'<p>{html.escape(sale["description"])}</p>' if sale["description"] else ""
    return f'''<div class="promo-banner sale-store-banner">
      <div>
        <span class="kicker">Sale on now</span>
        <h3>{html.escape(sale["title"])}</h3>
        {desc}
      </div>
      {_button(sale)}
    </div>'''

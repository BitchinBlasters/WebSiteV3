"""
visit_counter.py
A tiny, first-party page-view counter (no third-party analytics service).

Reads "User Input/analytics/visit-counter.txt" for `Endpoint:` (the Google Apps Script web app that
appends one row per page view to the "Site Visits" tab of the sign-ups sheet). With no endpoint,
nothing is added to the pages at all.

What is sent per page view: the page path, the referring site (host only), Mobile/Desktop, and a random
visitor ID kept in the visitor's own browser. No IP address, name, email or cookie is stored.
It does nothing on localhost / file previews, when the browser sends Do Not Track, or in a browser
that has opened any page with ?notrack on the end (use that once on your own phone and PC).
"""
import json
import os
import re

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "User Input", "analytics", "visit-counter.txt")


def endpoint():
    if not os.path.exists(PATH):
        return ""
    with open(PATH, "r", encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^Endpoint:\s*(\S+)\s*$", line.strip())
            if m and m.group(1).startswith("https://script.google.com/"):
                return m.group(1)
    return ""


SCRIPT = """<script>
(function(){
  try {
    var EP = %s;
    if (!EP) return;
    if (location.protocol === 'file:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1') return;
    if (navigator.doNotTrack === '1') return;
    try {
      if (location.search.indexOf('notrack') > -1) localStorage.setItem('bb_notrack', '1');
      if (localStorage.getItem('bb_notrack')) return;
    } catch (e) {}
    var vid = '';
    try {
      vid = localStorage.getItem('bb_vid');
      if (!vid) { vid = Math.random().toString(36).slice(2, 10) + Date.now().toString(36); localStorage.setItem('bb_vid', vid); }
    } catch (e) {}
    var ref = '';
    try { ref = document.referrer ? new URL(document.referrer).hostname : ''; } catch (e) {}
    if (ref === location.hostname) ref = '';
    var data = {
      page: location.pathname.replace(/index\\.html$/, '') || '/',
      ref: ref || 'direct',
      device: /Mobi|Android|iPhone|iPad/i.test(navigator.userAgent) ? 'Mobile' : 'Desktop',
      vid: vid
    };
    fetch(EP, { method: 'POST', mode: 'no-cors', keepalive: true,
      headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(data) });
  } catch (e) {}
})();
</script>"""


def script_html():
    ep = endpoint()
    if not ep:
        return ""
    return SCRIPT % json.dumps(ep)

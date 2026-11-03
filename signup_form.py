"""
signup_form.py
Builds the news sign-up page (signup.html) body and script.

Reads "User Input/signup/signup-settings.txt" for an optional `Endpoint:` (the Google Apps Script
web app address that writes to the sign-up Google Sheet). With no endpoint the form falls back to
opening the visitor's email app (same as the other forms on the site).
"""
import json
import os
import re

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "User Input", "signup", "signup-settings.txt")

CATEGORIES = [
    ("sales", "Sales &amp; Deals"),
    ("events", "Events &amp; Field Updates"),
    ("news", "Industry News &amp; Updates"),
    ("listings", "New Listings:<br>Parts, Prints, Services &amp; More"),
]


def endpoint():
    if not os.path.exists(PATH):
        return ""
    with open(PATH, "r", encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^Endpoint:\s*(\S+)\s*$", line.strip())
            if m and m.group(1).startswith("https://"):
                return m.group(1)
    return ""


def body_html():
    boxes = "\n".join(
        f'        <label class="chk"><input type="checkbox" name="int" value="{v}"><span>{label}</span></label>'
        for v, label in CATEGORIES)
    return f"""<section class="page-banner" style="min-height:180px;">
  <div class="page-banner-content">
    <h1>Stay Up-To-Date</h1>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">News &amp; updates</span>
      <p>Pick what you want to hear about. No spam.</p>
    </div>
    <form class="form-panel" id="su-form" novalidate>
      <div class="field-row">
        <div class="field"><label for="su-name">Name</label><input type="text" id="su-name" autocomplete="name" placeholder="Your name"></div>
        <div class="field"><label for="su-email">Email</label><input type="email" id="su-email" autocomplete="email" placeholder="you@example.com"></div>
      </div>
      <fieldset class="su-cats">
        <legend>What Do You Want To Hear About?</legend>
{boxes}
        <small class="su-hint">Pick at least one. You can change this any time.</small>
      </fieldset>
      <input class="su-hp" type="text" id="su-website" tabindex="-1" autocomplete="off" aria-hidden="true">
      <p class="su-fine">Want to stop or change what you get, or have your information permanently removed? Email <a href="mailto:b1tch1nblasters@gmail.com">b1tch1nblasters@gmail.com</a> and we will sort it within 5 business days. Order invoices and receipts are kept for tax and warranty only. We only use the details you provided here to send the news you pick. See <a href="terms.html">Terms &amp; Conditions</a>.</p>
      <button type="submit" class="btn primary" id="su-send">Sign Me Up</button>
      <p class="su-msg" id="su-msg" role="status"></p>
    </form>
  </div>
</section>"""


CSS = """
  .su-cats{ border:1px solid var(--line); margin:0 0 18px; padding:12px 16px; }
  .su-cats legend{ font-size:13px; font-weight:700; letter-spacing:.04em; text-transform:uppercase; color:var(--text-dim); padding:0 6px; }
  .chk{ display:flex; gap:12px; align-items:flex-start; padding:8px 0; cursor:pointer; font-size:15px; }
  .chk input{ width:20px; height:20px; accent-color:var(--lime); flex:none; margin-top:2px; }
  .su-hint{ display:block; color:var(--text-dim); font-size:12px; margin-top:6px; }
  .su-hp{ position:absolute; left:-9999px; }
  .su-fine{ font-size:12px; color:var(--text-dim); margin:0 0 18px; }
  .su-fine a{ color:var(--lime); }
  .su-msg{ margin:16px 0 0; min-height:1em; color:var(--lime); }
  .su-msg.err{ color:#ff6b6b; }
"""


def script(contact_email):
    ep = json.dumps(endpoint())
    return """
  (function(){
    const form = document.getElementById('su-form');
    if (!form) return;
    const ENDPOINT = %s;
    const msg = document.getElementById('su-msg');
    function say(t, err){ msg.textContent = t; msg.className = 'su-msg' + (err ? ' err' : ''); }
    form.addEventListener('submit', function(e){
      e.preventDefault();
      if (document.getElementById('su-website').value) { say('Thanks! You are on the list. We will be in touch.'); return; }
      const name = document.getElementById('su-name').value.trim();
      const email = document.getElementById('su-email').value.trim();
      const picks = Array.from(form.querySelectorAll('input[name=int]:checked')).map(function(c){ return c.value; });
      if (!name) { say('Please add your name.', true); return; }
      if (!/^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$/.test(email)) { say('Please check your email address.', true); return; }
      if (!picks.length) { say('Please pick at least one thing you want to hear about.', true); return; }
      if (ENDPOINT) {
        say('Sending...');
        const data = new URLSearchParams({ name: name, email: email, interests: picks.join(', ') });
        fetch(ENDPOINT, { method: 'POST', mode: 'no-cors', body: data })
          .then(function(){ form.reset(); say('Thanks! You are on the list. We will be in touch.'); })
          .catch(function(){ say('Something went wrong. Please email %s instead.', true); });
      } else {
        const body = 'NEWS SIGN-UP\\n\\nName: ' + name + '\\nEmail: ' + email + '\\nInterests: ' + picks.join(', ');
        window.location.href = 'mailto:%s?subject=' + encodeURIComponent('News sign-up') + '&body=' + encodeURIComponent(body);
        say('Your email app should open with your sign-up ready to send. Just press send.');
      }
    });
  })();
""" % (ep, contact_email, contact_email)

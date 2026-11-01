"""
terms_content.py
Turns "User Input/terms/terms.txt" into the HTML body of the Terms page.

Format of terms.txt:
  # Last updated: ...      first line, shown under the page title
  ## 1. Heading            a section heading
  plain line               a paragraph
  - line                   a bullet point
  **Lead.** rest of line   bold lead-in words
"""
import html
import os
import re

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "User Input", "terms", "terms.txt")


def _inline(text):
    text = html.escape(text, quote=False)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)


def sections_html():
    if not os.path.exists(PATH):
        return "<p>Terms &amp; Conditions coming soon.</p>"
    out, in_list, in_section = [], False, False
    updated = ""
    with open(PATH, "r", encoding="utf-8") as f:
        lines = [l.rstrip("\n") for l in f]
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("## "):
            if in_list:
                out.append("</ul>"); in_list = False
            if in_section:
                out.append("</div>")
            out.append('<div class="terms-section">')
            out.append(f"<h2>{_inline(s[3:])}</h2>")
            in_section = True
        elif s.startswith("# "):
            updated = s[2:].strip()
        elif s.startswith("- "):
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{_inline(s[2:])}</li>")
        else:
            if in_list:
                out.append("</ul>"); in_list = False
            out.append(f"<p>{_inline(s)}</p>")
    if in_list:
        out.append("</ul>")
    if in_section:
        out.append("</div>")
    head = f'<p class="terms-updated">{_inline(updated)}</p>' if updated else ""
    return head + "\n".join(out)

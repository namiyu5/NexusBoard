#!/usr/bin/env python3
"""
Update Django template `nexus_board/templates/nexus_board/index.html`
with the built Vite assets found in `nexusboard_vue/dist/index.html`.

Usage: run this after building the frontend:
  cd <repo root>
  python scripts/update_django_template.py

It will replace the existing stylesheet/script lines with ones that reference
the static files via Django's `{% static %}` tag.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST_INDEX = ROOT / 'nexusboard_vue' / 'dist' / 'index.html'
TEMPLATE = ROOT / 'nexus_board' / 'templates' / 'nexus_board' / 'index.html'

if not DIST_INDEX.exists():
    print('Error: frontend build not found at', DIST_INDEX)
    raise SystemExit(1)

dist_html = DIST_INDEX.read_text(encoding='utf8')
template_html = TEMPLATE.read_text(encoding='utf8')

# find link rel stylesheet and module script in dist index
css_match = re.search(r'<link[^>]+href=["\'](?P<href>[^"\']+\.css)["\'][^>]*>', dist_html)
js_match = re.search(r'<script[^>]+src=["\'](?P<src>[^"\']+\.js)["\'][^>]*></script>', dist_html)

if not css_match or not js_match:
    print('Error: could not find css or js tag in', DIST_INDEX)
    raise SystemExit(1)

css_href = css_match.group('href').lstrip('/')
js_src = js_match.group('src').lstrip('/')

# Build replacement lines using Django static tag and the nexusboard_vue path
css_line = f"    <link rel=\"stylesheet\" href={{% static 'nexusboard_vue/{css_href}' %}}>"
js_line = f"    <script type=\"module\" crossorigin src={{% static 'nexusboard_vue/{js_src}' %}}></script>"

# Replace existing single lines that include "nexusboard_vue/assets" or the old markers
new_template = re.sub(r"<!-- Built SPA assets[\s\S]*?-->",
                      f"<!-- Built SPA assets (injected) -->\n{css_line}\n{js_line}",
                      template_html,
                      flags=re.IGNORECASE)

if new_template == template_html:
    # fallback: replace the two specific lines if present
    new_template = re.sub(r"<link[^>]*nexusboard_vue[^>]*>\s*<script[^>]*nexusboard_vue[^>]*></script>",
                          f"{css_line}\n{js_line}",
                          template_html)

TEMPLATE.write_text(new_template, encoding='utf8')
print('Updated', TEMPLATE, 'to reference', css_href, 'and', js_src)

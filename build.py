#!/usr/bin/env python3
"""Build a single standalone invitation.html from the project's source files."""

import os

BASE = os.path.dirname(os.path.abspath(__file__))

def read(name):
    with open(os.path.join(BASE, name), 'r', encoding='utf-8') as f:
        return f.read()

def build_modified_app():
    """Return app.js (no API-specific build transforms needed now)."""
    app = read('js/app.js')
    return app


# ── Main: build the standalone HTML ───────────────────────────────────

html_src = read('index.html')
css_src  = read('css/styles.css')
config_js = read('js/config.js')

# Replace external CSS link with inline <style>
html_src = html_src.replace(
    '    <link rel="stylesheet" href="css/styles.css">',
    '<style>\n' + css_src + '\n</style>'
)

# Fix asset paths: css/assets/ -> assets/ (in HTML body only, config.js is inlined later)
html_src = html_src.replace('css/assets/', 'assets/')

# Also fix asset paths in the inlined config.js (gallery, venuePhotos src paths)
# We'll do this after inlining config.js

# Replace external script tags with inline scripts
# Fix asset paths in config.js before inlining
config_js_fixed = config_js.replace('css/assets/', 'assets/')
html_src = html_src.replace(
    '<script src="js/config.js"></script>',
    '<script>\n' + config_js_fixed + '\n</script>'
)

# Build the modified app.js (no API calls, localStorage only)
modified_app = build_modified_app()

html_src = html_src.replace(
    '<script src="js/app.js"></script>',
    '<script>\n' + modified_app + '\n</script>'
)

# Write output
out_path = os.path.join(BASE, 'invitation.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html_src)

print(f'Created {out_path}  ({len(html_src):,} bytes)')

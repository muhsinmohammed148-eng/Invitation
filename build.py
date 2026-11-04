#!/usr/bin/env python3
"""Build a single standalone invitation.html from the project's source files."""

import os

BASE = os.path.dirname(os.path.abspath(__file__))

def read(name):
    with open(os.path.join(BASE, name), 'r', encoding='utf-8') as f:
        return f.read()

def build_modified_app():
    """Return app.js with API calls replaced by localStorage-only logic for wishes."""
    
    app = read('js/app.js')
    
    # ── Replace initWishes ─────────────────────────────────────────
    old_wishes_start = '  (function initWishes() {'
    old_wishes_end_marker = '  const reveal = document.querySelectorAll'
    
    new_wishes = '''  (function initWishes() {
    const track = $("wishesTrack");
    const dotsContainer = $("wishesDots");
    const prevBtn = $("wishesPrev");
    const nextBtn = $("wishesNext");
    if (!track) return;

    // Load guest wishes from localStorage
    let guestWishes = [];
    try { guestWishes = JSON.parse(localStorage.getItem("wedding-guest-wishes") || "[]"); } catch (e) { /* ignore */ }
    let wishes = [...guestWishes, ...(wedding.wishes || [])];
    let current = 0;

    function render() {
      if (!wishes.length) return;
      track.innerHTML = wishes.map((w) => `
        <div class="wish-card">
          <p class="wish-quote">${w.text}</p>
          <p class="wish-author">\\u2014 ${w.author}</p>
        </div>
      `).join("");

      if (dotsContainer) {
        dotsContainer.innerHTML = wishes.map((_, i) => `<button class="carousel-dot${i === 0 ? " active" : ""}" data-index="${i}" aria-label="Go to wish ${i + 1}"></button>`).join("");
      }
    }

    function goTo(index) {
      if (!wishes.length) return;
      current = ((index % wishes.length) + wishes.length) % wishes.length;
      track.style.transform = `translateX(-${current * 100}%)`;
      dotsContainer?.querySelectorAll(".carousel-dot").forEach((dot, i) => {
        dot.classList.toggle("active", i === current);
      });
    }

    render();

    prevBtn?.addEventListener("click", () => goTo(current - 1));
    nextBtn?.addEventListener("click", () => goTo(current + 1));
    dotsContainer?.addEventListener("click", (e) => {
      const dot = e.target.closest(".carousel-dot");
      if (dot) goTo(parseInt(dot.dataset.index, 10));
    });

    let autoTimer = setInterval(() => goTo(current + 1), 6000);
    const carousel = $("wishesCarousel");
    if (carousel) {
      carousel.addEventListener("mouseenter", () => clearInterval(autoTimer));
      carousel.addEventListener("mouseleave", () => { autoTimer = setInterval(() => goTo(current + 1), 6000); });
    }

    let touchStartX = 0;
    track.addEventListener("touchstart", (e) => { touchStartX = e.touches[0].clientX; }, { passive: true });
    track.addEventListener("touchend", (e) => {
      const diff = touchStartX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 50) goTo(current + (diff > 0 ? 1 : -1));
    }, { passive: true });

    /* ── Wish Form ── */
    const wishForm = $("wishForm");
    wishForm?.addEventListener("submit", (event) => {
      event.preventDefault();
      const data = Object.fromEntries(new FormData(event.currentTarget));
      const newWish = { text: data.wish, author: data.name };

      // Save to localStorage
      let stored = [];
      try { stored = JSON.parse(localStorage.getItem("wedding-guest-wishes") || "[]"); } catch (e) { /* ignore */ }
      stored.unshift(newWish);
      localStorage.setItem("wedding-guest-wishes", JSON.stringify(stored));
      wishes = [...stored, ...(wedding.wishes || [])];
      current = 0;
      render();
      goTo(0);
      event.currentTarget.reset();
      set("wishStatus", `Thank you, ${data.name}! Your beautiful wish has been added.`);
      setTimeout(() => set("wishStatus", ""), 4000);
    });
  })();

'''
    
    start_idx = app.index(old_wishes_start)
    end_idx = app.index(old_wishes_end_marker)
    app = app[:start_idx] + new_wishes + app[end_idx:]
    
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

(function () {
  const wedding = window.WEDDING;
  const $ = (id) => document.getElementById(id);
  const groom = wedding.groom.display || wedding.groom.first;
  const set = (id, value) => { const element = $(id); if (element) element.textContent = value; };
  const maps = (query) => `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(query)}`;

  const invitationStateKey = "wedding-invitation-open";
  const gate = $("invitationGate");

  function openInvitation() {
    document.body.classList.remove("is-locked");
    gate?.classList.add("opened");
    sessionStorage.setItem(invitationStateKey, "true");
  }

  function reopenInvitation(event) {
    event?.preventDefault();
    document.body.classList.add("is-locked");
    gate?.classList.remove("opened");
    sessionStorage.removeItem(invitationStateKey);
  }

  document.title = `${wedding.bride.first} & ${groom} — Wedding Invitation`;
  set("coverTagline", wedding.tagline);
  set("brideName", wedding.bride.first); set("groomName", groom);
  set("heroDate", wedding.ceremony.displayDate); set("storyQuote", wedding.quote);
  set("brideParents", wedding.bride.parents); set("groomParents", wedding.groom.parents);
  set("footerMono", wedding.monogram); set("backMonogram", wedding.monogram); set("footerHashtag", wedding.hashtag);
  set("gateMonogram", wedding.monogram); set("gateBride", wedding.bride.first); set("gateGroom", groom);

  const date = new Date(`${wedding.ceremony.date}T12:00:00`);
  set("dateDay", String(date.getDate()).padStart(2, "0"));
  set("dateMonth", date.toLocaleString("en", { month: "long" }));
  set("dateYear", `${date.toLocaleString("en", { weekday: "long" })} · ${date.getFullYear()}`);

  [["ceremony", wedding.ceremony], ["reception", wedding.reception]].forEach(([prefix, event]) => {
    set(`${prefix}Title`, event.title); set(`${prefix}When`, `${event.displayDate} · ${event.displayTime}`);
    set(`${prefix}Where`, `${event.venueName} — ${event.venueHall}`); set(`${prefix}Notes`, event.notes);
    const link = $(`${prefix}Map`); if (link) link.href = maps(event.mapsQuery || wedding.ceremony.mapsQuery);
  });

  $("openInvitation")?.addEventListener("click", openInvitation);
  $("openInvitation")?.addEventListener("keydown", (event) => { if (event.key === "Enter" || event.key === " ") openInvitation(); });
  const reopenButton = document.createElement("a");
  reopenButton.href = "#"; reopenButton.textContent = "Cover"; reopenButton.setAttribute("aria-label", "Reopen invitation cover");
  reopenButton.addEventListener("click", reopenInvitation);
  document.querySelector(".quick-nav")?.prepend(reopenButton);

  let activeEvent = wedding.ceremony;
  document.querySelectorAll("[data-calendar]").forEach((button) => button.addEventListener("click", () => {
    activeEvent = button.dataset.calendar === "reception" ? wedding.reception : wedding.ceremony;
    set("calEventLabel", `${activeEvent.title} · ${activeEvent.displayDate}`);
    const start = activeEvent.date.replaceAll("-", "") + "T" + activeEvent.startTime.replace(":", "") + "00";
    const end = activeEvent.date.replaceAll("-", "") + "T" + activeEvent.endTime.replace(":", "") + "00";
    $("calGoogle").href = `https://calendar.google.com/calendar/render?${new URLSearchParams({ action: "TEMPLATE", text: `${activeEvent.title} — ${wedding.bride.first} & ${groom}`, dates: `${start}/${end}` })}`;
    $("calSheet").hidden = false;
  }));
  $("calClose")?.addEventListener("click", () => { $("calSheet").hidden = true; });

  /* ── Countdown Timer ── */
  (function initCountdown() {
    const target = new Date(`${wedding.ceremony.date}T${wedding.ceremony.startTime}:00`).getTime();
    const pad = (n) => String(n).padStart(2, "0");

    function tick() {
      const now = Date.now();
      const diff = Math.max(0, target - now);
      const days = Math.floor(diff / 86400000);
      const hours = Math.floor((diff % 86400000) / 3600000);
      const minutes = Math.floor((diff % 3600000) / 60000);
      const seconds = Math.floor((diff % 60000) / 1000);
      set("cdDays", pad(days));
      set("cdHours", pad(hours));
      set("cdMinutes", pad(minutes));
      set("cdSeconds", pad(seconds));
    }

    tick();
    setInterval(tick, 1000);
  })();

  /* ── Story Timeline ── */
  (function initTimeline() {
    const container = $("timeline");
    if (!container || !wedding.story?.length) return;

    container.innerHTML = wedding.story.map((item) => `
      <div class="timeline-item">
        <div class="timeline-dot"></div>
        <p class="timeline-date">${item.date}</p>
        <h3 class="timeline-title">${item.title}</h3>
        <p class="timeline-text">${item.text}</p>
      </div>
    `).join("");
  })();

  /* ── Gallery Carousel ── */
  (function initGallery() {
    const track = $("galleryTrack");
    const dotsContainer = $("galleryDots");
    const prevBtn = $("galleryPrev");
    const nextBtn = $("galleryNext");
    if (!track || !wedding.gallery?.length) return;

    const images = wedding.gallery;
    let current = 0;

    track.innerHTML = images.map((img) => `
      <div class="gallery-slide">
        <img src="${img.src}" alt="${img.alt}" loading="lazy">
        ${img.caption ? `<span class="slide-caption">${img.caption}</span>` : ""}
      </div>
    `).join("");

    dotsContainer.innerHTML = images.map((_, i) => `<button class="carousel-dot${i === 0 ? " active" : ""}" data-index="${i}" aria-label="Go to slide ${i + 1}"></button>`).join("");

    function goTo(index) {
      current = ((index % images.length) + images.length) % images.length;
      track.style.transform = `translateX(-${current * 100}%)`;
      dotsContainer.querySelectorAll(".carousel-dot").forEach((dot, i) => {
        dot.classList.toggle("active", i === current);
      });
    }

    prevBtn?.addEventListener("click", () => goTo(current - 1));
    nextBtn?.addEventListener("click", () => goTo(current + 1));
    dotsContainer.addEventListener("click", (e) => {
      const dot = e.target.closest(".carousel-dot");
      if (dot) goTo(parseInt(dot.dataset.index, 10));
    });

    let autoTimer = setInterval(() => goTo(current + 1), 5000);
    const carousel = $("galleryCarousel");
    if (carousel) {
      carousel.addEventListener("mouseenter", () => clearInterval(autoTimer));
      carousel.addEventListener("mouseleave", () => { autoTimer = setInterval(() => goTo(current + 1), 5000); });
    }

    let touchStartX = 0;
    track.addEventListener("touchstart", (e) => { touchStartX = e.touches[0].clientX; }, { passive: true });
    track.addEventListener("touchend", (e) => {
      const diff = touchStartX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 50) goTo(current + (diff > 0 ? 1 : -1));
    }, { passive: true });
  })();

  /* ── Wishes Carousel ── */
  (function initWishes() {
    const track = $("wishesTrack");
    const dotsContainer = $("wishesDots");
    const prevBtn = $("wishesPrev");
    const nextBtn = $("wishesNext");
    if (!track) return;

    let wishes = [...(wedding.wishes || [])];
    let current = 0;
    const API_BASE = '';

    function render() {
      if (!wishes.length) return;
      track.innerHTML = wishes.map((w) => `
        <div class="wish-card">
          <p class="wish-quote">${w.text}</p>
          <p class="wish-author">— ${w.author}</p>
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

    function fetchWishes() {
      fetch(API_BASE + '/api/wishes')
        .then(response => response.json())
        .then(data => {
          if (data.success && Array.isArray(data.wishes) && data.wishes.length) {
            // Prepend guest wishes from backend, then add static wishes
            wishes = [...data.wishes, ...(wedding.wishes || [])];
            current = 0;
            render();
            goTo(0);
          } else {
            // Fallback to static wishes only
            wishes = [...(wedding.wishes || [])];
            render();
          }
        })
        .catch(() => {
          // If API is unavailable, fall back to static wishes
          wishes = [...(wedding.wishes || [])];
          render();
        });
    }

    // Initial render with static wishes, then fetch from API
    render();
    fetchWishes();

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

      // Submit to backend API
      fetch(API_BASE + '/api/wishes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newWish)
      })
      .then(response => response.json())
      .then(result => {
        if (result.success) {
          // Refresh wishes from server
          fetchWishes();
          event.currentTarget.reset();
          set("wishStatus", `Thank you, ${data.name}! Your beautiful wish has been added.`);
          setTimeout(() => set("wishStatus", ""), 4000);
        } else {
          set("wishStatus", result.error || 'Failed to add wish. Please try again.');
          setTimeout(() => set("wishStatus", ""), 4000);
        }
      })
      .catch(() => {
        // Fallback to localStorage if API is unavailable
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
    });
  })();

  const reveal = document.querySelectorAll(".section,.portrait,.film");
  reveal.forEach((element) => element.classList.add("reveal"));
  const observer = new IntersectionObserver((entries) => entries.forEach((entry) => {
    if (entry.isIntersecting) { entry.target.classList.add("is-visible"); observer.unobserve(entry.target); }
  }), { threshold: 0.12 });
  reveal.forEach((element) => observer.observe(element));

  const petals = $("petalLayer");
  const petal = () => {
    if (!petals || document.hidden) return;
    const item = document.createElement("span"); item.className = `petal ${Math.random() > 0.76 ? "gold" : ""}`;
    item.style.left = `${Math.random() * 100}%`; item.style.setProperty("--drift", `${Math.round(Math.random() * 220 - 110)}px`);
    item.style.setProperty("--spin", `${Math.round(Math.random() * 900 - 450)}deg`); item.style.setProperty("--fall-time", `${7 + Math.random() * 7}s`);
    item.style.setProperty("--scale", `${0.45 + Math.random() * 1.05}`); petals.append(item); window.setTimeout(() => item.remove(), 15000);
  };
  for (let i = 0; i < 14; i += 1) window.setTimeout(petal, i * 130);
  window.setInterval(petal, 310);
})();

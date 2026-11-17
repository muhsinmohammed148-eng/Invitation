(function () {
  const wedding = window.WEDDING;
  const $ = (id) => document.getElementById(id);
  const groom = wedding.groom.display || wedding.groom.first;
  const set = (id, value) => { const element = $(id); if (element) element.textContent = value; };
  const maps = (query) => `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(query)}`;

  const invitationStateKey = "wedding-invitation-open";
  const gate = $("invitationGate");
  const gateScene = $("gateScene");
  const doorWrapper = $("doorWrapper");

  function openInvitation() {
    // Add 'open' class to trigger door panels sliding + gate fade animation
    gate?.classList.add("open");
    // Start background music on user gesture (envelope open)
    if (window._startMusicOnOpen) window._startMusicOnOpen();
    // CSS handles: panels slide (1.2s) + gate fades (0.6s with 0.8s delay) = ~2.6s total
    // Unlock body scroll after the full animation completes
    setTimeout(() => {
      document.body.classList.remove("is-locked");
      gate?.classList.add("opened");
      gate?.classList.remove("open");
    }, 2600);
    sessionStorage.setItem(invitationStateKey, "true");
  }

  // Allow clicking the seal or door panels to open
  doorWrapper?.addEventListener("click", openInvitation);
  // Keyboard support: Enter or Space opens the invitation
  doorWrapper?.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      openInvitation();
    }
  });

  function reopenInvitation(event) {
    event?.preventDefault();
    document.body.classList.add("is-locked");
    gate?.classList.remove("opened", "open");
    // Reset gate visibility
    if (gate) {
      gate.style.display = "";
      // Force reflow so the reset is visible
      gate.offsetHeight;
    }
    sessionStorage.removeItem(invitationStateKey);
  }

  document.title = `${groom} & ${wedding.bride.first} — Wedding Invitation`;
  set("coverTagline", wedding.tagline);
  set("brideName", wedding.bride.first); set("groomName", groom);
  set("heroDate", (wedding.event || wedding.ceremony).displayDate); set("storyQuote", wedding.quote);
  set("welcomeLine", wedding.welcomeLine || "");
  set("coupleBlessing", wedding.coupleBlessing || "");
  set("dresscodeText", wedding.dresscode || "");
  set("brideParents", wedding.bride.parents); set("groomParents", wedding.groom.parents);
  set("footerMono", wedding.monogram); set("backMonogram", wedding.monogram); set("footerHashtag", wedding.hashtag);
  set("gateMonogram", wedding.monogram); set("gateBride", groom); set("gateGroom", wedding.bride.first);

  const evt = wedding.event || wedding.ceremony;
  const date = new Date(`${evt.date}T12:00:00`);
  set("dateDay", String(date.getDate()).padStart(2, "0"));
  set("dateMonth", date.toLocaleString("en", { month: "long" }));
  set("dateYear", `${date.toLocaleString("en", { weekday: "long" })} · ${date.getFullYear()}`);

  set("eventTitle", evt.title);
  set("eventWhen", `${evt.displayDate} · ${evt.displayTime}`);
  set("eventWhere", `${evt.venueName} — ${evt.venueHall}`);
  set("eventNotes", evt.notes);
  const mapLink = $("eventMap");
  if (mapLink) mapLink.href = maps(evt.mapsQuery || "");

  // Door wrapper handles click and keyboard — no separate button needed

  const activeEvent = wedding.event || wedding.ceremony;
  $("eventCalendar")?.addEventListener("click", () => {
    set("calEventLabel", `${activeEvent.title} · ${activeEvent.displayDate}`);
    const start = activeEvent.date.replaceAll("-", "") + "T" + activeEvent.startTime.replace(":", "") + "00";
    const end = activeEvent.date.replaceAll("-", "") + "T" + activeEvent.endTime.replace(":", "") + "00";
    $("calGoogle").href = `https://calendar.google.com/calendar/render?${new URLSearchParams({ action: "TEMPLATE", text: `${activeEvent.title} — ${wedding.bride.first} & ${groom}`, dates: `${start}/${end}` })}`;
    $("calSheet").hidden = false;
  });
  $("calClose")?.addEventListener("click", () => { $("calSheet").hidden = true; });

  /* ── Countdown Timer ── */
  (function initCountdown() {
    const target = new Date(`${activeEvent.date}T${activeEvent.startTime}:00`).getTime();
    const pad = (n) => String(n).padStart(2, "0");
    const countdownEl = $("countdownTimer");

    function tick() {
      const now = Date.now();
      const diff = target - now;

      if (diff <= 0) {
        // Wedding day has arrived!
        if (countdownEl) {
          countdownEl.innerHTML = '<p style="font-size:28px;color:var(--gold);font-family:var(--serif);">🎉 The big day is here! 🎉</p>';
        }
        return;
      }

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

    let autoTimer = setInterval(() => goTo(current + 1), 8000);
    const carousel = $("galleryCarousel");
    if (carousel) {
      carousel.addEventListener("mouseenter", () => clearInterval(autoTimer));
      carousel.addEventListener("mouseleave", () => { autoTimer = setInterval(() => goTo(current + 1), 8000); });
    }

    // Keyboard navigation for gallery
    if (carousel) {
      carousel.addEventListener("keydown", (e) => {
        if (e.key === "ArrowLeft") { e.preventDefault(); goTo(current - 1); }
        if (e.key === "ArrowRight") { e.preventDefault(); goTo(current + 1); }
      });
      carousel.setAttribute("tabindex", "0");
    }

    let touchStartX = 0;
    track.addEventListener("touchstart", (e) => { touchStartX = e.touches[0].clientX; }, { passive: true });
    track.addEventListener("touchend", (e) => {
      const diff = touchStartX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 50) goTo(current + (diff > 0 ? 1 : -1));
    }, { passive: true });
  })();

  /* ── RSVP (WhatsApp) ── */
  (function initRsvp() {
    const form = $("rsvpForm");
    if (!form) return;
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const data = Object.fromEntries(new FormData(form));
      const phone = wedding.rsvpWhatsApp || "";
      const msg = [
        `RSVP for Muhsin & Murshida (28 Mar 2027)`,
        `Name: ${data.name || ""}`,
        `Guests: ${data.guests || "1"}`,
        `Attending: ${data.attending || ""}`,
        data.message ? `Message: ${data.message}` : ""
      ].filter(Boolean).join("\n");
      const url = `https://wa.me/${phone}?text=${encodeURIComponent(msg)}`;
      window.open(url, "_blank", "noopener");
      set("rsvpStatus", "Opening WhatsApp to send your RSVP…");
      setTimeout(() => set("rsvpStatus", ""), 5000);
    });
  })();

  const reveal = document.querySelectorAll(".section,.portrait,.film");
  reveal.forEach((element) => {
    element.classList.add("reveal", "reveal-stagger");
  });
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
  const isMobile = window.matchMedia("(max-width: 600px)").matches;
  const initialPetals = isMobile ? 8 : 14;
  const interval = isMobile ? 500 : 310;
  for (let i = 0; i < initialPetals; i += 1) window.setTimeout(petal, i * 130);
  window.setInterval(petal, interval);

  /* ── Music toggle ── */
  (function initMusic() {
    const btn = $("musicToggle");
    const audio = $("bgMusic");
    if (!btn || !audio) return;
    let musicStarted = false;
    function setPlaying() {
      btn.textContent = "🔊 Music";
      btn.setAttribute("aria-label", "Pause music");
    }
    function setPaused() {
      btn.textContent = "🔇 Music";
      btn.setAttribute("aria-label", "Play music");
    }
    async function startMusic() {
      if (musicStarted) return;
      musicStarted = true;
      try {
        await audio.play();
        setPlaying();
      } catch (e) {
        setPaused();
      }
    }
    // Start music on first user interaction (envelope open)
    const origOpen = window._openInvitationRef;
    window._startMusicOnOpen = startMusic;
    btn.addEventListener("click", async () => {
      try {
        if (audio.paused) { await audio.play(); setPlaying(); }
        else { audio.pause(); setPaused(); }
      } catch (e) { setPaused(); }
    });
  })();

  /* ── Video Play/Pause Toggle ── */
  (function initVideo() {
    const filmFrame = document.querySelector(".film-frame");
    const video = document.querySelector(".film video");
    if (!filmFrame || !video) return;

    const btn = document.createElement("button");
    btn.className = "video-play-pause";
    btn.setAttribute("aria-label", "Pause video");
    btn.textContent = "⏸";
    filmFrame.appendChild(btn);

    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      if (video.paused) {
        video.play();
        btn.textContent = "⏸";
        btn.setAttribute("aria-label", "Pause video");
      } else {
        video.pause();
        btn.textContent = "▶";
        btn.setAttribute("aria-label", "Play video");
      }
    });
  })();
})();

# Muhsin & Murshida – Digital Invitation Design Architecture

Nov 16, 2026 · @MUHSIN

Both videos show the same product: a scroll-driven mobile invitation website that opens with a "reveal" (key or wax-sealed envelope), then tells the wedding story in a fixed sequence. This blueprint combines the best of both for your wedding on 28 March 2027 (Sunday) at Vista Convention Center.

## What the two videos have in common

- **Format:** a vertical phone web page (720×1280 in the clips), opened from a link, not an app or a PDF.
- **A tap-to-open intro:** guests must act before they see anything. This builds anticipation and feels like opening a real invitation.
- **One long scroll, one idea per screen:** each section fills the phone, with soft fades between them.
- **Illustrated, not photographic, backgrounds:** painted or line-art scenes (chandelier, palace arch, villa) so the page feels like stationery.
- **Script names, small-caps details:** names in flowing calligraphy; date, time and address in quiet serif type.
- **Live countdown** to the wedding date.
- **Practical blocks:** venue with map link, schedule, RSVP.

## How they differ

|  | Video 1 (Arthur & Lilit, 27.6 s) | Video 2 (Yusup & Enes, 11.9 s) |
| --- | --- | --- |
| Opening | Gold filigree keyhole frame; tap the gold key to unlock | White embossed envelope; gold wax seal (monogram) breaks and the flap lifts |
| Mood | Romantic, European, blush pink and champagne gold | Regal, Central Asian, ivory, gold and deep red carpet |
| Hero scene | Hanging chandelier between pillars, names fade in below | Gold arched gateway with drapes, flowers and a carpet leading to a landscape |
| Content cards | Plain scrolling page with thin ornaments | Arch-shaped (mihrab-like) card laid over the carpet |
| Extras | Quote with couple photo, venue watercolor, dress-code swatches with illustrated guests, RSVP form | Pause/play music button, couple photo at sunset as the closing image |
| Countdown | Days, hours, minutes, seconds in a row | Same four units in large gold numerals |

## Recommended screen architecture

Ten screens, in this order. Screens 1–3 are the "wow" moment; 4–9 are information; 10 is the sign-off.

| # | Screen | Content | Motion |
| --- | --- | --- | --- |
| 1 | Cover / seal | Ivory embossed envelope with a gold wax seal monogram "M & M"; line "Tap to open" | Seal glows slowly; tap cracks it, flap lifts |
| 2 | Gateway | Arched gold door or window frame; "Muhsin & Murshida" in script; "are getting married" | Arch doors part, soft camera push-in; music starts |
| 3 | Welcome card | Arch-shaped card with a short invitation line, families' names, and **28 · 03 · 2027** | Text fades in line by line |
| 4 | Couple | Oval or arched portrait photo; one blessing or favourite line | Slow zoom on photo |
| 5 | Countdown | Days · Hours · Minutes · Seconds to 28 March 2027 | Live ticking numerals |
| 6 | Schedule | Timeline of events with times (Nikah, reception, dinner) | Items reveal as you scroll |
| 7 | Venue | Illustration of Vista Convention Center, address, "View on map" button | Illustration draws in; button opens Google Maps |
| 8 | Dress code | Colour swatches and, optionally, illustrated couple in the palette | Swatches pop in |
| 9 | RSVP | Name, number of guests, attending / not attending, optional message; WhatsApp send button | Form fields slide up |
| 10 | Closing | "We look forward to seeing you", date, small sign-off | Seal or monogram returns; footer credit |

Always-visible controls: a music play/pause button (bottom corner, as in video 2) and a language toggle if you choose bilingual.

## Visual system

- **Palette (proposal):** ivory `#FBF6EE`, champagne gold `#C9A66B`, deep emerald `#1F4D3F` for accents and the carpet or arch, blush `#F2DDD6` for soft backgrounds. Swap emerald for burgundy if you prefer the video 2 look.
- **Typography:** a flowing script for the names, an elegant high-contrast serif (Cormorant style) for body, small letter-spaced caps for labels.
- **Ornament:** gold filigree dividers, embossed paper texture on the envelope, a repeated arch shape as the signature motif.
- **Illustration:** one hero scene (arch gateway) and one venue drawing, both in the same watercolor-and-gold style.
- **Motion rules:** fades and slow zooms only; nothing faster than about 0.8 s; every screen readable without sound.
- **Performance:** compress images, keep first load under about 3 MB so it opens quickly on WhatsApp links.

## Build architecture

- **Front end:** a single mobile-first page (HTML, CSS, light JavaScript) with scroll-snap sections.
- **Assets:** envelope and seal artwork, arch gateway, venue illustration, couple photo, background music (licensed or your own).
- **Countdown:** JavaScript timer targeting 28 March 2027 at the ceremony time.
- **RSVP:** form posting to a Google Sheet or a WhatsApp pre-filled message; the second needs no backend.
- **Sharing:** one short link plus a preview image for WhatsApp.

## Open questions

- [ ] Ceremony and reception times, and the full list of events to show on the schedule.
- [ ] Language: English only, or English with Malayalam or Arabic text?
- [ ] Any blessing, verse or quote to include on the couple screen (I have not assumed one).
- [ ] Parents' and families' names for the welcome card.
- [ ] Colour preference: emerald and gold, or burgundy, or blush?
- [ ] Couple photos, and whether the RSVP should go to WhatsApp or a sheet.

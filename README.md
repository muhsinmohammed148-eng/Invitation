# Wedding Invitation — Standalone Hosting Guide

This is a **single-file** wedding invitation site. No backend, no database, no build tools needed.

## Files You Need

| File | Description |
|---|---|
| `invitation.html` | The entire site in one file (HTML + CSS + JS) |
| `assets/` | Folder with images and video |

That's it. Just these two items — place them in the same directory and you're done.

## Quick Local Preview

```bash
# Any of these will work:
python3 -m http.server 8080
# or
npx serve
# or
php -S localhost:8080
```

Then open `http://localhost:8080/invitation.html` in your browser.

## Hosting Options

### GitHub Pages (Free)

1. Create a new GitHub repository
2. Upload `invitation.html` and the `assets/` folder
3. Go to **Settings → Pages → Source: main branch**
4. Your site will be live at `https://yourusername.github.io/repo-name/invitation.html`

### Netlify (Free)

1. Drag and drop the folder containing `invitation.html` and `assets/` at [app.netlify.com/drop](https://app.netlify.com/drop)
2. Your site is live instantly

### Vercel (Free) — **Recommended**

The project includes a `vercel.json` config and a ready-to-deploy `vercel/` folder.

#### Option A: Deploy via Vercel CLI (fastest)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from the project root
vercel
```

Follow the prompts. The `vercel.json` config handles everything automatically.

#### Option B: Deploy via GitHub

1. Push this entire repository to GitHub
2. Go to [vercel.com](https://vercel.com) and sign in
3. Click **"Add New Project"** → **"Import"** your GitHub repo
4. Vercel will auto-detect the `vercel.json` config
5. Click **"Deploy"** — no extra settings needed

#### Option C: Deploy via Git (any provider)

```bash
# Link your Git repo and deploy
vercel link
vercel deploy --prod
```

#### Custom Domain

After deployment, go to your project settings on Vercel → **Domains** → add your custom domain (e.g., `murshida-and-muhsin.com`). Vercel provides free SSL certificates automatically.

### Any Static Host

Upload `invitation.html` and `assets/` to any web server, shared hosting, or cloud storage with static file serving enabled.

## Features

- **Invitation Gate** — Elegant opening animation
- **Countdown Timer** — Counts down to the wedding date
- **Love Story Timeline** — The couple's journey
- **Video Section** — Autoplay couple's video
- **Event Details** — Ceremony and reception with calendar integration
- **Gallery Carousel** — Image gallery with auto-play and touch support
- **Wishes Carousel** — Wedding wishes with guest submission form
- **Falling Petals** — Animated floral effects
- **Responsive Design** — Works on mobile, tablet, and desktop

## Customization

Edit `invitation.html` directly. Look for the `window.WEDDING` config block near the bottom `<script>` tag to change:

- Couple names, monogram, hashtag
- Wedding date, time, venue details
- Gallery images, story timeline
- Default wishes

## Notes

- **Wishes** are stored in each visitor's browser (localStorage). Without a backend server, guests can't see each other's wishes. For shared wishes, use the `server.py` backend version.
- **Images** are referenced as `assets/filename.ext`. Keep the `assets/` folder next to `invitation.html`.

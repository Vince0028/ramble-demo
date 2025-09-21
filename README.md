# RAMBLE Demo (Flask + React CDN)

This repository contains a Flask-based version of the RAMBLE demo UI so you can run it with a single command on Windows:

    py app.py

The UI and behavior mirror the original Next.js project. It uses React (UMD) and Tailwind CDN (no Node build step), plus Bootstrap (as requested) and Lucide icons via CDN.

## Prerequisites
- Python 3.10+ on Windows

## Setup
1. (Optional) Create a virtual environment

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\activate
   ```

2. Install dependencies

   ```powershell
   py -m pip install -r requirements.txt
   ```

3. Run the app

   ```powershell
   py app.py
   ```

4. Open your browser at:

   http://127.0.0.1:5000/

## Routes
- `/` — Login screen
- `/dashboard` — Main dashboard with countdown, stats, top ramblers, upcoming rounds, challenge modal
- `/groups` — Groups list and in-group chat UI
- `/leaderboard` — Leaderboard with podium, filters, full rankings
- `/profile` — Profile page with achievements, interests, history
- `/quiz` — Pop-up quiz flow

## Assets
- Images are served from the existing Next.js `public/` folder.
- The app expects `public/images/ramble-logo.png`. If you don't have it, the UI falls back to `public/placeholder-logo.png`.

## Notes
- The Next.js app is still present but not required for running the Flask version.
- Tailwind CSS is provided via CDN for zero build configuration. Bootstrap is also included (loaded before Tailwind to avoid overrides).
- Client-side interactions and navigation are implemented with React UMD + JSX compiled in the browser by Babel standalone.

## Development Tips
- If you add your own static assets for Flask, place them under `static/`.
- If you want to revert to the Next.js flow, you can still run:

  ```powershell
  pnpm install
  pnpm dev
  ```

  But this is not necessary for the Flask version.

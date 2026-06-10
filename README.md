# Spotify Playlist Quiz

A desktop quiz game that tests your knowledge of your own Spotify playlists using real music playback via Spotify Connect.

## Requirements

- Python 3.10+
- A Spotify account with **Premium** (required for playback control)
- Spotify open and active on any device (phone, desktop, browser) when playing

## Setup

1. Create an app at [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Add `http://127.0.0.1:8888/callback` as a Redirect URI in your app settings
3. Copy your **Client ID** and **Client Secret** into a `.env` file at the project root:

```
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
REDIRECT_URI=http://127.0.0.1:8888/callback
```

4. Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

5. Run:

```bash
python -m src.main
```

## How it works

1. Click **Connect with Spotify** — your browser opens for OAuth login
2. Choose a playlist from the dropdown
3. Pick your settings (artist hint on/off)
4. Hit **Start Quiz →** — make sure Spotify is playing on a device first

### Each question

- The track plays on your active Spotify device for 15 seconds, then auto-pauses
- Choose the correct song title from 4 options drawn from the same playlist
- Each song appears as the answer **at most once** per round
- The artist is revealed after you answer (even if the hint was hidden)

### Settings

| Option | Default | Effect |
|---|---|---|
| Show artist name | On | Displays the artist as a hint during the question |

## Project structure

```
src/
  controllers/   — one controller per screen, handles events and calls the model
  models/        — Spotify API access, quiz logic, auth state
  views/         — Tkinter UI, one file per screen
  exceptions.py  — app-level error types
  main.py        — entry point
tests/
logging_configs/ — YAML logging config
```

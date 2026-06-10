import json
import pathlib
from datetime import datetime

DATA_FILE = pathlib.Path(__file__).parent.parent.parent / "data" / "leaderboard.json"


class LeaderboardModel:
    """Persist quiz results to a local JSON file.

    Keeping this separate from Model keeps Spotify API concerns and local
    storage concerns in different classes — each with one reason to change.
    """

    def __init__(self):
        DATA_FILE.parent.mkdir(exist_ok=True)

    def save(self, playlist: str, score: int, total: int, show_artist: bool):
        entries = self.load()
        entries.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "playlist": playlist,
            "score": score,
            "total": total,
            "pct": score * 100 // total,
            "show_artist": show_artist,
        })
        DATA_FILE.write_text(json.dumps(entries, indent=2))

    def load(self) -> list[dict]:
        if not DATA_FILE.exists():
            return []
        try:
            return json.loads(DATA_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            return []

    def clear(self):
        if DATA_FILE.exists():
            DATA_FILE.unlink()

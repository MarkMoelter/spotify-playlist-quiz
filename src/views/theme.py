"""
Central design tokens for the app.

Keeping colors and fonts here means restyling the whole app is one file change.
All views import from here rather than hardcoding hex values inline.
"""
from tkinter import ttk

# ── Spotify-inspired palette ──────────────────────────────────────────────────
BG = "#121212"          # main background (near-black)
SURFACE = "#282828"     # elevated surfaces: frames, cards
GREEN = "#1DB954"       # Spotify green — primary action color
GREEN_HOVER = "#1ed760" # slightly lighter green for hover states
TEXT = "#FFFFFF"        # primary text
TEXT_DIM = "#B3B3B3"    # secondary / hint text
DANGER = "#f44336"      # wrong answer red
SUCCESS = "#4caf50"     # correct answer green

# ── Fonts ─────────────────────────────────────────────────────────────────────
FONT_TITLE  = ("Helvetica", 18, "bold")
FONT_HEADER = ("Helvetica", 13, "bold")
FONT_BODY   = ("Helvetica", 11)
FONT_SMALL  = ("Helvetica", 9, "italic")

# ── Widget keyword bundles ────────────────────────────────────────────────────
# Pass these as **LABEL_KW, **BUTTON_KW etc. to avoid repeating bg/fg everywhere.
FRAME_KW  = {"bg": BG}
# font is intentionally excluded — pass it explicitly when you need a non-default size
LABEL_KW  = {"bg": BG, "fg": TEXT, "font": FONT_BODY}
LABEL_DIM = {"bg": BG, "fg": TEXT_DIM, "font": FONT_SMALL}
# Use these when you need to override font — spreads bg/fg only
LABEL_BASE = {"bg": BG, "fg": TEXT}
LABEL_DIM_BASE = {"bg": BG, "fg": TEXT_DIM}


def apply(root):
    """Configure ttk styles and set the root window background.

    Call once from Root.__init__ before any widgets are created.
    ttk.Style is global — one call covers every ttk widget in the app.
    """
    root.configure(bg=BG)

    style = ttk.Style(root)

    # 'clam' is the most customisable built-in theme — the default ('vista' on
    # Windows) ignores many color overrides because it defers to the OS renderer.
    style.theme_use("clam")

    # Primary green button — used for main actions (Connect, Select Playlist, etc.)
    style.configure(
        "Green.TButton",
        background=GREEN,
        foreground=TEXT,
        font=FONT_BODY,
        padding=(12, 6),
        relief="flat",
        borderwidth=0,
    )
    style.map("Green.TButton", background=[("active", GREEN_HOVER)])

    # Subdued button — used for secondary actions (Sign Out, Back, etc.)
    style.configure(
        "Sub.TButton",
        background=SURFACE,
        foreground=TEXT_DIM,
        font=FONT_BODY,
        padding=(10, 5),
        relief="flat",
        borderwidth=0,
    )
    style.map("Sub.TButton", background=[("active", "#333333")])

    # Answer choice buttons — same width, left-aligned text
    style.configure(
        "Choice.TButton",
        background=SURFACE,
        foreground=TEXT,
        font=FONT_BODY,
        padding=(10, 8),
        relief="flat",
        borderwidth=0,
        anchor="w",
    )
    style.map(
        "Choice.TButton",
        background=[("active", "#3a3a3a"), ("disabled", SURFACE)],
        foreground=[("disabled", TEXT_DIM)],
    )

    # Correct / wrong variants reuse Choice layout, just change background
    style.configure("Correct.TButton", background=SUCCESS, foreground=TEXT)
    style.map("Correct.TButton", background=[("disabled", SUCCESS)])

    style.configure("Wrong.TButton", background=DANGER, foreground=TEXT)
    style.map("Wrong.TButton", background=[("disabled", DANGER)])

    # Combobox (playlist selector)
    style.configure(
        "TCombobox",
        fieldbackground=SURFACE,
        background=SURFACE,
        foreground=TEXT,
        selectbackground=SURFACE,
        selectforeground=TEXT,
        arrowcolor=TEXT,
    )

from tkinter import Frame, Label
from tkinter import ttk
from . import theme


class LeaderboardView(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, bg=theme.BG, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ── Header ────────────────────────────────────────────────────────────
        header_row = Frame(self, bg=theme.BG)
        header_row.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 0))
        header_row.grid_columnconfigure(1, weight=1)

        Label(header_row, text="Leaderboard",
              **theme.LABEL_BASE, font=theme.FONT_HEADER).grid(row=0, column=1)

        self.back_btn = ttk.Button(header_row, text="← Back", style="Sub.TButton")
        self.back_btn.grid(row=0, column=2, sticky="e")

        self.clear_btn = ttk.Button(header_row, text="Clear", style="Sub.TButton")
        self.clear_btn.grid(row=0, column=3, padx=(8, 0), sticky="e")

        ttk.Separator(self, orient="horizontal").grid(
            row=0, column=0, sticky="ews", padx=16, pady=(46, 0))

        # ── Table ─────────────────────────────────────────────────────────────
        # ttk.Treeview is Tkinter's table widget — rows and named columns.
        # show="headings" hides the default leftmost tree column we don't need.
        cols = ("date", "playlist", "score", "hint")
        self.table = ttk.Treeview(self, columns=cols, show="headings",
                                   selectmode="none")

        self.table.heading("date",     text="Date")
        self.table.heading("playlist", text="Playlist")
        self.table.heading("score",    text="Score")
        self.table.heading("hint",     text="Artist hint")

        self.table.column("date",     width=130, anchor="center")
        self.table.column("playlist", width=200, anchor="w")
        self.table.column("score",    width=80,  anchor="center")
        self.table.column("hint",     width=90,  anchor="center")

        self.table.grid(row=1, column=0, sticky="nsew", padx=16, pady=8)

        # Scrollbar attached to the table — needed when many entries exist
        scrollbar = ttk.Scrollbar(self, orient="vertical",
                                   command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=1, column=1, sticky="ns", pady=8)

        self.empty_label = Label(self, text="No results yet. Play a quiz!",
                                  **theme.LABEL_DIM)

        # Style the table rows to match the dark theme
        style = ttk.Style()
        style.configure("Treeview",
                         background=theme.SURFACE,
                         foreground=theme.TEXT,
                         fieldbackground=theme.SURFACE,
                         rowheight=28)
        style.configure("Treeview.Heading",
                         background=theme.BG,
                         foreground=theme.TEXT_DIM,
                         font=theme.FONT_BODY)
        style.map("Treeview", background=[("selected", theme.GREEN)])

    def populate(self, entries: list[dict]):
        """Replace table contents with the given entries (newest first)."""
        self.table.delete(*self.table.get_children())

        if not entries:
            self.empty_label.grid(row=2, column=0, pady=8)
            return

        self.empty_label.grid_remove()
        for e in reversed(entries):  # newest first
            hint = "On" if e.get("show_artist", True) else "Off"
            self.table.insert("", "end", values=(
                e["date"],
                e["playlist"],
                f"{e['score']}/{e['total']}  ({e['pct']}%)",
                hint,
            ))

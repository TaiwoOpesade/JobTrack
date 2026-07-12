"""
main.py
CustomTkinter GUI for the Job Listing Tracker.
Visual language and animation system modelled on TaiGuide Main.py.

Layout: a sidebar navigates between pages -
    Home      - animated summary statistics of your job searching
    Search    - search Adzuna listings, save/track from the results
    Saved     - saved listings, filterable with a search bar
    Employers - saved employers, load their current listings in an area
    Outreach  - tracked employers, email drafting and CSV export

    NEVER commit the real .env file - it's already in .gitignore
"""

import os
import datetime
from tkinter import filedialog
import customtkinter as ctk
from dotenv import load_dotenv
from api import search_jobs, AdzunaAPIError
from storage import flag_new_jobs
import contacts
import outreach
import export
import favorites
import employers
import history
import stats
import salary

load_dotenv()  # reads the .env file in this folder into environment variables

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

# Used to personalise outreach email drafts - edit these to suit you
SENDER_NAME = "Taiwo Opesade"
SENDER_BACKGROUND = "a UK sixth-form student"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ══════════════════════════════════════════════════════════════════════════════
# THEME
# ══════════════════════════════════════════════════════════════════════════════

THEME = {
    "bg":             "#0A0F1E",
    "sidebar":        "#0D1426",
    "card":           "#111827",
    "card2":          "#1a2236",
    "text_primary":   "#F1F5F9",
    "text_secondary": "#94A3B8",
    "text_muted":     "#475569",
    "border":         "#1E2D3D",
    "input_bg":       "#111827",
}

# One accent per page, TaiGuide-style
ACCENTS = {
    "home":      "#8B5CF6",
    "search":    "#3B82F6",
    "saved":     "#EC4899",
    "employers": "#10B981",
    "outreach":  "#F59E0B",
}

STATUS_COLORS = {
    "not contacted": "#475569",
    "emailed":       "#3B82F6",
    "replied":       "#10B981",
    "rejected":      "#EF4444",
}

DANGER = "#EF4444"
DANGER_BG = "#3B1A1A"

PAGES = [
    ("home", "🏠  Home"),
    ("search", "🔍  Search"),
    ("saved", "❤  Saved"),
    ("employers", "🏢  Employers"),
    ("outreach", "✉  Outreach"),
]

# Maximum-distance filter choices for the search bar. Adzuna filters
# server-side (km) around the location, which can be a place name or postcode.
DISTANCE_OPTIONS = ["Any distance", "Within 5 km", "Within 10 km",
                    "Within 25 km", "Within 50 km", "Within 100 km"]

# ══════════════════════════════════════════════════════════════════════════════
# ANIMATION HELPERS
# ══════════════════════════════════════════════════════════════════════════════
# Tkinter has no GPU compositing, so "animation" here means stepped tweens driven
# by widget.after(). Every tick guards winfo_exists() so a tween in flight when a
# page is rebuilt simply stops instead of throwing a Tcl error. Set ANIMATIONS to
# False to honour a reduced-motion preference.

ANIMATIONS = True
ANIM_MS = 16   # ~60 fps tick


def _hex_to_rgb(h):
    """Convert '#rrggbb' to an (r, g, b) tuple."""
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb):
    """Convert an (r, g, b) tuple back to '#rrggbb', clamping each channel."""
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c))) for c in rgb)


def lerp_colour(c1, c2, t):
    """Interpolate between two hex colours; t in [0, 1]."""
    a, b = _hex_to_rgb(c1), _hex_to_rgb(c2)
    return _rgb_to_hex(tuple(a[i] + (b[i] - a[i]) * t for i in range(3)))


def ease_out_cubic(t):
    """Cubic ease-out: fast start, gentle landing."""
    return 1 - (1 - t) ** 3


def animate(widget, start, end, duration_ms, apply_fn, easing=ease_out_cubic, on_done=None):
    """Tween a numeric value start->end, calling apply_fn(value) each step.

    Falls through to a single apply_fn(end) call when animations are disabled,
    so every animated property still reaches its final state.
    """
    if not ANIMATIONS or duration_ms <= 0 or start == end:
        try:
            apply_fn(end)
        except Exception:
            pass
        if on_done:
            on_done()
        return
    steps = max(1, duration_ms // ANIM_MS)
    state = {"i": 0}

    def tick():
        if not widget.winfo_exists():
            return
        state["i"] += 1
        t = easing(min(1.0, state["i"] / steps))
        try:
            apply_fn(start + (end - start) * t)
        except Exception:
            return
        if state["i"] < steps:
            widget.after(ANIM_MS, tick)
        elif on_done:
            on_done()

    tick()


def add_hover(card, base, hover, duration_ms=160):
    """Smoothly lerp a frame's fg_color on mouse enter/leave."""
    def _in(_):
        animate(card, 0, 1, duration_ms,
                lambda t: card.configure(fg_color=lerp_colour(base, hover, t)))

    def _out(_):
        animate(card, 0, 1, duration_ms,
                lambda t: card.configure(fg_color=lerp_colour(hover, base, t)))
    card.bind("<Enter>", _in)
    card.bind("<Leave>", _out)


def flash_button(button, flash_text, revert_text, ms=1400):
    """Swap a button's text to a confirmation, then revert after a beat."""
    button.configure(text=flash_text)
    button.after(ms, lambda: button.winfo_exists() and button.configure(text=revert_text))


def cascade(widgets, delay_ms=36):
    """Pack a list of (widget, pack_kwargs) with a staggered slide-in cascade."""
    if not ANIMATIONS:
        for widget, kwargs in widgets:
            widget.pack(**kwargs)
        return
    for i, (widget, kwargs) in enumerate(widgets):
        def show(w=widget, kw=kwargs):
            if w.winfo_exists():
                w.pack(**kw)
        widget.after(i * delay_ms, show)


def draw_ring(parent, done, total, size=110, color="#8B5CF6", surface=None):
    """Draw an animated progress ring sweeping in from 0 with a % count-up."""
    surface = surface or THEME["card"]
    canvas = ctk.CTkCanvas(parent, width=size, height=size, bg=surface,
                            highlightthickness=0, bd=0)
    canvas.pack()
    pct = done / total if total > 0 else 0
    cx = cy = size / 2
    r = size / 2 - 10
    stroke = 10
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                       outline=THEME["card2"], width=stroke)
    arc = canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                            start=90, extent=0,
                            outline=color, width=stroke, style="arc")
    text = canvas.create_text(cx, cy, text="0%", fill=THEME["text_primary"],
                              font=("Arial", int(size / 8), "bold"))

    def _apply(v):
        canvas.itemconfigure(arc, extent=-359.9 * v if v > 0 else 0)
        canvas.itemconfigure(text, text=f"{int(round(v * 100))}%")

    animate(canvas, 0, pct, 650, _apply)
    return canvas


# ══════════════════════════════════════════════════════════════════════════════
# APP
# ══════════════════════════════════════════════════════════════════════════════

class JobTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("JobTrack")
        self.geometry("1150x720")
        self.minsize(980, 600)
        self.configure(fg_color=THEME["bg"])

        self.build_sidebar()

        # --- Content area: one frame per page, swapped by show_page() ---
        self.content = ctk.CTkFrame(self, fg_color=THEME["bg"], corner_radius=0)
        self.content.pack(side="right", expand=True, fill="both")

        self.pages = {}
        self.page_spacers = {}
        self.build_home_page()
        self.build_search_page()
        self.build_saved_page()
        self.build_employers_page()
        self.build_outreach_page()

        self.current_page = None
        self.show_page("home")

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def build_sidebar(self):
        """Build the left navigation sidebar with one button per page."""
        sidebar = ctk.CTkFrame(self, width=210, corner_radius=0, fg_color=THEME["sidebar"])
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        logo = ctk.CTkFrame(sidebar, fg_color="transparent")
        logo.pack(pady=(28, 8), padx=18, fill="x")
        ctk.CTkLabel(logo, text="JobTrack", font=("Arial", 22, "bold"),
                      text_color=ACCENTS["search"]).pack(anchor="w")
        ctk.CTkLabel(logo, text="Job listing tracker", font=("Arial", 11),
                      text_color=THEME["text_muted"]).pack(anchor="w")

        ctk.CTkFrame(sidebar, height=1, fg_color=THEME["border"]).pack(fill="x", padx=14, pady=(8, 16))

        self.nav_buttons = {}
        for page_name, label in PAGES:
            button = ctk.CTkButton(sidebar, text=label, anchor="w", height=42,
                                     corner_radius=8, fg_color="transparent",
                                     hover_color=THEME["card2"],
                                     text_color=THEME["text_secondary"],
                                     font=("Arial", 14),
                                     command=lambda p=page_name: self.show_page(p))
            button.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[page_name] = button

        ctk.CTkLabel(sidebar, text="v2.0  •  Adzuna powered", font=("Arial", 10),
                      text_color=THEME["text_muted"]).pack(side="bottom", pady=16)

    def show_page(self, name):
        """Switch the content area to a page: swap frames, animate the nav
        highlight to the page's accent, and slide the new page's content in."""
        for page in self.pages.values():
            page.pack_forget()
        self.pages[name].pack(expand=True, fill="both")

        for page_name, button in self.nav_buttons.items():
            accent = ACCENTS[page_name]
            if page_name == name:
                animate(button, 0, 1, 220,
                        lambda t, b=button, a=accent:
                        b.configure(fg_color=lerp_colour(THEME["sidebar"], THEME["card2"], t),
                                     text_color=lerp_colour(THEME["text_secondary"], a, t)))
            else:
                button.configure(fg_color="transparent", text_color=THEME["text_secondary"])

        # Slide the page content up from a small offset
        spacer = self.page_spacers[name]
        if ANIMATIONS and self.current_page != name:
            spacer.configure(height=26)
            animate(spacer, 26, 1, 260, lambda v, s=spacer: s.configure(height=max(1, int(v))))
        else:
            spacer.configure(height=1)

        self.current_page = name
        refresh = getattr(self, f"refresh_{name}_page", None)
        if refresh:
            refresh()

    def new_page(self, name):
        """Create a page frame with its slide-in spacer and register it."""
        page = ctk.CTkFrame(self.content, fg_color=THEME["bg"], corner_radius=0)
        self.pages[name] = page
        spacer = ctk.CTkFrame(page, height=1, fg_color="transparent")
        spacer.pack(fill="x")
        spacer.pack_propagate(False)
        self.page_spacers[name] = spacer
        return page

    def add_page_header(self, page, heading, caption, accent):
        """Add the standard accent heading + muted caption at the top of a page."""
        ctk.CTkLabel(page, text=heading, font=("Arial", 24, "bold"), text_color=accent,
                      anchor="w").pack(fill="x", padx=28, pady=(22, 0))
        ctk.CTkLabel(page, text=caption, text_color=THEME["text_muted"], anchor="w",
                      font=("Arial", 13)).pack(fill="x", padx=28, pady=(2, 16))

    def add_accent_stripe(self, card, color):
        """Add the thin coloured stripe across the top of a card."""
        ctk.CTkFrame(card, height=4, fg_color=color, corner_radius=2).pack(fill="x")

    # ------------------------------------------------------------------
    # Home page
    # ------------------------------------------------------------------

    def build_home_page(self):
        """Build the homepage: greeting, stat tiles, rings and recent searches."""
        page = self.new_page("home")

        # Greeting header is rebuilt on refresh (time of day changes)
        self.home_body = ctk.CTkScrollableFrame(page, fg_color=THEME["bg"],
                                                  scrollbar_button_color=THEME["card2"],
                                                  scrollbar_button_hover_color=THEME["border"])
        self.home_body.pack(expand=True, fill="both", padx=16, pady=(4, 16))

    def refresh_home_page(self):
        """Rebuild the homepage: greeting, animated tiles, rings, recent searches."""
        for widget in self.home_body.winfo_children():
            widget.destroy()

        hour = datetime.datetime.now().hour
        greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
        first_name = SENDER_NAME.split()[0]
        ctk.CTkLabel(self.home_body, text=f"{greeting}, {first_name} 👋",
                      font=("Arial", 24, "bold"), text_color=ACCENTS["home"],
                      anchor="w").pack(fill="x", padx=12, pady=(12, 0))
        ctk.CTkLabel(self.home_body, text=datetime.datetime.now().strftime("%A, %d %B %Y"),
                      font=("Arial", 13), text_color=THEME["text_muted"],
                      anchor="w").pack(fill="x", padx=12, pady=(0, 16))

        summary = stats.get_summary_stats()

        # --- Stat tiles, numbers counting up ---
        self.section_label(self.home_body, "📊  Your activity")
        tiles = [
            (summary["searches_run"], "Searches run", ACCENTS["search"]),
            (summary["listings_seen"], "Listings seen", ACCENTS["search"]),
            (summary["saved_listings"], "Saved listings", ACCENTS["saved"]),
            (summary["saved_employers"], "Saved employers", ACCENTS["employers"]),
            (summary["tracked_employers"], "Employers tracked", ACCENTS["outreach"]),
            (summary["emails_sent"], "Emails sent", ACCENTS["outreach"]),
        ]
        for row_tiles in (tiles[:3], tiles[3:]):
            row = ctk.CTkFrame(self.home_body, fg_color="transparent")
            row.pack(fill="x", padx=8, pady=5)
            for value, label, accent in row_tiles:
                self.add_stat_tile(row, value, label, accent)

        # --- Outreach progress rings ---
        self.section_label(self.home_body, "🎯  Outreach progress")
        rings_row = ctk.CTkFrame(self.home_body, fg_color="transparent")
        rings_row.pack(fill="x", padx=8, pady=5)
        ring_data = [
            (summary["emails_sent"], summary["tracked_employers"],
             "Employers contacted", ACCENTS["outreach"]),
            (summary["replies"], summary["emails_sent"],
             "Replies received", ACCENTS["employers"]),
        ]
        for done, total, label, color in ring_data:
            card = ctk.CTkFrame(rings_row, fg_color=THEME["card"], corner_radius=14)
            card.pack(side="left", expand=True, fill="x", padx=6)
            add_hover(card, THEME["card"], THEME["card2"])
            inner = ctk.CTkFrame(card, fg_color="transparent")
            inner.pack(pady=14, padx=14)
            draw_ring(inner, done, total, size=100, color=color)
            ctk.CTkLabel(inner, text=label, font=("Arial", 13, "bold"),
                          text_color=THEME["text_primary"]).pack(pady=(8, 0))
            ctk.CTkLabel(inner, text=f"{done} of {total}" if total else "nothing tracked yet",
                          font=("Arial", 11), text_color=THEME["text_muted"]).pack()

        # --- Recent searches ---
        self.section_label(self.home_body, "🕓  Recent searches")
        recent = history.recent_searches(limit=5)
        if not recent:
            ctk.CTkLabel(self.home_body, text="No searches yet - head to the Search page to begin.",
                          text_color=THEME["text_muted"], anchor="w").pack(fill="x", padx=14)
            return

        rows = []
        for entry in recent:
            where = f" in {entry['location']}" if entry["location"] else ""
            text = (f"“{entry['keyword']}”{where}  •  {entry['results_found']} results "
                    f"({entry['new_found']} new)  •  {entry['date']}")
            row = ctk.CTkFrame(self.home_body, corner_radius=10, fg_color=THEME["card"])
            add_hover(row, THEME["card"], THEME["card2"])
            ctk.CTkLabel(row, text=text, anchor="w", font=("Arial", 12),
                          text_color=THEME["text_secondary"]).pack(fill="x", padx=14, pady=9)
            rows.append((row, {"fill": "x", "padx": 12, "pady": 3}))
        cascade(rows)

    def section_label(self, parent, text):
        """Add a small bold section heading, TaiGuide-style."""
        ctk.CTkLabel(parent, text=text, font=("Arial", 13, "bold"),
                      text_color=THEME["text_secondary"], anchor="w").pack(fill="x", padx=12, pady=(16, 6))

    def add_stat_tile(self, row, value, label, accent):
        """Add one stat tile whose number counts up from 0 on load."""
        tile = ctk.CTkFrame(row, corner_radius=14, fg_color=THEME["card"])
        tile.pack(side="left", expand=True, fill="both", padx=6)
        add_hover(tile, THEME["card"], THEME["card2"])
        self.add_accent_stripe(tile, accent)

        number = ctk.CTkLabel(tile, text="0", font=("Arial", 26, "bold"),
                                text_color=THEME["text_primary"])
        number.pack(anchor="w", padx=16, pady=(10, 0))
        animate(number, 0, value, 600,
                lambda v, n=number: n.configure(text=str(int(round(v)))))
        ctk.CTkLabel(tile, text=label, font=("Arial", 11),
                      text_color=THEME["text_muted"]).pack(anchor="w", padx=16, pady=(0, 12))

    # ------------------------------------------------------------------
    # Search page
    # ------------------------------------------------------------------

    def build_search_page(self):
        """Build the search page: search bar, status line and results list."""
        page = self.new_page("search")
        accent = ACCENTS["search"]

        self.add_page_header(page, "🔍  Search", "Find live listings on Adzuna.", accent)

        search_frame = ctk.CTkFrame(page, corner_radius=14, fg_color=THEME["card"])
        search_frame.pack(fill="x", padx=28, pady=(0, 10))
        self.add_accent_stripe(search_frame, accent)

        bar = ctk.CTkFrame(search_frame, fg_color="transparent")
        bar.pack(fill="x", padx=12, pady=12)

        self.keyword_entry = ctk.CTkEntry(bar, placeholder_text="Job title / keyword",
                                            height=38, fg_color=THEME["input_bg"],
                                            border_color=THEME["border"], font=("Arial", 13))
        self.keyword_entry.pack(side="left", expand=True, fill="x", padx=(0, 8))
        self.keyword_entry.bind("<Return>", lambda e: self.run_search())

        self.location_entry = ctk.CTkEntry(bar, placeholder_text="Location or postcode, e.g. London / LS1 4DY",
                                             height=38, fg_color=THEME["input_bg"],
                                             border_color=THEME["border"], font=("Arial", 13))
        self.location_entry.pack(side="left", expand=True, fill="x", padx=(0, 8))
        self.location_entry.bind("<Return>", lambda e: self.run_search())

        self.distance_menu = ctk.CTkOptionMenu(bar, values=DISTANCE_OPTIONS, height=38,
                                                 width=140, font=("Arial", 12),
                                                 fg_color=THEME["input_bg"],
                                                 button_color=THEME["card2"],
                                                 button_hover_color=THEME["border"])
        self.distance_menu.set(DISTANCE_OPTIONS[0])
        self.distance_menu.pack(side="left", padx=(0, 8))

        self.search_button = ctk.CTkButton(bar, text="Search", height=38, width=120,
                                             corner_radius=9, fg_color=accent,
                                             hover_color="#2563EB", font=("Arial", 13, "bold"),
                                             command=self.run_search)
        self.search_button.pack(side="left")

        self.status_label = ctk.CTkLabel(page, text="Enter a keyword and search to begin.",
                                           text_color=THEME["text_muted"], anchor="w",
                                           font=("Arial", 12))
        self.status_label.pack(fill="x", padx=32, pady=(0, 6))

        self.results_frame = ctk.CTkScrollableFrame(page, label_text="Results",
                                                      corner_radius=14, fg_color=THEME["card"],
                                                      label_fg_color=THEME["card2"],
                                                      scrollbar_button_color=THEME["card2"],
                                                      scrollbar_button_hover_color=THEME["border"])
        self.results_frame.pack(expand=True, fill="both", padx=28, pady=(0, 24))

    def flash_status(self, text, accent):
        """Set the status text and fade its colour from the accent to muted."""
        self.status_label.configure(text=text)
        animate(self.status_label, 0, 1, 900,
                lambda t: self.status_label.configure(
                    text_color=lerp_colour(accent, THEME["text_secondary"], t)))

    def selected_distance(self):
        """Read the distance dropdown as a number of kilometres (0 = no limit)."""
        choice = self.distance_menu.get()
        if choice == "Any distance":
            return 0
        return int(choice.split()[1])

    def run_search(self):
        keyword = self.keyword_entry.get().strip()
        location = self.location_entry.get().strip()
        distance = self.selected_distance()

        if not keyword:
            self.flash_status("Please enter a keyword to search for.", DANGER)
            return
        if distance and not location:
            self.flash_status("Enter a location to filter by distance.", DANGER)
            return

        self.status_label.configure(text="Searching...", text_color=THEME["text_muted"])
        self.search_button.configure(state="disabled")
        self.update_idletasks()  # force UI to repaint before the blocking network call

        try:
            jobs = search_jobs(APP_ID, APP_KEY, keyword, location, distance=distance)
        except AdzunaAPIError as e:
            self.flash_status(f"Error: {e}", DANGER)
            self.search_button.configure(state="normal")
            return

        jobs = flag_new_jobs(jobs)
        new_count = sum(1 for job in jobs if job["is_new"])
        history.record_search(keyword, location, len(jobs), new_count)

        found = f"Found {len(jobs)} listings ({new_count} new since last search)."
        if distance and location:
            found = (f"Found {len(jobs)} listings within {distance} km of "
                     f"{location} ({new_count} new).")
        self.flash_status(found, ACCENTS["search"])
        self.display_jobs(jobs)
        self.search_button.configure(state="normal")

    def run_employer_search(self, company, location):
        """Load all current listings from one saved employer, in an area."""
        self.show_page("search")
        self.status_label.configure(text=f"Loading listings from {company}...",
                                      text_color=THEME["text_muted"])
        self.search_button.configure(state="disabled")
        self.update_idletasks()  # force UI to repaint before the blocking network call

        try:
            jobs = search_jobs(APP_ID, APP_KEY, "", location, company=company)
        except AdzunaAPIError as e:
            self.flash_status(f"Error: {e}", DANGER)
            self.search_button.configure(state="normal")
            return

        jobs = flag_new_jobs(jobs)
        new_count = sum(1 for job in jobs if job["is_new"])
        history.record_search(company, location, len(jobs), new_count)

        where = f" in {location}" if location else ""
        self.flash_status(f"Found {len(jobs)} listings from {company}{where} ({new_count} new).",
                           ACCENTS["employers"])
        self.display_jobs(jobs)
        self.search_button.configure(state="normal")

    def display_jobs(self, jobs):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not jobs:
            ctk.CTkLabel(self.results_frame, text="No listings found.",
                          text_color=THEME["text_muted"]).pack(pady=10)
            return

        cards = [(self.add_job_card(job), {"fill": "x", "pady": 5, "padx": 4}) for job in jobs]
        cascade(cards)

    def add_job_card(self, job):
        """Build one result card; returns it unpacked so results can cascade in."""
        accent = ACCENTS["search"]
        card = ctk.CTkFrame(self.results_frame, corner_radius=12, fg_color=THEME["card2"])
        add_hover(card, THEME["card2"], THEME["border"])
        if job["is_new"]:
            self.add_accent_stripe(card, accent)

        title_text = job["title"]
        if job["is_new"]:
            title_text = "🆕  " + title_text
        ctk.CTkLabel(card, text=title_text, font=("Arial", 15, "bold"),
                      text_color=THEME["text_primary"], anchor="w",
                      justify="left").pack(fill="x", padx=14, pady=(10, 0))

        subtitle = f"{job['company']}  •  {job['location']}"
        if job["salary_min"] and job["salary_max"]:
            subtitle += f"  •  £{int(job['salary_min']):,} - £{int(job['salary_max']):,}"
        hourly = salary.hourly_line(job)
        if hourly:
            subtitle += f"  •  {hourly}"
        ctk.CTkLabel(card, text=subtitle, text_color=THEME["text_muted"], anchor="w",
                      font=("Arial", 12), justify="left").pack(fill="x", padx=14)

        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(anchor="e", padx=14, pady=(6, 10))

        if job["url"]:
            ctk.CTkButton(button_frame, text="View listing", width=100, height=30,
                           corner_radius=8, fg_color=accent, hover_color="#2563EB",
                           font=("Arial", 12),
                           command=lambda u=job["url"]: self.open_link(u)).pack(side="left", padx=(0, 8))

        already_saved = favorites.is_saved(job["id"])
        save_button = ctk.CTkButton(button_frame, text="❤ Saved" if already_saved else "♡ Save",
                                      width=90, height=30, corner_radius=8,
                                      fg_color=THEME["card"], hover_color=THEME["border"],
                                      text_color=ACCENTS["saved"], font=("Arial", 12),
                                      state="disabled" if already_saved else "normal")
        save_button.configure(command=lambda j=job, b=save_button: self.save_listing_clicked(j, b))
        save_button.pack(side="left", padx=(0, 8))

        already_tracked = contacts.is_tracked(job["id"])
        track_button = ctk.CTkButton(button_frame, text="✓ Tracked" if already_tracked else "Track employer",
                                       width=120, height=30, corner_radius=8,
                                       fg_color=THEME["card"], hover_color=THEME["border"],
                                       text_color=ACCENTS["outreach"], font=("Arial", 12),
                                       state="disabled" if already_tracked else "normal")
        track_button.configure(command=lambda j=job, b=track_button: self.track_employer_clicked(j, b))
        track_button.pack(side="left", padx=(0, 8))

        employer_saved = employers.is_saved_employer(job["company"])
        employer_button = ctk.CTkButton(button_frame,
                                          text="✓ Employer saved" if employer_saved else "＋ Save employer",
                                          width=130, height=30, corner_radius=8,
                                          fg_color=THEME["card"], hover_color=THEME["border"],
                                          text_color=ACCENTS["employers"], font=("Arial", 12),
                                          state="disabled" if employer_saved else "normal")
        employer_button.configure(command=lambda j=job, b=employer_button: self.save_employer_clicked(j, b))
        employer_button.pack(side="left")

        return card

    def open_link(self, url):
        import webbrowser
        webbrowser.open(url)

    def save_listing_clicked(self, job, button):
        """Save a listing to favourites and update the button to reflect it."""
        favorites.save_listing(job)
        button.configure(text="❤ Saved", state="disabled")

    def track_employer_clicked(self, job, button):
        """Track the employer behind a job listing and update the button to reflect it."""
        contacts.track_employer(job)
        button.configure(text="✓ Tracked", state="disabled")

    def save_employer_clicked(self, job, button):
        """Save a listing's employer to follow and update the button to reflect it."""
        employers.save_employer(job["company"])
        button.configure(text="✓ Employer saved", state="disabled")

    # ------------------------------------------------------------------
    # Saved listings page
    # ------------------------------------------------------------------

    def build_saved_page(self):
        """Build the saved-listings page: a filter bar over the saved list."""
        page = self.new_page("saved")
        accent = ACCENTS["saved"]

        self.add_page_header(page, "❤  Saved listings", "Listings you've saved to revisit.", accent)

        filter_frame = ctk.CTkFrame(page, corner_radius=14, fg_color=THEME["card"])
        filter_frame.pack(fill="x", padx=28, pady=(0, 10))
        self.add_accent_stripe(filter_frame, accent)

        bar = ctk.CTkFrame(filter_frame, fg_color="transparent")
        bar.pack(fill="x", padx=12, pady=12)

        self.saved_filter_entry = ctk.CTkEntry(bar, height=38, fg_color=THEME["input_bg"],
                                                 border_color=THEME["border"], font=("Arial", 13),
                                                 placeholder_text="Filter by title, company or location")
        self.saved_filter_entry.pack(side="left", expand=True, fill="x", padx=(0, 8))
        self.saved_filter_entry.bind("<KeyRelease>", lambda e: self.refresh_saved_list())

        ctk.CTkButton(bar, text="Clear", width=80, height=38, corner_radius=9,
                       fg_color=THEME["card2"], hover_color=THEME["border"],
                       text_color=THEME["text_secondary"], font=("Arial", 12),
                       command=self.clear_saved_filter).pack(side="left")

        self.saved_list_frame = ctk.CTkScrollableFrame(page, label_text="Saved",
                                                         corner_radius=14, fg_color=THEME["card"],
                                                         label_fg_color=THEME["card2"],
                                                         scrollbar_button_color=THEME["card2"],
                                                         scrollbar_button_hover_color=THEME["border"])
        self.saved_list_frame.pack(expand=True, fill="both", padx=28, pady=(0, 24))

    def refresh_saved_page(self):
        """Refresh the saved-listings list when the page is shown."""
        self.refresh_saved_list()

    def clear_saved_filter(self):
        """Clear the saved-listings filter and show everything again."""
        self.saved_filter_entry.delete(0, "end")
        self.refresh_saved_list()

    def refresh_saved_list(self):
        """Rebuild the saved-listings list, applying the filter text if any."""
        for widget in self.saved_list_frame.winfo_children():
            widget.destroy()

        query = self.saved_filter_entry.get().strip().lower()
        saved = favorites.load_favorites()
        if query:
            saved = [job for job in saved
                     if query in (job["title"] or "").lower()
                     or query in (job["company"] or "").lower()
                     or query in (job["location"] or "").lower()]

        if not saved:
            message = "No saved listings match your filter." if query else \
                      "Nothing saved yet - use ♡ Save on a search result."
            ctk.CTkLabel(self.saved_list_frame, text=message,
                          text_color=THEME["text_muted"]).pack(pady=10)
            return

        cards = [(self.add_saved_card(job), {"fill": "x", "pady": 5, "padx": 4}) for job in saved]
        cascade(cards)

    def add_saved_card(self, job):
        """Build one card on the saved-listings page; returned unpacked for cascade."""
        card = ctk.CTkFrame(self.saved_list_frame, corner_radius=12, fg_color=THEME["card2"])
        add_hover(card, THEME["card2"], THEME["border"])
        self.add_accent_stripe(card, ACCENTS["saved"])

        ctk.CTkLabel(card, text=job["title"], font=("Arial", 15, "bold"),
                      text_color=THEME["text_primary"], anchor="w",
                      justify="left").pack(fill="x", padx=14, pady=(10, 0))

        subtitle = f"{job['company']}  •  {job['location']}  •  saved {job['date_saved']}"
        if job["salary_min"] and job["salary_max"]:
            subtitle += f"  •  £{int(job['salary_min']):,} - £{int(job['salary_max']):,}"
        hourly = salary.hourly_line(job)
        if hourly:
            subtitle += f"  •  {hourly}"
        ctk.CTkLabel(card, text=subtitle, text_color=THEME["text_muted"], anchor="w",
                      font=("Arial", 12), justify="left").pack(fill="x", padx=14)

        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.pack(anchor="e", padx=14, pady=(6, 10))

        if job["url"]:
            ctk.CTkButton(button_frame, text="View listing", width=100, height=30,
                           corner_radius=8, fg_color=ACCENTS["search"], hover_color="#2563EB",
                           font=("Arial", 12),
                           command=lambda u=job["url"]: self.open_link(u)).pack(side="left", padx=(0, 8))

        already_tracked = contacts.is_tracked(job["id"])
        track_button = ctk.CTkButton(button_frame, text="✓ Tracked" if already_tracked else "Track employer",
                                       width=120, height=30, corner_radius=8,
                                       fg_color=THEME["card"], hover_color=THEME["border"],
                                       text_color=ACCENTS["outreach"], font=("Arial", 12),
                                       state="disabled" if already_tracked else "normal")
        track_button.configure(command=lambda j=job, b=track_button: self.track_employer_clicked(j, b))
        track_button.pack(side="left", padx=(0, 8))

        ctk.CTkButton(button_frame, text="✕ Remove", width=90, height=30, corner_radius=8,
                       fg_color=DANGER_BG, hover_color=DANGER, text_color=DANGER,
                       font=("Arial", 12),
                       command=lambda i=job["id"]: self.remove_saved_listing(i)).pack(side="left")

        return card

    def remove_saved_listing(self, job_id):
        """Remove a listing from favourites and refresh the list."""
        favorites.unsave_listing(job_id)
        self.refresh_saved_list()

    # ------------------------------------------------------------------
    # Saved employers page
    # ------------------------------------------------------------------

    def build_employers_page(self):
        """Build the saved-employers page: add bar plus employer rows."""
        page = self.new_page("employers")
        accent = ACCENTS["employers"]

        self.add_page_header(page, "🏢  Saved employers",
                              "Employers you follow - load their current listings in an area.", accent)

        add_frame = ctk.CTkFrame(page, corner_radius=14, fg_color=THEME["card"])
        add_frame.pack(fill="x", padx=28, pady=(0, 10))
        self.add_accent_stripe(add_frame, accent)

        bar = ctk.CTkFrame(add_frame, fg_color="transparent")
        bar.pack(fill="x", padx=12, pady=12)

        self.employer_name_entry = ctk.CTkEntry(bar, height=38, fg_color=THEME["input_bg"],
                                                  border_color=THEME["border"], font=("Arial", 13),
                                                  placeholder_text="Employer name, e.g. Tesco")
        self.employer_name_entry.pack(side="left", expand=True, fill="x", padx=(0, 8))
        self.employer_name_entry.bind("<Return>", lambda e: self.add_employer_clicked())

        ctk.CTkButton(bar, text="＋ Save employer", width=140, height=38, corner_radius=9,
                       fg_color=accent, hover_color="#059669", font=("Arial", 13, "bold"),
                       command=self.add_employer_clicked).pack(side="left")

        self.employers_list_frame = ctk.CTkScrollableFrame(page, label_text="Following",
                                                             corner_radius=14, fg_color=THEME["card"],
                                                             label_fg_color=THEME["card2"],
                                                             scrollbar_button_color=THEME["card2"],
                                                             scrollbar_button_hover_color=THEME["border"])
        self.employers_list_frame.pack(expand=True, fill="both", padx=28, pady=(0, 24))

    def refresh_employers_page(self):
        """Rebuild the saved-employers list when the page is shown."""
        for widget in self.employers_list_frame.winfo_children():
            widget.destroy()

        saved = employers.load_employers()
        if not saved:
            ctk.CTkLabel(self.employers_list_frame,
                          text="No employers saved yet - add one above, or use ＋ Save employer on a search result.",
                          text_color=THEME["text_muted"]).pack(pady=10)
            return

        rows = [(self.add_employer_row(employer), {"fill": "x", "pady": 5, "padx": 4})
                for employer in saved]
        cascade(rows)

    def add_employer_row(self, employer):
        """Build one row on the saved-employers page; returned unpacked for cascade."""
        accent = ACCENTS["employers"]
        row = ctk.CTkFrame(self.employers_list_frame, corner_radius=12, fg_color=THEME["card2"])
        add_hover(row, THEME["card2"], THEME["border"])
        self.add_accent_stripe(row, accent)

        ctk.CTkLabel(row, text=employer["name"], font=("Arial", 15, "bold"),
                      text_color=THEME["text_primary"], anchor="w",
                      justify="left").pack(fill="x", padx=14, pady=(10, 0))
        ctk.CTkLabel(row, text=f"following since {employer['date_saved']}",
                      text_color=THEME["text_muted"], anchor="w",
                      font=("Arial", 11)).pack(fill="x", padx=14)

        controls = ctk.CTkFrame(row, fg_color="transparent")
        controls.pack(fill="x", padx=14, pady=(6, 10))

        area_entry = ctk.CTkEntry(controls, placeholder_text="Area, e.g. London (optional)",
                                    height=32, fg_color=THEME["input_bg"],
                                    border_color=THEME["border"], font=("Arial", 12))
        area_entry.pack(side="left", expand=True, fill="x", padx=(0, 8))
        area_entry.bind("<Return>", lambda e, n=employer["name"], a=area_entry:
                        self.run_employer_search(n, a.get().strip()))

        ctk.CTkButton(controls, text="Load listings", width=110, height=32, corner_radius=8,
                       fg_color=accent, hover_color="#059669", font=("Arial", 12),
                       command=lambda n=employer["name"], a=area_entry:
                       self.run_employer_search(n, a.get().strip())).pack(side="left", padx=(0, 8))

        ctk.CTkButton(controls, text="✕ Remove", width=90, height=32, corner_radius=8,
                       fg_color=DANGER_BG, hover_color=DANGER, text_color=DANGER,
                       font=("Arial", 12),
                       command=lambda n=employer["name"]: self.remove_employer_clicked(n)).pack(side="left")

        return row

    def add_employer_clicked(self):
        """Save the employer typed into the add bar and refresh the list."""
        name = self.employer_name_entry.get().strip()
        if not name:
            return
        employers.save_employer(name)
        self.employer_name_entry.delete(0, "end")
        self.refresh_employers_page()

    def remove_employer_clicked(self, name):
        """Stop following an employer and refresh the list."""
        employers.remove_employer(name)
        self.refresh_employers_page()

    # ------------------------------------------------------------------
    # Outreach page
    # ------------------------------------------------------------------

    def build_outreach_page(self):
        """Build the outreach page: tracked employers with contact controls."""
        page = self.new_page("outreach")
        accent = ACCENTS["outreach"]

        self.add_page_header(page, "✉  Outreach",
                              "Employers you're contacting - drafts open in your mail client, unsent.",
                              accent)

        toolbar = ctk.CTkFrame(page, fg_color="transparent")
        toolbar.pack(fill="x", padx=28, pady=(0, 6))
        self.export_button = ctk.CTkButton(toolbar, text="⬇ Export CSV", width=120, height=32,
                                             corner_radius=8, fg_color=THEME["card"],
                                             hover_color=THEME["card2"],
                                             text_color=THEME["text_secondary"], font=("Arial", 12),
                                             command=self.export_outreach_csv)
        self.export_button.pack(side="right")

        self.outreach_list_frame = ctk.CTkScrollableFrame(page, label_text="Tracked employers",
                                                            corner_radius=14, fg_color=THEME["card"],
                                                            label_fg_color=THEME["card2"],
                                                            scrollbar_button_color=THEME["card2"],
                                                            scrollbar_button_hover_color=THEME["border"])
        self.outreach_list_frame.pack(expand=True, fill="both", padx=28, pady=(0, 24))

    def refresh_outreach_page(self):
        """Refresh the outreach list when the page is shown."""
        self.refresh_outreach_list()

    def refresh_outreach_list(self):
        """Clear and repopulate the outreach page's list of tracked employers."""
        for widget in self.outreach_list_frame.winfo_children():
            widget.destroy()

        tracked = contacts.load_contacts()

        if not tracked:
            ctk.CTkLabel(self.outreach_list_frame,
                          text="No employers tracked yet - use Track employer on a search result.",
                          text_color=THEME["text_muted"]).pack(pady=10)
            return

        rows = [(self.add_outreach_row(contact), {"fill": "x", "pady": 5, "padx": 4})
                for contact in tracked]
        cascade(rows)

    def add_outreach_row(self, contact):
        """Build one row on the outreach page; returned unpacked for cascade."""
        row = ctk.CTkFrame(self.outreach_list_frame, corner_radius=12, fg_color=THEME["card2"])
        add_hover(row, THEME["card2"], THEME["border"])
        self.add_accent_stripe(row, STATUS_COLORS.get(contact["status"], THEME["text_muted"]))

        header_text = f"{contact['company']}  •  {contact['job_title']}"
        ctk.CTkLabel(row, text=header_text, font=("Arial", 14, "bold"),
                      text_color=THEME["text_primary"], anchor="w",
                      justify="left").pack(fill="x", padx=14, pady=(10, 4))

        controls_frame = ctk.CTkFrame(row, fg_color="transparent")
        controls_frame.pack(fill="x", padx=14, pady=(0, 10))

        email_entry = ctk.CTkEntry(controls_frame, placeholder_text="Contact email",
                                     height=32, fg_color=THEME["input_bg"],
                                     border_color=THEME["border"], font=("Arial", 12))
        email_entry.insert(0, contact["contact_email"])
        email_entry.pack(side="left", expand=True, fill="x", padx=(0, 8))

        draft_button = ctk.CTkButton(controls_frame, text="✉ Draft email", width=110, height=32,
                                       corner_radius=8, fg_color=ACCENTS["outreach"],
                                       hover_color="#D97706", font=("Arial", 12),
                                       state="normal" if contact["contact_email"].strip() else "disabled",
                                       command=lambda c=contact, entry=email_entry: self.draft_outreach_email(c, entry))

        status_menu = ctk.CTkOptionMenu(controls_frame, values=contacts.VALID_STATUSES,
                                          height=32, width=140, font=("Arial", 12),
                                          fg_color=THEME["card"],
                                          button_color=STATUS_COLORS.get(contact["status"], THEME["card"]),
                                          button_hover_color=THEME["border"],
                                          command=lambda new_status, j=contact["job_id"], r=row:
                                          self.change_status(j, new_status))
        status_menu.set(contact["status"])
        status_menu.pack(side="left", padx=(0, 8))

        draft_button.pack(side="left", padx=(0, 8))

        ctk.CTkButton(controls_frame, text="✕ Remove", width=90, height=32, corner_radius=8,
                       fg_color=DANGER_BG, hover_color=DANGER, text_color=DANGER,
                       font=("Arial", 12),
                       command=lambda j=contact["job_id"]: self.remove_contact(j)).pack(side="left")

        # Persist the email when the field loses focus, and keep the Draft
        # button's enabled state in sync with what's currently typed - without
        # rebuilding the whole list mid-edit.
        email_entry.bind("<KeyRelease>", lambda e, entry=email_entry, btn=draft_button: self.update_draft_button_state(entry, btn))
        email_entry.bind("<FocusOut>", lambda e, c=contact, entry=email_entry: self.save_contact_email(c, entry))
        email_entry.bind("<Return>", lambda e, c=contact, entry=email_entry: self.save_contact_email(c, entry))

        return row

    def update_draft_button_state(self, entry, button):
        """Enable the Draft email button only when a contact email has been typed."""
        button.configure(state="normal" if entry.get().strip() else "disabled")

    def save_contact_email(self, contact, entry):
        """Persist the contact email typed into an outreach row.

        Updates both the on-disk record and the in-memory contact dict so the
        Draft email button always uses the latest address. Does not rebuild the
        list, so editing one row never disturbs another.
        """
        email = entry.get().strip()
        contacts.set_contact_email(contact["job_id"], email)
        contact["contact_email"] = email

    def change_status(self, job_id, new_status):
        """Persist a status change from an outreach row's dropdown, then rebuild
        the list so the row's stripe and dropdown colour reflect the new status."""
        contacts.set_status(job_id, new_status)
        self.refresh_outreach_list()

    def remove_contact(self, job_id):
        """Stop tracking an employer and refresh the outreach list."""
        contacts.untrack_employer(job_id)
        self.refresh_outreach_list()

    def draft_outreach_email(self, contact, entry, button=None):
        """Build an email draft for a tracked employer and open it in the mail client."""
        self.save_contact_email(contact, entry)
        if not contact["contact_email"]:
            return
        draft = outreach.build_draft(contact, SENDER_NAME, SENDER_BACKGROUND)
        outreach.open_in_mail_client(contact, draft["subject"], draft["body"])
        if button is not None:
            flash_button(button, "✓ Opened", "✉ Draft email")

    def export_outreach_csv(self):
        """Prompt for a save location and export tracked outreach records to CSV."""
        path = filedialog.asksaveasfilename(parent=self, defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")])
        if path:
            export.export_contacts_csv(path)
            flash_button(self.export_button, "✓ Exported", "⬇ Export CSV")


if __name__ == "__main__":
    if not APP_ID or not APP_KEY:
        print("ERROR: ADZUNA_APP_ID / ADZUNA_APP_KEY not found.")
        print("Copy .env.example to .env and fill in your Adzuna credentials.")
    else:
        app = JobTrackerApp()
        app.mainloop()

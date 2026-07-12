"""
TaiGuide – A-Level Revision Tracker
Subjects: AQA Computer Science | Edexcel Business | Edexcel Economics
Built with CustomTkinter
"""

import customtkinter as ctk
import datetime
import json
import os
import math
import random

# ── Persistence ────────────────────────────────────────────────────────────────
DATA_FILE = "taiguide_data.json"

# ══════════════════════════════════════════════════════════════════════════════
# CURRICULUM DATA
# ══════════════════════════════════════════════════════════════════════════════

CURRICULUM = {
    "cs": {
        "name": "Computer Science",
        "board": "AQA",
        "color": "#3B82F6",
        "icon": "💻",
        "papers": {
            "Paper 1": {
                "desc": "PPE – 19 June 2026, 09:00–10:45, Room J41  |  Sections A, B, C & D",
                "sections": {
                    "Section 1 – Fundamentals of Programming (pg. 2–32)": [
                        "Data types: integer, real, Boolean, character, string",
                        "Variables and constants",
                        "Arithmetic operators (+, –, *, /, DIV, MOD, ^)",
                        "Relational operators (=, ≠, <, >, ≤, ≥)",
                        "Boolean operators (AND, OR, NOT)",
                        "Sequence",
                        "Selection – IF / ELSE IF / ELSE, CASE / SELECT",
                        "Count-controlled iteration – FOR loops",
                        "Condition-controlled iteration – WHILE and REPEAT…UNTIL",
                        "Subroutines – procedures and functions",
                        "Local vs global variables and scope",
                        "Passing parameters by value and by reference",
                        "Returning values from functions",
                        "String-handling operations (length, substring, concatenation, etc.)",
                        "Random number generation",
                        "File handling – open, read, write, close, append",
                        "Exception handling – try/except/finally",
                    ],
                    "Section 2 – Problem Solving & Theory of Computation (pg. 33–66)": [
                        "Abstraction – removing unnecessary detail",
                        "Decomposition – breaking problems into sub-problems",
                        "Algorithm design – pseudocode and flowcharts",
                        "Trace tables",
                        "Linear search",
                        "Binary search",
                        "Bubble sort",
                        "Insertion sort",
                        "Merge sort",
                        "Big O notation – O(1), O(n), O(n²), O(n log n)",
                        "Time vs space complexity",
                        "Finite state machines (FSMs) – state transition diagrams and tables",
                        "Turing machines – read/write head, tape, transition function",
                        "Halting problem and limits of computation",
                        "Regular expressions – basic syntax and pattern matching",
                    ],
                    "Section 7 – Data Structures": [
                        "Queues – purpose and use cases",
                        "Linear queue – enqueue, dequeue, front, rear pointers",
                        "Circular queue – how it avoids wasted space",
                        "Priority queue – ordering by priority",
                        "Lists – ordered sequence, add, remove, search",
                        "Hash tables – hash function, purpose",
                        "Collision handling in hash tables",
                        "Dictionaries – key-value pairs",
                        "Dictionaries – adding, updating and retrieving values",
                        "Comparing queues, lists, hash tables and dictionaries",
                    ],
                    "Section 12 – Object-Oriented Programming (CH 67–68, pg. 346–359)": [
                        "Objects and classes – definition and relationship",
                        "Attributes (instance variables)",
                        "Methods – defining and calling",
                        "Instantiation – creating objects from a class",
                        "Constructors (__init__) and destructors",
                        "Encapsulation – public vs private attributes/methods",
                        "Inheritance – parent and child classes",
                        "Overriding methods in a subclass",
                        "Polymorphism – same interface, different behaviour",
                        "Class diagrams – notation and reading",
                    ],
                },
            },
            "Paper 2": {
                "desc": "Written theory exam  |  AS Level Computer Science – AQA Paper 2",
                "sections": {
                    "Number Systems": [
                        "Integers, rational, irrational, real and natural numbers",
                        "Fixed-point binary representation",
                        "Two's complement",
                        "Binary to decimal conversion",
                    ],
                    "Floating Point Representation": [
                        "Mantissa and exponent",
                        "Normalised floating point",
                        "Two's complement mantissa/exponent calculations",
                        "Converting floating point binary to decimal",
                    ],
                    "Sound Representation": [
                        "MIDI vs sampled sound",
                        "Storage requirements for sound",
                        "Advantages/disadvantages of MIDI",
                    ],
                    "Hardware and Security Systems": [
                        "Barcode scanners",
                        "Fingerprint scanners",
                        "Digital still cameras",
                        "Digital video cameras",
                        "RFID tag readers",
                        "Programmable door locks/turnstiles",
                        "Physical vs network security",
                    ],
                    "Processor Architecture": [
                        "Control Unit (CU)",
                        "General purpose registers",
                        "Status register",
                        "Roles of processor components",
                    ],
                    "Software Types": [
                        "Application software",
                        "System software",
                        "Utility software",
                        "Operating systems",
                        "Language translators",
                    ],
                    "Boolean Algebra and Logic Gates": [
                        "OR, XOR and other logic gates",
                        "Truth tables",
                        "Boolean expressions",
                        "Logic circuit diagrams",
                        "Simplifying Boolean expressions",
                        "Boolean algebra laws",
                    ],
                    "Logic Systems": [
                        "Designing circuits from truth tables",
                        "Purpose of logic circuits",
                        "Using exactly specified numbers of gates",
                    ],
                    "Databases": [
                        "Relational databases",
                        "Entities and relations",
                        "Primary and foreign keys",
                        "Data redundancy",
                        "Normalisation",
                        "Entity-Relationship (ER) diagrams",
                        "One-to-many relationships",
                    ],
                    "SQL": [
                        "SELECT queries",
                        "ORDER BY",
                        "JOINs",
                        "Querying multiple tables",
                        "Producing sorted outputs",
                    ],
                    "Assembly Language": [
                        "AQA instruction set",
                        "Registers and memory locations",
                        "Addressing modes",
                        "Trace tables",
                        "Branching and loops",
                        "Bitwise operations (AND, ORR, EOR, MVN)",
                        "Shift operations (LSL, LSR)",
                        "Purpose of assembly programs",
                        "Advantages of assembly language",
                        "Machine code vs assembly language",
                    ],
                    "Ethical, Legal and Privacy Issues": [
                        "RFID data collection",
                        "Barcode systems",
                        "Customer data analysis",
                        "Data privacy concerns",
                        "Ethical use of personal data",
                        "Data Protection laws/GDPR",
                        "Surveillance and monitoring",
                        "Consumer profiling",
                    ],
                },
            },
        },
    },

    "business": {
        "name": "Business",
        "board": "Edexcel",
        "color": "#10B981",
        "icon": "📊",
        "papers": {
            "Paper 1": {
                "desc": "Marketing, People & Global Business – Themes 1 & 4 (2h)",
                "sections": {
                    "Theme 1 – Marketing & People": {
                        "1.1 Meeting Customer Needs": [
                            "1.1.1 The market",
                            "1.1.2 Market research",
                            "1.1.3 Market positioning",
                        ],
                        "1.2 The Market": [
                            "1.2.1 Demand",
                            "1.2.2 Supply",
                            "1.2.3 Markets and equilibrium",
                            "1.2.4 Price elasticity of demand (PED)",
                            "1.2.5 Income elasticity of demand (YED)",
                        ],
                        "1.3 Marketing Mix and Strategy": [
                            "1.3.1 Product/service design",
                            "1.3.2 Branding and promotion",
                            "1.3.3 Pricing strategies",
                            "1.3.4 Distribution",
                            "1.3.5 Marketing strategy and the product life cycle",
                        ],
                        "1.4 Managing People": [
                            "1.4.1 Approaches to staffing",
                            "1.4.2 Recruitment, selection and training",
                            "1.4.3 Organisational design",
                            "1.4.4 Motivation in theory and practice",
                            "1.4.5 Leadership",
                        ],
                        "1.5 Entrepreneurs and Leaders": [
                            "1.5.1 Role of an entrepreneur",
                            "1.5.2 Entrepreneurial motives and characteristics",
                            "1.5.3 Business objectives",
                            "1.5.4 Forms of business",
                            "1.5.5 Business choices and opportunity cost",
                        ],
                    },
                    "Theme 4 – Global Business": {
                        "4.1 Globalisation": [
                            "4.1.1 Growing economies (BRIC, MINT)",
                            "4.1.2 International trade and business growth",
                            "4.1.3 Factors contributing to globalisation",
                            "4.1.4 Protectionism",
                        ],
                        "4.2 Global Markets and Business Expansion": [
                            "4.2.1 Conditions for growth internationally",
                            "4.2.2 Reasons for global expansion",
                            "4.2.3 Trading blocs",
                            "4.2.4 Competitive advantage in global markets",
                        ],
                        "4.3 Global Marketing": [
                            "4.3.1 Global vs local marketing",
                            "4.3.2 Cultural/social factors",
                            "4.3.3 Global niche markets",
                            "4.3.4 Digital technology in global marketing",
                        ],
                        "4.4 Global Industries and Businesses (MNCs)": [
                            "4.4.1 Multinational corporations (MNCs)",
                            "4.4.2 Impact of MNCs on home and host countries",
                            "4.4.3 Ethics of MNCs",
                            "4.4.4 Transfer pricing",
                            "4.4.5 Offshoring and reshoring",
                        ],
                    },
                },
            },
            "Paper 2": {
                "desc": "Business Activities, Decisions & Strategy – Themes 2 & 3 (2h)",
                "sections": {
                    "Theme 2 – Managing Business Activities": {
                        "2.1 Raising Finance": [
                            "2.1.1 Internal sources of finance",
                            "2.1.2 External sources of finance",
                            "2.1.3 Appropriateness of finance sources",
                        ],
                        "2.2 Financial Planning": [
                            "2.2.1 Sales forecasting",
                            "2.2.2 Sales, revenue and costs",
                            "2.2.3 Break-even analysis",
                            "2.2.4 Budgets",
                            "2.2.5 Cash flow forecasting",
                        ],
                        "2.3 Managing Finance": [
                            "2.3.1 Profit and loss accounts",
                            "2.3.2 Balance sheet",
                            "2.3.3 Liquidity ratios",
                            "2.3.4 Profitability ratios",
                            "2.3.5 Gearing ratio",
                        ],
                        "2.4 Resource Management": [
                            "2.4.1 Production, productivity and efficiency",
                            "2.4.2 Capacity utilisation",
                            "2.4.3 Stock control",
                            "2.4.4 Quality management",
                            "2.4.5 Lean production (JIT, Kaizen)",
                        ],
                        "2.5 External Influences": [
                            "2.5.1 Economic factors (inflation, interest rates, exchange rates)",
                            "2.5.2 Legislation and regulation",
                            "2.5.3 The competitive environment",
                            "2.5.4 Technological change",
                            "2.5.5 Social and environmental responsibilities",
                        ],
                    },
                    "Theme 3 – Business Decisions & Strategy": {
                        "3.1 Business Objectives and Strategy": [
                            "3.1.1 Understanding mission, vision and objectives",
                            "3.1.2 Ansoff Matrix",
                            "3.1.3 SWOT analysis",
                            "3.1.4 PESTLE analysis",
                            "3.1.5 Porter's Five Forces",
                        ],
                        "3.2 Business Growth": [
                            "3.2.1 Organic growth",
                            "3.2.2 Inorganic growth (mergers, takeovers)",
                            "3.2.3 Economies and diseconomies of scale",
                            "3.2.4 Diversification",
                            "3.2.5 Franchising",
                        ],
                        "3.3 Decision-Making Techniques": [
                            "3.3.1 Quantitative vs qualitative data",
                            "3.3.2 Decision trees",
                            "3.3.3 Critical path analysis",
                            "3.3.4 Investment appraisal (payback, ARR, NPV)",
                        ],
                        "3.4 Influences on Business Decisions": [
                            "3.4.1 Corporate culture",
                            "3.4.2 Stakeholders",
                            "3.4.3 Business ethics",
                            "3.4.4 Corporate social responsibility (CSR)",
                        ],
                        "3.5 Assessing Competitiveness": [
                            "3.5.1 Benchmarking",
                            "3.5.2 Core competencies",
                            "3.5.3 Kaizen and continuous improvement",
                        ],
                        "3.6 Managing Change": [
                            "3.6.1 Causes of change",
                            "3.6.2 Change management strategies",
                            "3.6.3 Flexible organisations",
                            "3.6.4 Managing innovation and knowledge",
                        ],
                    },
                },
            },
        },
    },

    "economics": {
        "name": "Economics",
        "board": "Edexcel",
        "color": "#F59E0B",
        "icon": "📈",
        "papers": {
            "Paper 1": {
                "desc": "Markets & Business Behaviour – Theme 1 (Micro) (2h)",
                "sections": {
                    "Theme 1 – Introduction to Markets and Market Failure": {
                        "1.1 Nature of Economics": [
                            "1.1.1 Economic methodology",
                            "1.1.2 The economic problem and opportunity cost",
                            "1.1.3 Factors of production",
                            "1.1.4 Production possibility frontiers (PPF)",
                            "1.1.5 Specialisation and the division of labour",
                            "1.1.6 Free market and mixed economies",
                        ],
                        "1.2 How Markets Work": [
                            "1.2.1 Rational behaviour and utility",
                            "1.2.2 Demand – individual and market demand",
                            "1.2.3 Price, income and cross elasticity of demand",
                            "1.2.4 Supply – individual and market supply",
                            "1.2.5 Price elasticity of supply (PES)",
                            "1.2.6 Market equilibrium and disequilibrium",
                            "1.2.7 The price mechanism (signalling, incentive, rationing)",
                            "1.2.8 Consumer and producer surplus",
                        ],
                        "1.3 Market Failure": [
                            "1.3.1 Types of market failure",
                            "1.3.2 Externalities (positive and negative)",
                            "1.3.3 Public goods",
                            "1.3.4 Information failures / asymmetric information",
                            "1.3.5 Immobility of factors of production",
                            "1.3.6 Inequality of income and wealth",
                        ],
                        "1.4 Government Intervention": [
                            "1.4.1 Government failure",
                            "1.4.2 Taxes (indirect – specific and ad valorem)",
                            "1.4.3 Subsidies",
                            "1.4.4 Maximum and minimum prices",
                            "1.4.5 State provision and regulation",
                            "1.4.6 Tradeable pollution permits",
                        ],
                    },
                },
            },
            "Paper 2": {
                "desc": "The National & Global Economy – Theme 2 (Macro) (2h)",
                "sections": {
                    "Theme 2 – The UK Economy: Performance and Policies": {
                        "2.1 Measures of Economic Performance": [
                            "2.1.1 Economic growth and GDP",
                            "2.1.2 Inflation (CPI, RPI)",
                            "2.1.3 Employment and unemployment",
                            "2.1.4 Balance of payments",
                            "2.1.5 Macroeconomic objectives and conflicts",
                        ],
                        "2.2 Aggregate Demand (AD)": [
                            "2.2.1 Components of AD (C + I + G + X – M)",
                            "2.2.2 Consumption and savings",
                            "2.2.3 Investment",
                            "2.2.4 Government expenditure",
                            "2.2.5 Net exports",
                            "2.2.6 The multiplier effect",
                        ],
                        "2.3 Aggregate Supply (AS)": [
                            "2.3.1 Short-run aggregate supply (SRAS)",
                            "2.3.2 Long-run aggregate supply (LRAS)",
                            "2.3.3 Keynesian vs Monetarist LRAS",
                            "2.3.4 Factors shifting AS",
                        ],
                        "2.4 National Income": [
                            "2.4.1 Circular flow of income",
                            "2.4.2 Injections and withdrawals",
                            "2.4.3 Measuring national income (output, income, expenditure)",
                            "2.4.4 Limitations of GDP as a measure of welfare",
                        ],
                        "2.5 Economic Growth": [
                            "2.5.1 Actual and potential growth",
                            "2.5.2 Output gaps",
                            "2.5.3 Trade cycle (boom, recession, slump, recovery)",
                            "2.5.4 Costs and benefits of growth",
                            "2.5.5 Sustainable development",
                        ],
                        "2.6 Macroeconomic Policy": [
                            "2.6.1 Fiscal policy – expansionary and contractionary",
                            "2.6.2 Government budget (surplus/deficit)",
                            "2.6.3 National debt",
                            "2.6.4 Monetary policy – interest rates and QE",
                            "2.6.5 Supply-side policies",
                            "2.6.6 Limitations and conflicts between policies",
                        ],
                    },
                },
            },
        },
    },
}

# ── Exam Defaults ──────────────────────────────────────────────────────────────
DEFAULT_EXAMS = [
    {"id": 1, "subject": "Computer Science", "paper": "Paper 1 (PPE)",
     "date": "2026-06-19", "time": "09:00", "room": "J41", "color": "#3B82F6"},
    {"id": 2, "subject": "Computer Science", "paper": "Paper 2",
     "date": "2026-06-25", "time": "09:00", "room": "TBC", "color": "#3B82F6"},
    {"id": 3, "subject": "Business", "paper": "Paper 1",
     "date": "2026-06-10", "time": "09:00", "room": "TBC", "color": "#10B981"},
    {"id": 4, "subject": "Business", "paper": "Paper 2",
     "date": "2026-06-17", "time": "09:00", "room": "TBC", "color": "#10B981"},
    {"id": 5, "subject": "Economics", "paper": "Paper 1",
     "date": "2026-06-11", "time": "09:00", "room": "TBC", "color": "#F59E0B"},
    {"id": 6, "subject": "Economics", "paper": "Paper 2",
     "date": "2026-06-18", "time": "09:00", "room": "TBC", "color": "#F59E0B"},
]

# ── Revision schedule constants ──────────────────────────────────────────────────
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

SCHEDULE_SUBJECTS = ["—", "Computer Science", "Business", "Economics", "Rest"]

SCHEDULE_COLORS = {
    "—":                "#475569",
    "Computer Science": "#3B82F6",
    "Business":         "#10B981",
    "Economics":        "#F59E0B",
    "Rest":             "#8B5CF6",
}

# ══════════════════════════════════════════════════════════════════════════════
# DATA HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def build_flat_topic_keys():
    """Return every topic key (subject/paper/section/subtopic)."""
    keys = []
    for subj_key, subj in CURRICULUM.items():
        for paper_name, paper in subj["papers"].items():
            for sec_name, sec_content in paper["sections"].items():
                if isinstance(sec_content, list):
                    for topic in sec_content:
                        keys.append(f"{subj_key}|{paper_name}|{sec_name}|{topic}")
                elif isinstance(sec_content, dict):
                    for sub_sec, topics in sec_content.items():
                        for topic in topics:
                            keys.append(f"{subj_key}|{paper_name}|{sec_name}|{sub_sec}|{topic}")
    return keys


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            d = json.load(f)
        # Back-fill any new topics added to curriculum
        for k in build_flat_topic_keys():
            if k not in d.get("checked", {}):
                d.setdefault("checked", {})[k] = False
        return d
    return {
        "checked": {k: False for k in build_flat_topic_keys()},
        "exams": DEFAULT_EXAMS,
        "next_exam_id": len(DEFAULT_EXAMS) + 1,
        "notes": {},
        "schedule": {"week": "", "days": {}},
    }


def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


data = load_data()


def get_progress(subj_key=None, paper_name=None):
    """Return (done, total) for a subject/paper/all."""
    total = done = 0
    for k, v in data["checked"].items():
        parts = k.split("|")
        if subj_key and parts[0] != subj_key:
            continue
        if paper_name and parts[1] != paper_name:
            continue
        total += 1
        if v:
            done += 1
    return done, total


def days_until(date_str):
    try:
        d = datetime.date.fromisoformat(date_str)
        delta = (d - datetime.date.today()).days
        return delta
    except Exception:
        return None


# ── Schedule helpers ─────────────────────────────────────────────────────────────

def _current_week_key():
    """ISO-week identifier, e.g. '2026-W25'. Changes every Monday."""
    iso = datetime.date.today().isocalendar()
    return f"{iso[0]}-W{iso[1]:02d}"


def _week_start_end():
    """Return (Monday, Sunday) date objects for the current week."""
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    sunday = monday + datetime.timedelta(days=6)
    return monday, sunday


def _week_range_str():
    monday, sunday = _week_start_end()
    return f"{monday.strftime('%d.%m.%y')} – {sunday.strftime('%d.%m.%y')}"


def ensure_schedule():
    """Return the current week's schedule, resetting it if the week has rolled over."""
    sched = data.setdefault("schedule", {"week": "", "days": {}})
    cur = _current_week_key()
    if sched.get("week") != cur:
        # New week → wipe assignments and notes
        sched["week"] = cur
        sched["days"] = {d: {"subject": "—", "notes": ""} for d in DAYS}
        save_data()
    # Make sure every day exists (e.g. after an app update)
    for d in DAYS:
        sched["days"].setdefault(d, {"subject": "—", "notes": ""})
    return sched


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
    "accent_cs":      "#3B82F6",
    "accent_biz":     "#10B981",
    "accent_econ":    "#F59E0B",
    "accent_home":    "#8B5CF6",
    "hover":          "#1a2236",
    "input_bg":       "#111827",
}

SUBJECT_COLORS = {
    "cs":       "#3B82F6",
    "business": "#10B981",
    "economics": "#F59E0B",
}

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
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c))) for c in rgb)


def lerp_colour(c1, c2, t):
    """Interpolate between two hex colours; t in [0, 1]."""
    a, b = _hex_to_rgb(c1), _hex_to_rgb(c2)
    return _rgb_to_hex(tuple(a[i] + (b[i] - a[i]) * t for i in range(3)))


def ease_out_cubic(t):
    return 1 - (1 - t) ** 3


def animate(widget, start, end, duration_ms, apply_fn,
            easing=ease_out_cubic, on_done=None):
    """Tween a numeric value start->end, calling apply_fn(value) each step."""
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

# ══════════════════════════════════════════════════════════════════════════════
# APP SETUP
# ══════════════════════════════════════════════════════════════════════════════

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("TaiGuide – A-Level Revision")
app.geometry("1200x780")
app.minsize(1100, 700)
app.resizable(True, True)

current_page = "home"

# ── Root layout ────────────────────────────────────────────────────────────────
sidebar = ctk.CTkFrame(app, width=220, corner_radius=0, fg_color=THEME["sidebar"])
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)

main_container = ctk.CTkFrame(app, fg_color=THEME["bg"], corner_radius=0)
main_container.pack(side="right", fill="both", expand=True)

pages = {}
for name in ["home", "cs", "business", "economics", "exams", "quiz", "schedule"]:
    p = ctk.CTkScrollableFrame(
        main_container,
        fg_color=THEME["bg"],
        scrollbar_button_color=THEME["card2"],
        scrollbar_button_hover_color=THEME["border"],
    )
    pages[name] = p


def clear_frame(f):
    for w in f.winfo_children():
        w.destroy()


def show_page(key):
    global current_page
    current_page = key
    for p in pages.values():
        p.pack_forget()
    pages[key].pack(fill="both", expand=True, padx=28, pady=28)
    # Update sidebar button highlight
    for k, btn in nav_buttons.items():
        color = THEME["card2"] if k == key else "transparent"
        btn.configure(fg_color=color)
    REFRESH_MAP[key]()


# ── Sidebar ────────────────────────────────────────────────────────────────────
logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
logo_frame.pack(pady=(28, 8), padx=18, fill="x")

ctk.CTkLabel(
    logo_frame, text="TaiGuide",
    font=("Arial", 22, "bold"), text_color="#8B5CF6"
).pack(anchor="w")
ctk.CTkLabel(
    logo_frame, text="A-Level Revision Tracker",
    font=("Arial", 11), text_color=THEME["text_muted"]
).pack(anchor="w")

ctk.CTkFrame(sidebar, height=1, fg_color=THEME["border"]).pack(fill="x", padx=14, pady=(8, 16))

nav_items = [
    ("🏠  Home",         "home"),
    ("💻  Computer Sci", "cs"),
    ("📊  Business",     "business"),
    ("📈  Economics",    "economics"),
    ("📅  Exams",        "exams"),
    ("🧠  CS Quiz",      "quiz"),
    ("🗓  Schedule",     "schedule"),
]

nav_buttons = {}
for label, key in nav_items:
    btn = ctk.CTkButton(
        sidebar, text=label, anchor="w",
        fg_color="transparent", hover_color=THEME["card2"],
        font=("Arial", 14), height=42, corner_radius=8,
        command=lambda k=key: show_page(k),
    )
    btn.pack(fill="x", padx=10, pady=2)
    nav_buttons[key] = btn

# Version footer
ctk.CTkLabel(
    sidebar, text="v1.0  •  AQA / Edexcel",
    font=("Arial", 10), text_color=THEME["text_muted"]
).pack(side="bottom", pady=16)


# ══════════════════════════════════════════════════════════════════════════════
# SHARED WIDGETS
# ══════════════════════════════════════════════════════════════════════════════

def page_header(parent, title, subtitle=None, color=THEME["text_primary"]):
    ctk.CTkLabel(parent, text=title, font=("Arial", 24, "bold"), text_color=color).pack(anchor="w")
    if subtitle:
        ctk.CTkLabel(parent, text=subtitle, font=("Arial", 13), text_color=THEME["text_muted"]).pack(anchor="w", pady=(2, 20))
    else:
        ctk.CTkFrame(parent, height=16, fg_color="transparent").pack()


def section_label(parent, text, color=THEME["text_secondary"]):
    ctk.CTkLabel(parent, text=text, font=("Arial", 13, "bold"), text_color=color).pack(anchor="w", pady=(14, 6))


def draw_circle_progress(parent, done, total, size=120, color="#8B5CF6"):
    """Draw a progress ring using a Canvas widget, sweeping in from 0."""
    canvas = ctk.CTkCanvas(parent, width=size, height=size, bg=THEME["bg"],
                            highlightthickness=0, bd=0)
    canvas.pack()
    pct = done / total if total > 0 else 0
    cx = cy = size / 2
    r = size / 2 - 10
    stroke = 10
    # Background ring
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                       outline=THEME["card2"], width=stroke)
    # Progress arc + centre text, both updated by the tween
    arc = canvas.create_arc(cx - r, cy - r, cx + r, cy + r,
                            start=90, extent=0,
                            outline=color, width=stroke, style="arc")
    text = canvas.create_text(cx, cy, text="0%",
                              fill=THEME["text_primary"],
                              font=("Arial", int(size / 8), "bold"))

    def _apply(v):
        # v is the animated fraction 0..pct
        canvas.itemconfigure(arc, extent=-360 * v if v > 0 else 0)
        canvas.itemconfigure(text, text=f"{int(round(v * 100))}%")

    animate(canvas, 0, pct, 650, _apply)
    return canvas


# ══════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════════════════════════

def refresh_home():
    p = pages["home"]
    clear_frame(p)

    hour = datetime.datetime.now().hour
    greeting = "Good morning" if hour < 12 else "Good afternoon" if hour < 18 else "Good evening"
    page_header(p, f"{greeting}, Tai 👋",
                datetime.datetime.now().strftime("%A, %d %B %Y"), color=THEME["text_primary"])

    # ── Exam countdown cards ───────────────────────────────────────────────────
    upcoming = sorted(
        [e for e in data["exams"] if days_until(e["date"]) is not None and days_until(e["date"]) >= 0],
        key=lambda e: e["date"]
    )[:4]

    if upcoming:
        section_label(p, "⏳  Upcoming Exams")
        row = ctk.CTkFrame(p, fg_color="transparent")
        row.pack(fill="x", pady=(0, 8))
        for exam in upcoming:
            days = days_until(exam["date"])
            card = ctk.CTkFrame(row, fg_color=THEME["card"], corner_radius=14)
            card.pack(side="left", expand=True, fill="x", padx=(0, 12))
            add_hover(card, THEME["card"], THEME["card2"])
            ctk.CTkFrame(card, height=4, fg_color=exam.get("color", "#8B5CF6"),
                         corner_radius=2).pack(fill="x")
            ctk.CTkLabel(card, text=exam["subject"], font=("Arial", 11),
                         text_color=THEME["text_muted"]).pack(anchor="w", padx=14, pady=(10, 0))
            ctk.CTkLabel(card, text=exam["paper"], font=("Arial", 13, "bold"),
                         text_color=THEME["text_primary"]).pack(anchor="w", padx=14)
            label = "Today!" if days == 0 else f"{days} day{'s' if days != 1 else ''}"
            ctk.CTkLabel(card, text=label, font=("Arial", 20, "bold"),
                         text_color=exam.get("color", "#8B5CF6")).pack(anchor="w", padx=14, pady=(4, 14))

    # ── Progress circles ───────────────────────────────────────────────────────
    section_label(p, "📚  Revision Progress")
    circles_row = ctk.CTkFrame(p, fg_color="transparent")
    circles_row.pack(fill="x", pady=(0, 8))

    subjects = [("cs", "Computer Science"), ("business", "Business"), ("economics", "Economics")]
    all_done = all_total = 0
    for subj_key, subj_label in subjects:
        done, total = get_progress(subj_key)
        all_done += done
        all_total += total
        color = SUBJECT_COLORS[subj_key]
        card = ctk.CTkFrame(circles_row, fg_color=THEME["card"], corner_radius=14)
        card.pack(side="left", expand=True, fill="x", padx=(0, 12))
        add_hover(card, THEME["card"], THEME["card2"])
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(pady=16, padx=16)
        draw_circle_progress(inner, done, total, size=110, color=color)
        ctk.CTkLabel(inner, text=subj_label, font=("Arial", 13, "bold"),
                     text_color=THEME["text_primary"]).pack(pady=(8, 0))
        ctk.CTkLabel(inner, text=f"{done}/{total} topics", font=("Arial", 11),
                     text_color=THEME["text_muted"]).pack()

    # Overall
    ov_card = ctk.CTkFrame(p, fg_color=THEME["card"], corner_radius=14)
    ov_card.pack(fill="x", pady=(0, 8))
    ov_inner = ctk.CTkFrame(ov_card, fg_color="transparent")
    ov_inner.pack(pady=18, padx=20, fill="x")
    left = ctk.CTkFrame(ov_inner, fg_color="transparent")
    left.pack(side="left")
    draw_circle_progress(left, all_done, all_total, size=90, color="#8B5CF6")
    right = ctk.CTkFrame(ov_inner, fg_color="transparent")
    right.pack(side="left", padx=20)
    ctk.CTkLabel(right, text="Overall Progress", font=("Arial", 16, "bold"),
                 text_color=THEME["text_primary"]).pack(anchor="w")
    ctk.CTkLabel(right, text=f"{all_done} of {all_total} topics completed",
                 font=("Arial", 13), text_color=THEME["text_muted"]).pack(anchor="w")
    pct = int(all_done / all_total * 100) if all_total else 0
    ctk.CTkLabel(right, text=f"{100 - pct}% remaining – keep going!",
                 font=("Arial", 12), text_color="#8B5CF6").pack(anchor="w", pady=(4, 0))

    # ── Quick links ────────────────────────────────────────────────────────────
    section_label(p, "🚀  Quick Access")
    ql_row = ctk.CTkFrame(p, fg_color="transparent")
    ql_row.pack(fill="x")
    for label, key, color in [
        ("💻 Computer Science", "cs", "#3B82F6"),
        ("📊 Business", "business", "#10B981"),
        ("📈 Economics", "economics", "#F59E0B"),
        ("🗓 Schedule", "schedule", "#8B5CF6"),
    ]:
        ctk.CTkButton(
            ql_row, text=label, fg_color=THEME["card"], hover_color=THEME["card2"],
            text_color=color, font=("Arial", 13), corner_radius=10, height=44,
            command=lambda k=key: show_page(k)
        ).pack(side="left", expand=True, fill="x", padx=(0, 10))


# ══════════════════════════════════════════════════════════════════════════════
# SUBJECT PAGE BUILDER
# ══════════════════════════════════════════════════════════════════════════════

def build_subject_page(subj_key):
    p = pages[subj_key]
    clear_frame(p)
    subj = CURRICULUM[subj_key]
    color = subj["color"]

    page_header(p,
                f"{subj['icon']}  {subj['name']}",
                f"{subj['board']}  •  Track your revision topic by topic",
                color=color)

    # Progress bar — kept as mutable references so on_toggle can update without a rebuild
    done, total = get_progress(subj_key)
    pct = done / total if total > 0 else 0
    pct_lbl = ctk.CTkLabel(p, text=f"{done}/{total} topics — {int(pct*100)}% complete",
                            font=("Arial", 12), text_color=THEME["text_muted"])
    pct_lbl.pack(anchor="w")
    bar_bg = ctk.CTkFrame(p, height=6, fg_color=THEME["card2"], corner_radius=3)
    bar_bg.pack(fill="x", pady=(4, 20))
    bar_fill = ctk.CTkFrame(bar_bg, height=6, fg_color=color, corner_radius=3)
    bar_fill.place(relwidth=0, relheight=1)
    cur_pct = [0.0]   # mutable holder for the animated bar fraction

    # Animate the initial fill + percentage count-up on load
    animate(bar_fill, 0, pct, 600,
            lambda v: bar_fill.place(relwidth=v, relheight=1))
    animate(pct_lbl, 0, pct * 100, 600,
            lambda v: pct_lbl.configure(text=f"{done}/{total} topics — {int(round(v))}% complete"))
    cur_pct[0] = pct

    # Lightweight updater — animates the label + bar, never destroys widgets
    def _update_progress():
        new_done, new_total = get_progress(subj_key)
        new_pct = new_done / new_total if new_total > 0 else 0
        animate(bar_fill, cur_pct[0], new_pct, 350,
                lambda v: bar_fill.place(relwidth=v, relheight=1))
        animate(pct_lbl, cur_pct[0] * 100, new_pct * 100, 350,
                lambda v: pct_lbl.configure(
                    text=f"{new_done}/{new_total} topics — {int(round(v))}% complete"))
        cur_pct[0] = new_pct
        if paper_progress_lbl[0] is not None:
            cur_paper = tab_var.get()
            pd, pt = get_progress(subj_key, cur_paper)
            paper_progress_lbl[0].configure(
                text=f"  {pd}/{pt} topics ticked  ({int(pd/pt*100) if pt else 0}%)"
            )

    # Tab selector (Paper 1 / Paper 2)
    paper_names = list(subj["papers"].keys())
    tab_var = ctk.StringVar(value=paper_names[0])
    # Mutable slot so render_paper can update it
    paper_progress_lbl = [None]

    content_frame = ctk.CTkFrame(p, fg_color="transparent")
    content_frame.pack(fill="both", expand=True)

    tab_row = ctk.CTkFrame(p, fg_color="transparent")
    tab_row.pack(fill="x", pady=(0, 12))

    def render_paper(paper_name):
        clear_frame(content_frame)
        tab_var.set(paper_name)
        for btn_name, btn_widget in tab_btns.items():
            if btn_name == paper_name:
                btn_widget.configure(fg_color=color, text_color="#fff")
            else:
                btn_widget.configure(fg_color=THEME["card"], text_color=THEME["text_secondary"])

        paper = subj["papers"][paper_name]
        ctk.CTkLabel(content_frame, text=paper["desc"],
                     font=("Arial", 12), text_color=THEME["text_muted"]).pack(anchor="w", pady=(0, 10))

        p_done, p_total = get_progress(subj_key, paper_name)
        lbl = ctk.CTkLabel(content_frame,
                           text=f"  {p_done}/{p_total} topics ticked  ({int(p_done/p_total*100) if p_total else 0}%)",
                           font=("Arial", 12, "bold"), text_color=color)
        lbl.pack(anchor="w", pady=(0, 12))
        paper_progress_lbl[0] = lbl

        for sec_name, sec_content in paper["sections"].items():
            render_section(content_frame, subj_key, paper_name, sec_name, sec_content, color, _update_progress)

    tab_btns = {}
    for pname in paper_names:
        btn = ctk.CTkButton(
            tab_row, text=pname,
            font=("Arial", 13), height=36, corner_radius=8,
            fg_color=THEME["card"], text_color=THEME["text_secondary"],
            hover_color=THEME["card2"],
            command=lambda n=pname: render_paper(n)
        )
        btn.pack(side="left", padx=(0, 8))
        tab_btns[pname] = btn

    render_paper(paper_names[0])


def render_section(parent, subj_key, paper_name, sec_name, sec_content, color, update_progress):
    """Render a section – handles both flat list and nested dict."""

    # Section header card
    sec_card = ctk.CTkFrame(parent, fg_color=THEME["card"], corner_radius=12)
    sec_card.pack(fill="x", pady=(0, 10))

    # Header row (collapsible)
    hdr = ctk.CTkFrame(sec_card, fg_color="transparent")
    hdr.pack(fill="x", padx=14, pady=10)

    body_frame = ctk.CTkFrame(sec_card, fg_color="transparent")

    expanded_var = ctk.BooleanVar(value=True)
    arrow_lbl = ctk.CTkLabel(hdr, text="▼", font=("Arial", 12), text_color=THEME["text_muted"])
    arrow_lbl.pack(side="right")

    ctk.CTkFrame(hdr, width=4, fg_color=color, corner_radius=2).pack(side="left", fill="y", padx=(0, 10))
    ctk.CTkLabel(hdr, text=sec_name, font=("Arial", 14, "bold"),
                 text_color=THEME["text_primary"]).pack(side="left")

    def toggle_expand():
        if expanded_var.get():
            body_frame.pack_forget()
            expanded_var.set(False)
            arrow_lbl.configure(text="▶")
        else:
            body_frame.pack(fill="x", padx=14, pady=(0, 10))
            expanded_var.set(True)
            arrow_lbl.configure(text="▼")

    hdr.bind("<Button-1>", lambda e: toggle_expand())
    arrow_lbl.bind("<Button-1>", lambda e: toggle_expand())

    body_frame.pack(fill="x", padx=14, pady=(0, 10))

    all_topic_vars = []
    if isinstance(sec_content, list):
        all_topic_vars = _render_topic_list(body_frame, subj_key, paper_name, sec_name, sec_content, color, update_progress)
    elif isinstance(sec_content, dict):
        for sub_sec_name, topics in sec_content.items():
            sub_vars = render_subsection(body_frame, subj_key, paper_name, sec_name, sub_sec_name, topics, color, update_progress)
            all_topic_vars.extend(sub_vars)

    # Section tick-all — does a bulk update then calls the lightweight updater
    all_keys = _get_all_keys_for_section(subj_key, paper_name, sec_name, sec_content)
    all_done_now = all(data["checked"].get(k, False) for k in all_keys)
    tick_all_var = ctk.BooleanVar(value=all_done_now)

    def tick_all(var=tick_all_var, keys=all_keys, tvars=all_topic_vars):
        val = var.get()
        for k in keys:
            data["checked"][k] = val
        for tv in tvars:
            tv.set(val)
        save_data()
        update_progress()

    ctk.CTkCheckBox(
        hdr, text=" Tick all", variable=tick_all_var,
        font=("Arial", 11), text_color=THEME["text_muted"],
        checkbox_width=16, checkbox_height=16, corner_radius=4,
        fg_color=color, hover_color=color,
        command=tick_all
    ).pack(side="right", padx=(0, 10))


def _get_all_keys_for_section(subj_key, paper_name, sec_name, sec_content):
    keys = []
    if isinstance(sec_content, list):
        for topic in sec_content:
            keys.append(f"{subj_key}|{paper_name}|{sec_name}|{topic}")
    elif isinstance(sec_content, dict):
        for sub_sec, topics in sec_content.items():
            for topic in topics:
                keys.append(f"{subj_key}|{paper_name}|{sec_name}|{sub_sec}|{topic}")
    return keys


def render_subsection(parent, subj_key, paper_name, sec_name, sub_sec_name, topics, color, update_progress):
    sub_card = ctk.CTkFrame(parent, fg_color=THEME["card2"], corner_radius=10)
    sub_card.pack(fill="x", pady=(0, 8))

    sub_hdr = ctk.CTkFrame(sub_card, fg_color="transparent")
    sub_hdr.pack(fill="x", padx=12, pady=8)

    sub_body = ctk.CTkFrame(sub_card, fg_color="transparent")
    sub_expanded = ctk.BooleanVar(value=True)
    sub_arrow = ctk.CTkLabel(sub_hdr, text="▼", font=("Arial", 11), text_color=THEME["text_muted"])
    sub_arrow.pack(side="right")

    ctk.CTkLabel(sub_hdr, text=sub_sec_name, font=("Arial", 13, "bold"),
                 text_color=THEME["text_secondary"]).pack(side="left")

    def toggle_sub():
        if sub_expanded.get():
            sub_body.pack_forget()
            sub_expanded.set(False)
            sub_arrow.configure(text="▶")
        else:
            sub_body.pack(fill="x", padx=12, pady=(0, 8))
            sub_expanded.set(True)
            sub_arrow.configure(text="▼")

    sub_hdr.bind("<Button-1>", lambda e: toggle_sub())
    sub_arrow.bind("<Button-1>", lambda e: toggle_sub())

    sub_body.pack(fill="x", padx=12, pady=(0, 8))
    topic_vars = _render_topic_list(sub_body, subj_key, paper_name, sec_name, topics, color, update_progress, sub_sec_name)

    sub_keys = [f"{subj_key}|{paper_name}|{sec_name}|{sub_sec_name}|{t}" for t in topics]
    all_sub_done = all(data["checked"].get(k, False) for k in sub_keys)
    sub_tick_var = ctk.BooleanVar(value=all_sub_done)

    def tick_all_sub(var=sub_tick_var, keys=sub_keys, tvars=topic_vars):
        val = var.get()
        for k in keys:
            data["checked"][k] = val
        for tv in tvars:
            tv.set(val)
        save_data()
        update_progress()

    ctk.CTkCheckBox(
        sub_hdr, text=" All", variable=sub_tick_var,
        font=("Arial", 10), text_color=THEME["text_muted"],
        checkbox_width=14, checkbox_height=14, corner_radius=3,
        fg_color=color, hover_color=color,
        command=tick_all_sub
    ).pack(side="right", padx=(0, 8))

    return topic_vars


def _render_topic_list(parent, subj_key, paper_name, sec_name, topics, color, update_progress, sub_sec_name=None):
    all_vars = []
    for topic in topics:
        if sub_sec_name:
            k = f"{subj_key}|{paper_name}|{sec_name}|{sub_sec_name}|{topic}"
        else:
            k = f"{subj_key}|{paper_name}|{sec_name}|{topic}"

        row = ctk.CTkFrame(parent, fg_color="transparent", height=32)
        row.pack(fill="x", pady=1)
        row.pack_propagate(False)

        var = ctk.BooleanVar(value=data["checked"].get(k, False))
        all_vars.append(var)

        def on_toggle(key=k, v=var):
            data["checked"][key] = v.get()
            save_data()
            update_progress()   # only updates the label + bar — no widget rebuild

        cb = ctk.CTkCheckBox(
            row,
            text=topic,
            variable=var,
            font=("Arial", 12),
            text_color=THEME["text_secondary"] if not var.get() else THEME["text_muted"],
            checkbox_width=16, checkbox_height=16, corner_radius=4,
            fg_color=color, hover_color=color,
            command=on_toggle,
        )
        cb.pack(anchor="w", padx=(4, 0))

    return all_vars


# ══════════════════════════════════════════════════════════════════════════════
# REVISION SCHEDULE PAGE
# ══════════════════════════════════════════════════════════════════════════════
# A weekly planner. Each day of the week can be assigned a subject and given
# free-text notes for your own methods. The whole week resets automatically
# every Monday (a new ISO week wipes the assignments and notes). The current
# date range is shown at the top, e.g. "16.06.26 – 22.06.26".

def refresh_schedule():
    p = pages["schedule"]
    clear_frame(p)
    sched = ensure_schedule()

    page_header(p, "🗓  Revision Schedule",
                f"Week of {_week_range_str()}  •  resets automatically every Monday",
                color="#8B5CF6")

    today_name = DAYS[datetime.date.today().weekday()]

    # Holds the day → notes textbox so we can save them all before any rebuild
    note_boxes = {}

    def _save_all_notes():
        for d, box in note_boxes.items():
            data["schedule"]["days"][d]["notes"] = box.get("1.0", "end").strip()
        save_data()

    # ── Top action row ──────────────────────────────────────────────────────────
    top = ctk.CTkFrame(p, fg_color="transparent")
    top.pack(fill="x", pady=(0, 14))

    def do_save():
        _save_all_notes()
        save_btn.configure(text="✓ Saved")
        p.after(1200, lambda: save_btn.configure(text="💾 Save notes"))

    save_btn = ctk.CTkButton(top, text="💾 Save notes", width=130, height=34,
                             corner_radius=8, fg_color="#8B5CF6", hover_color="#7C3AED",
                             font=("Arial", 12), command=do_save)
    save_btn.pack(side="left")

    def do_reset():
        _save_all_notes()  # not strictly needed, but keeps state consistent
        data["schedule"]["days"] = {d: {"subject": "—", "notes": ""} for d in DAYS}
        save_data()
        refresh_schedule()

    ctk.CTkButton(top, text="↻ Reset this week", width=150, height=34,
                  corner_radius=8, fg_color=THEME["card"], hover_color=THEME["card2"],
                  text_color=THEME["text_secondary"], font=("Arial", 12),
                  command=do_reset).pack(side="left", padx=(10, 0))

    # ── One card per day ────────────────────────────────────────────────────────
    monday, _ = _week_start_end()

    for offset, day in enumerate(DAYS):
        entry = sched["days"][day]
        subj = entry.get("subject", "—")
        accent = SCHEDULE_COLORS.get(subj, THEME["text_muted"])
        day_date = (monday + datetime.timedelta(days=offset)).strftime("%d.%m")
        is_today = (day == today_name)

        card = ctk.CTkFrame(p, fg_color=THEME["card"], corner_radius=12)
        card.pack(fill="x", pady=6)

        # Accent stripe (colour reflects the assigned subject)
        ctk.CTkFrame(card, height=4, fg_color=accent, corner_radius=2).pack(fill="x")

        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.pack(fill="x", padx=16, pady=(10, 6))

        title = f"{day}  •  {day_date}" + ("   (today)" if is_today else "")
        ctk.CTkLabel(hdr, text=title, font=("Arial", 15, "bold"),
                     text_color="#8B5CF6" if is_today else THEME["text_primary"]).pack(side="left")

        # Subject assignment
        subj_var = ctk.StringVar(value=subj)

        def on_subj(choice, d=day):
            _save_all_notes()  # preserve any typing before the rebuild
            data["schedule"]["days"][d]["subject"] = choice
            save_data()
            refresh_schedule()

        ctk.CTkOptionMenu(hdr, values=SCHEDULE_SUBJECTS, variable=subj_var,
                          command=on_subj, width=190,
                          fg_color=THEME["card2"], button_color=accent,
                          button_hover_color=accent, font=("Arial", 12)).pack(side="right")

        ctk.CTkLabel(card, text="Notes / method:", font=("Arial", 11),
                     text_color=THEME["text_muted"]).pack(anchor="w", padx=16)

        notes_box = ctk.CTkTextbox(card, height=70, fg_color=THEME["input_bg"],
                                   border_color=THEME["border"], border_width=1,
                                   font=("Arial", 12), corner_radius=8)
        notes_box.pack(fill="x", padx=16, pady=(2, 14))
        notes_box.insert("1.0", entry.get("notes", ""))
        note_boxes[day] = notes_box

        # Save this day's notes whenever the box loses focus
        def _save_one(_evt=None, d=day, box=notes_box):
            data["schedule"]["days"][d]["notes"] = box.get("1.0", "end").strip()
            save_data()

        notes_box.bind("<FocusOut>", _save_one)


# ══════════════════════════════════════════════════════════════════════════════
# EXAMS PAGE
# ══════════════════════════════════════════════════════════════════════════════

COLOR_OPTIONS = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6", "#EC4899"]


def _color_picker_row(parent, color_var):
    """Render a row of colour dot buttons, highlighting the selected one."""
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    btns = []

    def _select(cv):
        color_var.set(cv)
        for b, bc in zip(btns, COLOR_OPTIONS):
            b.configure(border_width=3 if bc == cv else 0,
                        border_color="#ffffff")

    for c in COLOR_OPTIONS:
        b = ctk.CTkButton(frame, text="", width=24, height=24, corner_radius=12,
                          fg_color=c, hover_color=c,
                          border_width=3 if c == color_var.get() else 0,
                          border_color="#ffffff",
                          command=lambda cv=c: _select(cv))
        b.pack(side="left", padx=3)
        btns.append(b)

    return frame


def _exam_entry(parent, placeholder, value, width):
    e = ctk.CTkEntry(parent, placeholder_text=placeholder,
                     fg_color=THEME["input_bg"], font=("Arial", 12),
                     height=32, width=width, border_color=THEME["border"])
    if value:
        e.insert(0, value)
    return e


def refresh_exams():
    p = pages["exams"]
    clear_frame(p)
    page_header(p, "📅  Exam Dates",
                "Click ✏️ to edit any exam inline  •  Countdowns auto-update on the Home screen")

    # ── Add new exam card ──────────────────────────────────────────────────────
    add_card = ctk.CTkFrame(p, fg_color=THEME["card"], corner_radius=14)
    add_card.pack(fill="x", pady=(0, 18))

    add_hdr = ctk.CTkFrame(add_card, fg_color="transparent")
    add_hdr.pack(fill="x", padx=16, pady=(12, 6))
    ctk.CTkLabel(add_hdr, text="＋  New Exam", font=("Arial", 13, "bold"),
                 text_color=THEME["text_secondary"]).pack(side="left")

    add_body = ctk.CTkFrame(add_card, fg_color="transparent")
    add_collapsed = ctk.BooleanVar(value=True)

    def toggle_add():
        if add_collapsed.get():
            add_body.pack(fill="x", padx=16, pady=(0, 12))
            add_collapsed.set(False)
            add_toggle_btn.configure(text="▲")
        else:
            add_body.pack_forget()
            add_collapsed.set(True)
            add_toggle_btn.configure(text="▼")

    add_toggle_btn = ctk.CTkButton(add_hdr, text="▼", width=32, height=28,
                                   fg_color="transparent", hover_color=THEME["card2"],
                                   text_color=THEME["text_muted"], font=("Arial", 13),
                                   command=toggle_add)
    add_toggle_btn.pack(side="right")

    # Fields inside add form
    new_color_var = ctk.StringVar(value=COLOR_OPTIONS[0])

    r1 = ctk.CTkFrame(add_body, fg_color="transparent")
    r1.pack(fill="x", pady=(0, 6))
    n_subj  = _exam_entry(r1, "Subject (e.g. Computer Science)", "", 200)
    n_paper = _exam_entry(r1, "Paper (e.g. Paper 1)", "", 180)
    n_date  = _exam_entry(r1, "Date  YYYY-MM-DD", "", 150)
    n_time  = _exam_entry(r1, "Time  HH:MM", "", 100)
    n_room  = _exam_entry(r1, "Room", "", 80)
    for w in (n_subj, n_paper, n_date, n_time, n_room):
        w.pack(side="left", padx=(0, 8))

    r2 = ctk.CTkFrame(add_body, fg_color="transparent")
    r2.pack(fill="x", pady=(0, 8))
    ctk.CTkLabel(r2, text="Colour:", font=("Arial", 12),
                 text_color=THEME["text_muted"]).pack(side="left", padx=(0, 8))
    _color_picker_row(r2, new_color_var).pack(side="left")

    def do_add():
        subj  = n_subj.get().strip()
        paper = n_paper.get().strip()
        date  = n_date.get().strip()
        if not subj or not paper or not date:
            return
        data["exams"].append({
            "id":      data["next_exam_id"],
            "subject": subj,
            "paper":   paper,
            "date":    date,
            "time":    n_time.get().strip() or "09:00",
            "room":    n_room.get().strip() or "TBC",
            "color":   new_color_var.get(),
        })
        data["next_exam_id"] += 1
        save_data()
        refresh_exams()

    ctk.CTkButton(r2, text="＋ Add Exam", width=110, height=32, corner_radius=8,
                  fg_color="#8B5CF6", hover_color="#7C3AED", font=("Arial", 12),
                  command=do_add).pack(side="left", padx=(16, 0))

    # ── Exam list ──────────────────────────────────────────────────────────────
    sorted_exams = sorted(data["exams"], key=lambda e: e.get("date", "9999"))

    for exam in sorted_exams:
        days = days_until(exam.get("date", ""))
        color = exam.get("color", "#8B5CF6")

        card = ctk.CTkFrame(p, fg_color=THEME["card"], corner_radius=12)
        card.pack(fill="x", pady=4)

        # ── View row ──────────────────────────────────────────────────────────
        view_row = ctk.CTkFrame(card, fg_color="transparent", height=62)
        view_row.pack(fill="x")
        view_row.pack_propagate(False)

        ctk.CTkFrame(view_row, width=5, fg_color=color,
                     corner_radius=3).place(x=0, y=0, relheight=1)

        ctk.CTkLabel(view_row,
                     text=f"{exam['subject']}  —  {exam['paper']}",
                     font=("Arial", 13, "bold"),
                     text_color=THEME["text_primary"]).place(x=22, y=10)
        ctk.CTkLabel(view_row,
                     text=f"📅 {exam.get('date','')}   🕐 {exam.get('time','')}   🏫 {exam.get('room','')}",
                     font=("Arial", 11),
                     text_color=THEME["text_muted"]).place(x=22, y=34)

        if days is not None:
            cd_text  = "Passed" if days < 0 else "TODAY!" if days == 0 else "Tomorrow" if days == 1 else f"{days} days"
            cd_color = THEME["text_muted"] if days < 0 else "#EF4444" if days == 0 else "#F59E0B" if days == 1 else color
            ctk.CTkLabel(view_row, text=cd_text, font=("Arial", 14, "bold"),
                         text_color=cd_color).place(relx=0.60, rely=0.5, anchor="w")

        # ── Edit / Delete buttons ──────────────────────────────────────────────
        btn_frame = ctk.CTkFrame(view_row, fg_color="transparent")
        btn_frame.place(relx=0.99, rely=0.5, anchor="e")

        edit_body  = ctk.CTkFrame(card, fg_color=THEME["card2"], corner_radius=0)
        edit_open  = ctk.BooleanVar(value=False)

        def make_toggle_edit(eb=edit_body, ev=edit_open, ex=exam, card_ref=card):
            def _toggle():
                if ev.get():
                    eb.pack_forget()
                    ev.set(False)
                else:
                    eb.pack(fill="x", padx=12, pady=(0, 12))
                    ev.set(True)
            return _toggle

        edit_btn = ctk.CTkButton(btn_frame, text="✏️", width=32, height=28,
                                 corner_radius=6, fg_color=THEME["card2"],
                                 hover_color=THEME["border"],
                                 text_color=THEME["text_secondary"], font=("Arial", 13),
                                 command=make_toggle_edit())
        edit_btn.pack(side="left", padx=(0, 6))

        def make_delete(eid=exam["id"]):
            def _del():
                data["exams"] = [e for e in data["exams"] if e["id"] != eid]
                save_data()
                refresh_exams()
            return _del

        ctk.CTkButton(btn_frame, text="✕", width=28, height=28, corner_radius=6,
                      fg_color="#3B1A1A", hover_color="#EF4444",
                      text_color="#EF4444", font=("Arial", 13),
                      command=make_delete()).pack(side="left")

        # ── Inline edit form (hidden by default) ──────────────────────────────
        ef = edit_body   # shorthand

        er1 = ctk.CTkFrame(ef, fg_color="transparent")
        er1.pack(fill="x", padx=8, pady=(10, 4))

        e_subj  = _exam_entry(er1, "Subject",      exam.get("subject", ""), 190)
        e_paper = _exam_entry(er1, "Paper",         exam.get("paper", ""),   160)
        e_date  = _exam_entry(er1, "YYYY-MM-DD",   exam.get("date", ""),    140)
        e_time  = _exam_entry(er1, "HH:MM",         exam.get("time", ""),     90)
        e_room  = _exam_entry(er1, "Room",           exam.get("room", ""),     70)
        for w in (e_subj, e_paper, e_date, e_time, e_room):
            w.pack(side="left", padx=(0, 6))

        er2 = ctk.CTkFrame(ef, fg_color="transparent")
        er2.pack(fill="x", padx=8, pady=(0, 8))

        ctk.CTkLabel(er2, text="Colour:", font=("Arial", 11),
                     text_color=THEME["text_muted"]).pack(side="left", padx=(0, 6))
        edit_color_var = ctk.StringVar(value=exam.get("color", COLOR_OPTIONS[0]))
        _color_picker_row(er2, edit_color_var).pack(side="left")

        def make_save(eid=exam["id"], es=e_subj, ep=e_paper, ed=e_date,
                      et=e_time, er=e_room, ecv=edit_color_var,
                      eb=edit_body, ev=edit_open):
            def _save():
                for ex in data["exams"]:
                    if ex["id"] == eid:
                        ex["subject"] = es.get().strip() or ex["subject"]
                        ex["paper"]   = ep.get().strip() or ex["paper"]
                        ex["date"]    = ed.get().strip() or ex["date"]
                        ex["time"]    = et.get().strip() or ex["time"]
                        ex["room"]    = er.get().strip() or ex["room"]
                        ex["color"]   = ecv.get()
                        break
                save_data()
                refresh_exams()
            return _save

        def make_cancel(eb=edit_body, ev=edit_open):
            def _cancel():
                eb.pack_forget()
                ev.set(False)
            return _cancel

        ctk.CTkButton(er2, text="💾 Save", width=90, height=30, corner_radius=7,
                      fg_color="#10B981", hover_color="#059669",
                      font=("Arial", 12), text_color="#fff",
                      command=make_save()).pack(side="left", padx=(16, 6))

        ctk.CTkButton(er2, text="Cancel", width=70, height=30, corner_radius=7,
                      fg_color=THEME["card"], hover_color=THEME["border"],
                      font=("Arial", 12), text_color=THEME["text_muted"],
                      command=make_cancel()).pack(side="left")


# ══════════════════════════════════════════════════════════════════════════════
# COMPUTER SCIENCE QUIZ
# ══════════════════════════════════════════════════════════════════════════════
# AQA AS-Level Computer Science — Paper 1 & Paper 2.
# Two question types:
#   "mcq"     → multiple choice. The app marks it right/wrong automatically and
#               shows one model answer/explanation.
#   "written" → free response. The app shows acceptable answer points + a model
#               answer, then trusts you to self-mark honestly.
#
# Each question dict:
#   type:        "mcq" | "written"
#   q:           the question text
#   options:     (mcq only) list of answer strings
#   answer:      (mcq only) index of the correct option
#   model:       model answer / explanation
#   acceptable:  (written only) list of credit-worthy points

CS_QUIZ = {
    "Paper 1": {
        "Section 1 – Fundamentals of Programming": [
            {
                "type": "mcq",
                "q": "Which data type is most appropriate for storing a person's age in whole years?",
                "options": ["Real", "Integer", "Boolean", "String"],
                "answer": 1,
                "model": "Integer. An age in whole years has no fractional part, so an integer is the most memory-efficient and appropriate choice. A real would waste space, and a Boolean only stores true/false.",
            },
            {
                "type": "mcq",
                "q": "Which arithmetic operator returns the remainder after integer division?",
                "options": ["DIV", "MOD", "^", "/"],
                "answer": 1,
                "model": "MOD returns the remainder (e.g. 17 MOD 5 = 2). DIV gives the integer quotient (17 DIV 5 = 3), / gives a real result, and ^ is exponentiation.",
            },
            {
                "type": "written",
                "q": "Explain the difference between a variable and a constant. [2 marks]",
                "acceptable": [
                    "A variable's value can change during program execution",
                    "A constant's value is fixed/cannot be changed after it is set",
                    "Constants are used for fixed values (e.g. Pi) to prevent accidental change",
                ],
                "model": "A variable is a named store whose value can change while the program runs. A constant is a named store whose value is set once and cannot be altered during execution, used for fixed values such as Pi to make code clearer and prevent accidental modification.",
            },
            {
                "type": "written",
                "q": "Describe the difference between passing a parameter by value and by reference. [2 marks]",
                "acceptable": [
                    "By value: a copy of the data is passed",
                    "By value: changes inside the subroutine do not affect the original",
                    "By reference: a pointer/address to the original is passed",
                    "By reference: changes inside the subroutine do affect the original",
                ],
                "model": "Passing by value sends a copy of the data, so any changes made inside the subroutine do not affect the original variable. Passing by reference sends the memory address of the original, so changes made inside the subroutine do alter the original variable.",
            },
            {
                "type": "written",
                "q": "State the purpose of exception handling (try/except) and give one example of when it is useful. [2 marks]",
                "acceptable": [
                    "Allows a program to deal with/catch runtime errors gracefully",
                    "Prevents the program from crashing",
                    "Example: dividing by zero / opening a file that doesn't exist / invalid user input",
                ],
                "model": "Exception handling lets a program detect and respond to runtime errors instead of crashing. The risky code goes in the try block and the recovery code in the except block. For example, it can catch a division-by-zero error or a missing file and display a helpful message instead of stopping abruptly.",
            },
        ],
        "Section 2 – Problem Solving & Theory of Computation": [
            {
                "type": "mcq",
                "q": "What is the time complexity of a binary search on a sorted list of n items?",
                "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
                "answer": 2,
                "model": "O(log n). Each comparison halves the remaining search space, so the number of steps grows with the logarithm of the list size. Linear search by contrast is O(n).",
            },
            {
                "type": "mcq",
                "q": "Which sorting algorithm repeatedly compares and swaps adjacent elements, 'bubbling' the largest to the end each pass?",
                "options": ["Merge sort", "Insertion sort", "Bubble sort", "Binary sort"],
                "answer": 2,
                "model": "Bubble sort. It steps through the list comparing adjacent pairs and swapping them if out of order, so the largest unsorted value moves to its correct position each pass. It is simple but inefficient at O(n²).",
            },
            {
                "type": "written",
                "q": "Explain the difference between abstraction and decomposition. [2 marks]",
                "acceptable": [
                    "Abstraction = removing/hiding unnecessary detail",
                    "Abstraction = focusing only on relevant information",
                    "Decomposition = breaking a problem into smaller sub-problems",
                ],
                "model": "Abstraction is the process of removing or hiding unnecessary detail so you focus only on the information relevant to the problem. Decomposition is breaking a large, complex problem down into smaller, more manageable sub-problems that can each be solved individually.",
            },
            {
                "type": "written",
                "q": "Describe how a binary search finds a target value in a sorted list. [3 marks]",
                "acceptable": [
                    "Examine the middle element",
                    "If it matches the target, the search ends",
                    "If target is smaller, search the left half; if larger, search the right half",
                    "Repeat until found or the search space is empty",
                ],
                "model": "Binary search checks the middle item of the sorted list. If it equals the target, the search ends. If the target is smaller, the search continues on the left half; if larger, on the right half. The process repeats on the chosen half, halving the search space each time, until the value is found or no items remain.",
            },
            {
                "type": "written",
                "q": "State what the halting problem demonstrates about computation. [2 marks]",
                "acceptable": [
                    "No general algorithm can decide whether any program will halt or loop forever",
                    "It proves some problems are non-computable / undecidable",
                ],
                "model": "The halting problem shows that it is impossible to write a single general algorithm that can decide, for every possible program and input, whether that program will eventually halt or run forever. It proves that some problems are undecidable, establishing a fundamental limit of computation.",
            },
        ],
        "Section 7 – Data Structures": [
            {
                "type": "mcq",
                "q": "A queue is best described as which type of data structure?",
                "options": ["LIFO (Last In, First Out)", "FIFO (First In, First Out)", "Random access", "Key-value"],
                "answer": 1,
                "model": "FIFO — First In, First Out. The first item added (enqueued) is the first removed (dequeued), like people waiting in a line. A stack, by contrast, is LIFO.",
            },
            {
                "type": "mcq",
                "q": "Which data structure stores data as key-value pairs?",
                "options": ["Queue", "Stack", "Dictionary", "Linear list"],
                "answer": 2,
                "model": "A dictionary stores key-value pairs, allowing a value to be looked up quickly using its unique key rather than a numeric index.",
            },
            {
                "type": "written",
                "q": "Explain how a circular queue avoids the wasted space of a simple linear queue. [2 marks]",
                "acceptable": [
                    "In a linear queue, front pointer advances and leaves unusable empty space at the start",
                    "A circular queue wraps the rear pointer back to the start when it reaches the end",
                    "Reuses the freed positions, so no space is wasted",
                ],
                "model": "In a linear queue, as items are dequeued the front pointer moves up, leaving empty cells at the start that cannot be reused, so the queue 'runs out' of space while cells are free. A circular queue treats the array as a loop: when the rear pointer reaches the end it wraps back to the start and reuses those freed positions, so no space is wasted.",
            },
            {
                "type": "written",
                "q": "State the purpose of a hash function in a hash table and explain what a collision is. [3 marks]",
                "acceptable": [
                    "A hash function converts a key into an index/address",
                    "Allows fast/direct storage and retrieval of data",
                    "A collision occurs when two different keys hash to the same index/address",
                ],
                "model": "A hash function takes a key and converts it into an index in the table, allowing data to be stored and retrieved quickly without searching. A collision happens when two different keys produce the same index; it is resolved using techniques such as storing the item in the next free slot (open addressing) or chaining items in a list at that index.",
            },
        ],
        "Section 12 – Object-Oriented Programming": [
            {
                "type": "mcq",
                "q": "In a class, what is the main purpose of the constructor method (e.g. __init__)?",
                "options": [
                    "To delete an object from memory",
                    "To initialise an object's attributes when it is created",
                    "To inherit from a parent class",
                    "To make all attributes public",
                ],
                "answer": 1,
                "model": "A constructor runs automatically when an object is instantiated and sets up its initial attribute values. In Python this is __init__.",
            },
            {
                "type": "mcq",
                "q": "Which OOP concept allows a child class to acquire the attributes and methods of a parent class?",
                "options": ["Encapsulation", "Polymorphism", "Inheritance", "Instantiation"],
                "answer": 2,
                "model": "Inheritance lets a child (sub) class reuse the attributes and methods of a parent (super) class, reducing duplicated code and modelling 'is-a' relationships.",
            },
            {
                "type": "written",
                "q": "Explain what encapsulation is and give one benefit of using it. [2 marks]",
                "acceptable": [
                    "Bundling attributes and methods together inside a class",
                    "Keeping attributes private / accessed only through methods",
                    "Benefit: protects data from invalid/accidental changes / easier maintenance",
                ],
                "model": "Encapsulation is bundling an object's data (attributes) and the methods that act on it inside a single class, with attributes usually kept private and accessed only through public methods (getters/setters). A benefit is that it protects the data from invalid or accidental changes and makes the code easier to maintain because the internal workings are hidden.",
            },
            {
                "type": "written",
                "q": "Define polymorphism in object-oriented programming. [2 marks]",
                "acceptable": [
                    "The same method/interface behaves differently for different classes",
                    "A method can be overridden in a subclass to give different behaviour",
                ],
                "model": "Polymorphism means that the same method name or interface can produce different behaviour depending on the object it is called on. For example, a parent class method can be overridden in a child class, so calling that method on different objects gives behaviour appropriate to each class.",
            },
        ],
    },

    "Paper 2": {
        "Number Systems": [
            {
                "type": "mcq",
                "q": "Which representation is most commonly used to store negative integers in binary?",
                "options": ["Sign and magnitude only", "Two's complement", "Pure binary", "BCD"],
                "answer": 1,
                "model": "Two's complement. It allows a single, consistent way to add and subtract signed numbers using normal binary addition, with the most significant bit acting as a negative place value.",
            },
            {
                "type": "mcq",
                "q": "What is the denary (decimal) value of the unsigned binary number 0011 0010?",
                "options": ["48", "50", "52", "100"],
                "answer": 1,
                "model": "50. The set bits are 32 + 16 + 2 = 50.",
            },
            {
                "type": "written",
                "q": "Convert the 8-bit two's complement number 1111 1011 to denary. Show your method. [2 marks]",
                "acceptable": [
                    "Recognise MSB = 1 so the number is negative",
                    "Method: invert and add 1 (0000 0100 = 4, so value = -5) OR use -128 place value",
                    "Answer = -5",
                ],
                "model": "The most significant bit is 1, so the value is negative. Using place values with a negative MSB: -128 + 64 + 32 + 16 + 8 + 2 + 1 = -5. (Alternatively, invert to 0000 0100 and add 1 = 0000 0101 = 5, so the original is -5.) Answer: -5.",
            },
        ],
        "Floating Point Representation": [
            {
                "type": "mcq",
                "q": "In floating point representation, what does the exponent determine?",
                "options": [
                    "The precision of the number",
                    "The sign of the number",
                    "The position of the binary point (the magnitude/range)",
                    "Whether the number is normalised",
                ],
                "answer": 2,
                "model": "The exponent fixes where the binary point sits, controlling the magnitude/range of the value. The mantissa holds the significant digits and determines precision.",
            },
            {
                "type": "written",
                "q": "State the roles of the mantissa and the exponent in floating point representation, and give one advantage of normalisation. [3 marks]",
                "acceptable": [
                    "Mantissa holds the significant figures / precision of the number",
                    "Exponent determines the position of the binary point / magnitude",
                    "Normalisation gives the most precise representation for a given number of bits / a unique representation",
                ],
                "model": "The mantissa stores the significant digits of the number and so governs its precision, while the exponent specifies the position of the binary point and so governs the number's magnitude or range. Normalisation maximises the number of significant figures held in the mantissa, giving the greatest possible precision for a fixed number of bits and ensuring each value has a unique representation.",
            },
        ],
        "Sound Representation": [
            {
                "type": "mcq",
                "q": "Compared with sampled audio, a MIDI file typically:",
                "options": [
                    "Requires far more storage",
                    "Stores instructions/events rather than the actual waveform, using less storage",
                    "Captures background noise more accurately",
                    "Cannot be edited",
                ],
                "answer": 1,
                "model": "MIDI stores event instructions (which note, when, how loud, which instrument) rather than the recorded sound wave, so files are much smaller and easily edited, though they rely on the playback device's sounds.",
            },
            {
                "type": "written",
                "q": "Give one advantage and one disadvantage of MIDI compared with sampled sound. [2 marks]",
                "acceptable": [
                    "Advantage: much smaller file size / easy to edit individual notes/instruments",
                    "Disadvantage: cannot record real-world sounds/voices / playback quality depends on the device",
                ],
                "model": "An advantage of MIDI is that files are very small and individual notes or instruments can be edited easily because it stores instructions rather than a waveform. A disadvantage is that it cannot capture real-world sounds such as vocals, and the playback quality depends on the synthesiser or device reproducing the sounds.",
            },
        ],
        "Hardware and Security Systems": [
            {
                "type": "mcq",
                "q": "An RFID tag reader works by:",
                "options": [
                    "Reading a printed pattern of black and white lines",
                    "Detecting a fingerprint's ridges",
                    "Using radio waves to read data stored on a tag without contact",
                    "Capturing a still image",
                ],
                "answer": 2,
                "model": "RFID (Radio-Frequency Identification) uses radio waves so the reader can retrieve data from a tag wirelessly, without line-of-sight or physical contact — unlike a barcode scanner which reads a visible line pattern.",
            },
            {
                "type": "written",
                "q": "Explain the difference between physical security and network security, giving one example of each. [3 marks]",
                "acceptable": [
                    "Physical security protects the actual hardware/premises (e.g. locks, CCTV, biometric door access)",
                    "Network security protects data/systems from digital threats (e.g. firewalls, encryption, passwords)",
                    "One valid example of each",
                ],
                "model": "Physical security protects the tangible hardware and premises from unauthorised access or damage — for example programmable door locks, turnstiles or CCTV. Network security protects systems and data from digital threats travelling over a network — for example firewalls, encryption or strong authentication. Both are needed because attackers can target either the equipment or the data.",
            },
        ],
        "Processor Architecture": [
            {
                "type": "mcq",
                "q": "Which component of the processor coordinates the fetch-decode-execute cycle and controls the flow of data?",
                "options": ["The status register", "The Control Unit (CU)", "A general purpose register", "The ALU's accumulator"],
                "answer": 1,
                "model": "The Control Unit directs operations: it manages the fetch-decode-execute cycle, sends control signals, and coordinates the movement of data between components.",
            },
            {
                "type": "written",
                "q": "State the purpose of the status register and give one example of a flag it might hold. [2 marks]",
                "acceptable": [
                    "Holds flags/bits showing the result/state of the last operation",
                    "Used for decisions/branching",
                    "Example flag: zero, carry, negative/sign, overflow",
                ],
                "model": "The status register holds a set of flag bits that record the outcome and conditions of the most recent operation, which the processor uses to make decisions such as conditional branching. Example flags include the zero flag, the carry flag and the negative/overflow flags.",
            },
        ],
        "Software Types": [
            {
                "type": "mcq",
                "q": "Which of the following is an example of utility software?",
                "options": ["A web browser", "A word processor", "A disk defragmenter", "A spreadsheet"],
                "answer": 2,
                "model": "A disk defragmenter is utility software — it performs maintenance/housekeeping tasks for the system. Browsers, word processors and spreadsheets are application software.",
            },
            {
                "type": "written",
                "q": "Explain the difference between application software and system software. [2 marks]",
                "acceptable": [
                    "Application software performs tasks for the user (e.g. word processor, browser)",
                    "System software runs/manages the computer and supports applications (e.g. OS, utilities, translators)",
                ],
                "model": "Application software is designed to help the user carry out specific tasks, such as a word processor or web browser. System software runs and manages the computer itself and provides a platform for applications to run — examples include the operating system, utility programs and language translators.",
            },
        ],
        "Boolean Algebra and Logic Gates": [
            {
                "type": "mcq",
                "q": "For a two-input XOR gate, the output is 1 (true) when:",
                "options": [
                    "Both inputs are 1",
                    "Both inputs are 0",
                    "The inputs are different from each other",
                    "Always",
                ],
                "answer": 2,
                "model": "An XOR (exclusive OR) gate outputs 1 only when its inputs differ (one is 1 and the other 0). If both inputs are the same, the output is 0.",
            },
            {
                "type": "mcq",
                "q": "A two-input AND gate outputs 1 only when:",
                "options": ["At least one input is 1", "Both inputs are 1", "Both inputs are 0", "The inputs differ"],
                "answer": 1,
                "model": "An AND gate outputs 1 only when both inputs are 1; in every other case it outputs 0.",
            },
            {
                "type": "written",
                "q": "State De Morgan's two laws (in words or notation) and explain why they are useful. [3 marks]",
                "acceptable": [
                    "NOT(A AND B) = (NOT A) OR (NOT B)",
                    "NOT(A OR B) = (NOT A) AND (NOT B)",
                    "Useful for simplifying Boolean expressions / converting between AND and OR / reducing number of gates",
                ],
                "model": "De Morgan's laws state that NOT(A AND B) is equivalent to (NOT A) OR (NOT B), and NOT(A OR B) is equivalent to (NOT A) AND (NOT B) — written with overbars, the bar over a whole bracket can be 'broken' if you also change the operator between the terms. They are useful for simplifying Boolean expressions and converting between AND/OR forms, which can reduce the number of logic gates needed in a circuit.",
            },
        ],
        "Logic Systems": [
            {
                "type": "written",
                "q": "Describe the steps you would take to design a logic circuit from a given truth table. [3 marks]",
                "acceptable": [
                    "Identify the input rows where the output is 1",
                    "Write a Boolean expression (e.g. sum of products) for those rows",
                    "Simplify the expression (Boolean algebra / De Morgan's)",
                    "Draw the circuit using the corresponding logic gates",
                ],
                "model": "First identify every row of the truth table where the output is 1. Write a Boolean expression for those rows (a sum-of-products: AND the inputs for each '1' row, then OR the terms together). Simplify the expression using Boolean algebra and De Morgan's laws to reduce the number of gates, then draw the final circuit using the AND, OR and NOT gates that match the simplified expression.",
            },
        ],
        "Databases": [
            {
                "type": "mcq",
                "q": "What is a primary key in a relational database?",
                "options": [
                    "A field that links to another table",
                    "A field (or fields) that uniquely identifies each record in a table",
                    "Any field that can be left blank",
                    "A duplicate of another table's data",
                ],
                "answer": 1,
                "model": "A primary key uniquely identifies each record in a table, so no two records share the same value and it is never null. A foreign key, by contrast, links to a primary key in another table.",
            },
            {
                "type": "mcq",
                "q": "A foreign key is used to:",
                "options": [
                    "Uniquely identify records in its own table",
                    "Create a link to the primary key of another table",
                    "Sort the table automatically",
                    "Encrypt the data",
                ],
                "answer": 1,
                "model": "A foreign key is a field in one table that refers to the primary key of another table, creating a relationship between the two and helping maintain referential integrity.",
            },
            {
                "type": "written",
                "q": "Explain why a database is normalised. Give two benefits. [3 marks]",
                "acceptable": [
                    "Normalisation organises data to reduce/remove redundancy (duplicate data)",
                    "Benefit: saves storage space",
                    "Benefit: avoids update/insertion/deletion anomalies / improves data consistency/integrity",
                ],
                "model": "Normalisation structures the tables so that data is stored without unnecessary duplication. Benefits include reduced storage requirements because data is not repeated, and improved data integrity/consistency because each fact is stored once, which avoids update anomalies where copies could disagree.",
            },
        ],
        "SQL": [
            {
                "type": "mcq",
                "q": "Which SQL clause is used to sort the results of a query?",
                "options": ["WHERE", "ORDER BY", "GROUP BY", "SELECT"],
                "answer": 1,
                "model": "ORDER BY sorts the returned rows by one or more fields, ascending (ASC) by default or descending (DESC). WHERE filters rows; SELECT chooses columns.",
            },
            {
                "type": "written",
                "q": "Write an SQL query that selects the Name and Grade of all students in the Students table who have a Grade of 'A', sorted by Name. [3 marks]",
                "acceptable": [
                    "SELECT Name, Grade",
                    "FROM Students",
                    "WHERE Grade = 'A'",
                    "ORDER BY Name",
                ],
                "model": "SELECT Name, Grade\nFROM Students\nWHERE Grade = 'A'\nORDER BY Name;\n\nSELECT chooses the columns, FROM names the table, WHERE filters to grade A, and ORDER BY Name sorts the output alphabetically by name.",
            },
        ],
        "Assembly Language": [
            {
                "type": "mcq",
                "q": "In the AQA assembly instruction set, what does LSL do?",
                "options": [
                    "Logical shift right",
                    "Logical shift left (multiplies by powers of two)",
                    "Loads a value from memory",
                    "Compares two registers",
                ],
                "answer": 1,
                "model": "LSL is a logical shift left: bits move left and zeros fill from the right, which has the effect of multiplying the value by powers of two. LSR shifts right (dividing).",
            },
            {
                "type": "mcq",
                "q": "Which bitwise operation in the AQA instruction set performs an exclusive OR?",
                "options": ["AND", "ORR", "EOR", "MVN"],
                "answer": 2,
                "model": "EOR performs a bitwise exclusive OR. AND and ORR perform bitwise AND/OR, and MVN performs a bitwise NOT (move not).",
            },
            {
                "type": "written",
                "q": "State two differences between assembly language and machine code. [2 marks]",
                "acceptable": [
                    "Assembly uses mnemonics (e.g. ADD, LDR); machine code is binary/0s and 1s",
                    "Assembly is human-readable; machine code is directly executed by the CPU",
                    "Assembly must be translated (by an assembler) into machine code",
                ],
                "model": "Assembly language uses human-readable mnemonics such as ADD and LDR, whereas machine code is pure binary that the processor executes directly. Assembly must be translated into machine code by an assembler before it can run, so it is one level of abstraction above machine code while still mapping closely to it.",
            },
        ],
        "Ethical, Legal and Privacy Issues": [
            {
                "type": "mcq",
                "q": "Under data protection law (GDPR), organisations must:",
                "options": [
                    "Keep all collected data forever",
                    "Sell data to improve services",
                    "Only collect data that is necessary and keep it secure",
                    "Share customer data freely between companies",
                ],
                "answer": 2,
                "model": "Data protection law requires organisations to collect only the personal data that is necessary, use it for the stated purpose, keep it accurate and secure, and not retain it longer than needed.",
            },
            {
                "type": "written",
                "q": "Discuss one ethical or privacy concern raised by using RFID tags and customer data for consumer profiling. [3 marks]",
                "acceptable": [
                    "Tracking without consent / awareness (RFID can be read remotely)",
                    "Building detailed profiles of behaviour/spending without permission",
                    "Risk of data being shared, sold or breached / loss of privacy",
                    "Could be used for surveillance or to disadvantage/target individuals",
                ],
                "model": "A key concern is that RFID tags can be read remotely, so customers may be tracked without their knowledge or consent. Combining this with purchase data lets companies build detailed profiles of individuals' behaviour and spending, which raises privacy issues if that data is shared, sold or breached. There is also a risk of intrusive surveillance or of profiling being used to unfairly target or disadvantage particular customers, so consent and data minimisation are important.",
            },
        ],
    },
}

# ── Quiz session state ──────────────────────────────────────────────────────────
quiz_state = {
    "phase":          "setup",      # setup | active | results
    "paper":          "Paper 1",    # Paper 1 | Paper 2 | Both papers
    "section":        "All sections",
    "pool":           [],
    "index":          0,
    "mcq_total":      0,
    "mcq_correct":    0,
    "written_total":  0,
    "written_correct": 0,
    # per-question runtime flags
    "answered":       False,   # mcq answered?
    "chosen":         None,    # mcq chosen index
    "revealed":       False,   # written revealed?
    "self_marked":    None,    # written: True/False once self-marked
    "written_draft":  "",
}

QUIZ_ACCENT = "#3B82F6"   # CS blue
QUIZ_GREEN  = "#10B981"
QUIZ_RED    = "#EF4444"


def _quiz_section_options():
    opts = ["All sections"]
    if quiz_state["paper"] == "Both papers":
        for pn in CS_QUIZ:
            opts += list(CS_QUIZ[pn].keys())
    else:
        opts += list(CS_QUIZ[quiz_state["paper"]].keys())
    return opts


def _build_quiz_pool(paper_choice, section_choice):
    pool = []
    papers = list(CS_QUIZ.keys()) if paper_choice == "Both papers" else [paper_choice]
    for pname in papers:
        for sec, questions in CS_QUIZ[pname].items():
            if section_choice != "All sections" and sec != section_choice:
                continue
            for q in questions:
                item = dict(q)
                item["_section"] = sec
                item["_paper"] = pname
                pool.append(item)
    random.shuffle(pool)
    return pool


def _count_quiz_questions(paper_choice, section_choice):
    n = 0
    papers = list(CS_QUIZ.keys()) if paper_choice == "Both papers" else [paper_choice]
    for pname in papers:
        for sec, questions in CS_QUIZ[pname].items():
            if section_choice != "All sections" and sec != section_choice:
                continue
            n += len(questions)
    return n


def _reset_question_flags():
    quiz_state["answered"] = False
    quiz_state["chosen"] = None
    quiz_state["revealed"] = False
    quiz_state["self_marked"] = None
    quiz_state["written_draft"] = ""


def _start_quiz():
    quiz_state["pool"] = _build_quiz_pool(quiz_state["paper"], quiz_state["section"])
    quiz_state["index"] = 0
    quiz_state["mcq_total"] = quiz_state["mcq_correct"] = 0
    quiz_state["written_total"] = quiz_state["written_correct"] = 0
    _reset_question_flags()
    quiz_state["phase"] = "active" if quiz_state["pool"] else "setup"
    refresh_quiz()


def _next_question():
    quiz_state["index"] += 1
    _reset_question_flags()
    if quiz_state["index"] >= len(quiz_state["pool"]):
        quiz_state["phase"] = "results"
        _save_quiz_stats()
    refresh_quiz()


def _save_quiz_stats():
    stats = data.setdefault("quiz_stats", {})
    total = quiz_state["mcq_total"] + quiz_state["written_total"]
    correct = quiz_state["mcq_correct"] + quiz_state["written_correct"]
    stats["attempts"] = stats.get("attempts", 0) + 1
    stats["total_answered"] = stats.get("total_answered", 0) + total
    stats["total_correct"] = stats.get("total_correct", 0) + correct
    if total:
        acc = correct / total * 100
        stats["best_accuracy"] = max(stats.get("best_accuracy", 0), acc)
    save_data()


# ── Quiz: dispatcher ─────────────────────────────────────────────────────────────
def refresh_quiz():
    p = pages["quiz"]
    clear_frame(p)
    phase = quiz_state["phase"]
    if phase == "active" and quiz_state["pool"]:
        _render_quiz_question(p)
    elif phase == "results":
        _render_quiz_results(p)
    else:
        _render_quiz_setup(p)


# ── Quiz: setup screen ───────────────────────────────────────────────────────────
def _render_quiz_setup(p):
    page_header(p, "🧠  Computer Science Quiz",
                "AQA AS-Level  •  Paper 1 & Paper 2  •  Mix of multiple choice and written answers",
                color=QUIZ_ACCENT)

    # Lifetime stats (if any)
    stats = data.get("quiz_stats", {})
    if stats.get("attempts"):
        s_card = ctk.CTkFrame(p, fg_color=THEME["card"], corner_radius=14)
        s_card.pack(fill="x", pady=(0, 16))
        inner = ctk.CTkFrame(s_card, fg_color="transparent")
        inner.pack(fill="x", padx=18, pady=14)
        ta = stats.get("total_answered", 0)
        tc = stats.get("total_correct", 0)
        acc = int(tc / ta * 100) if ta else 0
        for big, small in [
            (str(stats.get("attempts", 0)), "quizzes taken"),
            (f"{tc}/{ta}", "lifetime correct"),
            (f"{acc}%", "overall accuracy"),
            (f"{int(stats.get('best_accuracy', 0))}%", "best accuracy"),
        ]:
            col = ctk.CTkFrame(inner, fg_color="transparent")
            col.pack(side="left", expand=True)
            ctk.CTkLabel(col, text=big, font=("Arial", 20, "bold"),
                         text_color=QUIZ_ACCENT).pack()
            ctk.CTkLabel(col, text=small, font=("Arial", 11),
                         text_color=THEME["text_muted"]).pack()

    # Setup card
    card = ctk.CTkFrame(p, fg_color=THEME["card"], corner_radius=14)
    card.pack(fill="x", pady=(0, 16))
    body = ctk.CTkFrame(card, fg_color="transparent")
    body.pack(fill="x", padx=20, pady=18)

    ctk.CTkLabel(body, text="Build your quiz", font=("Arial", 15, "bold"),
                 text_color=THEME["text_primary"]).pack(anchor="w", pady=(0, 12))

    # Paper selector
    ctk.CTkLabel(body, text="Paper", font=("Arial", 12),
                 text_color=THEME["text_secondary"]).pack(anchor="w")
    paper_var = ctk.StringVar(value=quiz_state["paper"])

    def on_paper_change(choice):
        quiz_state["paper"] = choice
        quiz_state["section"] = "All sections"
        refresh_quiz()

    ctk.CTkOptionMenu(body, values=["Paper 1", "Paper 2", "Both papers"],
                      variable=paper_var, command=on_paper_change, width=240,
                      fg_color=THEME["card2"], button_color=QUIZ_ACCENT,
                      button_hover_color="#2563EB",
                      font=("Arial", 12)).pack(anchor="w", pady=(4, 14))

    # Section selector
    ctk.CTkLabel(body, text="Topic / section", font=("Arial", 12),
                 text_color=THEME["text_secondary"]).pack(anchor="w")
    sec_var = ctk.StringVar(value=quiz_state["section"])

    def on_section_change(choice):
        quiz_state["section"] = choice

    ctk.CTkOptionMenu(body, values=_quiz_section_options(),
                      variable=sec_var, command=on_section_change, width=460,
                      fg_color=THEME["card2"], button_color=QUIZ_ACCENT,
                      button_hover_color="#2563EB",
                      font=("Arial", 12)).pack(anchor="w", pady=(4, 14))

    n = _count_quiz_questions(quiz_state["paper"], quiz_state["section"])
    ctk.CTkLabel(body, text=f"{n} question{'s' if n != 1 else ''} available  •  questions are shuffled each time",
                 font=("Arial", 12), text_color=THEME["text_muted"]).pack(anchor="w", pady=(0, 16))

    ctk.CTkButton(body, text="▶  Start Quiz", height=42, width=200, corner_radius=10,
                  fg_color=QUIZ_ACCENT, hover_color="#2563EB", font=("Arial", 14, "bold"),
                  command=_start_quiz).pack(anchor="w")

    # How marking works
    info = ctk.CTkFrame(p, fg_color=THEME["card"], corner_radius=14)
    info.pack(fill="x")
    ib = ctk.CTkFrame(info, fg_color="transparent")
    ib.pack(fill="x", padx=20, pady=16)
    ctk.CTkLabel(ib, text="How marking works", font=("Arial", 13, "bold"),
                 text_color=THEME["text_secondary"]).pack(anchor="w", pady=(0, 6))
    ctk.CTkLabel(ib,
                 text="•  Multiple choice is marked automatically — your choice turns green if right, red if wrong, and the correct option is highlighted with a model answer.",
                 font=("Arial", 12), text_color=THEME["text_muted"],
                 justify="left", wraplength=820).pack(anchor="w", pady=2)
    ctk.CTkLabel(ib,
                 text="•  Written questions show the acceptable answer points and a model answer when you reveal them. You then mark yourself honestly as right or wrong.",
                 font=("Arial", 12), text_color=THEME["text_muted"],
                 justify="left", wraplength=820).pack(anchor="w", pady=2)


# ── Quiz: question screen ────────────────────────────────────────────────────────
def _render_quiz_question(p):
    pool = quiz_state["pool"]
    i = quiz_state["index"]
    q = pool[i]

    # Top bar: progress + running score + end button
    top = ctk.CTkFrame(p, fg_color="transparent")
    top.pack(fill="x", pady=(0, 10))
    ctk.CTkLabel(top, text=f"Question {i + 1} of {len(pool)}",
                 font=("Arial", 13, "bold"), text_color=QUIZ_ACCENT).pack(side="left")
    score = quiz_state["mcq_correct"] + quiz_state["written_correct"]
    answered_count = quiz_state["mcq_total"] + quiz_state["written_total"]
    ctk.CTkLabel(top, text=f"Score: {score}/{answered_count}",
                 font=("Arial", 13), text_color=THEME["text_muted"]).pack(side="left", padx=16)
    ctk.CTkButton(top, text="✕ End quiz", width=90, height=28, corner_radius=7,
                  fg_color=THEME["card"], hover_color=THEME["card2"],
                  text_color=THEME["text_muted"], font=("Arial", 11),
                  command=_end_quiz).pack(side="right")

    # Progress bar
    bar_bg = ctk.CTkFrame(p, height=5, fg_color=THEME["card2"], corner_radius=3)
    bar_bg.pack(fill="x", pady=(0, 16))
    q_fill = ctk.CTkFrame(bar_bg, height=5, fg_color=QUIZ_ACCENT, corner_radius=3)
    q_fill.place(relwidth=i / len(pool), relheight=1)
    animate(q_fill, i / len(pool), (i + 1) / len(pool), 300,
            lambda v: q_fill.place(relwidth=v, relheight=1))

    # Question card
    card = ctk.CTkFrame(p, fg_color=THEME["card"], corner_radius=14)
    card.pack(fill="x")
    body = ctk.CTkFrame(card, fg_color="transparent")
    body.pack(fill="x", padx=22, pady=20)

    # Tag row (paper + section + type)
    tag = "Multiple choice" if q["type"] == "mcq" else "Written answer"
    ctk.CTkLabel(body, text=f"{q['_paper']}  •  {q['_section']}  •  {tag}",
                 font=("Arial", 11), text_color=THEME["text_muted"]).pack(anchor="w")
    ctk.CTkLabel(body, text=q["q"], font=("Arial", 16, "bold"),
                 text_color=THEME["text_primary"], justify="left",
                 wraplength=800).pack(anchor="w", pady=(8, 16))

    if q["type"] == "mcq":
        _render_mcq_body(body, q)
    else:
        _render_written_body(body, q)


def _render_mcq_body(body, q):
    answered = quiz_state["answered"]
    chosen = quiz_state["chosen"]
    correct = q["answer"]
    labels = ["A", "B", "C", "D", "E", "F"]

    for idx, opt in enumerate(q["options"]):
        if not answered:
            fg, txt = THEME["card2"], THEME["text_primary"]

            def choose(chosen_idx=idx):
                quiz_state["answered"] = True
                quiz_state["chosen"] = chosen_idx
                quiz_state["mcq_total"] += 1
                if chosen_idx == correct:
                    quiz_state["mcq_correct"] += 1
                refresh_quiz()

            ctk.CTkButton(body, text=f"  {labels[idx]}.   {opt}", anchor="w",
                          height=44, corner_radius=9, fg_color=fg,
                          hover_color=THEME["border"], text_color=txt,
                          font=("Arial", 13), command=choose).pack(fill="x", pady=4)
        else:
            # Show result colours
            if idx == correct:
                fg, txt, mark = "#0E3D2E", QUIZ_GREEN, "  ✓"
            elif idx == chosen:
                fg, txt, mark = "#3B1A1A", QUIZ_RED, "  ✗"
            else:
                fg, txt, mark = THEME["card2"], THEME["text_muted"], ""
            row = ctk.CTkFrame(body, fg_color=fg, corner_radius=9, height=44)
            row.pack(fill="x", pady=4)
            row.pack_propagate(False)
            ctk.CTkLabel(row, text=f"   {labels[idx]}.   {opt}{mark}", anchor="w",
                         text_color=txt, font=("Arial", 13)).pack(side="left", padx=6)

    if quiz_state["answered"]:
        verdict = "Correct!" if chosen == correct else "Not quite."
        vcolor = QUIZ_GREEN if chosen == correct else QUIZ_RED
        ctk.CTkLabel(body, text=verdict, font=("Arial", 14, "bold"),
                     text_color=vcolor).pack(anchor="w", pady=(14, 4))
        _model_answer_box(body, q["model"])
        _nav_next_button(body)


def _render_written_body(body, q):
    ctk.CTkLabel(body, text="Type your answer (optional — just for your own working):",
                 font=("Arial", 11), text_color=THEME["text_muted"]).pack(anchor="w")

    if not quiz_state["revealed"]:
        tb = ctk.CTkTextbox(body, height=90, fg_color=THEME["input_bg"],
                            border_color=THEME["border"], border_width=1,
                            font=("Arial", 13), corner_radius=8)
        tb.pack(fill="x", pady=(6, 12))

        def reveal(box=tb):
            quiz_state["written_draft"] = box.get("1.0", "end").strip()
            quiz_state["revealed"] = True
            refresh_quiz()

        ctk.CTkButton(body, text="👁  Reveal acceptable answers & model answer",
                      height=40, corner_radius=9, fg_color=QUIZ_ACCENT,
                      hover_color="#2563EB", font=("Arial", 13, "bold"),
                      command=reveal).pack(anchor="w")
    else:
        # Show their draft (read-only) if they typed anything
        if quiz_state["written_draft"]:
            draft = ctk.CTkFrame(body, fg_color=THEME["input_bg"], corner_radius=8)
            draft.pack(fill="x", pady=(6, 12))
            ctk.CTkLabel(draft, text="Your answer:", font=("Arial", 11, "bold"),
                         text_color=THEME["text_muted"]).pack(anchor="w", padx=12, pady=(8, 0))
            ctk.CTkLabel(draft, text=quiz_state["written_draft"], font=("Arial", 12),
                         text_color=THEME["text_secondary"], justify="left",
                         wraplength=780).pack(anchor="w", padx=12, pady=(0, 10))

        # Acceptable answer points
        acc_box = ctk.CTkFrame(body, fg_color=THEME["card2"], corner_radius=10)
        acc_box.pack(fill="x", pady=(4, 10))
        ctk.CTkLabel(acc_box, text="Acceptable answer points", font=("Arial", 12, "bold"),
                     text_color=QUIZ_ACCENT).pack(anchor="w", padx=14, pady=(10, 4))
        for pt in q.get("acceptable", []):
            ctk.CTkLabel(acc_box, text=f"•  {pt}", font=("Arial", 12),
                         text_color=THEME["text_secondary"], justify="left",
                         wraplength=780).pack(anchor="w", padx=14, pady=1)
        ctk.CTkFrame(acc_box, height=6, fg_color="transparent").pack()

        _model_answer_box(body, q["model"])

        # Self-marking
        if quiz_state["self_marked"] is None:
            ctk.CTkLabel(body, text="Mark yourself honestly:", font=("Arial", 13, "bold"),
                         text_color=THEME["text_primary"]).pack(anchor="w", pady=(14, 6))
            mark_row = ctk.CTkFrame(body, fg_color="transparent")
            mark_row.pack(anchor="w")

            def mark(correct_flag):
                quiz_state["self_marked"] = correct_flag
                quiz_state["written_total"] += 1
                if correct_flag:
                    quiz_state["written_correct"] += 1
                refresh_quiz()

            ctk.CTkButton(mark_row, text="✓  I was right", height=40, width=160,
                          corner_radius=9, fg_color="#0E3D2E", hover_color=QUIZ_GREEN,
                          text_color=QUIZ_GREEN, font=("Arial", 13, "bold"),
                          command=lambda: mark(True)).pack(side="left", padx=(0, 10))
            ctk.CTkButton(mark_row, text="✗  I was wrong", height=40, width=160,
                          corner_radius=9, fg_color="#3B1A1A", hover_color=QUIZ_RED,
                          text_color=QUIZ_RED, font=("Arial", 13, "bold"),
                          command=lambda: mark(False)).pack(side="left")
        else:
            v = "Marked correct ✓" if quiz_state["self_marked"] else "Marked incorrect ✗"
            vc = QUIZ_GREEN if quiz_state["self_marked"] else QUIZ_RED
            ctk.CTkLabel(body, text=v, font=("Arial", 14, "bold"),
                         text_color=vc).pack(anchor="w", pady=(14, 4))
            _nav_next_button(body)


def _model_answer_box(parent, text):
    box = ctk.CTkFrame(parent, fg_color="#10243B", corner_radius=10)
    box.pack(fill="x", pady=(4, 4))
    ctk.CTkLabel(box, text="Model answer", font=("Arial", 12, "bold"),
                 text_color=QUIZ_ACCENT).pack(anchor="w", padx=14, pady=(10, 2))
    ctk.CTkLabel(box, text=text, font=("Arial", 12),
                 text_color=THEME["text_primary"], justify="left",
                 wraplength=780).pack(anchor="w", padx=14, pady=(0, 12))


def _nav_next_button(parent):
    last = quiz_state["index"] >= len(quiz_state["pool"]) - 1
    ctk.CTkButton(parent, text=("🏁  Finish & see results" if last else "Next question  →"),
                  height=42, width=220, corner_radius=10, fg_color=QUIZ_ACCENT,
                  hover_color="#2563EB", font=("Arial", 13, "bold"),
                  command=_next_question).pack(anchor="w", pady=(14, 0))


def _end_quiz():
    quiz_state["phase"] = "results"
    if quiz_state["mcq_total"] + quiz_state["written_total"] > 0:
        _save_quiz_stats()
    refresh_quiz()


# ── Quiz: results screen ─────────────────────────────────────────────────────────
def _render_quiz_results(p):
    page_header(p, "🏁  Quiz Results", color=QUIZ_ACCENT)

    mc, mt = quiz_state["mcq_correct"], quiz_state["mcq_total"]
    wc, wt = quiz_state["written_correct"], quiz_state["written_total"]
    total = mt + wt
    correct = mc + wc

    card = ctk.CTkFrame(p, fg_color=THEME["card"], corner_radius=16)
    card.pack(fill="x", pady=(0, 16))
    inner = ctk.CTkFrame(card, fg_color="transparent")
    inner.pack(padx=24, pady=24, fill="x")

    left = ctk.CTkFrame(inner, fg_color="transparent")
    left.pack(side="left")
    draw_circle_progress(left, correct, total, size=130, color=QUIZ_ACCENT)

    right = ctk.CTkFrame(inner, fg_color="transparent")
    right.pack(side="left", padx=26)

    if total == 0:
        msg = "No questions answered."
    else:
        pct = int(correct / total * 100)
        if pct >= 80:
            msg = "Excellent — you're exam-ready on this!"
        elif pct >= 60:
            msg = "Solid effort — review the ones you missed."
        elif pct >= 40:
            msg = "Getting there — worth another revision pass."
        else:
            msg = "Keep going — revisit these topics and try again."

    ctk.CTkLabel(right, text=f"{correct} / {total} correct",
                 font=("Arial", 22, "bold"), text_color=THEME["text_primary"]).pack(anchor="w")
    ctk.CTkLabel(right, text=msg, font=("Arial", 13),
                 text_color=QUIZ_ACCENT).pack(anchor="w", pady=(4, 12))
    ctk.CTkLabel(right, text=f"Multiple choice:  {mc}/{mt}",
                 font=("Arial", 13), text_color=THEME["text_secondary"]).pack(anchor="w", pady=1)
    ctk.CTkLabel(right, text=f"Written (self-marked):  {wc}/{wt}",
                 font=("Arial", 13), text_color=THEME["text_secondary"]).pack(anchor="w", pady=1)

    # Action buttons
    btns = ctk.CTkFrame(p, fg_color="transparent")
    btns.pack(fill="x")

    def again():
        # Same settings, fresh shuffle
        _start_quiz()

    def new_quiz():
        quiz_state["phase"] = "setup"
        refresh_quiz()

    ctk.CTkButton(btns, text="🔁  Try again (same settings)", height=44, corner_radius=10,
                  fg_color=QUIZ_ACCENT, hover_color="#2563EB", font=("Arial", 13, "bold"),
                  command=again).pack(side="left", expand=True, fill="x", padx=(0, 8))
    ctk.CTkButton(btns, text="⚙  New quiz", height=44, corner_radius=10,
                  fg_color=THEME["card"], hover_color=THEME["card2"],
                  text_color=THEME["text_secondary"], font=("Arial", 13),
                  command=new_quiz).pack(side="left", expand=True, fill="x", padx=(8, 0))



# ══════════════════════════════════════════════════════════════════════════════
# SUBJECT REFRESHERS
# ══════════════════════════════════════════════════════════════════════════════

def refresh_cs():        build_subject_page("cs")
def refresh_business():  build_subject_page("business")
def refresh_economics(): build_subject_page("economics")

REFRESH_MAP = {
    "home":      refresh_home,
    "cs":        refresh_cs,
    "business":  refresh_business,
    "economics": refresh_economics,
    "exams":     refresh_exams,
    "quiz":      refresh_quiz,
    "schedule":  refresh_schedule,
}


# ══════════════════════════════════════════════════════════════════════════════
# BOOT
# ══════════════════════════════════════════════════════════════════════════════

show_page("home")
app.mainloop()
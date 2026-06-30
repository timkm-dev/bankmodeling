"""
Bank Queue Simulator - Visual GUI
===================================
A modern dark-themed GUI for the single-server bank queue simulation.
Re-implements the C++ SimulationEngine logic in pure Python.

Usage:  python gui.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import math

# ── colour palette ──────────────────────────────────────────────────────────
BG_DARK       = "#0f1923"
BG_PANEL      = "#162232"
BG_CARD       = "#1c2e42"
BG_INPUT      = "#243447"
ACCENT        = "#00d4aa"
ACCENT_HOVER  = "#00f0c0"
ACCENT_DIM    = "#007a62"
TEXT_PRIMARY  = "#e8edf2"
TEXT_SECONDARY= "#8899aa"
TEXT_MUTED    = "#5a6d7e"
STAT_ORANGE   = "#ff9f43"
STAT_BLUE     = "#54a0ff"
STAT_PURPLE   = "#9b59b6"
STAT_GREEN    = "#00d4aa"
BAR_WAIT      = "#ff6b6b"
BAR_SERVICE   = "#54a0ff"
TABLE_STRIPE  = "#1a2b3d"
BORDER_COLOR  = "#2a3f55"

FONT_FAMILY   = "Segoe UI"

# ── simulation engine (mirrors C++ SimulationEngine exactly) ────────────────
class SimulationEngine:
    """Single-server queue simulator using uniform random distributions."""

    def __init__(self):
        self.arr_min = 0.5
        self.arr_max = 3.0
        self.srv_min = 1.0
        self.srv_max = 4.0

    def update_parameters(self, arr_min, arr_max, srv_min, srv_max):
        self.arr_min = arr_min
        self.arr_max = arr_max
        self.srv_min = srv_min
        self.srv_max = srv_max

    def run(self, total_customers):
        customers = []
        clock = 0.0
        next_free = 0.0

        for i in range(total_customers):
            inter_arrival = random.uniform(self.arr_min, self.arr_max)
            clock += inter_arrival
            arrival = clock

            service_time = random.uniform(self.srv_min, self.srv_max)
            service_start = max(arrival, next_free)
            wait = service_start - arrival
            service_end = service_start + service_time
            time_in_sys = service_end - arrival
            next_free = service_end

            customers.append({
                "id":               i + 1,
                "interarrival":     round(inter_arrival, 4),
                "arrival":          round(arrival, 4),
                "service_time":     round(service_time, 4),
                "service_start":    round(service_start, 4),
                "wait":             round(wait, 4),
                "service_end":      round(service_end, 4),
                "time_in_system":   round(time_in_sys, 4),
            })
        return customers


def compute_stats(customers):
    """Mirrors C++ StatsAnalyzer::calculateMetrics."""
    if not customers:
        return {"total": 0, "avg_wait": 0, "avg_tis": 0, "utilization": 0}
    n = len(customers)
    total_wait    = sum(c["wait"] for c in customers)
    total_tis     = sum(c["time_in_system"] for c in customers)
    total_service = sum(c["service_time"] for c in customers)
    total_sim     = customers[-1]["service_end"]
    return {
        "total":       n,
        "avg_wait":    total_wait / n,
        "avg_tis":     total_tis / n,
        "utilization": (total_service / total_sim) * 100 if total_sim else 0,
    }


# ── main application ───────────────────────────────────────────────────────
class BankQueueGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Queue Simulator")
        self.root.configure(bg=BG_DARK)
        self.root.minsize(1100, 720)

        # Centre on screen
        w, h = 1200, 780
        sx = (self.root.winfo_screenwidth()  - w) // 2
        sy = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f"{w}x{h}+{sx}+{sy}")

        self.engine = SimulationEngine()
        self.customers = []
        self.stats = {}

        self._configure_styles()
        self._build_ui()

    # ── ttk styling ─────────────────────────────────────────────────────────
    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(".", background=BG_DARK, foreground=TEXT_PRIMARY,
                         font=(FONT_FAMILY, 10))
        style.configure("TFrame", background=BG_DARK)
        style.configure("Panel.TFrame", background=BG_PANEL)
        style.configure("Card.TFrame", background=BG_CARD)

        style.configure("Title.TLabel", background=BG_DARK,
                         foreground=ACCENT, font=(FONT_FAMILY, 18, "bold"))
        style.configure("Subtitle.TLabel", background=BG_DARK,
                         foreground=TEXT_SECONDARY, font=(FONT_FAMILY, 10))
        style.configure("Panel.TLabel", background=BG_PANEL,
                         foreground=TEXT_PRIMARY, font=(FONT_FAMILY, 10))
        style.configure("CardTitle.TLabel", background=BG_CARD,
                         foreground=TEXT_SECONDARY, font=(FONT_FAMILY, 9))
        style.configure("CardValue.TLabel", background=BG_CARD,
                         foreground=TEXT_PRIMARY, font=(FONT_FAMILY, 22, "bold"))

        style.configure("Accent.TButton",
                         background=ACCENT, foreground=BG_DARK,
                         font=(FONT_FAMILY, 11, "bold"),
                         padding=(20, 10))
        style.map("Accent.TButton",
                   background=[("active", ACCENT_HOVER), ("pressed", ACCENT_DIM)])

        style.configure("Reset.TButton",
                         background=BG_INPUT, foreground=TEXT_SECONDARY,
                         font=(FONT_FAMILY, 10),
                         padding=(14, 8))
        style.map("Reset.TButton",
                   background=[("active", BORDER_COLOR)])

        # Treeview (table)
        style.configure("Custom.Treeview",
                         background=BG_PANEL, foreground=TEXT_PRIMARY,
                         fieldbackground=BG_PANEL, rowheight=28,
                         font=(FONT_FAMILY, 9),
                         borderwidth=0)
        style.configure("Custom.Treeview.Heading",
                         background=BG_CARD, foreground=ACCENT,
                         font=(FONT_FAMILY, 9, "bold"),
                         borderwidth=0)
        style.map("Custom.Treeview",
                   background=[("selected", ACCENT_DIM)],
                   foreground=[("selected", TEXT_PRIMARY)])

        # Scrollbar
        style.configure("Custom.Vertical.TScrollbar",
                         background=BG_INPUT, troughcolor=BG_PANEL,
                         arrowcolor=TEXT_MUTED, borderwidth=0)

    # ── build the layout ────────────────────────────────────────────────────
    def _build_ui(self):
        # Header
        hdr = ttk.Frame(self.root)
        hdr.pack(fill="x", padx=24, pady=(18, 4))
        ttk.Label(hdr, text="🏦  Bank Queue Simulator", style="Title.TLabel").pack(
            side="left")
        ttk.Label(hdr, text="Single-Server  ·  Uniform Distribution  ·  FIFO Queue",
                  style="Subtitle.TLabel").pack(side="left", padx=(16, 0), pady=(6, 0))

        # Separator line
        sep = tk.Canvas(self.root, height=1, bg=BORDER_COLOR, highlightthickness=0)
        sep.pack(fill="x", padx=24, pady=(10, 0))

        # Main content: left panel (inputs) | right panel (results)
        body = ttk.Frame(self.root)
        body.pack(fill="both", expand=True, padx=24, pady=14)

        self._build_input_panel(body)
        self._build_results_panel(body)

    # ── left panel: inputs ──────────────────────────────────────────────────
    def _build_input_panel(self, parent):
        panel = ttk.Frame(parent, style="Panel.TFrame", width=300)
        panel.pack(side="left", fill="y", padx=(0, 14))
        panel.pack_propagate(False)

        inner = ttk.Frame(panel, style="Panel.TFrame")
        inner.pack(fill="both", expand=True, padx=18, pady=18)

        ttk.Label(inner, text="⚙  Simulation Parameters",
                  background=BG_PANEL, foreground=ACCENT,
                  font=(FONT_FAMILY, 12, "bold")).pack(anchor="w", pady=(0, 16))

        self.entries = {}
        fields = [
            ("num_customers", "Number of Customers", "10"),
            ("arr_min",       "Arrival Time  MIN",   "0.5"),
            ("arr_max",       "Arrival Time  MAX",   "3.0"),
            ("srv_min",       "Service Time  MIN",   "1.0"),
            ("srv_max",       "Service Time  MAX",   "4.0"),
        ]

        for key, label, default in fields:
            self._make_input_row(inner, key, label, default)

        # Buttons
        btn_frame = ttk.Frame(inner, style="Panel.TFrame")
        btn_frame.pack(fill="x", pady=(24, 0))

        run_btn = ttk.Button(btn_frame, text="▶  Run Simulation",
                             style="Accent.TButton", command=self._run_simulation)
        run_btn.pack(fill="x", pady=(0, 8))

        reset_btn = ttk.Button(btn_frame, text="↺  Reset Defaults",
                               style="Reset.TButton", command=self._reset_defaults)
        reset_btn.pack(fill="x")

        # Keyboard shortcut
        self.root.bind("<Return>", lambda e: self._run_simulation())

    def _make_input_row(self, parent, key, label, default):
        frame = ttk.Frame(parent, style="Panel.TFrame")
        frame.pack(fill="x", pady=(0, 12))

        ttk.Label(frame, text=label, style="Panel.TLabel",
                  font=(FONT_FAMILY, 9, "bold")).pack(anchor="w")

        entry = tk.Entry(frame, bg=BG_INPUT, fg=TEXT_PRIMARY,
                         insertbackground=ACCENT, relief="flat",
                         font=(FONT_FAMILY, 11), bd=0,
                         highlightthickness=1, highlightcolor=ACCENT,
                         highlightbackground=BORDER_COLOR)
        entry.pack(fill="x", ipady=6, pady=(4, 0))
        entry.insert(0, default)

        self.entries[key] = entry

    # ── right panel: results ────────────────────────────────────────────────
    def _build_results_panel(self, parent):
        self.right_panel = ttk.Frame(parent)
        self.right_panel.pack(side="left", fill="both", expand=True)

        # Stat cards row
        self.cards_frame = ttk.Frame(self.right_panel)
        self.cards_frame.pack(fill="x", pady=(0, 12))

        self.stat_labels = {}
        card_defs = [
            ("total",       "Customers Processed", "—",   STAT_GREEN,  "👥"),
            ("avg_wait",    "Avg. Wait Time",      "—",   STAT_ORANGE, "⏳"),
            ("avg_tis",     "Avg. Time in System", "—",   STAT_BLUE,   "🔄"),
            ("utilization", "Server Utilization",  "—",   STAT_PURPLE, "📊"),
        ]

        for key, title, default, color, icon in card_defs:
            self._make_stat_card(self.cards_frame, key, title, default, color, icon)

        # Notebook with tabs: Table | Chart
        self.notebook = ttk.Notebook(self.right_panel)
        self.notebook.pack(fill="both", expand=True)

        # Tab 1: Table
        table_frame = ttk.Frame(self.notebook, style="Panel.TFrame")
        self.notebook.add(table_frame, text="  📋 Customer Data  ")
        self._build_table(table_frame)

        # Tab 2: Chart
        chart_frame = ttk.Frame(self.notebook, style="Panel.TFrame")
        self.notebook.add(chart_frame, text="  📊 Wait Time Chart  ")
        self.chart_canvas = tk.Canvas(chart_frame, bg=BG_PANEL,
                                       highlightthickness=0)
        self.chart_canvas.pack(fill="both", expand=True, padx=8, pady=8)

        # Tab 3: Timeline
        timeline_frame = ttk.Frame(self.notebook, style="Panel.TFrame")
        self.notebook.add(timeline_frame, text="  🕐 Server Timeline  ")
        self.timeline_canvas = tk.Canvas(timeline_frame, bg=BG_PANEL,
                                          highlightthickness=0)
        self.timeline_canvas.pack(fill="both", expand=True, padx=8, pady=8)

        # Placeholder message
        self.placeholder_label = ttk.Label(
            self.right_panel,
            text="Configure parameters and press  ▶ Run Simulation  to begin",
            background=BG_DARK, foreground=TEXT_MUTED,
            font=(FONT_FAMILY, 11), anchor="center")
        # Will be shown / hidden dynamically

    def _make_stat_card(self, parent, key, title, default, accent_color, icon):
        card = tk.Frame(parent, bg=BG_CARD, highlightbackground=BORDER_COLOR,
                        highlightthickness=1)
        card.pack(side="left", fill="both", expand=True, padx=(0, 8))

        inner = tk.Frame(card, bg=BG_CARD)
        inner.pack(fill="both", expand=True, padx=14, pady=12)

        header = tk.Frame(inner, bg=BG_CARD)
        header.pack(fill="x")

        tk.Label(header, text=icon, bg=BG_CARD, fg=accent_color,
                 font=(FONT_FAMILY, 14)).pack(side="left")
        tk.Label(header, text=title, bg=BG_CARD, fg=TEXT_SECONDARY,
                 font=(FONT_FAMILY, 9)).pack(side="left", padx=(6, 0))

        val_label = tk.Label(inner, text=default, bg=BG_CARD,
                             fg=accent_color,
                             font=(FONT_FAMILY, 22, "bold"), anchor="w")
        val_label.pack(fill="x", pady=(6, 0))

        self.stat_labels[key] = val_label

    # ── data table ──────────────────────────────────────────────────────────
    def _build_table(self, parent):
        container = ttk.Frame(parent, style="Panel.TFrame")
        container.pack(fill="both", expand=True, padx=8, pady=8)

        columns = ("id", "interarr", "arrival", "serv_time",
                   "serv_start", "wait", "serv_end", "tis")
        headings = ("ID", "Inter-Arr", "Arrival", "Serv Time",
                    "Serv Start", "Wait Time", "Serv End", "Time In Sys")

        self.tree = ttk.Treeview(container, columns=columns, show="headings",
                                 style="Custom.Treeview", selectmode="browse")

        for col, head in zip(columns, headings):
            self.tree.heading(col, text=head)
            w = 60 if col == "id" else 95
            self.tree.column(col, width=w, anchor="center", minwidth=60)

        scrollbar = ttk.Scrollbar(container, orient="vertical",
                                   command=self.tree.yview,
                                   style="Custom.Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ── run simulation ──────────────────────────────────────────────────────
    def _run_simulation(self):
        try:
            n       = int(self.entries["num_customers"].get())
            arr_min = float(self.entries["arr_min"].get())
            arr_max = float(self.entries["arr_max"].get())
            srv_min = float(self.entries["srv_min"].get())
            srv_max = float(self.entries["srv_max"].get())
        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Please enter valid numbers in all fields.")
            return

        if n <= 0:
            messagebox.showwarning("Invalid Input",
                                   "Number of customers must be at least 1.")
            return
        if arr_min >= arr_max or srv_min >= srv_max:
            messagebox.showwarning("Invalid Range",
                                   "MIN values must be less than MAX values.")
            return

        self.engine.update_parameters(arr_min, arr_max, srv_min, srv_max)
        self.customers = self.engine.run(n)
        self.stats = compute_stats(self.customers)

        self._update_stat_cards()
        self._update_table()
        self._draw_chart()
        self._draw_timeline()

    # ── update UI ───────────────────────────────────────────────────────────
    def _update_stat_cards(self):
        s = self.stats
        self.stat_labels["total"].config(text=str(s["total"]))
        self.stat_labels["avg_wait"].config(text=f'{s["avg_wait"]:.2f} min')
        self.stat_labels["avg_tis"].config(text=f'{s["avg_tis"]:.2f} min')
        self.stat_labels["utilization"].config(text=f'{s["utilization"]:.1f}%')

    def _update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for i, c in enumerate(self.customers):
            tag = "stripe" if i % 2 else ""
            self.tree.insert("", "end", values=(
                c["id"],
                f'{c["interarrival"]:.2f}',
                f'{c["arrival"]:.2f}',
                f'{c["service_time"]:.2f}',
                f'{c["service_start"]:.2f}',
                f'{c["wait"]:.2f}',
                f'{c["service_end"]:.2f}',
                f'{c["time_in_system"]:.2f}',
            ), tags=(tag,))

        self.tree.tag_configure("stripe", background=TABLE_STRIPE)

    # ── bar chart: wait time per customer ───────────────────────────────────
    def _draw_chart(self):
        canvas = self.chart_canvas
        canvas.delete("all")
        canvas.update_idletasks()

        cw = canvas.winfo_width()
        ch = canvas.winfo_height()
        if cw < 50 or ch < 50:
            return

        customers = self.customers
        n = len(customers)
        if n == 0:
            return

        pad_l, pad_r, pad_t, pad_b = 60, 20, 30, 40
        plot_w = cw - pad_l - pad_r
        plot_h = ch - pad_t - pad_b

        max_wait = max(c["wait"] for c in customers)
        max_tis  = max(c["time_in_system"] for c in customers)
        y_max = max(max_wait, max_tis, 0.1)

        # Title
        canvas.create_text(cw // 2, 14, text="Wait Time vs Time-in-System per Customer",
                           fill=TEXT_SECONDARY, font=(FONT_FAMILY, 10, "bold"))

        # Y-axis grid lines
        num_grid = 5
        for i in range(num_grid + 1):
            y = pad_t + plot_h - (i / num_grid) * plot_h
            val = (i / num_grid) * y_max
            canvas.create_line(pad_l, y, cw - pad_r, y, fill=BORDER_COLOR, dash=(2, 4))
            canvas.create_text(pad_l - 8, y, text=f"{val:.1f}", anchor="e",
                               fill=TEXT_MUTED, font=(FONT_FAMILY, 8))

        # Y-axis label
        canvas.create_text(14, ch // 2, text="Minutes", angle=90,
                           fill=TEXT_SECONDARY, font=(FONT_FAMILY, 9))

        # Bars
        bar_group_width = plot_w / max(n, 1)
        bar_w = max(bar_group_width * 0.35, 2)
        gap = max(bar_group_width * 0.05, 1)

        for i, c in enumerate(customers):
            x_centre = pad_l + (i + 0.5) * bar_group_width

            # Wait time bar
            h_wait = (c["wait"] / y_max) * plot_h if y_max else 0
            x1 = x_centre - bar_w - gap / 2
            canvas.create_rectangle(x1, pad_t + plot_h - h_wait,
                                    x1 + bar_w, pad_t + plot_h,
                                    fill=BAR_WAIT, outline="", width=0)

            # Time-in-system bar
            h_tis = (c["time_in_system"] / y_max) * plot_h if y_max else 0
            x2 = x_centre + gap / 2
            canvas.create_rectangle(x2, pad_t + plot_h - h_tis,
                                    x2 + bar_w, pad_t + plot_h,
                                    fill=BAR_SERVICE, outline="", width=0)

            # X label (show every few if many customers)
            if n <= 30 or i % max(1, n // 20) == 0:
                canvas.create_text(x_centre, pad_t + plot_h + 14,
                                   text=str(c["id"]), fill=TEXT_MUTED,
                                   font=(FONT_FAMILY, 7))

        # X-axis label
        canvas.create_text(pad_l + plot_w // 2, ch - 6, text="Customer ID",
                           fill=TEXT_SECONDARY, font=(FONT_FAMILY, 9))

        # Legend
        lx = cw - pad_r - 160
        ly = pad_t + 8
        canvas.create_rectangle(lx, ly, lx + 12, ly + 12, fill=BAR_WAIT, outline="")
        canvas.create_text(lx + 18, ly + 6, text="Wait Time", anchor="w",
                           fill=TEXT_PRIMARY, font=(FONT_FAMILY, 8))
        canvas.create_rectangle(lx + 100, ly, lx + 112, ly + 12,
                                fill=BAR_SERVICE, outline="")
        canvas.create_text(lx + 118, ly + 6, text="Time in System", anchor="w",
                           fill=TEXT_PRIMARY, font=(FONT_FAMILY, 8))

    # ── timeline: server busy/idle ──────────────────────────────────────────
    def _draw_timeline(self):
        canvas = self.timeline_canvas
        canvas.delete("all")
        canvas.update_idletasks()

        cw = canvas.winfo_width()
        ch = canvas.winfo_height()
        if cw < 50 or ch < 50 or not self.customers:
            return

        pad_l, pad_r, pad_t, pad_b = 60, 30, 50, 50
        plot_w = cw - pad_l - pad_r
        plot_h = ch - pad_t - pad_b

        total_time = self.customers[-1]["service_end"]
        if total_time == 0:
            return

        # Title
        canvas.create_text(cw // 2, 20, text="Server Timeline  (Green = Busy, Dark = Idle)",
                           fill=TEXT_SECONDARY, font=(FONT_FAMILY, 10, "bold"))

        # Draw timeline bar
        bar_h = min(60, plot_h * 0.35)
        bar_y = pad_t + plot_h * 0.15

        # Idle background
        canvas.create_rectangle(pad_l, bar_y, pad_l + plot_w, bar_y + bar_h,
                                fill=BG_INPUT, outline=BORDER_COLOR)

        # Busy segments
        for c in self.customers:
            x1 = pad_l + (c["service_start"] / total_time) * plot_w
            x2 = pad_l + (c["service_end"] / total_time) * plot_w
            canvas.create_rectangle(x1, bar_y, x2, bar_y + bar_h,
                                    fill=ACCENT_DIM, outline=ACCENT, width=1)

            # Customer ID label (if wide enough)
            if (x2 - x1) > 20:
                canvas.create_text((x1 + x2) / 2, bar_y + bar_h / 2,
                                   text=str(c["id"]), fill=TEXT_PRIMARY,
                                   font=(FONT_FAMILY, 8, "bold"))

        # Time axis
        num_ticks = min(10, max(4, len(self.customers)))
        for i in range(num_ticks + 1):
            x = pad_l + (i / num_ticks) * plot_w
            t = (i / num_ticks) * total_time
            canvas.create_line(x, bar_y + bar_h, x, bar_y + bar_h + 8,
                               fill=TEXT_MUTED)
            canvas.create_text(x, bar_y + bar_h + 18, text=f"{t:.1f}",
                               fill=TEXT_MUTED, font=(FONT_FAMILY, 8))

        canvas.create_text(pad_l + plot_w / 2, bar_y + bar_h + 36,
                           text="Time (minutes)", fill=TEXT_SECONDARY,
                           font=(FONT_FAMILY, 9))

        # Wait-time visualization below
        wait_y = bar_y + bar_h + 60
        if wait_y + 40 < ch:
            canvas.create_text(cw // 2, wait_y - 10,
                               text="Customer Wait Times",
                               fill=TEXT_SECONDARY, font=(FONT_FAMILY, 10, "bold"))

            max_wait = max(c["wait"] for c in self.customers)
            if max_wait > 0:
                dot_area_h = ch - wait_y - pad_b
                for c in self.customers:
                    cx = pad_l + (c["arrival"] / total_time) * plot_w
                    r = max(3, min(12, (c["wait"] / max_wait) * 12))
                    cy = wait_y + 10 + (c["wait"] / max_wait) * (dot_area_h - 20)
                    alpha_hex = hex(int(100 + (c["wait"] / max_wait) * 155))[2:]
                    canvas.create_oval(cx - r, cy - r, cx + r, cy + r,
                                       fill=BAR_WAIT, outline="", width=0)
                    if r > 6:
                        canvas.create_text(cx, cy, text=str(c["id"]),
                                           fill=TEXT_PRIMARY,
                                           font=(FONT_FAMILY, 7))
            else:
                canvas.create_text(cw // 2, wait_y + 20,
                                   text="No waiting occurred — server was never busy at arrival",
                                   fill=TEXT_MUTED, font=(FONT_FAMILY, 9))

    # ── reset defaults ──────────────────────────────────────────────────────
    def _reset_defaults(self):
        defaults = {
            "num_customers": "10",
            "arr_min": "0.5",
            "arr_max": "3.0",
            "srv_min": "1.0",
            "srv_max": "4.0",
        }
        for key, val in defaults.items():
            entry = self.entries[key]
            entry.delete(0, tk.END)
            entry.insert(0, val)

        # Clear results
        for key in self.stat_labels:
            self.stat_labels[key].config(text="—")
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.chart_canvas.delete("all")
        self.timeline_canvas.delete("all")
        self.customers = []
        self.stats = {}


# ── entry point ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = BankQueueGUI(root)

    # Redraw charts on window resize
    def on_resize(event):
        if app.customers:
            app.root.after(100, app._draw_chart)
            app.root.after(100, app._draw_timeline)

    root.bind("<Configure>", on_resize)
    root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import winsound

# -------------------- App Window --------------------
window = tk.Tk()
window.title("Timer")
window.geometry("520x520")
window.minsize(520, 520)

# -------------------- Theme / Style --------------------
BG = "#0B1220"
CARD = "#121B2E"
TEXT = "#E5E7EB"
MUTED = "#9CA3AF"
ACCENT = "#60A5FA"
SUCCESS = "#34D399"
DANGER = "#F87171"

window.configure(bg=BG)

style = ttk.Style()
style.theme_use("clam")

# Base
style.configure(".", background=BG, foreground=TEXT, font=("Segoe UI", 11))
style.configure("TFrame", background=BG)
style.configure("Card.TFrame", background=CARD)

style.configure("Title.TLabel", background=CARD, foreground=TEXT, font=("Segoe UI Semibold", 18))
style.configure("Sub.TLabel", background=CARD, foreground=MUTED, font=("Segoe UI", 10))
style.configure("Clock.TLabel", background=CARD, foreground=TEXT, font=("Consolas", 40, "bold"))
style.configure("Timer.TLabel", background=CARD, foreground=TEXT, font=("Consolas", 22, "bold"))

# Buttons
style.configure(
    "Primary.TButton",
    background=ACCENT,
    foreground="#0B1220",
    font=("Segoe UI Semibold", 11),
    padding=(14, 10),
    borderwidth=0,
)
style.map(
    "Primary.TButton",
    background=[("active", "#7CB7FF"), ("disabled", "#334155")],
    foreground=[("disabled", "#94A3B8")],
)

style.configure(
    "Success.TButton",
    background=SUCCESS,
    foreground="#04120C",
    font=("Segoe UI Semibold", 11),
    padding=(14, 10),
    borderwidth=0,
)
style.map("Success.TButton", background=[("active", "#5BE7BE")])

style.configure(
    "Danger.TButton",
    background=DANGER,
    foreground="#1F0A0A",
    font=("Segoe UI Semibold", 11),
    padding=(14, 10),
    borderwidth=0,
)
style.map("Danger.TButton", background=[("active", "#FF9A9A")])

style.configure(
    "Ghost.TButton",
    background=CARD,
    foreground=TEXT,
    font=("Segoe UI", 11),
    padding=(14, 10),
    borderwidth=1,
    relief="solid",
)
style.map("Ghost.TButton", background=[("active", "#1B2742")])

# Inputs
style.configure(
    "Modern.TSpinbox",
    fieldbackground="#0F172A",
    background="#0F172A",
    foreground=TEXT,
    bordercolor="#22304A",
    lightcolor="#22304A",
    darkcolor="#22304A",
    padding=(10, 8),
    arrowsize=14,
)
style.map(
    "Modern.TSpinbox",
    bordercolor=[("focus", ACCENT)],
    lightcolor=[("focus", ACCENT)],
    darkcolor=[("focus", ACCENT)],
)

pages = {}
timer_seconds = 0


def show_page(PageClass):
    name = PageClass.__name__
    if name not in pages:
        pages[name] = PageClass(window)
        pages[name].place(relx=0, rely=0, relwidth=1, relheight=1)
    pages[name].tkraise()


class Page1(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)

        outer = ttk.Frame(self, style="TFrame")
        outer.pack(fill="both", expand=True, padx=18, pady=18)

        card = ttk.Frame(outer, style="Card.TFrame")
        card.pack(fill="both", expand=True)

        header = ttk.Frame(card, style="Card.TFrame")
        header.pack(fill="x", padx=22, pady=(22, 8))

        ttk.Label(header, text="Clock", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Current time (local)", style="Sub.TLabel").pack(anchor="w", pady=(4, 0))

        body = ttk.Frame(card, style="Card.TFrame")
        body.pack(fill="both", expand=True, padx=22, pady=18)

        self.time_label = ttk.Label(body, style="Clock.TLabel")
        self.time_label.pack(pady=(24, 18))

        ttk.Button(
            body,
            text="Go to Timer",
            style="Primary.TButton",
            command=lambda: show_page(Page2),
        ).pack(pady=(10, 0))

        footer = ttk.Frame(card, style="Card.TFrame")
        footer.pack(fill="x", padx=22, pady=(0, 22))

        ttk.Label(
            footer,
            text="Tip: Press Start after setting the duration.",
            style="Sub.TLabel",
        ).pack(anchor="w")

        self.update_clock()

    def update_clock(self):
        self.time_label.config(text=datetime.now().strftime("%H:%M:%S"))
        self.after(1000, self.update_clock)


class Page2(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)

        outer = ttk.Frame(self, style="TFrame")
        outer.pack(fill="both", expand=True, padx=18, pady=18)

        card = ttk.Frame(outer, style="Card.TFrame")
        card.pack(fill="both", expand=True)

        header = ttk.Frame(card, style="Card.TFrame")
        header.pack(fill="x", padx=22, pady=(22, 8))

        ttk.Label(header, text="Timer", style="Title.TLabel").pack(anchor="w")
        ttk.Label(header, text="Set a duration and start the countdown.", style="Sub.TLabel").pack(anchor="w", pady=(4, 0))

        body = ttk.Frame(card, style="Card.TFrame")
        body.pack(fill="both", expand=True, padx=22, pady=18)

        inputs = ttk.Frame(body, style="Card.TFrame")
        inputs.pack(fill="x", pady=(6, 10))

        inputs.columnconfigure((0, 1, 2), weight=1, uniform="col")

        self.hour_spinbox = ttk.Spinbox(inputs, from_=0, to=24, justify="center", width=8, style="Modern.TSpinbox")
        self.minute_spinbox = ttk.Spinbox(inputs, from_=0, to=59, justify="center", width=8, style="Modern.TSpinbox")
        self.second_spinbox = ttk.Spinbox(inputs, from_=0, to=59, justify="center", width=8, style="Modern.TSpinbox")

        self.hour_spinbox.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.minute_spinbox.grid(row=0, column=1, sticky="ew", padx=8)
        self.second_spinbox.grid(row=0, column=2, sticky="ew", padx=(8, 0))

        ttk.Label(inputs, text="Hours", style="Sub.TLabel").grid(row=1, column=0, pady=(8, 0))
        ttk.Label(inputs, text="Minutes", style="Sub.TLabel").grid(row=1, column=1, pady=(8, 0))
        ttk.Label(inputs, text="Seconds", style="Sub.TLabel").grid(row=1, column=2, pady=(8, 0))

        self.timer_label = ttk.Label(body, style="Timer.TLabel")
        self.timer_label.pack(pady=(18, 10))

        buttons = ttk.Frame(body, style="Card.TFrame")
        buttons.pack(fill="x", pady=(10, 0))
        buttons.columnconfigure((0, 1, 2), weight=1, uniform="btn")

        self.pause_button = ttk.Button(buttons, text="Pause", style="Ghost.TButton", command=self.toggle_pause)
        self.start_button = ttk.Button(buttons, text="Start", style="Success.TButton", command=self.start_timer)
        self.reset_button = ttk.Button(buttons, text="Reset", style="Danger.TButton", command=self.reset_timer)

        self.pause_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.start_button.grid(row=0, column=1, sticky="ew", padx=8)
        self.reset_button.grid(row=0, column=2, sticky="ew", padx=(8, 0))

        self.pause_button.grid_remove()
        self.reset_button.grid_remove()

        footer = ttk.Frame(card, style="Card.TFrame")
        footer.pack(fill="x", padx=22, pady=(0, 22))

        ttk.Button(
            footer,
            text="Back to Clock",
            style="Primary.TButton",
            command=lambda: show_page(Page1),
        ).pack(fill="x")

        self.running = False

    def tick(self):
        global timer_seconds

        if not self.running:
            return

        if timer_seconds > 0:
            self.timer_label.config(text=str(timedelta(seconds=timer_seconds)))
            timer_seconds -= 1
            self.after(1000, self.tick)
        else:
            self.timer_label.config(text="Time's up!")
            winsound.Beep(2000, 750)
            self.running = False
            self.pause_button.config(text="Pause")

    def start_timer(self):
        global timer_seconds

        try:
            hours = int(self.hour_spinbox.get() or 0)
            minutes = int(self.minute_spinbox.get() or 0)
            seconds = int(self.second_spinbox.get() or 0)
        except ValueError:
            return messagebox.showerror("Error", "Please enter numbers only.")

        if hours == 0 and minutes == 0 and seconds == 0:
            return messagebox.showinfo("Warning", "Please set a duration before starting.")

        hours = max(0, min(hours, 24))
        minutes = max(0, min(minutes, 59))
        seconds = max(0, min(seconds, 59))

        timer_seconds = int(timedelta(hours=hours, minutes=minutes, seconds=seconds).total_seconds())

        self.running = True
        self.pause_button.grid()
        self.reset_button.grid()
        self.start_button.state(["disabled"])
        self.pause_button.config(text="Pause")

        self.tick()

    def toggle_pause(self):
        global timer_seconds

        if timer_seconds <= 1:
            return

        self.running = not self.running
        self.pause_button.config(text="Resume" if not self.running else "Pause")

        if self.running:
            self.tick()

    def reset_timer(self):
        global timer_seconds

        self.running = False
        timer_seconds = 0

        for sp in (self.hour_spinbox, self.minute_spinbox, self.second_spinbox):
            sp.delete(0, tk.END)

        self.pause_button.grid_remove()
        self.reset_button.grid_remove()
        self.timer_label.config(text="")
        self.start_button.state(["!disabled"])


show_page(Page1)
window.mainloop()

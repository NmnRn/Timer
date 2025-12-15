import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import winsound

window = tk.Tk()
window.title("Timer")
window.minsize(width=500, height=500)

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
        super().__init__(master)

        self.time_label = ttk.Label(self, font=("Arial", 30, "roman"))
        self.time_label.pack(pady=(30, 20))

        ttk.Button(self, text="Go to Timer", command=lambda: show_page(Page2), width=20).pack(pady=10)

        self.update_clock()

    def update_clock(self):
        self.time_label.config(text=f'⏱️ {datetime.now().strftime("%H:%M:%S")}')
        self.after(1000, self.update_clock)


class Page2(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        container = ttk.Frame(self, padding=20)
        container.grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        container.columnconfigure((0, 1, 2), weight=1, uniform="col")
        container.rowconfigure((0, 1, 2, 3, 4, 5), weight=0)
        container.rowconfigure(6, weight=1)

        ttk.Label(container, text="Set the Duration", font=("Arial", 16, "roman")).grid(
            row=0, column=0, columnspan=3, pady=(0, 15)
        )

        self.hour_spinbox = ttk.Spinbox(container, from_=0, to=24, justify="center", width=6)
        self.minute_spinbox = ttk.Spinbox(container, from_=0, to=59, justify="center", width=6)
        self.second_spinbox = ttk.Spinbox(container, from_=0, to=59, justify="center", width=6)

        self.hour_spinbox.grid(row=1, column=0, pady=(0, 6))
        self.minute_spinbox.grid(row=1, column=1, pady=(0, 6))
        self.second_spinbox.grid(row=1, column=2, pady=(0, 6))

        ttk.Label(container, text="Hours").grid(row=2, column=0, pady=(0, 15))
        ttk.Label(container, text="Minutes").grid(row=2, column=1, pady=(0, 15))
        ttk.Label(container, text="Seconds").grid(row=2, column=2, pady=(0, 15))

        self.timer_label = ttk.Label(container, font=("Arial", 18, "roman"))
        self.timer_label.grid(row=3, column=0, columnspan=3, pady=(0, 18))

        self.pause_button = ttk.Button(container, text="Pause", command=self.toggle_pause)
        self.start_button = ttk.Button(container, text="Start Timer", command=self.start_timer)
        self.reset_button = ttk.Button(container, text="Reset", command=self.reset_timer)

        self.pause_button.grid(row=4, column=0, pady=10, sticky="ew")
        self.start_button.grid(row=4, column=1, pady=10, sticky="ew")
        self.reset_button.grid(row=4, column=2, pady=10, sticky="ew")

        self.pause_button.grid_remove()
        self.reset_button.grid_remove()

        ttk.Button(container, text="Back to Clock", command=lambda: show_page(Page1)).grid(
            row=5, column=0, columnspan=3, pady=(10, 0), sticky="ew"
        )

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

    def start_timer(self):
        global timer_seconds

        self.running = True

        try:
            hours = int(self.hour_spinbox.get() or 0)
            minutes = int(self.minute_spinbox.get() or 0)
            seconds = int(self.second_spinbox.get() or 0)
        except ValueError:
            return messagebox.showerror(title="Error", message="Please enter numbers only.")

        if hours == 0 and minutes == 0 and seconds == 0:
            return messagebox.showinfo(title="Warning", message="Please set a duration before starting.")

        hours = max(0, min(hours, 24))
        minutes = max(0, min(minutes, 59))
        seconds = max(0, min(seconds, 59))

        timer_seconds = int(timedelta(hours=hours, minutes=minutes, seconds=seconds).total_seconds())

        self.pause_button.grid()
        self.reset_button.grid()
        self.start_button.config(state=tk.DISABLED)
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
        self.start_button.config(state=tk.NORMAL)


show_page(Page1)
window.mainloop()

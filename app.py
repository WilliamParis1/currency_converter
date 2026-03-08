import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import datetime
import os

from currency_converter import get_exchange_rate

CURRENCIES = [
    "USD - US Dollar",
    "EUR - Euro",
    "GBP - British Pound",
    "JPY - Japanese Yen",
    "KRW - Korean Won",
    "CNY - Chinese Yuan",
    "CAD - Canadian Dollar",
    "AUD - Australian Dollar",
    "CHF - Swiss Franc",
    "INR - Indian Rupee",
]

SOJU_PRICE_KRW = 2200
ASSETS = os.path.dirname(os.path.abspath(__file__))


def currency_code(selection: str) -> str:
    return selection.split(" - ")[0]


def update_soju_bottom():
    base = currency_code(from_var.get())
    if base == "KRW":
        soju_bottom_label.config(text="You need 2,200 KRW to buy one Strawberry Soju.")
        return
    rate = get_exchange_rate("KRW", base)
    if rate:
        cost = SOJU_PRICE_KRW * rate
        soju_bottom_label.config(
            text=f"You need {cost:,.2f} {base} to buy one Strawberry Soju."
        )
    else:
        soju_bottom_label.config(text="Could not calculate Strawberry Soju price.")


def convert():
    raw = amount_var.get().strip()
    if not raw:
        messagebox.showwarning("Missing input", "Please enter an amount.")
        return
    try:
        amount = float(raw)
    except ValueError:
        messagebox.showerror("Invalid input", "Amount must be a number.")
        return

    base = currency_code(from_var.get())
    target = currency_code(to_var.get())

    if base == target:
        result_label.config(text=f"{amount:,.2f} {base} = {amount:,.2f} {target}")
        rate_label.config(text="Exchange rate: 1.0000")
        update_soju_bottom()
        return

    rate = get_exchange_rate(base, target)
    if rate is None:
        messagebox.showerror(
            "Error", "Could not fetch exchange rate.\nCheck your internet connection."
        )
        return

    result = amount * rate
    result_label.config(text=f"{amount:,.2f} {base} = {result:,.2f} {target}")
    rate_label.config(text=f"Exchange rate: 1 {base} = {rate:.4f} {target}")
    update_soju_bottom()


def load_gif_frames(path, size):
    """Extract every frame from an animated GIF and resize it."""
    img = Image.open(path)
    frames = []
    try:
        while True:
            frames.append(ImageTk.PhotoImage(img.copy().resize(size, Image.LANCZOS)))
            img.seek(img.tell() + 1)
    except EOFError:
        pass
    return frames


def animate(label, frames, idx=0):
    label.config(image=frames[idx])
    label.after(80, animate, label, frames, (idx + 1) % len(frames))


# ── Window ────────────────────────────────────────────────────────────────────
WIN_W, WIN_H = 800, 580

root = tk.Tk()
root.title("Currency Converter")
root.resizable(False, False)
root.geometry(f"{WIN_W}x{WIN_H}")

# ── Canvas + background ───────────────────────────────────────────────────────
canvas = tk.Canvas(root, width=WIN_W, height=WIN_H, highlightthickness=0)
canvas.pack(fill="both", expand=True)

bg_path = os.path.join(ASSETS, "strawberrywallpaper.jpg")
if os.path.exists(bg_path):
    _bg = Image.open(bg_path).resize((WIN_W, WIN_H), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(_bg)
    canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# ── Styles ────────────────────────────────────────────────────────────────────
PANEL_BG  = "#fff0f3"
ACCENT    = "#c0003c"
BTN_BG    = "#e6004a"
BTN_FG    = "#ffffff"
MUTED     = "#888888"

FONT_TITLE  = ("Helvetica", 20, "bold")
FONT_BOLD   = ("Helvetica", 13, "bold")
FONT        = ("Helvetica", 12)
FONT_RESULT = ("Helvetica", 14, "bold")
FONT_SMALL  = ("Helvetica", 9)
FONT_SOJU   = ("Helvetica", 11, "italic")

# ── Left panel — form ─────────────────────────────────────────────────────────
panel = tk.Frame(canvas, bg=PANEL_BG, padx=22, pady=20, bd=0, relief="flat")
canvas.create_window(30, 30, anchor="nw", window=panel)

# Title
tk.Label(panel, text="Currency Converter", font=FONT_TITLE, bg=PANEL_BG, fg=ACCENT).grid(
    row=0, column=0, columnspan=2, pady=(0, 16)
)

# Amount label + entry
tk.Label(panel, text="Amount", font=FONT_BOLD, bg=PANEL_BG, anchor="w").grid(
    row=1, column=0, columnspan=2, sticky="w"
)
amount_var = tk.StringVar()
tk.Entry(
    panel, textvariable=amount_var, font=FONT, width=30, relief="solid", bd=1
).grid(row=2, column=0, columnspan=2, pady=(4, 2), ipady=6, sticky="ew")

# Asterisk / rate date
today_str = datetime.date.today().strftime("%B %d, %Y")
tk.Label(
    panel,
    text=f"* Conversion rates as of {today_str}",
    font=FONT_SMALL,
    bg=PANEL_BG,
    fg=MUTED,
    anchor="w",
).grid(row=3, column=0, columnspan=2, sticky="w", pady=(0, 14))

# From / To dropdowns
tk.Label(panel, text="From", font=FONT_BOLD, bg=PANEL_BG).grid(
    row=4, column=0, sticky="w", padx=(0, 8)
)
tk.Label(panel, text="To", font=FONT_BOLD, bg=PANEL_BG).grid(row=4, column=1, sticky="w")

from_var = tk.StringVar(value=CURRENCIES[0])
to_var   = tk.StringVar(value=CURRENCIES[1])

ttk.Combobox(
    panel, textvariable=from_var, values=CURRENCIES, state="readonly", font=FONT, width=21
).grid(row=5, column=0, pady=(4, 16), padx=(0, 8), ipady=4)

ttk.Combobox(
    panel, textvariable=to_var, values=CURRENCIES, state="readonly", font=FONT, width=21
).grid(row=5, column=1, pady=(4, 16), ipady=4)

# Convert button
tk.Button(
    panel,
    text="Convert",
    command=convert,
    bg=BTN_BG, fg=BTN_FG,
    font=FONT_BOLD,
    relief="flat",
    cursor="hand2",
    padx=20, pady=8,
    activebackground="#99002e",
    activeforeground=BTN_FG,
).grid(row=6, column=0, columnspan=2, pady=(0, 16), sticky="ew")

# Result + rate labels
result_label = tk.Label(panel, text="", font=FONT_RESULT, bg=PANEL_BG, fg=ACCENT)
result_label.grid(row=7, column=0, columnspan=2)

rate_label = tk.Label(panel, text="", font=FONT_SMALL, bg=PANEL_BG, fg=MUTED)
rate_label.grid(row=8, column=0, columnspan=2, pady=(4, 0))

# ── Right panel — soju GIF ────────────────────────────────────────────────────
soju_panel = tk.Frame(canvas, bg=PANEL_BG, padx=14, pady=14, bd=0)
canvas.create_window(WIN_W - 30, 60, anchor="ne", window=soju_panel)

gif_path = os.path.join(ASSETS, "cutesoju.gif")
if os.path.exists(gif_path):
    gif_frames = load_gif_frames(gif_path, (140, 200))
    gif_label  = tk.Label(soju_panel, bg=PANEL_BG)
    gif_label.pack()
    animate(gif_label, gif_frames)
else:
    tk.Label(
        soju_panel,
        text="[soju gif\nhere]",
        font=FONT_SMALL,
        bg=PANEL_BG,
        fg=MUTED,
        width=12,
        height=10,
        relief="solid",
        bd=1,
    ).pack()

tk.Label(soju_panel, text="2,200 KRW", font=FONT_BOLD, bg=PANEL_BG, fg=ACCENT).pack(
    pady=(8, 0)
)

# ── Bottom — Strawberry Soju price message ────────────────────────────────────
bottom_panel = tk.Frame(canvas, bg=PANEL_BG, padx=18, pady=10, bd=0)
canvas.create_window(WIN_W // 2, WIN_H - 16, anchor="s", window=bottom_panel)

soju_bottom_label = tk.Label(
    bottom_panel,
    text="Select currencies above and convert to see the Strawberry Soju price.",
    font=FONT_SOJU,
    bg=PANEL_BG,
    fg=ACCENT,
)
soju_bottom_label.pack()

# Populate soju bottom on startup
update_soju_bottom()

root.mainloop()

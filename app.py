import tkinter as tk
from tkinter import ttk, messagebox
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

def currency_code(selection: str) -> str:
    return selection.split(" - ")[0]


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
        return

    rate = get_exchange_rate(base, target)
    if rate is None:
        messagebox.showerror("Error", "Could not fetch exchange rate.\nCheck your internet connection.")
        return

    result = amount * rate
    result_label.config(text=f"{amount:,.2f} {base} = {result:,.2f} {target}")
    rate_label.config(text=f"Exchange rate: 1 {base} = {rate:.4f} {target}")


# ── Window ────────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Currency Converter")
root.resizable(False, False)

BG = "#f0f4f8"
ACCENT = "#2d6a4f"
BTN_FG = "#ffffff"
FONT = ("Helvetica", 12)
FONT_BOLD = ("Helvetica", 13, "bold")
FONT_TITLE = ("Helvetica", 20, "bold")
FONT_RESULT = ("Helvetica", 15, "bold")

root.configure(bg=BG)

frame = tk.Frame(root, bg=BG, padx=30, pady=24)
frame.pack()

# Title
tk.Label(frame, text="Currency Converter", font=FONT_TITLE, bg=BG, fg=ACCENT).grid(
    row=0, column=0, columnspan=2, pady=(0, 20)
)

# Amount
tk.Label(frame, text="Amount", font=FONT_BOLD, bg=BG, anchor="w").grid(
    row=1, column=0, columnspan=2, sticky="w"
)
amount_var = tk.StringVar()
amount_entry = tk.Entry(frame, textvariable=amount_var, font=FONT, width=30, relief="solid", bd=1)
amount_entry.grid(row=2, column=0, columnspan=2, pady=(4, 16), ipady=6, sticky="ew")

# From
tk.Label(frame, text="From", font=FONT_BOLD, bg=BG, anchor="w").grid(
    row=3, column=0, sticky="w", padx=(0, 8)
)
tk.Label(frame, text="To", font=FONT_BOLD, bg=BG, anchor="w").grid(
    row=3, column=1, sticky="w"
)

from_var = tk.StringVar(value=CURRENCIES[0])
to_var = tk.StringVar(value=CURRENCIES[1])

from_menu = ttk.Combobox(frame, textvariable=from_var, values=CURRENCIES,
                         state="readonly", font=FONT, width=22)
from_menu.grid(row=4, column=0, pady=(4, 20), padx=(0, 8), ipady=4)

to_menu = ttk.Combobox(frame, textvariable=to_var, values=CURRENCIES,
                       state="readonly", font=FONT, width=22)
to_menu.grid(row=4, column=1, pady=(4, 20), ipady=4)

# Convert button
tk.Button(
    frame, text="Convert", command=convert,
    bg=ACCENT, fg=BTN_FG, font=FONT_BOLD,
    relief="flat", cursor="hand2", padx=20, pady=8,
    activebackground="#1b4332", activeforeground=BTN_FG,
).grid(row=5, column=0, columnspan=2, pady=(0, 20), sticky="ew")

# Result
result_label = tk.Label(frame, text="", font=FONT_RESULT, bg=BG, fg=ACCENT)
result_label.grid(row=6, column=0, columnspan=2)

rate_label = tk.Label(frame, text="", font=("Helvetica", 10), bg=BG, fg="#6b7280")
rate_label.grid(row=7, column=0, columnspan=2, pady=(4, 0))

root.mainloop()

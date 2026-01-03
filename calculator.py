import tkinter as tk

current_expression = ""

def on_button_click(text):
    global current_expression
    if text == "C":
        current_expression = ""
        entry.delete(0, tk.END)
    elif text == "=":
        try:
            result = str(eval(current_expression))
            entry.delete(0, tk.END)
            entry.insert(tk.END, result)
            current_expression = result
        except Exception as e:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")
            current_expression = ""
    else:
        current_expression += text
        entry.delete(0, tk.END)
        entry.insert(tk.END, current_expression)

def set_theme(theme_name):
    def hex_to_rgb(h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(rgb):
        return '#{:02X}{:02X}{:02X}'.format(*rgb)

    def adjust_color(hex_color, amount):
        r, g, b = hex_to_rgb(hex_color)
        def clamp(x):
            return max(0, min(255, x))
        return rgb_to_hex((clamp(r + amount), clamp(g + amount), clamp(b + amount)))

    themes = {
        "Светлая": {"bg": "#FFFFFF", "fg": "#000000", "button_bg": "#F0F0F0", "button_fg": "#000000"},
        "Темная": {"bg": "#333333", "fg": "#FFFFFF", "button_bg": "#555555", "button_fg": "#FFFFFF"},
        "Синяя": {"bg": "#E0F7FA", "fg": "#01579B", "button_bg": "#B3E5FC", "button_fg": "#01579B"},
        "Зеленая": {"bg": "#E8F5E8", "fg": "#2E7D32", "button_bg": "#C8E6C9", "button_fg": "#2E7D32"},
        "Красная": {"bg": "#FFEBEE", "fg": "#B71C1C", "button_bg": "#FFCDD2", "button_fg": "#B71C1C"}
    }
    theme = themes.get(theme_name, themes["Светлая"])

    r, g, b = hex_to_rgb(theme["button_bg"])
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    delta = -25 if brightness > 128 else 25
    frame_bg = adjust_color(theme["button_bg"], delta)

    root.config(bg=theme["bg"])
    entry.config(bg=theme["bg"], fg=theme["fg"])
    frame.config(bg=frame_bg)
    for button in buttons:
        button.config(bg=theme["button_bg"], fg=theme["button_fg"],
                      activebackground=adjust_color(theme["button_bg"], -10 if brightness <=128 else 10))

root = tk.Tk()
root.title("Калькулятор")
root.geometry("300x300")
root.resizable(0, 0)

entry = tk.Entry(root, font=("Arial", 24), justify='right')
entry.pack(fill=tk.X, padx=10, pady=10)

button_texts = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", "C", "=", "+"
]

buttons = []
frame = tk.Frame(root)
frame.pack()

for i, text in enumerate(button_texts):
    button = tk.Button(frame, text=text, font=("Arial", 30), command=lambda t=text: on_button_click(t))
    button.grid(row=i//4, column=i%4, sticky="nsew", padx=5, pady=5)
    buttons.append(button)

for i in range(4):
    frame.grid_columnconfigure(i, weight=1)
for i in range(4):
    frame.grid_rowconfigure(i, weight=1)

menubar = tk.Menu(root)
settings_menu = tk.Menu(menubar, tearoff=0)
settings_menu.add_command(label="Светлая", command=lambda: set_theme("Светлая"))
settings_menu.add_command(label="Темная", command=lambda: set_theme("Темная"))
settings_menu.add_command(label="Синяя", command=lambda: set_theme("Синяя"))
settings_menu.add_command(label="Зеленая", command=lambda: set_theme("Зеленая"))
settings_menu.add_command(label="Красная", command=lambda: set_theme("Красная"))
menubar.add_cascade(label="Настройки", menu=settings_menu)
root.config(menu=menubar)

set_theme("Светлая")

root.mainloop()
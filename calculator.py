import tkinter as tk
from tkinter import ttk
import math
from typing import List, Optional
import json
from datetime import datetime

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Calculator")
        self.root.geometry("400x600")
        self.root.configure(bg="#2D2D2D")

        # Variables
        self.current = ""
        self.memory = 0
        self.history: List[str] = []
        self.is_dark_mode = True
        
        # Colors
        self.dark_theme = {
            "bg": "#2D2D2D",
            "fg": "#FFFFFF",
            "button": "#404040",
            "button_fg": "#FFFFFF",
            "operator": "#FF9500",
            "equals": "#FF9500"
        }
        
        self.light_theme = {
            "bg": "#F0F0F0",
            "fg": "#000000",
            "button": "#E0E0E0",
            "button_fg": "#000000",
            "operator": "#FF9500",
            "equals": "#FF9500"
        }

        self.setup_ui()
        self.load_history()
        self.bind_keys()

    def setup_ui(self):
        # Display Frame
        display_frame = tk.Frame(self.root, bg=self.dark_theme["bg"])
        display_frame.pack(expand=True, fill="both", padx=10, pady=5)

        # History Display
        self.history_display = tk.Text(
            display_frame,
            height=2,
            bg=self.dark_theme["bg"],
            fg=self.dark_theme["fg"],
            font=("Arial", 12),
            bd=0
        )
        self.history_display.pack(expand=True, fill="both")

        # Main Display
        self.display = tk.Entry(
            display_frame,
            font=("Arial", 24),
            justify="right",
            bg=self.dark_theme["bg"],
            fg=self.dark_theme["fg"],
            bd=0
        )
        self.display.pack(expand=True, fill="both", pady=10)

        # Buttons Frame
        buttons_frame = tk.Frame(self.root, bg=self.dark_theme["bg"])
        buttons_frame.pack(expand=True, fill="both", padx=10, pady=5)

        # Button layout
        buttons = [
            ('MC', 'MR', 'M+', 'M-', 'C'),
            ('sin', 'cos', 'tan', '√', '^'),
            ('7', '8', '9', '÷', 'DEL'),
            ('4', '5', '6', '×', '('),
            ('1', '2', '3', '-', ')'),
            ('0', '.', '=', '+', '±')
        ]

        # Create buttons
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    font=("Arial", 16),
                    bd=0,
                    relief="ridge",
                    bg=self.dark_theme["button"],
                    fg=self.dark_theme["button_fg"],
                    activebackground=self.dark_theme["operator"]
                )
                btn.grid(row=i, column=j, padx=2, pady=2, sticky="nsew")
                btn.bind('<Button-1>', self.button_click)

                # Configure grid weights
                buttons_frame.grid_columnconfigure(j, weight=1)
            buttons_frame.grid_rowconfigure(i, weight=1)

        # Theme toggle button
        self.theme_btn = tk.Button(
            self.root,
            text="🌙",
            font=("Arial", 16),
            command=self.toggle_theme,
            bg=self.dark_theme["button"],
            fg=self.dark_theme["button_fg"],
            bd=0
        )
        self.theme_btn.pack(pady=5)

    def button_click(self, event):
        button = event.widget
        text = button["text"]

        if text == "=":
            try:
                result = eval(self.current.replace('×', '*').replace('÷', '/'))
                self.history.append(f"{self.current} = {result}")
                self.current = str(result)
                self.update_display()
                self.save_history()
            except:
                self.current = "Error"
                self.update_display()
        elif text == "C":
            self.current = ""
            self.update_display()
        elif text == "DEL":
            self.current = self.current[:-1]
            self.update_display()
        elif text == "±":
            try:
                if self.current and float(self.current):
                    if self.current[0] == '-':
                        self.current = self.current[1:]
                    else:
                        self.current = '-' + self.current
                    self.update_display()
            except ValueError:
                pass
        elif text in ["sin", "cos", "tan"]:
            try:
                num = float(self.current)
                if text == "sin":
                    result = math.sin(math.radians(num))
                elif text == "cos":
                    result = math.cos(math.radians(num))
                else:
                    result = math.tan(math.radians(num))
                self.current = str(result)
                self.update_display()
            except:
                self.current = "Error"
                self.update_display()
        elif text == "√":
            try:
                self.current = str(math.sqrt(float(self.current)))
                self.update_display()
            except:
                self.current = "Error"
                self.update_display()
        elif text == "MC":
            self.memory = 0
        elif text == "MR":
            self.current = str(self.memory)
            self.update_display()
        elif text == "M+":
            try:
                self.memory += float(self.current)
            except:
                pass
        elif text == "M-":
            try:
                self.memory -= float(self.current)
            except:
                pass
        else:
            self.current += text
            self.update_display()

    def update_display(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, self.current)
        
        # Update history display
        self.history_display.delete(1.0, tk.END)
        recent_history = self.history[-2:] if len(self.history) > 1 else self.history
        self.history_display.insert(1.0, "\n".join(recent_history))

    def bind_keys(self):
        self.root.bind('<Return>', lambda e: self.button_click(tk.Event(widget=self.find_button("="))))
        self.root.bind('<BackSpace>', lambda e: self.button_click(tk.Event(widget=self.find_button("DEL"))))
        self.root.bind('<Escape>', lambda e: self.button_click(tk.Event(widget=self.find_button("C"))))
        
        for key in "0123456789.+-*/()":
            self.root.bind(key, lambda e, k=key: self.button_click(tk.Event(widget=self.find_button(k))))

    def find_button(self, text: str) -> Optional[tk.Button]:
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button) and widget["text"] == text:
                return widget
        return None

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        theme = self.dark_theme if self.is_dark_mode else self.light_theme
        
        self.root.configure(bg=theme["bg"])
        self.theme_btn.configure(
            text="🌙" if self.is_dark_mode else "☀️",
            bg=theme["button"],
            fg=theme["button_fg"]
        )
        
        # Update all widgets with new theme
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Button, tk.Entry, tk.Text)):
                widget.configure(bg=theme["bg"], fg=theme["fg"])

    def save_history(self):
        with open("calc_history.json", "w") as f:
            json.dump(self.history[-100:], f)  # Keep last 100 calculations

    def load_history(self):
        try:
            with open("calc_history.json", "r") as f:
                self.history = json.load(f)
        except:
            self.history = []

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()
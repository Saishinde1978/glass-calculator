import tkinter as tk
import ast
import operator
import re

# Glassmorphism + macOS-inspired calculator
# Built with Python's standard Tkinter library.

BG = "#111318"
GLASS = "#1c2028"
DISPLAY = "#171a21"
TEXT = "#f5f6f7"
MUTED = "#9ba3b0"
ACCENT = "#f0a45d"       # warm macOS-inspired operator accent
KEY = "#30343d"
KEY_HOVER = "#414752"
OPERATOR = "#e99a4d"
OPERATOR_HOVER = "#f3b16f"
SPECIAL = "#454a55"
SPECIAL_HOVER = "#5a606d"
BORDER = "#3a404b"

_ALLOWED = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def safe_calculate(expression):
    """Safely evaluate a basic arithmetic expression without eval()."""
    expression = expression.replace("×", "*").replace("÷", "/").replace("−", "-")
    tree = ast.parse(expression, mode="eval")

    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED:
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 8:
                raise ValueError("Exponent too large")
            result = _ALLOWED[type(node.op)](left, right)
            if isinstance(result, complex) or abs(result) > 1e100:
                raise ValueError("Result too large")
            return result
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED:
            return _ALLOWED[type(node.op)](visit(node.operand))
        raise ValueError("Invalid expression")

    return visit(tree)


class GlassCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Glass • Calculator")
        self.root.geometry("390x610")
        self.root.minsize(330, 520)
        self.root.configure(bg=BG)

        self.expression = ""
        self.just_calculated = False
        self.error_shown = False

        # Outer glass card
        shell = tk.Frame(
            root, bg=GLASS, padx=18, pady=18,
            highlightbackground=BORDER, highlightthickness=1
        )
        shell.pack(fill="both", expand=True, padx=14, pady=14)

        # macOS-style traffic lights
        top = tk.Frame(shell, bg=GLASS)
        top.pack(fill="x", pady=(0, 20))
        for color in ("#ff5f57", "#febc2e", "#28c840"):
            dot = tk.Canvas(top, width=12, height=12, bg=GLASS,
                            highlightthickness=0, bd=0)
            dot.create_oval(1, 1, 11, 11, fill=color, outline=color)
            dot.pack(side="left", padx=(0, 7))
        tk.Label(
            top, text="GLASS CALCULATOR", bg=GLASS, fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(side="right")

        # Display panel
        display = tk.Frame(
            shell, bg=DISPLAY, padx=14, pady=18,
            highlightbackground=BORDER, highlightthickness=1
        )
        display.pack(fill="x", pady=(0, 18))

        self.expression_label = tk.Label(
            display, text="Ready", bg=DISPLAY, fg=MUTED,
            anchor="e", font=("Segoe UI", 10)
        )
        self.expression_label.pack(fill="x")

        self.display_var = tk.StringVar(value="0")
        self.result_label = tk.Label(
            display, textvariable=self.display_var, bg=DISPLAY,
            fg=TEXT, anchor="e", font=("Segoe UI", 30, "normal")
        )
        self.result_label.pack(fill="x", pady=(7, 0))

        # macOS-like button layout
        rows = [
            [("AC", "special"), ("±", "special"), ("%", "special"), ("÷", "operator")],
            [("7", "number"), ("8", "number"), ("9", "number"), ("×", "operator")],
            [("4", "number"), ("5", "number"), ("6", "number"), ("−", "operator")],
            [("1", "number"), ("2", "number"), ("3", "number"), ("+", "operator")],
            [("⌫", "special"), ("0", "number"), (".", "number"), ("=", "equals")],
        ]

        grid = tk.Frame(shell, bg=GLASS)
        grid.pack(fill="both", expand=True)

        for r, row in enumerate(rows):
            grid.rowconfigure(r, weight=1, uniform="row")
            for c, (label, kind) in enumerate(row):
                grid.columnconfigure(c, weight=1, uniform="col")
                if kind == "operator":
                    normal, hover, foreground = OPERATOR, OPERATOR_HOVER, "#151515"
                elif kind == "equals":
                    normal, hover, foreground = ACCENT, OPERATOR_HOVER, "#151515"
                elif kind == "special":
                    normal, hover, foreground = SPECIAL, SPECIAL_HOVER, TEXT
                else:
                    normal, hover, foreground = KEY, KEY_HOVER, TEXT

                btn = tk.Button(
                    grid, text=label,
                    command=lambda value=label: self.press(value),
                    bg=normal, fg=foreground,
                    activebackground=hover, activeforeground=foreground,
                    relief="flat", bd=0, highlightthickness=0,
                    font=("Segoe UI", 16, "normal"),
                    cursor="hand2"
                )
                btn.grid(row=r, column=c, sticky="nsew",
                         padx=4, pady=4, ipadx=2, ipady=8)
                btn.bind("<Enter>", lambda event, b=btn, col=hover: b.configure(bg=col))
                btn.bind("<Leave>", lambda event, b=btn, col=normal: b.configure(bg=col))

        tk.Label(
            shell, text="GLASSMORPHISM  •  PYTHON + TKINTER",
            bg=GLASS, fg="#737d8c", font=("Segoe UI", 8)
        ).pack(pady=(13, 0))

        self.root.bind("<Key>", self.on_key)

    def update_display(self):
        self.display_var.set(self.expression if self.expression else "0")
        if not self.expression:
            self.expression_label.config(text="Ready")

    def press(self, key):
        if key == "AC":
            self.expression = ""
            self.just_calculated = False
            self.error_shown = False
            self.update_display()
            return

        if key == "⌫":
            if self.just_calculated or self.error_shown:
                self.expression = ""
            else:
                self.expression = self.expression[:-1]
            self.just_calculated = False
            self.error_shown = False
            self.update_display()
            return

        if key == "=":
            self.calculate()
            return

        if key == "±":
            if not self.expression:
                return
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            else:
                self.expression = "-" + self.expression
            self.just_calculated = False
            self.update_display()
            return

        if self.just_calculated and (key.isdigit() or key == "."):
            self.expression = ""
        self.just_calculated = False
        self.error_shown = False

        mapped = {"÷": "/", "×": "*", "−": "-"}
        value = mapped.get(key, key)

        # Avoid duplicate decimal points in the current number.
        if key == ".":
            current = re.split(r"[+\-*/%]", self.expression)[-1]
            if "." in current:
                return

        # Replace the last operator if another operator is pressed.
        if value in "+-*/%" and self.expression and self.expression[-1] in "+-*/%":
            self.expression = self.expression[:-1]

        self.expression += value
        self.update_display()

    def calculate(self):
        if not self.expression:
            return
        try:
            result = safe_calculate(self.expression)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            result_text = format(result, ".10g") if isinstance(result, float) else str(result)
            self.expression_label.config(text=f"{self.expression.replace('*', '×').replace('/', '÷')} =")
            self.expression = result_text
            self.display_var.set(result_text)
            self.just_calculated = True
            self.error_shown = False
        except ZeroDivisionError:
            self.display_var.set("Cannot divide by zero")
            self.expression_label.config(text="Math error")
            self.expression = ""
            self.just_calculated = False
            self.error_shown = True
        except (SyntaxError, ValueError, TypeError, OverflowError):
            self.display_var.set("Invalid expression")
            self.expression_label.config(text="Check your input")
            self.expression = ""
            self.just_calculated = False
            self.error_shown = True

    def on_key(self, event):
        key_map = {
            "Return": "=", "KP_Enter": "=", "BackSpace": "⌫",
            "Escape": "AC", "asterisk": "×", "slash": "÷",
            "plus": "+", "minus": "−", "percent": "%"
        }
        if event.keysym in key_map:
            self.press(key_map[event.keysym])
        elif event.char.isdigit() or event.char == ".":
            self.press(event.char)
        elif event.char in "+-*/%":
            self.press({"*": "×", "/": "÷", "-": "−"}.get(event.char, event.char))


if __name__ == "__main__":
    root = tk.Tk()
    GlassCalculator(root)
    root.mainloop()

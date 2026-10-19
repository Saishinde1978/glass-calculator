# Glass Calculator 🧊

A desktop calculator that combines a **glassmorphism-inspired dark interface** with the clean, rounded-button layout of the macOS Calculator.

## Features

- Addition, subtraction, multiplication, and division
- Modulo (`%`)
- Clear (`AC`), backspace (`⌫`), and sign toggle (`±`)
- Keyboard shortcuts
- Hover feedback on buttons
- Handles invalid expressions and division by zero
- Safe arithmetic parser (does not use Python's `eval()`)
- Built with Python's standard Tkinter library — no third-party packages

## Preview

Run the app locally and add a screenshot here, for example:

```markdown
![Glass Calculator screenshot](screenshots/calculator.png)
```

## Requirements

- Python 3.10 or newer recommended
- Tkinter (usually included with Python on Windows)

## Run locally

```bash
python main.py
```

If your system uses `python3`, run:

```bash
python3 main.py
```

## Keyboard shortcuts

- `0`–`9` and `.` — enter numbers
- `+`, `-`, `*`, `/`, `%` — arithmetic operations
- `Enter` — calculate
- `Backspace` — delete the last character
- `Esc` — clear

## Project structure

```text
glass-calculator/
├── main.py
├── README.md
├── .gitignore
└── LICENSE
```

## Built with

- Python
- Tkinter
- AST-based restricted arithmetic evaluation

## License

MIT
#Contributor1 Learning Git branches and GitHub collaboration.
# Game of Life — Conway

This project is a **Python implementation of Conway's Game of Life** with a **Tkinter graphical interface**.

The program allows users to create, edit, and observe the evolution of a population of cells on a grid according to the classic rules of the Game of Life.

---

## Concept

The **Game of Life** is a cellular automaton created by mathematician **John Conway** in 1970.

Each cell in a grid can be in one of two states:

- alive
- dead

At each generation, the state of the grid evolves according to the following rules:

1. A living cell with fewer than **2 live neighbors** dies (underpopulation).
2. A living cell with **2 or 3 live neighbors** survives.
3. A living cell with more than **3 live neighbors** dies (overpopulation).
4. A dead cell with exactly **3 live neighbors** becomes alive (reproduction).

These simple rules can produce complex and emergent behaviors.

---

## Features

- **Tkinter graphical interface**
- Grid generation:
  - random
  - empty
  - full
- Edit cells by clicking on them
- **Step-by-step** or **automatic** simulation
- Save and load grid templates from the `templates` directory

---

## Installation

### Requirements

- Any version of Python 3 **(Python 3.10 recommended)**

Dependencies are defined in `pyproject.toml`.

### Install with uv (recommended)

If you use **uv**, install the dependencies with:

```bash
uv sync
```

### Install with pip

```bash
python -m venv .venv
source .venv/bin/activate (on Linux) / .venv\Scripts\activate (on Windows)
pip install -e .
python main.py
```


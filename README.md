# Adventure of Prince

A 2D side-scrolling platformer built with Python and Tkinter. Guide the prince
across three hand-crafted levels — collect coins and water for points, dodge
fire, bombs, and monsters, and reach the queen to win.

## Gameplay

- **Move:** `←` / `→` arrow keys
- **Jump:** `Space`
- **Collect** coins and water to raise your score.
- **Avoid** fire (loses points), bombs, and monsters (instant game over).
- Each level's exit **door** requires a score above 20 to pass through.
- Reach the **queen** in level 3 to win.

## Requirements

- **Python 3.8+**
- **Tkinter** — bundled with most Python installs (see notes below)
- **Pillow** — image loading
- **pygame** — sound playback

## Setup

### 1. Clone / open the project

```bash
cd Game-tkiner-jum
```

### 2. (Recommended) Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install pillow pygame
```

### 4. Make sure Tkinter is available

Tkinter ships with Python but is a separate system package on some Linux
distros:

```bash
# Debian / Ubuntu
sudo apt install python3-tk

# Fedora
sudo dnf install python3-tkinter

# macOS (Homebrew) / Windows
# Included with the official Python installer — nothing to install.
```

Verify:

```bash
python3 -c "import tkinter; print('tkinter OK')"
```

## Run

Run from the **project root** so the `image/` and `sound/` asset paths resolve
correctly:

```bash
python3 AdvantureOfPrince.py
```

## Project structure

```
Game-tkiner-jum/
├── AdvantureOfPrince.py   # Game source (single file)
├── image/                 # PNG sprites and backgrounds
├── sound/                 # MP3 sound effects and music
└── README.md
```

## Troubleshooting

- **`ModuleNotFoundError: No module named 'tkinter'`** — install the system
  Tkinter package for your OS (see step 4).
- **`No module named 'PIL'`** — run `pip install pillow` (the import name is
  `PIL`, the package name is `pillow`).
- **`pygame.error` / no sound** — ensure `pygame` is installed and your system
  has a working audio device. On headless machines audio may be unavailable.
- **`_tkinter.TclError: couldn't open "image/..."`** — you launched the game
  from the wrong directory. Run it from the project root.

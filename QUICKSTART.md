# Quick Start Guide

## 🚀 One-Command Setup

### macOS/Linux
```bash
./setup.sh
```

### Windows
```powershell
.\setup.ps1
```

That's it! The script handles everything automatically.

---

## 📋 Manual Setup (3 Steps)

### 1. Install uv (if not installed)

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Setup Environment

```bash
uv venv                          # Create virtual environment
source .venv/bin/activate        # Activate (macOS/Linux)
# or
.venv\Scripts\activate           # Activate (Windows)
```

### 3. Install & Run

```bash
uv pip install -r requirements.txt    # Install dependencies
python main.py                        # Start the game!
```

---

## 🎮 Playing the Game

```bash
python main.py
```

Follow the prompts to:
1. Choose your class (Warrior, Mage, Paladin, Shaman, Monk, Priest)
2. Choose your role (Tank or Damage)
3. Battle against an AI opponent!

---

## 🧪 Running Tests

```bash
pytest              # Run all 79 tests
pytest -v           # Verbose output
pytest --cov=.      # With coverage
```

---

## 🔧 Development Commands

```bash
# Linting
ruff check .                    # Check code quality
ruff check . --fix              # Auto-fix issues

# Testing
pytest Tests/test_spell_contracts.py    # Run specific test file
pytest -k "test_fireball"               # Run tests matching pattern

# Code formatting
ruff format .                   # Format all Python files
```

---

## 📚 Available Classes & Roles

| Class   | Roles                    | Resource      |
|---------|--------------------------|---------------|
| Warrior | Tank, Damage (Fury)      | Rage          |
| Paladin | Tank, Damage (Retribution) | Holy Power  |
| Mage    | Damage (Fire)            | Mana          |
| Priest  | Damage (Shadow)          | Mana/Insanity |
| Monk    | Tank, Damage (Windwalker)| Chi/Energy    |
| Shaman  | Damage (Enhancement)     | Mana/Maelstrom|

---

## 🆘 Troubleshooting

**"uv: command not found"**
- Restart your terminal after installing uv
- Or manually add `~/.cargo/bin` to your PATH

**"Python version not found"**
- Install Python 3.10 or higher from [python.org](https://www.python.org/downloads/)

**Tests failing**
- Make sure you're in the project root directory
- Activate the virtual environment first

**Import errors**
- Run: `uv pip install -r requirements.txt`

---

## 📖 More Information

- **Full Installation Guide:** [INSTALL.md](INSTALL.md)
- **Project Status:** [PROGRESS.md](PROGRESS.md)
- **Project Overview:** [README.md](README.md)

---

**Need help?** Open an issue on GitHub!

**Ready to play?** Run `python main.py` and enjoy! ⚔️🔥🛡️

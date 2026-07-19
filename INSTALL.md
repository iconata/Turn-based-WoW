# Installation Guide

This guide will help you install and run the Turn-based WoW game using `uv`, a fast Python package installer and resolver.

## Prerequisites

- Python 3.10 or higher
- `uv` package manager (we'll install this first)

## Quick Start (Recommended)

### 1. Install uv

`uv` is a fast Python package installer written in Rust. Install it using one of these methods:

**macOS and Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Using pip (if you already have Python):**
```bash
pip install uv
```

**Using Homebrew (macOS):**
```bash
brew install uv
```

After installation, verify it works:
```bash
uv --version
```

### 2. Clone the Repository

```bash
git clone https://github.com/yourusername/Turn-based-WoW.git
cd Turn-based-WoW
```

### 3. Create a Virtual Environment and Install Dependencies

Using `uv`, this is incredibly fast:

```bash
# Create a virtual environment with Python 3.11 (or 3.10, 3.12)
uv venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# Install the project with development dependencies
uv pip install -e ".[dev]"
```

**Alternative:** If you just want to install dependencies without installing the project as a package:
```bash
uv pip install -r requirements.txt
```

### 4. Verify Installation

Run the test suite to make sure everything is working:

```bash
pytest
```

You should see:
```
============================== 79 passed in 0.XX s ==============================
```

### 5. Run the Game

```bash
python main.py
```

Or if you installed the project as a package:
```bash
turn-based-wow
```

## Alternative Installation Methods

### Using Standard pip (without uv)

If you prefer not to use `uv`, you can use standard Python tools:

```bash
# Create virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

### Development Installation

For development work with all tools:

```bash
# Using uv (recommended)
uv pip install -e ".[dev]"

# Or using pip
pip install -r requirements-dev.txt
```

This installs:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `ruff` - Fast Python linter

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=. --cov-report=term-missing

# Run specific test file
pytest Tests/test_spell_contracts.py

# Run specific test class
pytest Tests/test_spell_contracts.py::TestFireMageSpells

# Run specific test
pytest Tests/test_spell_contracts.py::TestFireMageSpells::test_fireball_contract
```

## Code Quality Checks

```bash
# Run linter
ruff check .

# Run linter with auto-fix
ruff check . --fix

# Format code
ruff format .
```

## Playing the Game

### Command-line Options

```bash
# Show available classes
python main.py --show-classes

# Show available roles
python main.py --show-roles

# Start the game (interactive mode)
python main.py
```

### Gameplay

1. Choose your class (Warrior, Mage, Paladin, Shaman, Monk, Priest)
2. Choose your role (Tank, Damage)
3. The game will create an AI opponent
4. Take turns casting spells
5. Each spell has:
   - Damage/healing effects
   - Resource costs (mana, rage, chi, holy power, etc.)
   - Cooldowns
   - Multi-turn effects (DOT, damage reduction, buffs)

## Project Structure

```
Turn-based-WoW/
├── Heroes/              # Hero base classes and factory
│   ├── hero_base_stats.py
│   └── hero_factory.py
├── Spells/              # Spell handlers for each class
│   ├── mage_spell_handler.py
│   ├── monk_spell_handler.py
│   ├── paladin_spell_handler.py
│   ├── priest_spell_handler.py
│   ├── shaman_spell_handler.py
│   └── warrior_spell_handler.py
├── Tests/               # Test suite (79 tests)
│   ├── test_ai_player.py
│   ├── test_battles.py
│   ├── test_cooldowns.py
│   ├── test_paladin_spell_handler.py
│   └── test_spell_contracts.py
├── ai_player.py         # AI decision-making
├── battle_state.py      # Cooldown and effect tracking
├── battles_handler.py   # Combat mechanics
├── main.py              # CLI entry point
├── pyproject.toml       # Project configuration
├── requirements.txt     # Dependencies
└── README.md            # Project overview
```

## Troubleshooting

### "uv: command not found"

Make sure `uv` is in your PATH. After installation, you may need to:
- Restart your terminal
- Run `source ~/.bashrc` or `source ~/.zshrc` (macOS/Linux)
- Add `~/.cargo/bin` to your PATH manually

### "Python version not found"

Ensure you have Python 3.10 or higher:
```bash
python --version
```

If you need to install Python, visit [python.org](https://www.python.org/downloads/) or use:
- **macOS:** `brew install python@3.11`
- **Ubuntu/Debian:** `sudo apt install python3.11`
- **Windows:** Download from python.org

### Tests failing

Make sure you're in the project root directory and have activated the virtual environment:
```bash
cd Turn-based-WoW
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pytest
```

### Import errors

If you see import errors, make sure you've installed the dependencies:
```bash
uv pip install -r requirements.txt
```

## Uninstallation

To remove the virtual environment and clean up:

```bash
# Deactivate the virtual environment
deactivate

# Remove the virtual environment directory
rm -rf .venv

# Remove Python cache files (optional)
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name "*.egg-info" -exec rm -rf {} +
```

## Contributing

If you want to contribute to the project:

1. Fork the repository
2. Create a feature branch
3. Install development dependencies: `uv pip install -e ".[dev]"`
4. Make your changes
5. Run tests: `pytest`
6. Run linter: `ruff check .`
7. Submit a pull request

## Support

For issues or questions:
- Open an issue on GitHub
- Check the [README.md](README.md) for project overview
- Review [PROGRESS.md](PROGRESS.md) for development status

## License

MIT License - see LICENSE file for details

---

**Enjoy the game!** ⚔️🔥🛡️

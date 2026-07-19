# Turn-based WoW
This is a simple turn based terminal game, based on World of Warcraft.

## Quick Start

### Automated Setup (Recommended)

**macOS/Linux:**
```bash
./setup.sh
```

**Windows (PowerShell):**
```powershell
.\setup.ps1
```

The setup script will:
- Install `uv` if not already installed
- Create a virtual environment
- Install all dependencies
- Run tests to verify everything works

### Manual Setup

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

## Features

The game has:
- 6 classes to choose from - Paladin, Warrior, Priest, Monk, Mage, Shaman
- 3 roles for the classes  - Ranged DPS, Melee DPS, Tank
- The ability to read the input from terminal
- Turn-based play style
- Cooldown system for spells
- Multi-turn effects (DOT, damage reduction, buffs)
- AI opponents with strategic decision-making

## Playing the Game

```bash
# Activate virtual environment (if not already active)
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Run the game
python main.py
```

## Development

### Running Tests

```bash
pytest                    # Run all tests
pytest -v                 # Verbose output
pytest --cov=.           # With coverage report
```

**Test Status:** ✅ 79 tests passing

### Code Quality

```bash
ruff check .             # Run linter
ruff check . --fix       # Auto-fix issues
ruff format .            # Format code
```

## Project Status

- ✅ Core battle engine (stable)
- ✅ 6 classes with unique spells
- ✅ AI opponents
- ✅ Comprehensive test suite (79 tests)
- ✅ CI/CD pipeline (GitHub Actions)

See [PROGRESS.md](PROGRESS.md) for detailed development status.

## Future Plans

I'm planning to add in a future update:
- UI
- More complex actions like the ability to enter a combo (for example, combo of 4 moves - Crusader Strike, Judgement, Blade of Justice, Templar Strike)
- Simulation harness for balance tuning
- TUI (Textual) or web interface

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Install dev dependencies: `uv pip install -e ".[dev]"`
4. Make your changes
5. Run tests and linter
6. Submit a pull request

## License

MIT License

## About

I'm doing this as a hobby and a learning opportunity.

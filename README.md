# Turn-based WoW
This is a simple turn based terminal game, based on World of Warcraft.

The game has:
- 6 classes to choose from - Paladin, Warrior, Priest, Monk, Mage, Shaman
- 3 roles for the classes  - Ranged DPS, Melee DPS, Tank
- The ability to read the input from terminal
- Turn-based play style

I'm planning to add in a future update:
- UI
- More complex actions like the ability to enter a combo (for example, combo of 4 moves - Crusader Strike, Judgement, Blade of Justice, Templar Strike)


I'm doing this as a hobby and a learning opportunity.

## Run & Test

Quick instructions to run and test the project locally (recommended Python 3.11):

```bash
# create and activate a virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

# update pip and install test deps
pip install -U pip
pip install -r requirements.txt

# run unit tests
python -m pytest -q

# run the interactive CLI
python main.py
```

## Continuous Integration

This repository includes a GitHub Actions workflow that runs the test suite on push and pull requests to `main` using Python 3.11. The workflow file is located at `.github/workflows/python-tests.yml`.

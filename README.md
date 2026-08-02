# Turn-based-WoW

## Project summary

Turn-based-WoW is a terminal-based hobby and software-engineering learning project inspired by World of Warcraft combat. It provides six playable classes across nine supported specializations, local player-vs-player and player-vs-AI modes, class resources, spells, immediate damage and healing, cooldowns, multi-turn effects, health displays, and combat logs.

## Project status

Active development has ended. This repository is preserved as a learning prototype and a record of its implementation and design experiments. It is not a production application or an actively maintained game.

The current Python implementation remains in place. Earlier ideas for a reorganized combat engine, FastAPI adapter, and React frontend were not implemented and are deferred indefinitely.

## Verification status

The latest verified local run completed with **80 tests passing** on Python 3.14.4 using `uv run python -m pytest`. The suite includes a deterministic full-battle acceptance test that characterizes the current outcome of a selected Fury Warrior scenario, including its winner, duration, surviving health, and initial cooldown-driven action sequence.

Passing tests describe covered behavior; they do not prove that every gameplay rule or timing decision is correct. The latest recorded full-repository Ruff run reported 107 findings, so repository-wide lint is not clean.

A tracked GitHub Actions workflow runs tests on Python 3.10, 3.11, and 3.12 for configured push and pull-request branches. Its current remote status has not been verified as part of this final snapshot.

## Run and test

From a prepared environment:

```bash
python main.py
uv run python -m pytest
```

See [INSTALL.md](INSTALL.md) for prerequisites, environment setup, platform-specific commands, and troubleshooting.

## Documentation

- [Final project snapshot](PROGRESS.md)
- [Installation and development commands](INSTALL.md)
- [Architecture](ARCHITECTURE.md) — current structure plus historical, unimplemented design ideas
- [Technical debt](TECHNICAL_DEBT.md) — known limitations and previously considered improvements
- [Archived roadmap](ROADMAP.md) — previous intentions, not an active delivery plan

# Turn-based-WoW

## Project summary

Turn-based-WoW is a hobby and hands-on software-engineering learning project. The current product is a terminal-based turn-combat game with six classes and their currently supported specializations, player-vs-player and player-vs-AI modes, spells, cooldowns, multi-turn effects, and combat logs.

The developer implements the work manually. AI tools are used for guidance, code review, explanations, repository inspection, and test assistance; they are not intended to implement entire backlog items autonomously.

## Current direction

The immediate architecture is a standalone, pure-Python combat engine. The later user-facing product is a browser game using FastAPI and React:

```text
React frontend
    ↓
FastAPI application/API adapter
    ↓
Standalone Python combat engine
```

Option D—the standalone engine—is the current architecture direction. Option B—the browser product—is the later product direction. FastAPI and React are intentionally not immediate work.

## Quick start

Python 3.10 or later is declared in the project configuration.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

Windows activation and development commands are in [INSTALL.md](INSTALL.md).

## Current status

Repository inspection confirms a runnable terminal entry point, `HeroFactory`, six classes with nine supported specializations, local PvP and player-vs-AI selection, spell selection, immediate damage and healing, cooldown/effect tracking, turn progression, health display, and a combat log.

Latest recorded local run: 79 tests passed. This was reproduced during the documentation review with `python -m pytest`, but passing tests characterize tested behavior; they do not prove that all game rules are correct. The result should also be reproduced from a clean checkout.

A GitHub Actions workflow is present but has not yet been verified on a pull request.

## Documentation

- [Installation and development](INSTALL.md)
- [Current progress](PROGRESS.md)
- [Architecture](ARCHITECTURE.md)
- [Technical debt](TECHNICAL_DEBT.md)
- [Roadmap](ROADMAP.md)

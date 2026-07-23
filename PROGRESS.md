# Project progress

This is the current repository snapshot. Future design belongs in [ARCHITECTURE.md](ARCHITECTURE.md) and planned work belongs in [ROADMAP.md](ROADMAP.md).

## Current branch snapshot

- Source branch: `local-state`.
- `local-state` is one commit ahead of the previous `main` branch and zero commits behind it.
- It contains the current local implementation.
- The branch consists of one large safety-snapshot commit rather than a series of small, reviewable changes.

## Implemented state

### Heroes and spells

- Six classes: Paladin, Warrior, Monk, Mage, Shaman, and Priest.
- Nine supported specializations: Protection and Retribution Paladin; Protection and Fury Warrior; Brewmaster and Windwalker Monk; Fire Mage; Enhancement Shaman; and Shadow Priest.
- `HeroFactory` constructs the supported class/specialization combinations.
- Per-class spell-handler modules provide the current actions.
- Classes maintain class-specific resources such as holy power, rage, chi, mana, fire stacks, maelstrom, and insanity.
- Cast methods make fresh dictionary copies from the shared result template, preventing reuse of the same result dictionary between casts.

### Combat

- `Attacking` invokes spells and applies immediate damage; spell methods can apply healing directly.
- `BattleState` tracks cooldowns and multi-turn effects.
- Current effect support includes damage over time and damage-reduction changes.
- The CLI advances turns by ticking battle state and swapping active/passive heroes.
- The battle loop ends when either hero's health is no longer above zero.

### CLI

- Interactive hero and specialization selection.
- Local player-vs-player and player-vs-AI modes.
- Spell selection with remaining cooldown display.
- Health bars and combat-log messages.
- Action skipping when no zero-argument spell is available or all listed spells are on cooldown.
- `--show-classes` and `--show-roles` information flags.

### AI

- `SimpleHeuristicAI` and `RandomAI` strategies exist.
- `SimpleHeuristicAI` simulates candidate casts on deep-copied hero objects and scores dictionary result fields.
- `SimpleHeuristicAI` filters actions using `BattleState` cooldown state when supplied.
- `RandomAI` accepts a `BattleState` argument but currently does not use it to filter cooldowns.

### Tests and tooling

- Pytest tests cover AI choices, immediate battle behavior, cooldowns/effects, Paladin behavior, and spell-result contracts.
- `requirements.txt` and `requirements-dev.txt` are present.
- Pytest, pytest-cov, and Ruff are listed as development dependencies (and are also currently listed in `requirements.txt`).
- Setup scripts exist for macOS/Linux (`setup.sh`) and Windows PowerShell (`setup.ps1`). They were inspected during this review but not executed end to end.
- Latest recorded local run: 79 tests passed. During this review, `python -m pytest` passed on Python 3.14.4. A bare `pytest` invocation failed collection because local modules were not on its import path in this environment.
- Ruff is configured, but `ruff check . --no-cache` currently reports 107 errors; lint is not passing.
- A GitHub Actions workflow is present but has not yet been verified on a pull request.
- Passing tests confirm only the behavior covered by those tests; they do not establish that the game rules are correct.

## Current strengths

- A runnable vertical slice connects hero creation, spells, battle helpers, CLI interaction, and AI.
- Characterization coverage provides a useful record of existing spell contracts.
- `BattleState` is a centralized prototype for cooldown and multi-turn-effect handling.
- CLI and AI exercise shared hero, spell, and battle-helper code.
- The repository is a suitable baseline for incremental refactoring.

## Current limitations

- Architecture and state mutation are tightly coupled.
- Battle helpers, effects, spells, tests, and CLI directly access or mutate private state.
- Spell and effect contracts are dictionaries rather than typed values.
- Standard actions are discovered through method-name reflection.
- The CLI owns orchestration as well as input and rendering.
- Documentation overlaps and previously contained contradictory completion claims.
- The current branch packages the safety snapshot into one large commit rather than small, reviewable changes.

## Immediate next actions

1. Reproduce pytest and Ruff from a clean checkout.
2. Correct contradictory documentation.
3. Add or restore CI.
4. Audit and consolidate pyproject.toml, dependency files, test configuration, and Ruff configuration.
5. Add deterministic acceptance coverage.
6. Begin domain-invariant refactoring.
7. Do not start FastAPI or React yet.

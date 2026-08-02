# Final project snapshot

## Final status

Active development of Turn-based-WoW has ended. The repository is preserved for reference and may be revisited later, but no FastAPI or React application, major combat-engine rewrite, or other roadmap phase is currently planned. A final focused migration placed the existing code in a conventional lowercase Python package without redesigning it.

This snapshot records the implementation on the `local-state` branch. The implementation and tests remain the source of truth; [ARCHITECTURE.md](ARCHITECTURE.md), [TECHNICAL_DEBT.md](TECHNICAL_DEBT.md), and the archived [ROADMAP.md](ROADMAP.md) include ideas that were not completed and are not current commitments.

## Implemented functionality

### Heroes and spells

- Six classes: Paladin, Warrior, Monk, Mage, Shaman, and Priest.
- Nine supported specializations: Protection and Retribution Paladin; Protection and Fury Warrior; Brewmaster and Windwalker Monk; Fire Mage; Enhancement Shaman; and Shadow Priest.
- `HeroFactory` constructs the supported class and specialization combinations.
- Per-class spell handlers provide the current actions.
- Application code is organized under `turn_based_wow/`, with heroes, spells, combat helpers, AI, and CLI modules grouped by their existing responsibilities.
- Heroes maintain class-specific resources including holy power, rage, chi, mana, fire stacks, maelstrom, and insanity.
- Cast methods return fresh dictionary copies of the shared spell-result template.

### Combat and terminal interface

- `Attacking` invokes spells and applies immediate damage; some spell methods apply healing directly.
- `BattleState` tracks cooldowns, damage-over-time effects, and damage-reduction changes.
- The terminal loop ticks battle state, alternates the active and passive heroes, and ends when a hero's health is no longer above zero.
- Interactive selection supports local player-vs-player and player-vs-AI modes.
- The interface lists spells and remaining cooldowns, displays health and combat messages, and skips an action when no zero-argument spell is available.
- `--show-classes` and `--show-roles` provide information without starting a battle.

### AI

- `SimpleHeuristicAI` and `RandomAI` strategies are present.
- `SimpleHeuristicAI` evaluates zero-argument actions on copied heroes and filters cooldown-bound actions when given `BattleState`.
- `RandomAI` chooses among reflected zero-argument actions but does not filter them using the supplied cooldown state.

## Final verification

- Latest verified local test run: `uv run python -m pytest` completed with **80 tests passing** on Python 3.14.4.
- `tests/test_full_battle.py` characterizes a deterministic battle between two Fury Warriors using fixed preferred and fallback actions. The first warrior wins on turn 79 with 29 health, and the test records the initial cooldown-driven action sequence.
- Tests also cover AI choices, immediate battle behavior, cooldowns and effects, Paladin behavior, and spell-result contracts. These tests characterize covered behavior but do not establish that every combat rule is correct.
- Ruff is configured in `pyproject.toml`. The latest recorded full-repository run, `ruff check . --no-cache`, reported 107 findings; repository-wide lint is not passing. A later focused Ruff check on the full-battle test passed, but it did not re-evaluate the rest of the repository.
- `.github/workflows/python-tests.yml` is tracked. It is configured for pushes and pull requests targeting `main`, `master`, and `develop`, runs Python 3.10–3.12, performs a blocking limited Ruff check, a non-blocking full Ruff check, and pytest with coverage. Its current remote result was not verified for this snapshot.
- `setup.sh` and `setup.ps1` are present and were inspected previously, but they were not executed end to end. Their bare `pytest` verification step may behave differently from the documented module invocation in some environments.
- Only Python 3.14.4 was used for the latest local test run; the full declared Python range was not tested locally.

## Known limitations

- Battle orchestration remains distributed across `turn_based_wow/cli.py`, `Attacking`, `BattleState`, spell handlers, and the terminal loop.
- Battle helpers, effects, spells, tests, and CLI code still read or mutate private hero state directly.
- Spell results and active effects remain dictionary contracts rather than typed values.
- Standard actions are discovered through `cast_` method-name reflection and signature inspection.
- The CLI combines input, rendering, metadata, hero creation, AI selection, and battle orchestration.
- Some effect timing, stacking, targeting, mitigation, invalid-action, and defeat semantics are not formally specified or comprehensively tested.
- Broad exception handling remains in parts of the CLI and AI flow and can obscure programming errors.
- Repository-wide Ruff findings remain unresolved.

These limitations are retained as part of the preserved prototype. The project is not being further refactored to address them.

## Closure note

The repository remains useful as a record of experimentation with turn-based spell design, terminal interaction, heuristic AI, characterization testing, incremental refactoring, AI-assisted development, and architectural tradeoffs.

If development resumes, the first step should be to inspect and re-verify the preserved implementation, then establish clear ownership of hero state and battle resolution. Future work should not assume that the archived roadmap or target architecture is still the right plan.

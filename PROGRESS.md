# Project Progress — Detailed Update

Date: 2026-04-26 (Updated)

Overview
--------
This document records a verbose snapshot of recent work on the Turn-based WoW prototype, what changed in the codebase, current test status, and next steps. The goal of the last iteration was to stabilize the core battle engine (cooldowns, multi-turn effects, and spell contract consistency), harden the turn execution surface area, and improve the CLI experience so manual playtesting and automated tests behave deterministically.

High-level accomplishments
-------------------------
- Centralized multi-turn state and cooldown tracking via `BattleState`.
- Converted all per-class spell handlers to return a fresh attributes dict per cast (removed the shared `spell_attributes` mutation class-wide).
- Hardened `Attacking.attack` to only pick zero-argument `cast_` methods by default and to gracefully handle signature errors when a cast cannot be invoked.
- Fixed a number of concrete runtime bugs found during tests (for example: Shaman `cast_flame_shock` cost deducted from mana not health, several spells now consistently use returned attrs for cost/damage values).
- Improved the CLI in `main.py` to list per-spell cooldowns, re-prompt when the player chooses a spell on cooldown, and skip the player's action when all spells are currently unavailable.
- Added and refined AI logic (`SimpleHeuristicAI`, `RandomAI`) with simulation-based scoring that respects cooldowns when a `BattleState` is provided.
- Replaced many placeholder docstrings with concise descriptions in core modules (hero API, battle state, hero factory, AI).
- Kept the test suite green while making the above changes; current run shows all tests passing locally.

Files changed (representative)
-----------------------------
- [battle_state.py](battle_state.py) — central cooldown/effect manager and `tick()` logic.
- [battles_handler.py](battles_handler.py) — `Attacking.attack` hardened, structured error return on bad signatures.
- [main.py](main.py) — interactive CLI: per-spell cooldown display, re-prompt on cooldown, skip-turn behavior.
- [ai_player.py](ai_player.py) — `SimpleHeuristicAI` and `RandomAI` with simulation and cooldown-awareness.
- `Spells/*` (all handlers) — replaced in-place mutation of `self.spell_attributes` with per-call copies (`attrs = dict(self.spell_attributes)` and return `attrs`). Notable files changed: [Spells/paladin_spell_handler.py](Spells/paladin_spell_handler.py), [Spells/mage_spell_handler.py](Spells/mage_spell_handler.py), [Spells/shaman_spell_handler.py](Spells/shaman_spell_handler.py), [Spells/priest_spell_handler.py](Spells/priest_spell_handler.py), [Spells/warrior_spell_handler.py](Spells/warrior_spell_handler.py), [Spells/monk_spell_handler.py](Spells/monk_spell_handler.py).
- [Heroes/hero_base_stats.py](Heroes/hero_base_stats.py) — cleaned up interface docstrings and clarified the `spell_attributes` template comment.
- [Heroes/hero_factory.py](Heroes/hero_factory.py) — small docstring improvements.
- `Tests/*` — added and adjusted tests to reflect the new behavior and the presence of `BattleState` (examples: [Tests/test_cooldowns.py](Tests/test_cooldowns.py), [Tests/test_battles.py](Tests/test_battles.py), [Tests/test_ai_player.py](Tests/test_ai_player.py), [Tests/test_paladin_spell_handler.py](Tests/test_paladin_spell_handler.py)).
- [Tests/test_spell_contracts.py](Tests/test_spell_contracts.py) — comprehensive per-class spell contract tests (66 new tests covering all 6 classes).
- [.github/workflows/python-tests.yml](.github/workflows/python-tests.yml) — CI workflow for automated testing and linting on push/PR.

Detailed technical notes
------------------------
- BattleState
  - Tracks cooldowns by hero object id and holds active effects (DOT, DR, buff/debuff).
  - `register_spell_cast(attacker, defender, spell_name, info)` now records cooldowns and creates an effect dict when `turns_active` > 0. It applies damage reduction immediately when appropriate and marks whether DR was applied so it can be reverted when the effect expires.
  - `tick()` applies DOT damage, decrements durations, reverts DR when effects expire, and decrements cooldowns.

- Spells API
  - Each `cast_*` now returns a fresh dictionary (copied from a shared template) so that multiple casts do not leak state between different spells or between tests.
  - Spell return contract remains a mapping with keys such as `spell_cost`, `spell_damage`, `cooldown`, `turns_active`, `damage_over_time`, `damage_reduction`, `initial_spell_damage`, `health_leech`.

- Attacking / Battles
  - `Attacking.attack` now selects default spells only among zero-argument `cast_` methods (using `inspect.signature`) to avoid accidental invocation of spells that expect parameters.
  - Invocation is wrapped to catch `TypeError` and return a structured info dict with an `error` field instead of raising; this reduces accidental crashes during interactive play and in tests.

- CLI
  - `main.py` lists each available zero-arg spell and shows remaining cooldowns next to spells; choosing a spell on cooldown prompts for another selection, and when no non-cooldown spells exist the player skips their action.

Test status (local)
-------------------
- Test runner: `pytest` (local runs during development).
- Last full run (local dev environment) result: **79 passed** (all tests green).
- Test coverage now includes:
  - Cooldown mechanics and multi-turn effects
  - Battle damage application and healing
  - AI decision-making (killing blows, healing priority)
  - Per-class spell contracts for all 6 classes (Mage, Monk, Paladin, Priest, Shaman, Warrior)
  - Resource management (mana, rage, chi, holy power, fire stacks, maelstrom, insanity)
  - Spell return contract validation (all required keys present)
  - Template immutability (spells return fresh dicts, not shared references)

How to reproduce locally
------------------------
Create and activate a virtual environment and run the tests:

```bash
python -m venv .venv
source .venv/bin/activate
# (optional) install pinned deps if you maintain requirements
# pip install -r requirements.txt
python -m pytest -q
```

Current TODO list (tracked)
---------------------------

# Todo List

- [x] Add unit tests for cooldowns, heal reporting, and effect-targeting
- [x] Add docstrings to public functions and remove AI comments
- [x] Improve CLI UX in `main.py` (clear combat log, health bars, cooldown display)
- [x] Implement AI player module and integrate into CLI
- [x] Add unit tests for AI behavior (kill selection, healing selection)
- [x] Run test suite and fix any regressions
- [ ] Commit and push changes
- [x] Stop reusing shared `spell_attributes` (per-spell result dicts)
- [x] Harden `Attacking.attack` to validate spell signatures and handle TypeError
- [x] Add per-spell unit tests to cover return contract and edge cases (all 6 classes)
- [x] Add CI (GitHub Actions) to run tests and linter on push

Notes on TODOs:
- Docstring sweep is complete: all auto-generated placeholders replaced with real docstrings.
- Per-class spell contract tests added in `Tests/test_spell_contracts.py` covering all 6 classes (79 tests total).
- CI workflow added in `.github/workflows/python-tests.yml` with pytest, ruff linting, and coverage reporting.
- Ready for manual commit and push.

Next steps (recommended priority)
--------------------------------
1. ~~Finish docstring sweep and remove any remaining assistant-generated comments in public modules (low risk, cosmetic).~~ **DONE**
   - ~~Files: `Heroes/hero_base_stats.py`, `ai_player.py`, `battle_state.py`, `Spells/*`~~
2. ~~Add per-spell unit tests to cover return contract and edge cases (insufficient resources, signature mismatches).~~ **DONE**
   - ~~Files: `Tests/test_spell_contracts.py`, `Tests/test_<class>.py` per specialization.~~
3. ~~Add CI (GitHub Actions) to run tests and a linter on push, and optionally add `mypy` for type coverage.~~ **DONE**
   - ~~Files: `.github/workflows/python-tests.yml`, `pyproject.toml` / `requirements.txt`.~~
4. Balance & simulation harness (medium-term): create a small simulation harness to run many matches for telemetry and parameter tuning.
   - Files: `tools/simulate.py` (new), `tools/metrics.md` (new).
5. Optional: implement a TUI (Textual) or tiny web UI once the core engine and tests are stable.

**All immediate tasks complete!** The project is now ready for:
- Manual commit and push
- Opening a pull request
- Further feature development (simulation harness, TUI, balance tuning)

---
This file was updated automatically to reflect the current development snapshot.

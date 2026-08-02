# Architecture

This document distinguishes the verified current structure from the agreed target direction. The target is incremental guidance, not a claim about code that already exists.

## Current architecture

The current flow is approximately:

```text
turn_based_wow/__main__.py
    ↓
turn_based_wow/cli.py
    ↓
HeroFactory / hero classes
    ↓
Attacking + BattleState
    ↓
Spell handlers
```

The application code is grouped in the lowercase `turn_based_wow` package, with `combat`, `heroes`, `spells`, and `ai` subpackages. The CLI still owns argument parsing, metadata, terminal input/output, hero creation, AI selection, action discovery, the battle loop, logging, and rendering. Actions are discovered by reflecting over `cast_` method names and inspecting signatures; parameterized cast methods are excluded from normal CLI/AI discovery. Spell results and active effects are dictionaries. Hero health, resources, and damage reduction are often mutated directly by spells or battle helpers.

## Agreed architecture direction

```text
React frontend
    ↓
FastAPI adapter
    ↓
Application layer / BattleService
    ↓
Pure Python domain engine
```

The pure-Python domain engine is the immediate direction (Option D). The React/FastAPI product is the later user-facing direction (Option B), after the engine and application boundaries are stable.

## Target package direction

```text
turn_based_wow/
├── domain/
│   ├── hero.py
│   ├── resources.py
│   ├── actions.py
│   ├── effects.py
│   ├── battle.py
│   └── exceptions.py
├── content/
│   ├── registry.py
│   ├── paladin.py
│   ├── warrior.py
│   ├── mage.py
│   ├── priest.py
│   ├── monk.py
│   └── shaman.py
├── application/
│   ├── battle_service.py
│   └── hero_factory.py
├── adapters/
│   └── cli.py
└── __main__.py

tests/
├── unit/
├── integration/
└── acceptance/
```

This is a target direction. It is not an instruction to move every file immediately; migration should proceed through tested vertical slices.

## Intended responsibilities

### Hero

- Own valid combat state: health, resources, and stats.
- Expose controlled mutation methods.
- Prevent external writes to private fields.

### ResourcePool

- Define minimum and maximum values.
- Spend and generate resources.
- Reject invalid operations without partial mutation.

### Action

- Provide a stable identifier and display name.
- Define cost, cooldown, target, calculation, and effects.

### ActionResult

- Be a fresh, typed, immutable value.
- Represent damage, healing, resource changes, and effects.
- Represent failure information where a result is more appropriate than an exception.

### Effect

- Record source, target, duration, tick timing, payload, and stacking/replacement rule.

### Battle

- Own participants, active actor, turn number, cooldowns, effects, victory state, and resolution order.

### BattleService

- Create battles.
- List eligible actions.
- Submit actions.
- Expose inspectable battle state.

### CLI adapter

- Translate terminal input into application calls and render output only.

### Future FastAPI adapter

- Translate HTTP requests and responses only.
- Contain no combat rules.

## Resolution order

The intended resolution sequence is:

1. Validate actor, target, and action.
2. Validate resources and cooldown.
3. Spend cost.
4. Calculate result.
5. Apply mitigation.
6. Apply damage or healing.
7. Register effects.
8. Generate resources.
9. Check defeat.
10. Advance turn.

Invalid actions must not partially mutate state.

## Architecture principles

- Correctness before features.
- Small pull requests.
- Tests accompany behavioral changes.
- Refactoring stays separate from balancing.
- One source of truth for game metadata.
- No framework dependency in domain code.
- Avoid pattern-driven overengineering.
- No broad rewrite.

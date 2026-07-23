# Roadmap

This is planned work, not a description of completed implementation. FastAPI and React remain deferred until the engine and application boundaries are established.

## Phase 0 — Reproducible baseline

**Goals:** Clean checkout; reproduce tests and Ruff; verify setup scripts; add or restore CI; correct documentation.

**Exit criteria:** Tests and lint work from a clean clone; CI runs on pull requests; no false completion claims.

## Phase 1 — Characterization and invariants

**Goals:** Full deterministic battle test; health/resource invariant tests; invalid-action atomicity; effect-boundary tests; controlled hero state methods.

**Exit criteria:** No new direct private-field mutation; existing behavior protected; domain boundaries tested.

## Phase 2 — Typed `ActionResult` vertical slice

**Goals:** Introduce a typed immutable `ActionResult`; migrate one hero/specialization and one complete battle path; temporarily support legacy dictionary spells through an adapter.

**Exit criteria:** One vertical slice no longer relies on arbitrary dictionary keys; results are fresh and immutable; tests prove compatibility.

## Phase 3 — Explicit action registry

**Goals:** Stable action identifiers; central metadata; replace reflection for migrated content; one eligibility API for CLI and AI.

**Exit criteria:** No `dir(hero)` discovery for the migrated hero; one source of truth for actions and class/specialization metadata.

## Phase 4 — Battle aggregate and typed effects

**Goals:** Move orchestration out of `main.py`; add typed cooldown/effect models; define resolution order; support safe stacking and expiry.

**Exit criteria:** `Battle` owns turns and victory; no direct `_curr_health` mutation in battle flow; effects have tested lifecycle rules.

## Phase 5 — CLI adapter

**Goals:** Extract terminal I/O; add `BattleService`; emit structured events; remove `exit()` from reusable code.

**Exit criteria:** Core code imports no CLI concerns; CLI remains playable; simulations use the same application service.

## Phase 6 — Content migration

**Goals:** Migrate all spells; audit descriptions; consolidate resource and healing behavior; correct naming; separate balance changes from refactors.

**Exit criteria:** Every action is typed and tested; adding an action does not modify the engine.

## Phase 7 — Simulation and balancing

**Goals:** Seeded AI-vs-AI simulation; metrics for win rates, battle length, damage, healing, and action use.

**Exit criteria:** Simulations are reproducible, output is machine-readable, and balance changes are evidence-based.

## Phase 8 — FastAPI

**Goals:** A thin HTTP adapter with in-memory battles initially:

```text
POST /battles
GET /battles/{battle_id}
POST /battles/{battle_id}/actions
```

**Exit criteria:** A full battle is playable over HTTP; the API layer contains no combat logic.

## Phase 9 — React

**Goals:** Hero selection, battle screen, health/resources, eligible actions, cooldowns/effects, combat log, and victory state.

**Constraints:** No authentication, database, multiplayer, or advanced animation initially.

**Exit criteria:** A full browser battle uses the same engine.

## Immediate backlog

1. Documentation correction and consolidation.
2. Clean-clone test/lint verification.
3. CI workflow.
4. Audit and consolidate pyproject.toml, dependency files, test configuration, and Ruff configuration.
5. Deterministic battle acceptance test.
6. Hero invariant tests.
7. Controlled `Hero` state API.
8. Typed `ActionResult` design and vertical slice.


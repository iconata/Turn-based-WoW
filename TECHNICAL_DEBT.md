# Technical debt

These findings come from inspection of the `local-state` repository snapshot. Desired directions and tests are plans, not current implementation claims.

## 1. `IBaseHero` and interface hierarchy

**Current observation:** `IBaseHero` is both an abstract interface and a concrete mutable state holder. It supplies default stats and a spell-result template while requiring `get_name`, `create_hero`, `heal_up`, class-resource spending, and class-resource generation. `create_hero` overlaps with `HeroFactory`. `ICommonGetters`, `ICommonSetters`, and `ICommonCheckers` pass `hero_instance` to operations that conceptually belong to `self`; several interfaces appear unused or only partly aligned with concrete classes.

**Risk:** Ownership and initialization are unclear, invariants are weak, abstraction exceeds demonstrated polymorphic needs, and interfaces do not accurately describe actual usage.

**Desired direction:** Use a concrete `Hero` domain object, with state owned by the instance and small protocols only where true polymorphism exists. Remove redundant getter/setter/checker interfaces and finalize construction in the factory or configuration layer.

**Migration notes:** Add characterization tests before removing interfaces. Migrate one hero/specialization vertical slice first; do not rewrite every spell handler in one pull request.

## 2. Hero state and invariants

**Current observation:** `_curr_health` is read and changed directly. `BattleState` and `Attacking` bypass hero methods, damage reduction is modified directly, and resource behavior differs by class.

**Risk:** State can become negative, exceed maxima, or be partially mutated; an effect can corrupt unrelated state.

**Desired direction:** Introduce `hero.take_damage()`, `hero.heal()`, `hero.spend_resource()`, `hero.gain_resource()`, `hero.apply_modifier()`, and `hero.is_alive`.

**Suggested tests:** Health lower and upper bounds; resource lower and upper bounds; zero side effects for invalid operations; defeat from direct damage and DOT.

## 3. Spell and action contracts

**Current observation:** Spells are `cast_` methods discovered with `dir()` and `inspect.signature()`. Parameterized spells are omitted from standard discovery. Results are generic dictionaries. Fresh per-cast copies prevent shared-reference reuse but remain weakly typed. Spells mix calculation, resource mutation, healing, and result creation.

**Risk:** Key typos become runtime bugs; keys and targets can be missing or unclear; side effects are hidden; CLI and AI depend on implementation naming.

**Desired direction:** Provide an explicit `Action` catalogue, typed `ActionResult`, explicit target types and eligibility results, and no reflection for standard gameplay.

**Suggested tests:** Action eligibility, resource validation, result immutability, absence of stale fields, parameterized-action support, and invalid-action rejection.

## 4. Battle engine

**Current observation:** `Attacking` applies immediate damage, `BattleState` applies DOT and effect state, `main.py` advances turns, and `Defending` calculates mitigation separately. Resolution is distributed across modules. `Attacking` catches `TypeError` and treats it as an invalid signature.

**Risk:** Ordering is ambiguous; effects may be doubled or missed; programming bugs can be hidden; partial changes are possible; acceptance testing is difficult.

**Desired direction:** Let a `Battle` aggregate own resolution through an explicit pipeline. Expected invalid actions should use domain errors/results; programming errors should not be silently swallowed.

**Suggested tests:** Deterministic full battle, mitigation order, cooldown order, effect timing, invalid-action atomicity, and death before/after an effect tick.

## 5. `BattleState`, cooldowns, and effects

**Current observation:** Cooldowns are keyed by `id(hero)`. Effects are dictionaries containing live object references. Targets are inferred from nonzero damage fields. Damage reduction is applied through attribute addition and reverted by subtraction. Cooldowns and effects tick together.

**Risk:** Overlapping effects are fragile, target inference can be wrong, state is hard to serialize, behavior is coupled to object identity, and stacking/expiry semantics are unclear.

**Desired direction:** Use stable participant IDs; typed `Cooldown` and `Effect` values; explicit source, target, stacking rules, and tick phase; and safe modifier composition.

**Suggested tests:** Two overlapping DR effects; buff and debuff on one stat; replacement; stacking; expiration; DOT defeat; cooldown at zero; and cooldown consistency for AI and humans.

## 6. CLI coupling

**Current observation:** `main.py` handles parsing, metadata, input, hero creation, AI selection, action discovery, battle looping, logging, and rendering. `input()`, `print()`, and `exit()` occur in reusable functions. Class/role metadata is duplicated, and helper functions catch broad exceptions.

**Risk:** Testing and a future FastAPI adapter become difficult, metadata gains competing sources of truth, and domain behavior leaks into presentation.

**Desired direction:** Add a `BattleService`; keep the CLI as input/output translation; emit structured battle events; centralize metadata in a registry.

**Suggested tests:** Run battles without terminal mocking, test the CLI adapter separately, and assert metadata consistency.

## 7. AI design

**Current observation:** `SimpleHeuristicAI` uses `deepcopy` to simulate spells, scores dictionary fields, and uses broad exception handling to skip failures. `RandomAI` accepts but ignores cooldown state. Both discover actions through reflection.

**Risk:** Broken spells can silently disappear from decisions, copying may become expensive or fail with richer state, eligibility logic is duplicated, and AI rules can diverge from human rules.

**Desired direction:** Give AI eligible `Action` objects from `BattleService`. Use immutable state snapshots or engine preview methods for simulation. Strategies select actions; the engine remains responsible for validity.

**Suggested tests:** AI never selects unavailable actions, respects cooldowns, does not mutate real state, supports deterministic seeded `RandomAI`, and surfaces broken-action errors where appropriate.

## 8. Testing strategy

**Current observation:** Latest recorded local run: 79 tests passed. Many are spell-contract or characterization tests. Tests live under `Tests/`. Coverage helps preserve behavior but also encodes the dictionary design.

**Risk:** Implementation-specific assertions can obstruct refactoring; passing tests may preserve incorrect gameplay; acceptance boundaries are missing. Passing tests do not prove the game rules are correct.

**Desired direction:** Organize tests under `tests/unit`, `tests/integration`, and `tests/acceptance`; retain characterization tests during migration; make new tests assert domain behavior rather than private fields.

**Suggested additions:** A full-battle acceptance test, invalid-action atomicity, hero invariants, overlapping effects, and clean-checkout verification.

## 9. AI-generated and overlapping documentation

**Current observation:** Multiple installation and completion documents overlap and make strong completion claims. Earlier versions of `PROGRESS.md`, `SUMMARY.md`, and `README.md` conflicted.

**Risk:** There is no clear source of truth, setup instructions drift, and completion language creates false confidence.

**Desired direction:** Use `README.md` as the entry point, `INSTALL.md` for setup, `PROGRESS.md` for the current snapshot, `ARCHITECTURE.md` for design, this file for findings, and `ROADMAP.md` for planned phases.

**Migration notes:** Review these obsolete candidates for later deletion, but do not delete them in this task: `INSTALLATION_COMPLETE.md`, `INSTALLATION_SUMMARY.md`, `QUICKSTART.md`, and `SUMMARY.md`.


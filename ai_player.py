"""Simple AI players for the turn-based game.

This module provides a lightweight interface ``IAIPlayer`` and a concrete
``SimpleHeuristicAI`` implementation. The AI uses a non-cheating simulation
approach: it only inspects the public state of the attacker and defender and
simulates spell calls on a deep-copied attacker instance to estimate the
effect of each spell without mutating the real game state.

The implementation is intentionally small and follows SOLID principles:
- Single Responsibility: AI code only contains decision-making logic.
- Open/Closed: new AI strategies can inherit from ``IAIPlayer``.
- Dependency Inversion: callers depend on the interface, not concrete AI.
"""

from __future__ import annotations

import copy
import inspect
from abc import ABC, abstractmethod
from typing import Optional

from Heroes.hero_base_stats import IBaseHero
from battle_state import BattleState


class IAIPlayer(ABC):
    """AI interface — select a spell name to cast for the supplied hero.

    Implementations must be deterministic and must not mutate the real
    ``attacker`` or ``defender`` objects when estimating outcomes.
    """

    @abstractmethod
    def choose_spell(self, attacker: IBaseHero, defender: IBaseHero, battle_state: Optional[BattleState] = None) -> Optional[str]:
        """Return the name of the spell the AI wants to cast (e.g. ``cast_fireball``).

        Return ``None`` if no action is possible.
        """


class SimpleHeuristicAI(IAIPlayer):
    """A small heuristic-based AI.

    Strategy summary:
    - Prefer spells that immediately kill the opponent.
    - Prefer heals when the AI's health is low.
    - Otherwise pick the spell with the best immediate expected value
      (damage + some weight for DOT and defensive effects) per cost.
    """

    def choose_spell(self, attacker: IBaseHero, defender: IBaseHero, battle_state: Optional[BattleState] = None) -> Optional[str]:
        """Choose the best available zero-argument ``cast_`` method to invoke.

        The method simulates each candidate spell on a deep-copied attacker
        instance so the real hero's state is not modified during decision
        making. It uses simple scoring to rank spells.
        """
        candidates = []
        for name in dir(attacker):
            if not name.startswith("cast_"):
                continue
            method = getattr(attacker, name)
            if not callable(method):
                continue
            # skip methods that require parameters
            try:
                sig = inspect.signature(method)
            except Exception:
                continue
            if len(sig.parameters) != 0:
                continue
            candidates.append(name)

        if not candidates:
            return None

        best = None
        best_score = float("-inf")

        defender_hp = getattr(defender, "_curr_health", getattr(defender, "max_health", 0))
        attacker_hp = getattr(attacker, "_curr_health", getattr(attacker, "max_health", 0))
        attacker_max_hp = getattr(attacker, "max_health", 1)

        for name in candidates:
            # safely clone attacker and simulate the spell
            # skip spells on cooldown if a BattleState was provided
            if battle_state and battle_state.is_on_cooldown(attacker, name):
                continue
            try:
                sim = copy.deepcopy(attacker)
            except Exception:
                # fallback: shallow clone of attrs
                sim = type(attacker)()
                try:
                    sim.__dict__.update(copy.deepcopy(attacker.__dict__))
                except Exception:
                    continue

            method = getattr(sim, name, None)
            if method is None or not callable(method):
                continue

            before_hp = getattr(sim, "_curr_health", None)
            try:
                info = method()
            except Exception:
                # if the simulation raises, skip candidate
                continue

            if info is None:
                # spell could not be cast (e.g. not enough specific resource)
                continue

            # derive numeric metrics
            immediate = int(info.get("spell_damage") or info.get("initial_spell_damage") or 0)
            turns = int(info.get("turns_active") or 0)
            dot = int(info.get("damage_over_time") or 0)
            dot_total = dot * turns if dot and turns else 0
            heal = 0
            after_hp = getattr(sim, "_curr_health", None)
            if before_hp is not None and after_hp is not None:
                heal = max(0, after_hp - before_hp)

            damage_reduction = int(info.get("damage_reduction") or 0)
            cost = int(info.get("spell_cost") or 0)

            # scoring
            score = immediate + 0.5 * dot_total + 0.1 * damage_reduction + 0.9 * heal
            score -= 0.05 * cost

            # prefer killing blows
            if immediate + dot_total >= defender_hp:
                score += 10000

            # prefer healing when low
            if attacker_hp / max(1, attacker_max_hp) < 0.35 and heal > 0:
                score += 500

            if score > best_score:
                best_score = score
                best = name

        return best


class RandomAI(IAIPlayer):
    """A fallback AI that picks a random available spell."""

    def __init__(self, rng=None):
        """Create a RandomAI with an optional RNG for deterministic tests.

        Args:
            rng: an object implementing `choice(seq)` (e.g. a `random.Random`).
        """
        import random

        self._rng = rng or random.Random()

    def choose_spell(self, attacker: IBaseHero, defender: IBaseHero, battle_state: Optional[BattleState] = None) -> Optional[str]:
        """Return a random zero-argument `cast_` method name or ``None``.

        The implementation skips spells that require parameters and does not
        consult `battle_state` for cooldowns -- callers should avoid using
        `RandomAI` when cooldown-awareness is required.
        """
        candidates = []
        for name in dir(attacker):
            if not name.startswith("cast_"):
                continue
            method = getattr(attacker, name)
            if not callable(method):
                continue
            try:
                sig = inspect.signature(method)
            except Exception:
                continue
            if len(sig.parameters) != 0:
                continue
            candidates.append(name)

        if not candidates:
            return None
        return self._rng.choice(candidates)

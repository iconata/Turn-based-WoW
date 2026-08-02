"""Battle helpers: simple attacking and defending utilities.

This module keeps the turn-level application of spell results simple and
imperative: it calls the spell method on the attacker and applies any
immediate effects (damage, heals) to the target. It purposefully keeps
state mutation local and minimal so unit tests can exercise individual
spells and simple attacks without a full ``BattleState`` manager.
"""

import inspect
from typing import Any, Optional, Tuple

from battle_state import BattleState
from Heroes.hero_base_stats import IBaseHero


class Attacking:
    """Invoke a hero's spell and apply its immediate effects to the defender.

    The attacker is expected to expose spell methods named ``cast_*`` that
    return a dictionary of ``spell_attributes`` (for example containing keys
    like ``spell_damage``, ``cooldown`` or ``turns_active``). This helper
    calls the selected spell (or the first available spell when
    ``selected_spell`` is ``None``) and applies immediate damage to the
    defender if the return dict contains ``spell_damage`` or
    ``initial_spell_damage``.
    """

    def __init__(self, attacker: IBaseHero, defender: IBaseHero, battle_state: Optional[BattleState] = None) -> None:
        """Create an Attacking helper for ``attacker`` vs ``defender``.

        Args:
            attacker: the hero casting spells
            defender: the hero receiving effects
        """
        self._attacker = attacker
        self._defender = defender
        self._battle_state = battle_state

    def attack(self, selected_spell: Optional[str] = None) -> Tuple[IBaseHero, Optional[dict]]:
        """Call the attacker's spell and apply immediate results.

        Args:
            selected_spell: optional name of the spell to call. If ``None`` the
                first attribute on the attacker that starts with ``cast_`` is
                invoked.

        Returns:
            A tuple of ``(defender, info)`` where ``info`` is the dict
            returned by the spell call (or ``None`` if the call returned
            nothing). The defender's in-memory health field may be mutated
            in-place (``_curr_health``) if present.
        """
        # pick a default zero-arg spell if none was provided
        if selected_spell is None:
            candidates = []
            for n in dir(self._attacker):
                if not n.startswith("cast_"):
                    continue
                m = getattr(self._attacker, n)
                if not callable(m):
                    continue
                try:
                    sig = inspect.signature(m)
                except (ValueError, TypeError):
                    continue
                # count required positional parameters
                required_pos = [p for p in sig.parameters.values() if p.default is inspect._empty and p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
                if len(required_pos) == 0:
                    candidates.append(n)

            if not candidates:
                return self._defender, None
            selected_spell = candidates[0]

        if not hasattr(self._attacker, selected_spell):
            raise ValueError(f"Invalid spell: {selected_spell}")

        # check cooldown if a BattleState is provided
        if self._battle_state and self._battle_state.is_on_cooldown(self._attacker, selected_spell):
            remaining = self._battle_state.get_cooldown(self._attacker, selected_spell)
            return self._defender, {"spell": selected_spell, "on_cooldown": True, "remaining": remaining}

        method = getattr(self._attacker, selected_spell)
        if not callable(method):
            raise ValueError(f"Spell {selected_spell} is not callable")

        try:
            info: Optional[dict[str, Any]] = method()  # call the spell
        except TypeError as exc:
            # method signature mismatch or incorrect invocation; return structured error
            return self._defender, {"spell": selected_spell, "error": "invalid_signature", "message": str(exc)}

        # apply immediate damage (if any)
        if isinstance(info, dict):
            dmg = info.get("spell_damage") or info.get("initial_spell_damage") or 0
            if dmg:
                if hasattr(self._defender, "_curr_health"):
                    self._defender._curr_health -= dmg
                    if self._defender._curr_health < 0:
                        self._defender._curr_health = 0

        # register multi-turn effects and cooldowns
        if self._battle_state and isinstance(info, dict):
            self._battle_state.register_spell_cast(self._attacker, self._defender, selected_spell, dict(info))

        return self._defender, info

    def heal(self, hp_restore: int) -> None:
        """Heal the attacker by delegating to the hero's healing method.

        This is a thin convenience wrapper around the hero's
        ``heal_up`` implementation.
        """
        if hasattr(self._attacker, "heal_up"):
            self._attacker.heal_up(hp_restore)


class Defending:
    """Simple defending helpers (damage mitigation).

    The helpers operate on the defender instance. They attempt to use a
    standard getter when available and fall back to attributes when needed.
    """

    def __init__(self, defender: IBaseHero) -> None:
        """Store the defender instance.

        Args:
            defender: hero receiving damage
        """
        self._defender = defender

    def deflect(self, damage: int) -> int:
        """Return the damage after applying the defender's damage reduction.

        The defender is expected to expose either a ``get_current_damage_reduction``
        method or a ``damage_reduction`` attribute.
        """
        if hasattr(self._defender, "get_current_damage_reduction"):
            damage_reduction = self._defender.get_current_damage_reduction()
        else:
            damage_reduction = getattr(self._defender, "damage_reduction", 0)

        mitigated_damage = damage - damage_reduction
        if mitigated_damage < 0:
            mitigated_damage = 0
        return mitigated_damage

    def parry(self, damage: int) -> int:
        """Alias for ``deflect`` (parry behaves like a deflect in this simple model)."""
        return self.deflect(damage)

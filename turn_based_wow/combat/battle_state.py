"""Manage multi-turn effects and per-hero cooldowns for battles.

This class centralizes cooldown tracking and active-effect bookkeeping so
game logic and AI can query and mutate state in a single place.
"""

from typing import Any, Dict, List, Optional


class BattleState:
    """Track cooldowns and active effects for heroes.

    The implementation stores cooldowns keyed by the Python object id of a
    hero instance. Active effects are held in a list; each effect is a dict
    describing the owner, target, remaining turns and effect payload (DOT,
    damage reduction, etc.).
    """

    def __init__(self) -> None:
        """Initialize cooldown and active-effect storage.

        `_cooldowns` maps hero ids to per-spell remaining-turn counters.
        `_effects` is a list of active multi-turn effects (DOT, DR, buff).
        """
        self._cooldowns: Dict[int, Dict[str, int]] = {}
        self._effects: List[Dict[str, Any]] = []

    # ------------------- cooldowns -------------------------------------
    def _hid(self, hero: object) -> int:
        """Return a stable integer key for a hero instance (object id)."""
        return id(hero)

    def set_cooldown(self, hero: object, spell_name: str, turns: int) -> None:
        """Set or overwrite the remaining cooldown for a hero's spell.

        `turns` will be stored as an integer number of turns.
        """
        hid = self._hid(hero)
        self._cooldowns.setdefault(hid, {})[spell_name] = int(turns)

    def get_cooldown(self, hero: object, spell_name: str) -> int:
        """Return remaining cooldown turns for `spell_name` (0 if none)."""
        return int(self._cooldowns.get(self._hid(hero), {}).get(spell_name, 0))

    def is_on_cooldown(self, hero: object, spell_name: str) -> bool:
        """Return True when a spell has >0 remaining cooldown turns."""
        return self.get_cooldown(hero, spell_name) > 0

    # ------------------- effects ---------------------------------------
    def register_spell_cast(self, attacker: object, defender: object, spell_name: str, info: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Register cooldowns and multi-turn effects for a cast.

        This method does not re-apply immediate damage (the caller is
        expected to have applied any immediate effects). It returns a copy of
        the information stored for the spell.
        """
        if info is None:
            return {}

        # set cooldown if present
        cd = int(info.get("cooldown", 0) or 0)
        if cd > 0:
            self.set_cooldown(attacker, spell_name, cd)

        # decide effect target: if the spell deals damage or DOT target is defender,
        # otherwise the effect is assumed to apply to the caster (buff)
        if any(info.get(k) for k in ("spell_damage", "initial_spell_damage", "damage_over_time")):
            eff_target = defender
        else:
            eff_target = attacker

        turns = int(info.get("turns_active", 0) or 0)
        if turns > 0:
            effect = {
                "name": spell_name,
                "owner": attacker,
                "target": eff_target,
                "remaining": turns,
                "dot": int(info.get("damage_over_time", 0) or 0),
                "dr": int(info.get("damage_reduction", 0) or 0),
                "info": dict(info),
                "applied_dr": False,
            }

            # apply immediate DR buffs/debuffs to the target so subsequent
            # incoming damage is affected
            if effect["dr"]:
                # add or subtract according to sign
                current = getattr(eff_target, "damage_reduction", 0)
                setattr(eff_target, "damage_reduction", current + effect["dr"])
                effect["applied_dr"] = True

            self._effects.append(effect)

        return dict(info)

    def get_active_effects(self, hero: object) -> List[Dict[str, Any]]:
        """Return a list of active effects whose target is `hero`.

        Each effect dict contains keys like ``name``, ``owner``, ``remaining``,
        ``dot`` and ``dr`` describing the active effect.
        """
        return [e for e in self._effects if e.get("target") is hero]

    def tick(self) -> Dict[str, Any]:
        """Advance state by one turn: apply DOTs, decrement durations and cooldowns.

        Returns a brief summary of what changed (for logging/testing).
        """
        summary: Dict[str, Any] = {"dots": [], "expired": [], "cooldowns": []}

        # apply DOTs and decrement effect durations
        for effect in list(self._effects):
            dot = int(effect.get("dot", 0) or 0)
            if dot and effect.get("target") is not None:
                target = effect["target"]
                if hasattr(target, "_curr_health"):
                    target._curr_health -= dot
                    if target._curr_health < 0:
                        target._curr_health = 0
                summary["dots"].append({"name": effect["name"], "target": target, "dot": dot})

            effect["remaining"] -= 1
            if effect["remaining"] <= 0:
                # revert DR if applied
                if effect.get("applied_dr"):
                    target = effect["target"]
                    current = getattr(target, "damage_reduction", 0)
                    new = current - int(effect.get("dr", 0) or 0)
                    if new < 0:
                        new = 0
                    setattr(target, "damage_reduction", new)
                self._effects.remove(effect)
                summary["expired"].append(effect["name"])

        # decrement cooldowns
        for hid, spells in list(self._cooldowns.items()):
            for spell, remaining in list(spells.items()):
                spells[spell] = remaining - 1
                if spells[spell] <= 0:
                    del spells[spell]
            if not spells:
                del self._cooldowns[hid]

        return summary

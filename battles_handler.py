"""
Handler class, which contains the logic behind the battles.
Heroes can attack to deal damage or heal, deflect or parry to mitigate some of the damage dealt.
"""

from Heroes.hero_base_stats import IBaseHero


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class Attacking:
    # ------------------------------------------------------------------------ #
    def __init__(self, attacker: IBaseHero, defender: IBaseHero, battle_state: "BattleState" = None) -> None:
        self._attacker = attacker
        self._defender = defender
        self._battle_state = battle_state

    # ------------------------------------------------------------------------ #
    def attack(self, selected_spell) -> tuple:
        # selected_spell is expected to be the name of a callable spell on the attacker
        if not isinstance(selected_spell, str):
            raise TypeError("selected_spell must be a string name of the spell method")

        if not hasattr(self._attacker, selected_spell):
            return self._defender, {"spell": selected_spell, "error": "unknown_spell"}

        # Check cooldown (if a BattleState manager is present)
        if self._battle_state is not None and self._battle_state.is_on_cooldown(self._attacker, selected_spell):
            remaining = self._battle_state.cooldowns.get(self._attacker, {}).get(selected_spell, 0)
            return self._defender, {"spell": selected_spell, "on_cooldown": True, "remaining": remaining}

        spell_fn = getattr(self._attacker, selected_spell)

        # Reset spell attributes before casting to avoid stale keys from previous casts
        try:
            self._attacker.set_spell_attributes({})
        except Exception:
            self._attacker.spell_attributes = {}

        # record health before cast to detect heals or other side-effects
        attacker_hp_before = self._attacker.get_current_health()
        defender_hp_before = self._defender.get_current_health()

        # Call the spell method; some spells return None (they may heal or have side-effects)
        result = spell_fn()

        # If the spell returned no actionable result, return info so caller can handle it
        if not result or not isinstance(result, dict):
            return self._defender, {"spell": selected_spell, "result": result}

        # Delegate effect application to BattleState when available
        if self._battle_state is not None:
            try:
                info = self._battle_state.register_spell_cast(self._attacker, self._defender, selected_spell, result)
            except Exception:
                # protect against BattleState bugs - fall back to old behaviour
                damage = int(result.get("spell_damage", 0))
                mitigated = Defending(self._defender).deflect(damage)
                self._defender.apply_damage(mitigated)
                info = {
                    "spell": selected_spell,
                    "raw_result": dict(result),
                    "immediate_damage": damage,
                    "damage_applied": mitigated,
                }

            # compute heal/damage deltas for clearer reporting
            attacker_hp_after = self._attacker.get_current_health()
            defender_hp_after = self._defender.get_current_health()
            info["healed"] = max(0, attacker_hp_after - attacker_hp_before)
            # if BattleState already reported damage_applied, keep it; otherwise compute
            if "damage_applied" not in info or info.get("damage_applied", 0) == 0:
                info["damage_applied"] = max(0, defender_hp_before - defender_hp_after)

            return self._defender, info

        # Fallback (no BattleState): apply immediate damage only
        damage = int(result.get("spell_damage", 0))
        defender_layer = Defending(self._defender)
        mitigated = defender_layer.deflect(damage)

        if hasattr(self._defender, "apply_damage"):
            self._defender.apply_damage(mitigated)
        else:
            if hasattr(self._defender, "_curr_health"):
                self._defender._curr_health -= mitigated
            else:
                curr = getattr(self._defender, "curr_health", getattr(self._defender, "max_health", 0))
                try:
                    setattr(self._defender, "curr_health", curr - mitigated)
                except Exception:
                    pass

        attacker_hp_after = self._attacker.get_current_health()
        defender_hp_after = self._defender.get_current_health()
        info = {
            "spell": selected_spell,
            "raw_result": dict(result),
            "immediate_damage": damage,
            "damage_applied": mitigated,
            "healed": max(0, attacker_hp_after - attacker_hp_before),
        }

        return self._defender, info

    # ------------------------------------------------------------------------ #
    def heal(self, hp_restore) -> None:
        self._attacker.heal_up(hp_restore)


# ---------------------------------------------------------------------------- #
class Defending:

    # ------------------------------------------------------------------------ #
    def __init__(self, defender: IBaseHero) -> None:
        self._defender = defender

    # ------------------------------------------------------------------------ #
    def deflect(self, damage: int) -> int:
        damage_reduction = self._defender.get_current_damage_reduction()
        mitigated_damage = damage - damage_reduction
        if mitigated_damage < 0:
            mitigated_damage = 0
        return mitigated_damage

    # ------------------------------------------------------------------------ #
    def parry(self, damage: int) -> int:
        return self.deflect(damage)


# --------------------------------------------------------------------------- #
# BattleState: manage persistent effects (DOT, damage-reduction) and cooldowns
# --------------------------------------------------------------------------- #


class BattleState:
    """Simple battle manager to track active effects and per-hero cooldowns.

    This is intentionally minimal: it registers spell casts, applies immediate
    damage, registers multi-turn effects (damage over time, damage reduction)
    and ticks them each turn.
    """

    def __init__(self, hero_a: IBaseHero, hero_b: IBaseHero) -> None:
        self.heroes = [hero_a, hero_b]
        self.effects: dict = {hero_a: [], hero_b: []}
        self.cooldowns: dict = {hero_a: {}, hero_b: {}}

    def register_spell_cast(self, caster: IBaseHero, target: IBaseHero, spell_name: str, result: dict) -> None:
        # Always return a summary dict describing what was applied so callers
        # (e.g. the CLI) can display meaningful output.
        info = {
            "spell": spell_name,
            "raw_result": dict(result) if isinstance(result, dict) else result,
            "immediate_damage": 0,
            "damage_applied": 0,
            "health_leech": 0,
            "turns_active": int(result.get("turns_active", 0) or 0) if isinstance(result, dict) else 0,
            "cooldown": int(result.get("cooldown", 0) or 0) if isinstance(result, dict) else 0,
        }

        if not isinstance(result, dict):
            return info

        # set cooldown for caster (if any)
        cd = int(result.get("cooldown", 0))
        if cd > 0:
            self.cooldowns.setdefault(caster, {})[spell_name] = cd

        # immediate damage: prefer 'spell_damage', fallback to 'initial_spell_damage'
        damage = int(result.get("spell_damage", 0) or result.get("initial_spell_damage", 0) or 0)
        info["immediate_damage"] = damage
        if damage > 0:
            mitigated = Defending(target).deflect(damage)
            target.apply_damage(mitigated)
            info["damage_applied"] = mitigated

        # immediate heal/leech to caster (if present)
        health_leech = int(result.get("health_leech", 0) or 0)
        info["health_leech"] = health_leech
        if health_leech > 0:
            caster.apply_heal(health_leech)

        # multi-turn effects
        turns = int(result.get("turns_active", 0) or 0)
        if turns > 0:
            # decide which hero the effect applies to: default to target when
            # the spell contains damage; otherwise apply to caster (buffs)
            if "spell_damage" in result or "initial_spell_damage" in result or "damage_over_time" in result:
                eff_target = target
            else:
                eff_target = caster

            effect = {"name": spell_name, "remaining": turns, "data": dict(result), "source": caster}

            # if effect grants damage reduction, apply it immediately and store previous
            if "damage_reduction" in result:
                prev = eff_target.get_current_damage_reduction()
                effect["_prev_damage_reduction"] = prev
                eff_target.set_damage_reduction(int(result.get("damage_reduction", 0)))

            self.effects.setdefault(eff_target, []).append(effect)

        return info

    def tick(self) -> None:
        # process effects (damage over time and expiration)
        for hero in list(self.heroes):
            new_effects = []
            for eff in list(self.effects.get(hero, [])):
                if eff.get("remaining", 0) <= 0:
                    # expired; revert damage reduction if we changed it
                    if "_prev_damage_reduction" in eff:
                        hero.set_damage_reduction(eff["_prev_damage_reduction"])
                    continue

                # apply DOT if present
                dot = int(eff["data"].get("damage_over_time", 0) or 0)
                if dot > 0:
                    mitigated = Defending(hero).deflect(dot)
                    hero.apply_damage(mitigated)

                    # health leech for source (if configured)
                    hl = int(eff["data"].get("health_leech", 0) or 0)
                    if hl > 0 and eff.get("source"):
                        eff["source"].apply_heal(hl)

                # decrement and keep if still active
                eff["remaining"] -= 1
                if eff["remaining"] > 0:
                    new_effects.append(eff)
                else:
                    if "_prev_damage_reduction" in eff:
                        hero.set_damage_reduction(eff["_prev_damage_reduction"])

            self.effects[hero] = new_effects

        # tick cooldowns
        for hero, cds in list(self.cooldowns.items()):
            for spell, val in list(cds.items()):
                if val <= 1:
                    cds.pop(spell, None)
                else:
                    cds[spell] = val - 1

    def is_on_cooldown(self, hero: IBaseHero, spell_name: str) -> bool:
        return bool(self.cooldowns.get(hero, {}).get(spell_name, 0) > 0)

    def get_active_effects(self, hero: IBaseHero):
        return list(self.effects.get(hero, []))

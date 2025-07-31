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
    def __init__(self, attacker: IBaseHero, defender: IBaseHero) -> None:
        self._attacker = attacker
        self._defender = defender

    # ------------------------------------------------------------------------ #
    def attack(self, selected_spell) -> IBaseHero:
        is_spell_valid = hasattr(self._attacker, selected_spell)

        if is_spell_valid:
            # result = is_spell_valid()

            self._defender.curr_health -= result["spell_damage"]

        return self._defender

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

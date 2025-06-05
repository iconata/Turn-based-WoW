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
    def attack(self, selected_spell):
        is_spell_valid = hasattr(self._attacker, selected_spell)

        if is_spell_valid:
            result = is_spell_valid()

            self._defender.curr_health -= result["spell_damage"]

        return self._defender

    # ------------------------------------------------------------------------ #
    def heal(self, hp_restore):
        self._attacker.heal_up(hp_restore)

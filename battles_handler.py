"""
Handler class, which contains the logic behind the battles.
Heroes can attack to deal damage or heal, deflect or parry to mitigate some of the damage dealt.
"""


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class BattleHandler:

    # ------------------------------------------------------------------------ #
    def __init__(self, first_hero, second_hero) -> None:
        self._first_hero  = first_hero
        self._second_hero = second_hero

    # ------------------------------------------------------------------------ #
    def attack(self, value: int):
        pass

    # ------------------------------------------------------------------------ #
    def heal(self, value: int):
        pass

    # ------------------------------------------------------------------------ #
    def deflect(self, value: int):
        pass

    # ------------------------------------------------------------------------ #
    def parry(self, value: int):
        pass

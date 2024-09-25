"""
Handler class, used to cast different types of spells, based on the selected role of the hero.
"""


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class CommonSpellsMixin:

    # ------------------------------------------------------------------------ #
    def cast_divine_protection(self):
        cooldown = 3
        # TODO: add docstring
        # TODO: implement cooldown logic

        percent_damage_reduction = 20

    # ------------------------------------------------------------------------ #
    def cast_divine_shield(self):
        cooldown = 9
        # TODO: add docstring
        # TODO: implement cooldown logic

        percent_damage_reduction = 100


# ---------------------------------------------------------------------------- #
class RetributionPaladinSpells(CommonSpellsMixin):

    # ------------------------------------------------------------------------ #
    def __init__(self):
        self._holy_power     = 0
        self._max_holy_power = 5

    # ------------------------------------------------------------------------ #
    def cast_judgement(self):
        # TODO: add docstring
        holy_power_generation = 2
        self._holy_power     += holy_power_generation

        self._check_holy_power(holy_power_generation)

    # ------------------------------------------------------------------------ #
    def cast_word_of_glory(self):
        # TODO: Implement heal percent of max hero hp. This is a strong healing spell.
        # TODO: add docstring
        cost = 3
        if self._holy_power < 3:
            print(f"Not enough Holy Power! You need at least 3 and you have {self._holy_power}")
            # TODO: Implement wait for input after printing out message

        self._holy_power -= cost

        self._check_holy_power()

    # ------------------------------------------------------------------------ #
    def cast_blade_of_justice(self):
        # TODO: add docstring
        holy_power_generation = 2
        self._holy_power     += holy_power_generation

        self._check_holy_power(holy_power_generation)

    # ------------------------------------------------------------------------ #
    def cast_final_verdict(self):
        # TODO: add docstring
        cost = 3
        if self._holy_power < 3:
            print(f"Not enough Holy Power! You need at least 3 and you have {self._holy_power}")
            # TODO: Implement wait for input after printing out message

        self._holy_power -= cost

        self._check_holy_power()

    # ------------------------------------------------------------------------ #
    def display_amount_of_holy_power(self):
        # TODO: add docstring
        print(f"Holy power: {self._holy_power}")

    # ------------------------------------------------------------------------ #
    def _check_holy_power(self, holy_power_generated=0):
        # TODO: add docstring
        # if the holy power becomes a negative number, it will be changed to 0. Negative power should not be possible.
        if self._holy_power < 0:
            self._holy_power = 0

        # if the holy power becomes a larger than max_holy_power, value will be changed to the max.
        elif self._holy_power + holy_power_generated >= self._max_holy_power:
            print("MAX holy power!")
            self._holy_power = self._max_holy_power


# ---------------------------------------------------------------------------- #
class HolyPaladinSpells(CommonSpellsMixin):
    def __init__(self):
        pass  # placeholder


# ---------------------------------------------------------------------------- #
class ProtectionPaladinSpells(CommonSpellsMixin):
    def __init__(self):
        pass  # placeholder

import math

from Heroes.hero_base_stats import BaseHeroStats


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class CommonSpellsMixin:
    # ------------------------------------------------------------------------ #
    def _is_chi_spent(self, chi_cost):
        pass

    # ------------------------------------------------------------------------ #
    def _heal_up(self, heal_ammount):
        pass

    # ------------------------------------------------------------------------ #
    def cast_spinning_crane_kick(self):
        pass

    # ------------------------------------------------------------------------ #
    def cast_vivify(self):
        pass


# ---------------------------------------------------------------------------- #
class WindwalkerMonkSpells(BaseHeroStats, CommonSpellsMixin):
    # ------------------------------------------------------------------------ #
    # TODO: add docstring
    def __init__(self):
        self._curr_chi              = 0
        self._max_chi               = 5
        self._health                = 800
        self._secondary_pool        = 300
        self._attack_power          = 65
        self._max_damage_red        = 100
        self._max_health            = self._health
        self._max_mana              = self._secondary_pool
        self._base_damage_red       = self._damage_reduction
        self._current_damage_red    = self._damage_reduction

    # ------------------------------------------------------------------------ #
    def cast_tiger_palm(self):
        pass

    # ------------------------------------------------------------------------ #
    def cast_rising_sun_kick(self):
        pass

    # ------------------------------------------------------------------------ #
    def cast_fists_of_fury(self):
        pass

    # ------------------------------------------------------------------------ #
    def cast_whirling_dragon_punch(self):
        pass


# ---------------------------------------------------------------------------- #
class BrewmasterMonkSpells(BaseHeroStats, CommonSpellsMixin):
    # ------------------------------------------------------------------------ #
    # TODO: add docstring
    def __init__(self):
        self._curr_chi              = 0
        self._max_chi               = 5
        self._health                = 1100
        self._secondary_pool        = 200
        self._attack_power          = 45
        self._spell_power           = 30
        self._max_damage_red        = 100
        self._max_health            = self._health
        self._max_mana              = self._secondary_pool
        self._base_damage_red       = self._damage_reduction

    # ------------------------------------------------------------------------ #
    def cast_rushing_jade_wind(self):
        pass

    # ------------------------------------------------------------------------ #
    def cast_chi_burst(self):
        pass

    # ------------------------------------------------------------------------ #
    def cast_keg_smash(self):
        pass

    # ------------------------------------------------------------------------ #
    def cast_blackout_kick(self):
        pass

    # ------------------------------------------------------------------------ #
    def cast_breath_of_fire(self):
        pass

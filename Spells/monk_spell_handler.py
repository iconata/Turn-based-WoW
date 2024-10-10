import math

from Heroes.hero_base_stats import BaseHeroStats

# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #


class WindwalkerMonkSpells(BaseHeroStats):

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


# ---------------------------------------------------------------------------- #
class BrewmasterMonkSpells(BaseHeroStats):

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
        self._current_damage_red    = self._damage_reduction

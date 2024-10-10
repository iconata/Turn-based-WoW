import math

from Heroes.hero_base_stats import BaseHeroStats


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class EnhancementShamanSpells(BaseHeroStats):

    # ------------------------------------------------------------------------ #
    # TODO: add docstring
    def __init__(self):
        self._curr_maelstrom_stacks = 0
        self._max_maelstrom_stacks  = 5
        self._health                = 850
        self._secondary_pool        = 300
        self._attack_power          = 35
        self._spell_power           = 60
        self._max_damage_red        = 100
        self._max_health            = self._health
        self._max_mana              = self._secondary_pool
        self._base_damage_red       = self._damage_reduction
        self._current_damage_red    = self._damage_reduction

    # ------------------------------------------------------------------------ #
    def cast_strormstrike(self):
        pass


# ---------------------------------------------------------------------------- #
class ElementalShamanSpells(BaseHeroStats):

    # ------------------------------------------------------------------------ #
    # TODO: add docstring
    def __init__(self):
        self._curr_maelstrom_stacks = 0
        self._max_maelstrom_stacks  = 5
        self._health                = 750
        self._secondary_pool        = 750
        self._spell_power           = 100
        self._max_damage_red        = 100
        self._max_health            = self._health
        self._max_mana              = self._secondary_pool
        self._base_damage_red       = self._damage_reduction
        self._current_damage_red    = self._damage_reduction

    # ------------------------------------------------------------------------ #
    def cast_strormstrike(self):
        pass

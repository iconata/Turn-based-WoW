import math

from Heroes.hero_base_stats import BaseHeroStats


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class CommonSpellsMixin:
    # ------------------------------------------------------------------------ #
    def cast_lighting_bolt(self):
        raise NotImplementedError

    # ------------------------------------------------------------------------ #
    def cast_flame_shock(self):
        raise NotImplementedError

    # ------------------------------------------------------------------------ #
    def cast_primordial_wave(self):
        raise NotImplementedError

    # ------------------------------------------------------------------------ #
    def cast_lava_burst(self):
        raise NotImplementedError


# ---------------------------------------------------------------------------- #
class EnhancementShamanSpells(BaseHeroStats, CommonSpellsMixin):
    # ------------------------------------------------------------------------ #
    # TODO: add docstring
    def __init__(self):
        self._curr_maelstrom_stacks = 0
        self._max_maelstrom_stacks = 5
        self._health = 850
        self._secondary_pool = 300
        self._attack_power = 35
        self._spell_power = 60
        self._max_damage_red = 100
        self._max_health = self._health
        self._max_mana = self._secondary_pool
        self._base_damage_red = self._damage_reduction
        self._current_damage_red = self._damage_reduction

    # ------------------------------------------------------------------------ #
    def cast_strormstrike(self):
        raise NotImplementedError

    # ------------------------------------------------------------------------ #
    def cast_lava_lash(self):
        raise NotImplementedError

    # ------------------------------------------------------------------------ #
    def cast_tempest(self):
        raise NotImplementedError

    # ------------------------------------------------------------------------ #
    def cast_feral_spirit(self):
        raise NotImplementedError


# ---------------------------------------------------------------------------- #
class ElementalShamanSpells(BaseHeroStats, CommonSpellsMixin):
    # ------------------------------------------------------------------------ #
    # TODO: add docstring
    def __init__(self):
        self._curr_maelstrom_stacks = 0
        self._max_maelstrom_stacks = 5
        self._health = 750
        self._secondary_pool = 750
        self._spell_power = 100
        self._max_damage_red = 100
        self._max_health = self._health
        self._max_mana = self._secondary_pool
        self._base_damage_red = self._damage_reduction
        self._current_damage_red = self._damage_reduction

    # ------------------------------------------------------------------------ #
    def cast_earth_shock(self):
        raise NotImplementedError

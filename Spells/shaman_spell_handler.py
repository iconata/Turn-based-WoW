import math

from Heroes.hero_base_stats import BaseHeroStats


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class CommonSpellsMixin:
    """
    Common Spells Mixin
    This class contains the common spells and abilities of the Shaman.
    """

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
    """
    Enhancement Shaman Spells
    This class contains the spells and abilities of the Enhancement Shaman.
    """

    def __init__(self):
        super().__init__()
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
    """
    Elemental Shaman Spells
    This class contains the spells and abilities of the Elemental Shaman.
    """

    def __init__(self):
        super().__init__()
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

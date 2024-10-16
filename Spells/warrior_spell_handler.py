from Heroes.hero_base_stats import BaseHeroStats


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class FuryWarriorSpells(BaseHeroStats):

    # ------------------------------------------------------------------------ #
    def __init__(self):
        # TODO: add docstring and implementation
        self._curr_rage             = 0
        self._health                = 1000
        self._secondary_pool        = 200
        self._attack_power          = 70
        self._max_health            = self._health
        self._max_rage              = self._secondary_pool
        self._base_damage_red       = self._damage_reduction
        self._current_damage_red    = self._damage_reduction
        self._max_damage_red        = 100

    # ------------------------------------------------------------------------ #
    def cast_bladestorm(self):
        pass

    # ------------------------------------------------------------------------ #
    def cast_rampage(self):
        pass

    # ------------------------------------------------------------------------ #
    def cast_bloodbath(self):
        pass

    # ------------------------------------------------------------------------ #
    def cast_bloodthrist(self):
        pass

    # ------------------------------------------------------------------------ #
    def cast_raging_blow(self):
        pass


# ---------------------------------------------------------------------------- #
class ProtectionWarriorSpells(BaseHeroStats):

    # ------------------------------------------------------------------------ #
    def __init__(self):
        # TODO: add docstring and implementation
        self._curr_rage             = 0
        self._health                = 1500
        self._secondary_pool        = 200
        self._attack_power          = 50
        self._max_health            = self._health
        self._max_rage              = self._secondary_pool
        self._base_damage_red       = self._damage_reduction
        self._current_damage_red    = self._damage_reduction
        self._max_damage_red        = 100

    # ------------------------------------------------------------------------ #
    def cast_charge(self):
        pass

    # ------------------------------------------------------------------------ #
    def cast_shield_block(self):
        pass

    # ------------------------------------------------------------------------ #
    def cast_champions_spear(self):
        pass

    # ------------------------------------------------------------------------ #
    def cast_shield_charge(self):
        pass

    # ------------------------------------------------------------------------ #
    def cast_sheild_slam(self):
        pass

    # ------------------------------------------------------------------------ #
    def cast_ignore_pain(self):
        pass

"""
This module contains a base hero class, to hold basic hero attributes.
"""


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class BaseHeroStats:
    def __init__(self):
        self._health            = 1000
        self._secondary_pool    = 500
        self._spell_power       = 10
        self._attack_power      = 10
        self._damage_reduction  = 0

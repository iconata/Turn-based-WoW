"""
This module contains a base hero class, to hold basic hero attributes.
"""


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class BaseHeroStats:
    """
    Base class for all heroes. This class holds the basic attributes of a hero.
    """

    def __init__(self):
        self._health = 1000
        self._secondary_pool = 500
        self._spell_power = 10
        self._attack_power = 10
        self._damage_reduction = 0
        self._spell_attributes = {
            'spell_cost': 0,
            'spell_damage': 0,
            'cooldown': 0,
            'turns_active': 0,
            'damage_reduction': 0,
        }

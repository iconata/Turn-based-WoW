"""
Base class with attributes, which are similar for every hero.
It is to be used to construct every hero type.
"""


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class Hero:
    """
    Base Hero class

    Args:
        hero_class  (str): Class of the hero.
        hero_role   (str): Role of the hero.

    Returns:
        Hero: Hero instance with base attributes
    """

    # ---------------------------------------------------------------------------- #
    def __init__(self, hero_class: str, hero_role: str):
        """
        Constructor of the Hero class.

        Args:
            hero_class  (str): Class of the hero.
            hero_role   (str): Role of the hero.
        """
        self._health            = 0
        self._attack_power      = 0
        self._spell_power       = 0
        self._secondary_pool    = 0
        self._damage_reduction  = 0
        self._hero_class        = hero_class
        self._hero_role: str    = hero_role

    # ------------------------------------------------------------------------ #
    def create_hero_based_on_role(self):
        """
        Method that creates a hero, based on the input from the user.
        """
        class_and_role_map = {
            "Paladin": {
                "Melee DPS" : {"health": 800, "secondary_pool": 300, "spell_power": 30, "attack_power": 75, "damage_reduction": 0},
                "Tank"      : {"health": 1200, "secondary_pool": 300, "spell_power": 30, "attack_power": 45, "damage_reduction": 0}
            },
            "Warrior": {
                "Tank"      : {"health": 1500, "secondary_pool": 200, "spell_power": 0, "attack_power": 50, "damage_reduction": 0},
                "Melee DPS" : {"health": 1000, "secondary_pool": 300, "spell_power": 0, "attack_power": 70, "damage_reduction": 0},
            },
            "Mage": {
                "Ranged DPS": {"health": 700, "secondary_pool": 900, "spell_power": 110, "attack_power": 10, "damage_reduction": 0},
            },
            "Priest": {
                "Ranged DPS": {"health": 750, "secondary_pool": 900, "spell_power": 90, "attack_power": 10, "damage_reduction": 0},
            },
            "Shaman": {
                "Melee DPS" : {"health": 850, "secondary_pool": 300, "spell_power": 60, "attack_power": 35, "damage_reduction": 0},
                "Ranged DPS": {"health": 750, "secondary_pool": 700, "spell_power": 100, "attack_power": 10, "damage_reduction": 0}
            },
            "Monk": {
                "Melee DPS" : {"health": 800, "secondary_pool": 300, "spell_power": 30, "attack_power": 65, "damage_reduction": 0},
                "Tank"      : {"health": 1100, "secondary_pool": 200, "spell_power": 30, "attack_power": 45, "damage_reduction": 0}
            },
        }

        default_attributes      = {"health": 1000, "secondary_pool": 500, "spell_power": 10, "attack_power": 60, "damage_reduction": 20}

        attributes              = class_and_role_map.get(self._hero_class, {}).get(self._hero_role, default_attributes)

        self._health            = attributes["health"]
        self._secondary_pool    = attributes["secondary_pool"]
        self._spell_power       = attributes["spell_power"]
        self._attack_power      = attributes["attack_power"]
        self._damage_reduction  = attributes["damage_reduction"]

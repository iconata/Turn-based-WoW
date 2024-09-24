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
        self._health          = 0
        self._physical_damage = 0
        self._magic_damage    = 0
        self._secondary_pool  = 0
        self._hero_class      = hero_class
        self._hero_role: str  = hero_role

    # ------------------------------------------------------------------------ #
    def create_hero_based_on_role(self):
        """
        Method that creates a hero, based on the input from the user.
        """
        class_and_role_map = {
            "Paladin": {
                "Healer"    : {"health": 700, "secondary_pool": 900, "magic_damage": 50, "physical_damage": 50},
                "Melee DPS" : {"health": 800, "secondary_pool": 300, "magic_damage": 0, "physical_damage": 95},
                "Tank"      : {"health": 1200, "secondary_pool": 300, "magic_damage": 0, "physical_damage": 55}
            },
            "Warrior": {
                "Tank"      : {"health": 1500, "secondary_pool": 200, "magic_damage": 0, "physical_damage": 60},
                "Melee DPS" : {"health": 1000, "secondary_pool": 300, "magic_damage": 0, "physical_damage": 80},
            },
            "Mage": {
                "Ranged DPS": {"health": 600, "secondary_pool": 900, "magic_damage": 120, "physical_damage": 10},
            },
            "Priest": {
                "Healer"    : {"health": 600, "secondary_pool": 900, "magic_damage": 60, "physical_damage": 10},
                "Ranged DPS": {"health": 600, "secondary_pool": 900, "magic_damage": 100, "physical_damage": 10},
            },
            "Shaman": {
                "Healer"    : {"health": 700, "secondary_pool": 900, "magic_damage": 50, "physical_damage": 10},
                "Melee DPS" : {"health": 850, "secondary_pool": 300, "magic_damage": 70, "physical_damage": 45},
                "Ranged DPS": {"health": 650, "secondary_pool": 700, "magic_damage": 110, "physical_damage": 10}
            },
            "Monk": {
                "Healer"    : {"health": 700, "secondary_pool": 900, "magic_damage": 50, "physical_damage": 50},
                "Melee DPS" : {"health": 800, "secondary_pool": 300, "magic_damage": 30, "physical_damage": 75},
                "Tank"      : {"health": 1100, "secondary_pool": 200, "magic_damage": 0, "physical_damage": 55}
            },
        }

        default_attributes      = {"health": 1000, "secondary_pool": 500, "magic_damage": 30, "physical_damage": 40}

        attributes              = class_and_role_map.get(self._hero_class, {}).get(self._hero_role, default_attributes)

        self._health            = attributes["health"]
        self._secondary_pool    = attributes["secondary_pool"]
        self._magic_damage      = attributes["magic_damage"]
        self._physical_damage   = attributes["physical_damage"]

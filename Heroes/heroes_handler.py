"""
This module creates a hero class, based on the input from the user.
"""

from heroes_base_abilities import Hero


class CreateHero(Hero):
    """
    Create a Hero.

    Args:
        Hero (int, int, int, str, str): Initial attributes for each hero created.
    """

    # ------------------------------------------------------------------------ #
    def __init__(self, hp: int, dmg: int, second_pool: int, hero_type: str, hero_class: str):
        super().__init__(hp, dmg, second_pool, hero_type)

        self._hero_class = hero_class

    # ------------------------------------------------------------------------ #
    @property
    def hero_class(self):
        """
        Getter of the hero class property.

        Returns:
            str: The current class of the hero.
        """
        return self._hero_class

    # ------------------------------------------------------------------------ #
    @hero_class.setter
    def hero_class(self, selected_class: str):
        *possible_classes, = [
            "Paladin",
            "Warrior",
            "Shaman",
            "Priest",
            "Mage",
            "Monk"
        ]

        if selected_class not in possible_classes:
            raise TypeError(
                f"Hero must be one of the predefined classes - {possible_classes}!")

        self._hero_class = selected_class

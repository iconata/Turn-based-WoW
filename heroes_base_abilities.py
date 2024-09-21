"""
Base class with attributes, which are similar for every hero.
It is to be used to construct every hero type.
"""


class Hero:
    """
    Base Hero class

    Raises:
        ValueError: If the given health pool value is below 0.
        ValueError: If the given damage value is below 0.
        ValueError: If the size of the secondary pool is a negative number.
        TypeError : If the selected type is not found in the predefined

    Returns:
        Hero: Hero instance with base attributes
    """

    # ---------------------------------------------------------------------------- #
    def __init__(self, hp: int, dmg: int, second_pool: int, hero_type: str):
        """
        Constructor of the Hero class.

        Args:
            hp          (int): Hero health pool
            dmg         (int): Hero damage
            second_pool (int): Secondary pool of the hero.
            hero_type   (str): Type of the hero.
        """
        self._health      = hp
        self._damage      = dmg
        self._second_pool = second_pool
        self._hero_type: str   = hero_type

    # ---------------------------------------------------------------------------- #
    @property
    def health(self):
        """
        Getter fo the health property.

        Returns:
            int: Current health pool of the hero
        """
        return self._health

    # ---------------------------------------------------------------------------- #
    @health.setter
    def health(self, value: int):
        """
        Setter of the health pool property. If the given value is below 0, a ValueError is raised.

        Args:
            value (int): Health pool of the hero. Must be a value above 0.

        Raises:
            ValueError: If the given health pool value is below 0.
        """

        if value <= 0:
            raise ValueError(
                "Health must be above 0! Hero cannot be dead when created.")

        self._health = value

    # ---------------------------------------------------------------------------- #
    @property
    def damage(self):
        """
        Getter of the damage property.

        Returns:
            int: Damage of the hero
        """
        return self._damage

    # ---------------------------------------------------------------------------- #
    @damage.setter
    def damage(self, value: int):
        """
        Setter of the damage property. If the given value is below 0, a ValueError is raised.

        Args:
            value (int): Damage of the hero. Must be a value above 0.

        Raises:
            ValueError: If the given damage value is below 0.
        """

        if value <= 0:
            raise ValueError(
                "Damage must be at least 1! Hero cannot do 0 damage.")

        self._damage = value

    # ---------------------------------------------------------------------------- #
    @property
    def second_pool(self):
        """
        Getter of the mana pool property.

        Returns:
            int: Current mana pool of the hero
        """
        return self._second_pool

    # ---------------------------------------------------------------------------- #
    @second_pool.setter
    def second_pool(self, value: int):
        """
        Args:
            value (int): size of the secondary pool

        Raises:
            ValueError: If the size of the secondary pool is a negative number.
        """

        if value < 0:
            raise ValueError(
                "Size of secondary pool must be at least 0!")

        self._second_pool = value

    # ------------------------------------------------------------------------ #
    @property
    def hero_type(self):
        """
        Getter for the hero_type property.

        Returns:
            str: Type of the hero selected.
        """
        return self._hero_type

    # ------------------------------------------------------------------------ #
    @hero_type.setter
    def hero_type(self, value: str):
        """
        Setter for the hero_type property.

        Args:
            value (str): selected type

        Raises:
            TypeError: If the selected type is not found in the predefined
        """
        possible_types = [
            "Caster",
            "Melee",
            "Healer",
            "Tank"
        ]

        if value.capitalize() not in possible_types:
            raise TypeError(f"Hero type must be one of the following types - {possible_types}")

        self._hero_type = value

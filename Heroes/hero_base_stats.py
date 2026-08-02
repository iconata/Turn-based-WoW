"""
This module contains a base hero class, to hold basic hero attributes.
"""

from abc import ABC, abstractmethod


# ---------------------------------------------------------------------------- #
#                                  Base Class                                  #
# ---------------------------------------------------------------------------- #
class IBaseHero(ABC):
    """
    Base interface class for all heroes. This class holds the basic attributes of a hero as well
    as all common spells.
    """

    # ------------------------------------------------------------------------ #
    def __init__(self) -> None:
        """Initialize the base hero stats and default spell template.

        Sets sensible defaults for health, secondary resource pool and
        basic combat stats. Also creates a template ``spell_attributes``
        dictionary which individual spells copy and return when cast.
        """
        self.max_health: int = 1000
        self.max_secondary_pool: int = 500
        self.spell_power: int = 10
        self.attack_power: int = 10
        self.damage_reduction: int = 0
        self.max_damage_reduction: int = 100
        self.spell_attributes = {
            "spell_cost": 0,
            "spell_damage": 0,
            "cooldown": 0,
            "turns_active": 0,
            "damage_reduction": 0,
            "initial_spell_damage": 0,
            "health_leech": 0,
            "damage_over_time": 0,
        }

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of the hero class.

        Returns:
            str: name of the hero class
        """
        raise NotImplementedError

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def create_hero(self, hero_instance: "IBaseHero"):
        """
        Create a hero based on the instance provided.

        Args:
            hero_instance (IBaseHero): class instance

        Raises:
            NotImplementedError: the method must be implemented in the child class

        Returns:
            Any: class instance
        """
        raise NotImplementedError

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def heal_up(self, heal_amount: int) -> None:
        """
        Healing method, which is to be implemented in the child class.

        Args:
            heal_amount (int): amount to heal

        Raises:
            NotImplementedError: if the abstract method is not implemented in the child class, raise an Exception.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def is_specific_stat_spent(self, stat_value: int) -> bool:
        """
        Checker if class specific stat is enough and if it can be cast. Every child class should
        implement and make use of the specific class attribute. For example - Paladin uses holy power, Warrior - rage.

        Args:
            stat_value (int): _description_

        Returns:
            bool: True if spent, else False

        Raises:
            NotImplementedError: if the abstract method is not implemented in the child class, raise an Exception.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def add_specific_stat(self, stat_value: int) -> None:
        """
        Adds the passed, class specific stat to the total amount. Each child class should implement it and check
        if by adding the value, the max amount of the stat will be exceed.

        Args:
            stat_value (int): class specific stat to be added

        Raises:
            NotImplementedError: if the abstract method is not implemented in the child class, raise an Exception.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------- #
#                                    Getters                                   #
# ---------------------------------------------------------------------------- #
class ICommonGetters(ABC):
    """Interface for read-only accessors to a hero's runtime state.

    Implementations should return values such as the hero's current
    health, secondary resource (mana/rage), and offensive stats.
    """
    # ------------------------------------------------------------------------ #
    @abstractmethod
    def get_current_health(self, hero_instance: IBaseHero) -> int:
        """Return the hero's current health.

        Concrete implementations should return the current health value for the
        provided hero instance.
        """
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def get_current_secondary_pool(self, hero_instance: IBaseHero) -> int:
        """Return the current value of the hero's secondary resource (mana, rage, etc.)."""
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def get_current_spell_power(self, hero_instance: IBaseHero) -> int:
        """Return the current spell power/stat used for spell damage calculations."""
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def get_current_attack_power(self, hero_instance: IBaseHero) -> int:
        """Return the current attack power value for the hero instance."""
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def get_current_damage_reduction(self, hero_instance: IBaseHero) -> int:
        """Return the hero's current damage reduction value (flat amount)."""
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def get_current_spell_attributes(self, hero_instance: IBaseHero) -> dict[str, int]:
        """Return the dictionary of current spell attributes for the hero."""
        pass


# ---------------------------------------------------------------------------- #
#                                    Setters                                   #
# ---------------------------------------------------------------------------- #
class ICommonSetters(ABC):
    """Interface for mutating a hero's runtime state.

    Methods allow setting health, resource pools, stats and the
    per-hero spell attribute dictionary.
    """
    @abstractmethod
    def set_health(self, value: int, hero_instance: IBaseHero) -> None:
        """Set the hero's current health to ``value`` (clamped to max health)."""
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def set_secondary_pool(self, value: int, hero_instance: IBaseHero) -> None:
        """Set the hero's secondary resource (mana/rage) to ``value``."""
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def set_spell_power(self, value: int, hero_instance: IBaseHero) -> None:
        """Set the hero's spell power value to ``value``."""
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def set_attack_power(self, value: int, hero_instance: IBaseHero) -> None:
        """Set the hero's attack power value to ``value``."""
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def set_damage_reduction(self, value: int, hero_instance: IBaseHero) -> None:
        """Set the hero's damage reduction to ``value`` (clamped if needed)."""
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def set_spell_attributes(
        self, value: dict[str, int], hero_instance: IBaseHero
    ) -> None:
        """Replace the hero's current spell attributes dictionary with ``value``."""
        pass


# ---------------------------------------------------------------------------- #
#                                   Checkers                                   #
# ---------------------------------------------------------------------------- #
class ICommonCheckers(ABC):
    """Interface exposing boolean checks about a hero's state.

    Examples include whether the hero is alive, low on resource, or
    currently prevented from casting by cooldowns.
    """
    # ------------------------------------------------------------------------ #
    @abstractmethod
    def is_secondary_pool_zero(self, hero_instance: IBaseHero) -> bool:
        """Return True if the hero's secondary resource pool is zero."""
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def is_damage_reduction_zero(self, hero_instance: IBaseHero) -> bool:
        """Return True if the hero currently has zero damage reduction."""
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def is_alive(self, hero_instance: IBaseHero) -> bool:
        """Return True if the hero's current health is greater than zero."""
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def is_on_cooldown(self, hero_instance: IBaseHero) -> bool:
        """Return True if the hero has active cooldowns preventing spell casts."""
        pass

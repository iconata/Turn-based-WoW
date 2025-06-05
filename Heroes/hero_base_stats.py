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
    # ------------------------------------------------------------------------ #
    @abstractmethod
    def get_current_health(self, hero_instance: IBaseHero) -> int:
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def get_current_secondary_pool(self, hero_instance: IBaseHero) -> int:
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def get_current_spell_power(self, hero_instance: IBaseHero) -> int:
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def get_current_attack_power(self, hero_instance: IBaseHero) -> int:
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def get_current_damage_reduction(self, hero_instance: IBaseHero) -> int:
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def get_current_spell_attributes(self, hero_instance: IBaseHero) -> dict[str, int]:
        pass


# ---------------------------------------------------------------------------- #
#                                    Setters                                   #
# ---------------------------------------------------------------------------- #
class ICommonSetters(ABC):
    @abstractmethod
    def set_health(self, value: int, hero_instance: IBaseHero) -> None:
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def set_secondary_pool(self, value: int, hero_instance: IBaseHero) -> None:
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def set_spell_power(self, value: int, hero_instance: IBaseHero) -> None:
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def set_attack_power(self, value: int, hero_instance: IBaseHero) -> None:
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def set_damage_reduction(self, value: int, hero_instance: IBaseHero) -> None:
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def set_spell_attributes(
        self, value: dict[str, int], hero_instance: IBaseHero
    ) -> None:
        pass


# ---------------------------------------------------------------------------- #
#                                   Checkers                                   #
# ---------------------------------------------------------------------------- #
class ICommonCheckers(ABC):
    # ------------------------------------------------------------------------ #
    @abstractmethod
    def is_secondary_pool_zero(self, hero_instance: IBaseHero) -> bool:
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def is_damage_reduction_zero(self, hero_instance: IBaseHero) -> bool:
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def is_alive(self, hero_instance: IBaseHero) -> bool:
        pass

    # ------------------------------------------------------------------------ #
    @abstractmethod
    def is_on_cooldown(self, hero_instance: IBaseHero) -> bool:
        pass

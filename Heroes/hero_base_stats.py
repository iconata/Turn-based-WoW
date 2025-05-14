"""
This module contains a base hero class, to hold basic hero attributes.
"""

from abc import ABC, abstractmethod
from typing import Any

"""
Steps to create a strategy pattern:
    1. Create an interface for the strategy.
        - The interface will contain the common spells, that are used by each class
    2. Create concrete classes that implement the strategy interface.
        - Every hero class will implement the specific classes
    3. Create a context class that uses the strategy interface
        - caller class, which knows that the given instance will contain an implemetation of the interface.
    4. Use the context class to call the strategy.
        - Context class will be contained used by the battles or other actions
    5. Create a factory class to create the context class.
        - Factory class to create a hero of a certain type
    6. Use the factory class to create the context class.
        - TBD
    7. Use the context class to call the strategy.
        - TBD
"""


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class IBaseHero(ABC):
    """
    Base interface class for all heroes. This class holds the basic attributes of a hero as well
    as all common spells.
    """

    def __init__(self) -> None:
        self.max_health = 1000
        self.max_secondary_pool = 500
        self.spell_power = 10
        self.attack_power = 10
        self.damage_reduction = 0
        self.max_damage_reduction = 100
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

    @abstractmethod
    def create_hero(self, hero_instance) -> Any:
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


class ICommonGetters(ABC):
    """
    Abstract class for all heroes. This class holds the common methods for all heroes.
    """

    @abstractmethod
    def get_current_health(self, hero_instance: IBaseHero) -> int:
        pass

    @abstractmethod
    def get_current_secondary_pool(self, hero_instance: IBaseHero) -> int:
        pass

    @abstractmethod
    def get_current_spell_power(self, hero_instance: IBaseHero) -> int:
        pass

    @abstractmethod
    def get_current_attack_power(self, hero_instance: IBaseHero) -> int:
        pass

    @abstractmethod
    def get_current_damage_reduction(self, hero_instance: IBaseHero) -> int:
        pass

    @abstractmethod
    def get_current_spell_attributes(self, hero_instance: IBaseHero) -> dict:
        pass


class ICommonSetters(ABC):
    @abstractmethod
    def set_health(self, value: int, hero_instance: IBaseHero) -> None:
        pass

    @abstractmethod
    def set_secondary_pool(self, value: int, hero_instance: IBaseHero) -> None:
        pass

    @abstractmethod
    def set_spell_power(self, value: int, hero_instance: IBaseHero) -> None:
        pass

    @abstractmethod
    def set_attack_power(self, value: int, hero_instance: IBaseHero) -> None:
        pass

    @abstractmethod
    def set_damage_reduction(self, value: int, hero_instance: IBaseHero) -> None:
        pass

    @abstractmethod
    def set_spell_attributes(self, value: dict, hero_instance: IBaseHero) -> None:
        pass


class ICommonCheckers(ABC):
    @abstractmethod
    def is_secondary_pool_zero(self, hero_instance: IBaseHero) -> bool:
        pass

    @abstractmethod
    def is_spell_power_zero(self, hero_instance: IBaseHero) -> bool:
        pass

    @abstractmethod
    def is_damage_reduction_zero(self, hero_instance: IBaseHero) -> bool:
        pass

    @abstractmethod
    def is_alive(self, hero_instance: IBaseHero) -> bool:
        pass

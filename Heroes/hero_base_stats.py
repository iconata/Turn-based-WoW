"""
This module contains a base hero class, to hold basic hero attributes.
"""
from abc import ABC, abstractmethod

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

    @abstractmethod
    def heal_up(self) -> None:
        pass

    @abstractmethod
    def is_specific_stat_spent(self, value: int) -> bool:
        pass

    @abstractmethod
    def add_specific_stat(self, value: int) -> None:
        pass


class ICommonGetters(ABC):
    """
    Abstract class for all heroes. This class holds the common methods for all heroes.
    """

    @abstractmethod
    def get_health(self, hero_instance: IBaseHero) -> int:
        pass

    @abstractmethod
    def get_secondary_pool(self, hero_instance: IBaseHero) -> int:
        pass

    @abstractmethod
    def get_spell_power(self, hero_instance: IBaseHero) -> int:
        pass

    @abstractmethod
    def get_attack_power(self, hero_instance: IBaseHero) -> int:
        pass

    @abstractmethod
    def get_damage_reduction(self, hero_instance: IBaseHero) -> int:
        pass

    @abstractmethod
    def get_spell_attributes(self, hero_instance: IBaseHero) -> dict:
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
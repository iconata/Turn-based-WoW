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

    # -------------------------------------------------------------------- #
    # Default concrete helpers (provide a stable, instance-based API)
    # These are offered as defaults so other modules can rely on consistent
    # hero methods without requiring every spell handler to reimplement them.
    # -------------------------------------------------------------------- #
    def get_current_health(self) -> int:
        return getattr(self, "_curr_health", self.max_health)

    def get_current_secondary_pool(self) -> int:
        if hasattr(self, "_curr_mana"):
            return self._curr_mana
        return getattr(self, "_curr_secondary_pool", self.max_secondary_pool)

    def get_current_spell_power(self) -> int:
        return getattr(self, "spell_power", 0)

    def get_current_attack_power(self) -> int:
        return getattr(self, "attack_power", 0)

    def get_current_damage_reduction(self) -> int:
        return getattr(self, "damage_reduction", 0)

    def get_current_spell_attributes(self) -> dict:
        return dict(getattr(self, "spell_attributes", {}))

    def set_health(self, value: int) -> None:
        if not hasattr(self, "_curr_health"):
            self._curr_health = self.max_health
        self._curr_health = max(0, min(self.max_health, int(value)))

    def set_secondary_pool(self, value: int) -> None:
        if hasattr(self, "_curr_mana"):
            self._curr_mana = max(0, int(value))
        else:
            self._curr_secondary_pool = max(0, int(value))

    def set_spell_power(self, value: int) -> None:
        self.spell_power = int(value)

    def set_attack_power(self, value: int) -> None:
        self.attack_power = int(value)

    def set_damage_reduction(self, value: int) -> None:
        self.damage_reduction = int(value)

    def set_spell_attributes(self, value: dict, hero_instance: "IBaseHero" = None) -> None:
        # Accept both dict-like values and copy them so callers don't mutate internals
        self.spell_attributes = dict(value or {})

    def is_secondary_pool_zero(self) -> bool:
        return self.get_current_secondary_pool() <= 0

    def is_damage_reduction_zero(self) -> bool:
        return self.get_current_damage_reduction() <= 0

    def is_alive(self) -> bool:
        return self.get_current_health() > 0

    def is_on_cooldown(self) -> bool:
        # Basic fallback: check if spell_attributes expose a cooldown > 0
        return bool(self.spell_attributes.get("cooldown", 0) > 0)

    def apply_damage(self, amount: int) -> None:
        amount = max(0, int(amount))
        self.set_health(self.get_current_health() - amount)

    def apply_heal(self, amount: int) -> None:
        amount = max(0, int(amount))
        self.set_health(self.get_current_health() + amount)

    def reduce_secondary_pool(self, amount: int) -> None:
        amount = max(0, int(amount))
        self.set_secondary_pool(self.get_current_secondary_pool() - amount)


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

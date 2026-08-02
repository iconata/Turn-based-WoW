"""Spell handler library containing all Warrior spells (Fury and Protection)."""

import math

from turn_based_wow.heroes.hero_base_stats import IBaseHero


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class WarriorCommonSpells(IBaseHero):
    """
    Common Spells Mixin
    This class contains the common spells and abilities of the Warrior.
    """

    # ------------------------------------------------------------------------ #
    def __init__(self) -> None:
        """Initialize shared Warrior stats: rage pool and current health."""
        super().__init__()
        self._curr_rage = 0
        self._curr_health = self.max_health
        self._max_rage = self.max_secondary_pool

    # ------------------------------------------------------------------------ #
    def create_hero(self, hero_instance: IBaseHero):
        """Apply spec-specific stat overrides for Fury and Protection Warriors."""
        if isinstance(hero_instance, FuryWarriorSpells):
            hero_instance.max_health = 1000
            hero_instance.max_secondary_pool = 200
            hero_instance.attack_power = 70

        elif isinstance(hero_instance, ProtectionWarriorSpells):
            hero_instance.max_health = 1500
            hero_instance.max_secondary_pool = 200
            hero_instance.attack_power = 50

        return hero_instance

    # ------------------------------------------------------------------------ #
    def is_specific_stat_spent(self, stat_value: int) -> bool:
        """Return True and deduct rage when the warrior has at least ``stat_value`` rage.

        Args:
            stat_value: rage cost to check and deduct.
        """
        if self._curr_rage >= stat_value:
            self._curr_rage -= stat_value
            return True

        return False

    # ------------------------------------------------------------------------ #
    def heal_up(self, heal_amount: float) -> None:
        """
        Check if the amount of incoming heal will overheal and the max health will
        be exceeded. If so, set the health to the max health.
        If not, add the heal amount to the current health.

        Args:
            heal_ammount (float): amount of incoming heal
        """

        if self._curr_health + heal_amount > self.max_health:
            self._curr_health = self.max_health
        else:
            self._curr_health += heal_amount

    # ------------------------------------------------------------------------ #
    def add_specific_stat(self, stat_value: int) -> None:
        """
        Checks if the amount of generated rage will exceed the max rage.
        If so, set the rage to the max rage.

        Args:
            stat_value (int): amount of generated rage
        """

        if self._curr_rage + stat_value > self._max_rage:
            self._curr_rage = self._max_rage
        else:
            self._curr_rage += stat_value


# ---------------------------------------------------------------------------- #
class FuryWarriorSpells(WarriorCommonSpells):
    """
    Fury Warrior Spells.
    This class contains the spells and abilities of the Fury Warrior.
    It inherits from the IBaseHero class and implements the spells and abilities of the Fury Warrior.
    """

    # ------------------------------------------------------------------------ #
    def get_name(self) -> str:
        """Return the display name of this hero class."""
        return "Fury Warrior"

    # ------------------------------------------------------------------------ #
    def cast_bladestorm(self) -> dict[str, int]:
        """
        Become and unstoppable storm of destructive force, striking your enemy,
        dealing Physiscal damage.

        Returns:
            dict: spell damage, cooldown
        """
        rage_generated = 10
        self.add_specific_stat(rage_generated)

        attrs = dict(self.spell_attributes)
        attrs["spell_cost"] = 0
        attrs["spell_damage"] = math.ceil(self.attack_power * 140 / 100)
        attrs["cooldown"] = 8

        return attrs

    # ------------------------------------------------------------------------ #
    def cast_rampage(self) -> dict[str, int] | None:
        """
        Enrages you and unleashes a flurry of brutal attacks, dealing Physical damage.
        The spell requires 80 rage to cast.

        Returns:
            dict: spell_cost, spell_damage
        """

        attrs = dict(self.spell_attributes)
        attrs["spell_cost"] = 80
        attrs["spell_damage"] = math.ceil(self.attack_power * 230 / 100)

        return attrs if self.is_specific_stat_spent(attrs["spell_cost"]) else None

    # ------------------------------------------------------------------------ #
    def cast_bloodbath(self) -> dict[str, int]:
        """
        Assault the target in a bloodthirsty craze, dealing Physical damage and
        restoring 3% of your health.

        Returns:
            dict: spell_cost, spell_damage, cooldown
        """
        rage_generated = 8
        health_restored = math.ceil(self.max_health * 3 / 100)

        self.add_specific_stat(rage_generated)
        self.heal_up(health_restored)

        attrs = dict(self.spell_attributes)
        attrs["spell_cost"] = 0
        attrs["spell_damage"] = math.ceil(self.attack_power * 390 / 100)
        attrs["cooldown"] = 3

        return attrs

    # ------------------------------------------------------------------------ #
    def cast_raging_blow(self) -> dict[str, int]:
        """
        A might blow with both weapons, that deals Physical damage.

        Returns:
            dict: spell_cost, spell_damage, cooldown
        """

        rage_generated = 12
        self.add_specific_stat(rage_generated)

        attrs = dict(self.spell_attributes)
        attrs["spell_cost"] = 0
        attrs["spell_damage"] = math.ceil(self.attack_power * 400 / 100)
        attrs["cooldown"] = 4

        return attrs


# ---------------------------------------------------------------------------- #
class ProtectionWarriorSpells(WarriorCommonSpells):
    """
    Protection Warrior Spells.
    This class contains the spells and abilities of the Protection Warrior.
    It inherits from the IBaseHero class and implements the spells and abilities of the Protection Warrior.
    """

    # ------------------------------------------------------------------------ #
    def get_name(self) -> str:
        """Return the display name of this hero class."""
        return "Protection Warrior"

    # ------------------------------------------------------------------------ #
    def cast_charge(self) -> dict[str, int]:
        """
        Charge to an enemy dealing physical damage and generating 20 rage.

        Returns:
            dict: spell_cost, spell_damage, cooldown
        """

        rage_generated = 20
        self.add_specific_stat(rage_generated)

        attrs = dict(self.spell_attributes)
        attrs["spell_cost"] = 0
        attrs["spell_damage"] = math.ceil(self.attack_power * 50 / 100)
        attrs["cooldown"] = 7

        return attrs

    # ------------------------------------------------------------------------ #
    def cast_shield_block(self) -> dict[str, int] | None:
        """
        Raise your shield, blocking 100% of incoming damage for 2 turns.

        Returns:
            dict: spell_cost, damage_reduction, cooldown
        """
        spell_cost = 30

        if self.is_specific_stat_spent(spell_cost):
            attrs = dict(self.spell_attributes)
            attrs["spell_cost"] = 30
            attrs["damage_reduction"] = self.max_damage_reduction
            attrs["cooldown"] = 2

            return attrs

        return None

    # ------------------------------------------------------------------------ #
    def cast_champions_spear(self) -> dict[str, int]:
        """
        Throw a spear at the target, dealing Physical damage and generating 10 rage.

        Returns:
            dict: spell_damage, cooldown
        """

        rage_generated = 10
        self.add_specific_stat(rage_generated)

        attrs = dict(self.spell_attributes)
        attrs["spell_damage"] = math.ceil(self.attack_power * 240 / 100)
        attrs["cooldown"] = 10

        return attrs

    # ------------------------------------------------------------------------ #
    def cast_shield_charge(self) -> dict[str, int]:
        """
        Charge to an enemy with your shield, dealing Physical damage and generating 20 rage.

        Returns:
            dict: spell_cost, spell_damage, cooldown
        """

        rage_generated = 20
        self.add_specific_stat(rage_generated)

        attrs = dict(self.spell_attributes)
        attrs["spell_cost"] = 0
        attrs["spell_damage"] = math.ceil(self.attack_power * 420 / 100)
        attrs["cooldown"] = 8

        return attrs

    # ------------------------------------------------------------------------ #
    def cast_sheild_slam(self) -> dict[str, int]:
        """
        Slams the target with your shield, dealing Physical damage and generating 15 rage.

        Returns:
            dict: spell_cost, spell_damage, cooldown
        """

        rage_generated = 15
        self.add_specific_stat(rage_generated)

        attrs = dict(self.spell_attributes)
        attrs["spell_cost"] = 0
        attrs["spell_damage"] = math.ceil(self.attack_power * 130 / 100)
        attrs["cooldown"] = 2

        return attrs

    # ------------------------------------------------------------------------ #
    def cast_ignore_pain(self) -> dict[str, int] | None:
        """
        Fight through the pain, ingoring 50% of incoming damage for 1 turn.
        This spell costs 35 rage to cast.

        Returns:
            dict: spell_cost, damage_reduction, cooldown, turns_active
        """
        spell_cost = 35

        if self.is_specific_stat_spent(spell_cost):
            attrs = dict(self.spell_attributes)
            attrs["spell_cost"] = 35
            attrs["damage_reduction"] = 50
            attrs["cooldown"] = 0
            attrs["turns_active"] = 1

            return attrs

        return None


# -------------------------------- End of file ------------------------------- #

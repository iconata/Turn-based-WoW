"""
Handler library, used to cast different types of Paladin spells, based on the selected role of the hero.
"""

import math

from Heroes.hero_base_stats import IBaseHero


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class PaladinCommonSpells(IBaseHero):
    """
    Common Spells Mixin
    This class contains the common spells and abilities of the Paladin.
    """

    # ------------------------------------------------------------------------ #
    def __init__(self) -> None:
        super().__init__()
        self._curr_holy_power = 0
        self._max_holy_power = 5
        self._curr_health = self.max_health
        self._curr_mana = self.max_secondary_pool

    # ------------------------------------------------------------------------ #
    def create_hero(self, hero_instance: IBaseHero):
        if isinstance(hero_instance, RetributionPaladinSpells):
            hero_instance.max_health = 800
            hero_instance.max_secondary_pool = 300
            hero_instance.spell_power = 30
            hero_instance.attack_power = 75

        elif isinstance(hero_instance, ProtectionPaladinSpells):
            hero_instance.max_health = 1200
            hero_instance.max_secondary_pool = 300
            hero_instance.spell_power = 30
            hero_instance.attack_power = 45

        return hero_instance

    # ------------------------------------------------------------------------ #
    def cast_divine_shield(self) -> dict[str, int]:
        """
        Powerfull protection spell, which block all incoming damage for 2 turns.
        Cooldown - 15 turns.

        Returns:
            tuple: cooldown of the spell and for how many turns it is active
        """
        self.spell_attributes["cooldown"] = 15
        self.spell_attributes["damage_reduction"] = self.max_damage_reduction
        self.spell_attributes["turns_active"] = 2

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_judgement(self) -> dict[str, int]:
        """
        Judges the target, dealing damage based on the hero's attack power. Generates 1 Holy Power.

        Returns:
            tuple: damage of the spell, cooldown of the spell
        """
        holy_power_generation = 1
        self.spell_attributes["cooldown"] = 3
        self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 61 / 100)
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 5 / 100
        )
        self._curr_mana -= self.spell_attributes["spell_cost"]
        self.add_specific_stat(holy_power_generation)

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_word_of_glory(self) -> None:
        """
        Fairly strong healing spell, healing for percent amount of the hero's spell power.
        Because of the spell cost, the internal logic will check if there's enough holy power so the spell can be cast.
        """
        cost = 3
        amount_to_heal = math.ceil(self.spell_power * 346 / 100)
        if self.is_specific_stat_spent(cost):
            self.heal_up(amount_to_heal)

    # ------------------------------------------------------------------------ #
    def heal_up(self, heal_amount: int) -> None:
        """
        Main healing spell logic. Checks the current health of the hero and also the incoming amount.
        If the incoming amount is overhealing, the current health will be set to the max health.

        Args:
            heal_amount (int): value of the incoming heal
        """
        self._curr_health += heal_amount

        if self._curr_health > self.max_health:
            self._curr_health = self.max_health

    # ------------------------------------------------------------------------ #
    def add_specific_stat(self, stat_value: int = 0) -> None:
        """
        Checks the current amount of holy power available to the hero.
        If the holy power goes beyond the max holy power, the current holy power is set to the max

        Args:
            stat_value (int, optional): Adds the generated holy power to the currently available.
        """

        self._curr_holy_power += stat_value

        if self._curr_holy_power >= self._max_holy_power:
            self._curr_holy_power = self._max_holy_power

    # ------------------------------------------------------------------------ #
    def is_specific_stat_spent(self, stat_value: int) -> bool:
        """
        Boolean check if the hero has enough holy power for the spell that was casted.

        Args:
            stat_value (int): cost of the spell

        Returns:
            bool: returns True if there's enough spell power for the spell, otherwise returns False
        """
        if self._curr_holy_power >= stat_value:
            self._curr_holy_power -= stat_value
            return True
        else:
            return False


# ---------------------------------------------------------------------------- #
class RetributionPaladinSpells(PaladinCommonSpells):
    """
    Class that handles the Retribution Paladin spells.
    """

    # ------------------------------------------------------------------------ #
    def get_name(self) -> str:
        return "Retribution Paladin"

    # ------------------------------------------------------------------------ #
    def cast_divine_protection(self) -> dict[str, int]:
        """
        Protection spell, which reduces the amount of incoming damage by 20%.
        Cooldown - 4 turns.

        Returns:
            tuple: cooldown of the spell, amount of turns for which it is active
        """
        self.spell_attributes["damage_reduction"] = math.ceil(
            self.attack_power * 20 / 100
        )
        self.spell_attributes["cooldown"] = 4
        self.spell_attributes["turns_active"] = 2
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 5 / 100
        )
        self._curr_mana -= self.spell_attributes["spell_cost"]

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_blade_of_justice(self) -> dict[str, int]:
        """
        Pierce the target with a blade of light, dealing percent damage based on the hero's attack power.
        Generates 3 Holy Power.
        Cooldown - 3 turns.

        Returns:
            tuple: damage of the spell, cooldown of the spell
        """
        holy_power_generation = 1
        self.spell_attributes["cooldown"] = 3
        self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 135 / 100)
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 5 / 100
        )
        self._curr_mana -= self.spell_attributes["spell_cost"]
        self.add_specific_stat(holy_power_generation)

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_final_verdict(self) -> dict[str, int] | None:
        """
        Powerfull spell, dealing percent damage based on the hero's attack power.
        Cost - 3 Holy Power.

        Returns:
            tuple: damage of the spell or None if the hero does not have enough holy power
        """
        cost = 3
        if self.is_specific_stat_spent(cost):
            self.spell_attributes["spell_damage"] = math.ceil(
                self.attack_power * 161 / 100
            )
            self.spell_attributes["spell_cost"] = math.ceil(
                self.max_secondary_pool * 7 / 100
            )
            self._curr_mana -= self.spell_attributes["spell_cost"]

            return self.spell_attributes
        else:
            return None

    # ------------------------------------------------------------------------ #
    def cast_wake_of_ashes(self) -> dict[str, int]:
        """
        Lash out at your enemies, dealing heavy weapon damage. Generates 3 Holy Power.
        Cooldown - 6 turns.

        Returns:
            tuple: spell damage, cooldown of the spell.
        """
        holy_power_generated = 3
        self.spell_attributes["cooldown"] = 6
        self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 293 / 100)
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 15 / 100
        )
        self._curr_mana -= self.spell_attributes["spell_cost"]

        self.add_specific_stat(holy_power_generated)

        return self.spell_attributes


# ---------------------------------------------------------------------------- #
class ProtectionPaladinSpells(PaladinCommonSpells):
    """
    Class that handles the Protection Paladin spells.
    """

    # ------------------------------------------------------------------------ #
    def get_name(self) -> str:
        return "Protection Paladin"

    # ------------------------------------------------------------------------ #
    def cast_consecration(self) -> dict[str, int]:
        """
        Ignite the ground beneath you, dealing damage over time to your enemies.
        Turns active - 3.

        Returns:
            tuple: spell damage per turn, turns for which the spell is active
        """
        self.spell_attributes["turns_active"] = 3
        self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 30 / 100)
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 5 / 100
        )
        self._curr_mana -= self.spell_attributes["spell_cost"]

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_blessed_hammer(self) -> dict[str, int]:
        """
        Hurl a blessed hammer to your enemies, dealing holy damage and reducing
        damage taked by 30% from your attack power for 1 turn.

        Returns:
            tuple: damage of the spell, cooldown of the spell, turns for which is active
        """
        holy_power_generation = 1
        self.spell_attributes["turns_active"] = 1
        self.spell_attributes["cooldown"] = 2
        self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 30 / 100)
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 5 / 100
        )
        self.damage_reduction = math.ceil(self.attack_power * 30 / 100)
        self._curr_mana -= self.spell_attributes["spell_cost"]

        self.add_specific_stat(holy_power_generation)

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_shield_of_the_righteous(self) -> dict[str, int] | None:
        """
        Slam the enemy with your shield, dealing holy damage.
        Cost - 3 Holy Power.

        Returns:
            int: spell damage or None if the hero does not have enough holy power
        """
        holy_power_cost = 3
        if self.is_specific_stat_spent(holy_power_cost):
            self.spell_attributes["spell_damage"] = math.ceil(
                self.attack_power * 42 / 100
            )
            self.spell_attributes["spell_cost"] = math.ceil(
                self.max_secondary_pool * 5 / 100
            )
            self._curr_mana -= self.spell_attributes["spell_cost"]

            return self.spell_attributes
        else:
            return None

    # ------------------------------------------------------------------------ #
    def cast_crusader_strike(self) -> dict[str, int]:
        """
        Strike the target, dealing holy damage. Generates 1 Holy Power.

        Returns:
            int: damage of the spell
        """
        holy_power_generation = 1
        self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 110 / 100)
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 5 / 100
        )
        self._curr_mana -= self.spell_attributes["spell_cost"]
        self.add_specific_stat(holy_power_generation)

        return self.spell_attributes

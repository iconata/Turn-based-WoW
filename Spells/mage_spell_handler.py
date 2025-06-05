"""
Handler library, that contains all Mage spells.
"""

import math

from Heroes.hero_base_stats import IBaseHero


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class FireMageSpells(IBaseHero):
    """
    Fire Mage Spells Handler
    This class contains all the spells and abilities of the Fire Mage.
    It inherits from the IBaseHero class, which contains the base stats of the hero.
    The Fire Mage is a ranged damage dealer, specializing in fire magic.

    Args:
        IBaseHero (cls): Base class for all heroes, containing base stats and methods.
    """

    # ------------------------------------------------------------------------ #
    def __init__(self) -> None:
        super().__init__()
        self._curr_fire_stacks = 0
        self._max_fire_stacks = 8
        self._curr_health = self.max_health
        self._curr_mana = self.max_secondary_pool

    # ------------------------------------------------------------------------ #
    def cast_fireball(self) -> dict[str, int]:
        """
        Hurl a fireball to the target, dealing significant fire damage. Heals you for 1% of your max health.
        Generated 1 fire stack.

        Returns:
            tuple: damage of the spell, cooldown of the spell
        """
        generated_fire_stack = 1
        spell_damage = math.ceil(self.spell_power * 155 / 100)
        heal_amount = math.ceil(self.max_health * 1 / 100)
        self.heal_up(heal_amount)
        self.add_specific_stat(generated_fire_stack)

        if self.is_specific_stat_spent(self._max_fire_stacks):
            spell_damage = (math.ceil(self.spell_power * 155 / 100)) * 2

        self.spell_attributes["cooldown"] = 3
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 2 / 100
        )
        self.spell_attributes["spell_damage"] = spell_damage
        self._curr_mana -= self.spell_attributes["spell_cost"]

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_fire_blast(self) -> dict[str, int]:
        """
        Blast the target with fire, decreasing their damage reduction by 15% for 3 turns.
        Generates 1 fire stack.

        Returns:
            tuple: damage of the spell, amount of damage reduction to be applied,
            turns for which the effect is active
        """
        generated_fire_stack = 1
        spell_damage = math.ceil(self.spell_power * 82 / 100)
        self.add_specific_stat(generated_fire_stack)

        if self.is_specific_stat_spent(self._max_fire_stacks):
            spell_damage = (math.ceil(self.spell_power * 82 / 100)) * 2

        self.spell_attributes["turns_active"] = 3
        self.spell_attributes["damage_reduction"] = 15
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 1 / 100
        )
        self.spell_attributes["spell_damage"] = spell_damage
        self._curr_mana -= self.spell_attributes["spell_cost"]

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_flamestrike(self) -> dict[str, int]:
        """
        Ignite the ground under the feet of your target, making them take damage over time for 3 turns.
        Cooldown - 5 turns. Generates 1 fire stack.

        Returns:
            tuple: damage of the spell, cooldown of the spell, turns for which the spell is active
        """
        generated_fire_stack = 1
        spell_damage = math.ceil(self.spell_power * 57 / 100)
        self.add_specific_stat(generated_fire_stack)

        if self.is_specific_stat_spent(self._max_fire_stacks):
            spell_damage = (math.ceil(self.spell_power * 57 / 100)) * 2

        self.spell_attributes["turns_active"] = 3
        self.spell_attributes["cooldown"] = 5
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 1 / 100
        )
        self.spell_attributes["spell_damage"] = spell_damage
        self._curr_mana -= self.spell_attributes["spell_cost"]

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_polymorph(self) -> dict[str, int]:
        """
        Pacify the target for 2 turns, making them unable to cast any spells.
        Any damage suffered by the target will break the effect.
        Cooldown - 5 turns.

        Returns:
            tuple: cooldown of the spell, turns for which the spell is active
        """
        self.spell_attributes["turns_active"] = 2
        self.spell_attributes["cooldown"] = 5
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 1 / 100
        )
        self._curr_mana -= self.spell_attributes["spell_cost"]

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_arcane_intellect(self) -> dict[str, int]:
        """
        Your arcane understanding, increases your spell power by 10% for 4 turns
        and restoring 20% of you max mana
        .
        Cooldown - 4 turns.

        Returns:
            tuple: cooldown of the spell, turns for which the spell is active
        """
        self.spell_attributes["turns_active"] = 4
        self.spell_attributes["cooldown"] = 4
        self.spell_power += math.ceil(self.spell_power * 10 / 100)
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 4 / 100
        )
        self._curr_mana -= self.spell_attributes["spell_cost"]

        return self.spell_attributes

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
        Checks the current amount of fire stacks available to the hero.
        If the current fire stacks goes beyond the max fire stacks, the current fire stacks are set to the max

        Args:
            stat_value (int, optional): Adds the generated fire stacks to the currently available.
        """

        self._curr_fire_stacks += stat_value

        if self._curr_fire_stacks >= self._max_fire_stacks:
            self._curr_fire_stacks = self._max_fire_stacks

    # ------------------------------------------------------------------------ #
    def is_specific_stat_spent(self, stat_value: int) -> bool:
        """
        Boolean check if the hero has enough fire stacks to double the damage of next spell cast.

        Args:
            stat_value (int): cost of the spell

        Returns:
            bool: returns True if the stacks are enough to double the damage, otherwise returns False
        """

        if self._curr_fire_stacks == stat_value:
            self._curr_fire_stacks = 0
            return True
        else:
            return False

    # ------------------------------------------------------------------------ #
    def create_hero(self, hero_instance: IBaseHero):
        if isinstance(hero_instance, FireMageSpells):
            hero_instance.max_health = 700
            hero_instance.max_secondary_pool = 900
            hero_instance.spell_power = 110

        return hero_instance

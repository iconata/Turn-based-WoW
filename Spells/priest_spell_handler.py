"""
Handler library, which contains all Priest spells
"""

import math

from Heroes.hero_base_stats import IBaseHero


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class ShadowPriestSpells(IBaseHero):

    # ------------------------------------------------------------------------ #
    def get_name(self) -> str:
        return "Shadow Priest"

    # ------------------------------------------------------------------------ #
    def __init__(self) -> None:
        super().__init__()
        self._curr_health = self.max_health
        self._curr_mana = self.max_secondary_pool
        self._max_insanity = 100
        self._curr_insanity = 0

    # ------------------------------------------------------------------------ #
    def cast_mind_blast(self) -> dict[str, int]:
        """
        Blast the mind of the target, dealing shadow damage. Generates 30 insanity.

        Returns:
            tuple: damage of the spell, cooldown of the spell
        """
        self.spell_attributes["cooldown"] = 3
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 4 / 100
        )
        self.spell_attributes["spell_damage"] = math.ceil(self.spell_power * 73 / 100)
        self._curr_mana -= self.spell_attributes["spell_cost"]

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_shadow_word_death(self) -> dict[str, int]:
        """
        A word of dark binding, dealing moderate shadow damage. If the target is below 20% hp,
        the damage is increased by 150%. If the target does not die, the caster suffers a backash,
        equal to 5% of the casters max health. Generates 25 insanity.

        Returns:
            tuple: damage of the spell, cooldown of the spell
        """
        self.spell_attributes["cooldown"] = 3
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 1 / 100
        )
        self.spell_attributes["spell_damage"] = math.ceil(self.spell_power * 85 / 100)
        self._curr_mana -= self.spell_attributes["spell_cost"]

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_devouring_plague(self) -> dict[str, int]:
        """
        Afflict the target with a disease, dealing initial shadow damage, damage over time
        and restoring health to the caster. Generates 7 insanity per tick.

        Returns:
            tuple: initial spell damage, damage over time, amount of health restored
            to the caster, cooldown of the spell, turns for which the spell is active
        """
        self.spell_attributes["cooldown"] = 4
        self.spell_attributes["turns_active"] = 3
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 10 / 100
        )
        self.spell_attributes["initial_spell_damage"] = math.ceil(
            self.spell_power * 155 / 100
        )
        self.spell_attributes["health_leech"] = math.ceil(
            self.spell_attributes["initial_spell_damage"] * 30 / 100
        )
        self.spell_attributes["damage_over_time"] = math.ceil(
            self.spell_attributes["initial_spell_damage"] * 13 / 100
        )
        self._curr_mana -= self.spell_attributes["spell_cost"]

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_flash_heal(self) -> dict[str, int]:
        """
        Quick healing spell, healing for moderate amount. Healing restores you state of mind, removing 20 insanity.
        """
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 10 / 100
        )
        amount_to_heal = math.ceil(self.spell_power * 203 / 100)
        self._curr_mana -= self.spell_attributes["spell_cost"]
        self.heal_up(amount_to_heal)
        self.remove_specific_stat(stat_value=20)

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_power_word_shield(self) -> dict[str, int]:
        """
        Powerfull word that creates a shield around the caster, absorbing a fixed amount of incoming damage.

        Returns:
            tuple: amount of damage that will be absorbed, cooldown of the spell
        """
        self.spell_attributes["cooldown"] = 5
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 10 / 100
        )
        self.spell_attributes["damage_reduction"] = self.max_damage_reduction
        self.spell_attributes["turns_active"] = 2
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
    def add_specific_stat(self, stat_value: int) -> None:
        self._curr_insanity += stat_value

        if self._curr_insanity > self._max_insanity:
            self._curr_insanity = self._max_insanity

    # ------------------------------------------------------------------------ #
    def is_specific_stat_spent(self, stat_value: int) -> bool:
        if self._curr_insanity == stat_value:
            return True
        else:
            return False

    # ------------------------------------------------------------------------ #
    def remove_specific_stat(self, stat_value: int) -> None:
        self._curr_insanity -= stat_value

        if self._curr_insanity < 0:
            self._curr_insanity = 0

    # ------------------------------------------------------------------------ #
    def create_hero(self, hero_instance: IBaseHero):
        if isinstance(hero_instance, ShadowPriestSpells):
            hero_instance.max_health = 750
            hero_instance.max_secondary_pool = 900
            hero_instance.spell_power = 90

        return hero_instance

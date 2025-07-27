import math

from Heroes.hero_base_stats import IBaseHero


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class ShamanCommonSpells(IBaseHero):
    """
    Common Spells Mixin
    This class contains the common spells and abilities of the Shaman.
    """

    # ------------------------------------------------------------------------ #
    def __init__(self):
        super().__init__()
        self._curr_maelstrom_stacks = 0
        self._max_maelstrom_stacks = 5
        self._curr_health = self.max_health
        self._curr_mana = self.max_secondary_pool

    # ------------------------------------------------------------------------ #
    def create_hero(self, hero_instance: IBaseHero):
        if isinstance(hero_instance, ElementalShamanSpells):
            hero_instance.max_health = 750
            hero_instance.max_secondary_pool = 750
            hero_instance.spell_power = 100

        elif isinstance(hero_instance, EnhancementShamanSpells):
            hero_instance.max_health = 850
            hero_instance.max_secondary_pool = 300
            hero_instance.attack_power = 35
            hero_instance.spell_power = 60

        return hero_instance

    # ------------------------------------------------------------------------ #
    @staticmethod
    def __is_flame_shock_active(active_spells: list[str]) -> bool:
        if "flame_shock" in active_spells:
            return True

        return False

    # ------------------------------------------------------------------------ #
    def cast_lighting_bolt(self) -> dict[str, int]:
        """
        Hurls a bolt of lightning at the target, dealing nature damage.

        Returns:
            tuple: spell damage, cooldown

        """
        self.spell_attributes["cooldown"] = 1
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 4 / 100
        )
        self.spell_attributes["spell_damage"] = math.ceil(self.spell_power * 131 / 100)
        self._curr_mana -= self.spell_attributes["spell_cost"]

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_flame_shock(self) -> dict[str, int]:
        """
        Sears the target with fire, causing initial damage and then dealing damage over time.

        Returns:
            tuple: initial spell damage, damage over time, cooldown, turns active

        """
        self.spell_attributes["cooldown"] = 5
        self.spell_attributes["turns_active"] = 3
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 5 / 100
        )
        self.spell_attributes["initial_spell_damage"] = math.ceil(
            self.spell_power * 30 / 100
        )
        self.spell_attributes["damage_over_time"] = math.ceil(
            self.spell_power * 120 / 100
        )
        self._curr_health -= self.spell_attributes["spell_cost"]

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_primordial_wave(self) -> dict[str, int]:
        """
        Blast the target with a Primordial Wave of energy, dealing elemental damage.

        Returns:
            tuple: spell damage, cooldown

        """
        self.spell_attributes["cooldown"] = 7
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 5 / 100
        )
        self.spell_attributes["spell_damage"] = math.ceil(self.spell_power * 525 / 100)
        self._curr_mana -= self.spell_attributes["spell_cost"]

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_lava_burst(self, active_spells: list[str]) -> dict[str, int]:
        """
        Hurls a molten lava ball towards the target, dealing fire damage. Lava Burst will
        always critically strike if the target is affected by Flame Shock.

        Returns:
            tuple: spell damage, cooldown

        """
        self.spell_attributes["cooldown"] = 2
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 5 / 100
        )
        self.spell_attributes["spell_damage"] = math.ceil(self.spell_power * 140 / 100)
        self._curr_mana -= self.spell_attributes["spell_cost"]

        if self.__is_flame_shock_active(active_spells):
            self.spell_attributes["spell_damage"] *= 2

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
        Checks the current amount of maelstrom stacks available to the hero.
        If the maelstrom stacks goes beyond the max maelstrom stacks, the current maelstrom stacks are set to the max

        Args:
            stat_value (int): Add the maelstrom stack to the amount currently available.
        """

        self._curr_maelstrom_stacks += stat_value

        if self._curr_maelstrom_stacks >= self._max_maelstrom_stacks:
            self._curr_maelstrom_stacks = self._max_maelstrom_stacks

    # ------------------------------------------------------------------------ #
    def is_specific_stat_spent(self, stat_value: int) -> bool:
        """
        Boolean check if the hero has enough maelstrom stacks for the spell that was casted.

        Args:
            stat_value (int): cost of the spell

        Returns:
            bool: returns True if there are enough maelstrom stacks for the spell, otherwise returns False
        """
        if self._curr_maelstrom_stacks >= stat_value:
            self._curr_maelstrom_stacks -= stat_value
            return True
        else:
            return False


# ---------------------------------------------------------------------------- #
class EnhancementShamanSpells(ShamanCommonSpells):
    """
    Enhancement Shaman Spells
    This class contains the spells and abilities of the Enhancement Shaman.
    """

    # ------------------------------------------------------------------------ #
    def get_name(self) -> str:
        return "Enhancement Shaman"

    # ------------------------------------------------------------------------ #
    def cast_stormstrike(self) -> dict[str, int]:
        """
        Energizes both weapons with lightning and delivers a massive blow to your target,
        dealing Physical damage.

        Returns:
            tuple: spell damage, cooldown

        """

        self.spell_attributes["cooldown"] = 2
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 5 / 100
        )
        self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 400 / 100)
        self._curr_mana -= self.spell_attributes["spell_cost"]

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_lava_lash(self) -> dict[str, int]:
        """
        Charges your off-hand weapon with lava and burns your target, dealing Fire damage.

        Returns:
            tuple: spell damage, cooldown

        """

        self.spell_attributes["cooldown"] = 2
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 3 / 100
        )
        self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 240 / 100)
        self._curr_mana -= self.spell_attributes["spell_cost"]

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_tempest(self) -> dict[str, int]:
        """
        Calls down a tremendous lightning strike, dealing Nature damage to you target.

        Returns:
            tuple: spell damage, cooldown

        """

        self.spell_attributes["cooldown"] = 5
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 3 / 100
        )
        self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 310 / 100)
        self._curr_mana -= self.spell_attributes["spell_cost"]

        return self.spell_attributes

    # ------------------------------------------------------------------------ #
    def cast_feral_spirit(self) -> dict[str, int]:
        """
        Summon two Spirit Wolves to fight by your side for 4 turns.

        Returns:
            tuple: spell damage, cooldown, turns active

        """

        self.spell_attributes["cooldown"] = 8
        self.spell_attributes["turns_active"] = 4
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 5 / 100
        )
        self.spell_attributes["spell_damage"] = math.ceil(
            self.attack_power * 80 / 100
        ) + math.ceil(self.spell_power * 80 / 100)
        self._curr_mana -= self.spell_attributes["spell_cost"]

        return self.spell_attributes


# ---------------------------------------------------------------------------- #
class ElementalShamanSpells(ShamanCommonSpells):
    """
    Elemental Shaman Spells
    This class contains the spells and abilities of the Elemental Shaman.
    """

    # ------------------------------------------------------------------------ #
    def get_name(self) -> str:
        return "Elemental Shaman"

    # ------------------------------------------------------------------------ #
    def cast_earth_shock(self):
        """
        Instantly shocks the target with concussive force, dealing Nature damage.

        Returns:
            tuple: spell damage, cooldown
        """

        self.spell_attributes["cooldown"] = 3
        self.spell_attributes["spell_cost"] = math.ceil(
            self.max_secondary_pool * 10 / 100
        )
        self.spell_attributes["spell_damage"] = math.ceil(self.spell_power * 550 / 100)
        self._curr_health -= self.spell_attributes["spell_cost"]

        return self.spell_attributes

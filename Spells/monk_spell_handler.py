import math

from Heroes.hero_base_stats import IBaseHero


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class MonkCommonSpells(IBaseHero):
    """
    Common Spells Mixin
    This class contains the common spells and abilities of the Monk.
    """

    # ------------------------------------------------------------------------ #
    def __init__(self) -> None:
        super().__init__()
        self._curr_chi = 0
        self._max_chi = 5
        self._curr_health = self.max_health
        self._curr_energy = self.max_secondary_pool

    # ------------------------------------------------------------------------ #
    def create_hero(self, hero_instance: IBaseHero):
        if isinstance(hero_instance, WindwalkerMonkSpells):
            hero_instance.max_health = 800
            hero_instance.max_secondary_pool = 300
            hero_instance.attack_power = 65

        elif isinstance(hero_instance, BrewmasterMonkSpells):
            hero_instance.max_health = 1100
            hero_instance.max_secondary_pool = 200
            hero_instance.attack_power = 45

        return hero_instance

    # ------------------------------------------------------------------------ #
    def is_specific_stat_spent(self, stat_value: int) -> bool:
        """
        Check if the player has enough chi to cast a spell.
        """
        if self._curr_chi >= stat_value:
            self._curr_chi -= stat_value
            return True

        return False

    # ------------------------------------------------------------------------ #
    def add_specific_stat(self, stat_value: int) -> None:
        self._curr_chi += stat_value
        self._curr_chi = min(self._curr_chi, self._max_chi)

    # ------------------------------------------------------------------------ #
    def heal_up(self, heal_amount: int) -> None:
        self._curr_health += heal_amount
        self._curr_health = min(self._curr_health, self.max_health)

    # ------------------------------------------------------------------------ #
    def cast_spinning_crane_kick(self) -> dict[str, int]:
        self.spell_attributes["cooldown"] = 2
        self.spell_attributes["spell_cost"] = 40
        self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 40 / 100)
        self._curr_energy -= self.spell_attributes["spell_cost"]

        return dict(self.spell_attributes)

    # ------------------------------------------------------------------------ #
    def cast_vivify(self) -> None:
        energy_cost = 30
        amount_to_heal = math.ceil(self.spell_power * 258 / 100)
        if self._curr_energy >= energy_cost:
            self._curr_energy -= energy_cost
            self.heal_up(amount_to_heal)


# ---------------------------------------------------------------------------- #
class WindwalkerMonkSpells(MonkCommonSpells):
    def get_name(self) -> str:
        return "Windwalker Monk"

    def cast_tiger_palm(self) -> dict[str, int]:
        generated_chi = 2
        self.spell_attributes["cooldown"] = 1
        self.spell_attributes["spell_cost"] = math.ceil(self.max_secondary_pool * 12 / 100)
        self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 28 / 100)
        self._curr_energy -= self.spell_attributes["spell_cost"]
        self.add_specific_stat(generated_chi)

        return dict(self.spell_attributes)

    def cast_rising_sun_kick(self) -> dict[str, int]:
        self.spell_attributes["cooldown"] = 1
        chi_cost = 2
        if self.is_specific_stat_spent(chi_cost):
            self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 28 / 100)

        return dict(self.spell_attributes)

    def cast_fists_of_fury(self) -> dict[str, int]:
        chi_cost = 3
        self.spell_attributes["cooldown"] = 2
        if self.is_specific_stat_spent(chi_cost):
            self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 138 / 100)

        return dict(self.spell_attributes)

    def cast_whirling_dragon_punch(self) -> dict[str, int]:
        self.spell_attributes["cooldown"] = 5
        self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 230 / 100)

        return dict(self.spell_attributes)


# ---------------------------------------------------------------------------- #
class BrewmasterMonkSpells(MonkCommonSpells):
    def get_name(self) -> str:
        return "Brewmaster Monk"

    def cast_rushing_jade_wind(self) -> dict[str, int]:
        chi_cost = 1
        self.spell_attributes["cooldown"] = 1
        if self.is_specific_stat_spent(chi_cost):
            self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 14 / 100)

        return dict(self.spell_attributes)

    def cast_chi_burst(self) -> dict[str, int]:
        self.spell_attributes["cooldown"] = 7
        self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 280 / 100)

        return dict(self.spell_attributes)

    def cast_keg_smash(self) -> dict[str, int]:
        spell_cost = 40
        self.spell_attributes["spell_cost"] = spell_cost
        self.spell_attributes["cooldown"] = 3
        self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 100 / 100)
        self._curr_energy -= spell_cost
        self.spell_attributes["damage_reduction"] = 30
        self.spell_attributes["turns_active"] = 1

        return dict(self.spell_attributes)

    def cast_blackout_kick(self) -> dict[str, int]:
        chi_cost = 3
        self.spell_attributes["cooldown"] = 1
        if self.is_specific_stat_spent(chi_cost):
            self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 85 / 100)

        return dict(self.spell_attributes)

    def cast_breath_of_fire(self) -> dict[str, int]:
        self.spell_attributes["cooldown"] = 5
        self.spell_attributes["spell_damage"] = math.ceil(self.attack_power * 54 / 100)

        return dict(self.spell_attributes)

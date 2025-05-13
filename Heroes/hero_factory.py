"""
Hero Factory which creates a hero based on the input.
"""

from Spells.mage_spell_handler import FireMageSpells
from Spells.monk_spell_handler import BrewmasterMonkSpells, WindwalkerMonkSpells
from Spells.paladin_spell_handler import (
    ProtectionPaladinSpells,
    RetributionPaladinSpells,
)
from Spells.priest_spell_handler import ShadowPriestSpells
from Spells.shaman_spell_handler import ElementalShamanSpells, EnhancementShamanSpells
from Spells.warrior_spell_handler import FuryWarriorSpells, ProtectionWarriorSpells


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class HeroFactory:
    # ------------------------------------------------------------------------ #
    def create_hero(
        self, hero_type: str, hero_role: str
    ) -> (
        ProtectionPaladinSpells
        | RetributionPaladinSpells
        | FuryWarriorSpells
        | ProtectionWarriorSpells
        | ShadowPriestSpells
        | ElementalShamanSpells
        | EnhancementShamanSpells
        | BrewmasterMonkSpells
        | WindwalkerMonkSpells
        | FireMageSpells
        | None
    ):
        match hero_type:
            case "Paladin":
                match hero_role:
                    case "Protection":
                        return self.__create_protection_paladin()
                    case "Retribution":
                        return self.__create_retribution_paladin()
            case "Warrior":
                match hero_role:
                    case "Protection":
                        return self.__create_fury_warrior()
                    case "Fury":
                        return self.__create_protection_warrior()
            case "Priest":
                match hero_role:
                    case "Shadow":
                        return self.__create_shadow_priest()
            case "Shaman":
                match hero_role:
                    case "Elemental":
                        return self.__create_elemental_shaman()
                    case "Enhancement":
                        return self.__create_enhancement_shaman()
            case "Monk":
                match hero_role:
                    case "Brewmaster":
                        return self.__create_brewmaster_monk()
                    case "Windweaver":
                        return self.__create_windwalker_monk()
            case "Mage":
                match hero_role:
                    case "Fire":
                        return self.__create_fire_mage()

    # ------------------------------------------------------------------------ #
    def __create_retribution_paladin(self) -> RetributionPaladinSpells:
        cls_instance = RetributionPaladinSpells()
        cls_instance.max_health = 800
        cls_instance.max_secondary_pool = 300
        cls_instance.spell_power = 30
        cls_instance.attack_power = 75

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_protection_paladin(self) -> ProtectionPaladinSpells:
        cls_instance = ProtectionPaladinSpells()
        cls_instance.max_health = 1200
        cls_instance.max_secondary_pool = 300
        cls_instance.spell_power = 30
        cls_instance.attack_power = 45

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_fury_warrior(self) -> FuryWarriorSpells:
        cls_instance = FuryWarriorSpells()
        cls_instance.max_health = 1000
        cls_instance.max_secondary_pool = 200
        cls_instance.attack_power = 70

        return cls_instance

    # ------------------------------------------------------------------------ #

    def __create_protection_warrior(self) -> ProtectionWarriorSpells:
        cls_instance = ProtectionWarriorSpells()
        cls_instance.max_health = 1500
        cls_instance.max_secondary_pool = 200
        cls_instance.attack_power = 50

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_fire_mage(self) -> FireMageSpells:
        cls_instance = FireMageSpells()
        cls_instance.max_health = 700
        cls_instance.max_secondary_pool = 900
        cls_instance.spell_power = 110

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_shadow_priest(self) -> ShadowPriestSpells:
        cls_instance = ShadowPriestSpells()
        cls_instance.max_health = 750
        cls_instance.max_secondary_pool = 900
        cls_instance.spell_power = 90

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_enhancement_shaman(self) -> EnhancementShamanSpells:
        cls_instance = EnhancementShamanSpells()
        cls_instance.max_health = 850
        cls_instance.max_secondary_pool = 300
        cls_instance.attack_power = 35
        cls_instance.spell_power = 60

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_elemental_shaman(self) -> ElementalShamanSpells:
        cls_instance = ElementalShamanSpells()
        cls_instance.max_health = 750
        cls_instance.max_secondary_pool = 750
        cls_instance.spell_power = 100

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_windwalker_monk(self) -> WindwalkerMonkSpells:
        cls_instance = WindwalkerMonkSpells()
        cls_instance.max_health = 800
        cls_instance.max_secondary_pool = 300
        cls_instance.attack_power = 65

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_brewmaster_monk(self) -> BrewmasterMonkSpells:
        cls_instance = BrewmasterMonkSpells()
        cls_instance.max_health = 1100
        cls_instance.max_secondary_pool = 200
        cls_instance.attack_power = 45

        return cls_instance

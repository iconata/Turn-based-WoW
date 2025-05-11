"""
Hero Factory which creates a hero based on the input.
"""

from Spells.paladin_spell_handler import (
    RetributionPaladinSpells,
    ProtectionPaladinSpells,
)
from Spells.warrior_spell_handler import FuryWarriorSpells, ProtectionWarriorSpells
from Spells.mage_spell_handler import FireMageSpells
from Spells.monk_spell_handler import WindwalkerMonkSpells, BrewmasterMonkSpells
from Spells.priest_spell_handler import ShadowPriestSpells
from Spells.shaman_spell_handler import ElementalShamanSpells, EnhancementShamanSpells


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class HeroFactory:
    # ------------------------------------------------------------------------ #
    def create_hero(self, hero_type: str, hero_role: str):
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
    def __create_retribution_paladin(self):
        cls_instance = RetributionPaladinSpells()
        cls_instance.max_health = 800
        cls_instance.max_secondary_pool = 300
        cls_instance.spell_power = 30
        cls_instance.attack_power = 75

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_protection_paladin(self):
        cls_instance = ProtectionPaladinSpells()
        cls_instance.max_health = 1200
        cls_instance.max_secondary_pool = 300
        cls_instance.spell_power = 30
        cls_instance.attack_power = 45

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_fury_warrior(self):
        cls_instance = FuryWarriorSpells()

        return cls_instance

    # ------------------------------------------------------------------------ #

    def __create_protection_warrior(self):
        cls_instance = ProtectionWarriorSpells()

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_fire_mage(self):
        cls_instance = FireMageSpells()

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_shadow_priest(self):
        cls_instance = ShadowPriestSpells()

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_enhancement_shaman(self):
        cls_instance = EnhancementShamanSpells()
        cls_instance.max_health = 850
        cls_instance.max_secondary_pool = 300
        cls_instance.attack_power = 35
        cls_instance.spell_power = 60

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_elemental_shaman(self):
        cls_instance = ElementalShamanSpells()
        cls_instance.max_health = 750
        cls_instance.max_secondary_pool = 750
        cls_instance.spell_power = 100

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_windwalker_monk(self):
        cls_instance = WindwalkerMonkSpells()

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_brewmaster_monk(self):
        cls_instance = BrewmasterMonkSpells()

        return cls_instance

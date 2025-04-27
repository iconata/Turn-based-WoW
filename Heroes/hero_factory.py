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
            case 'Paladin':
                match hero_role:
                    case 'Protection':
                        return self.__create_protection_paladin()
                    case 'Retribution':
                        return self.__create_retribution_paladin()
            case 'Warrior':
                match hero_role:
                    case 'Protection':
                        return self.__create_fury_warrior()
                    case 'Fury':
                        return self.__create_protection_warrior()
            case 'Priest':
                match hero_role:
                    case 'Shadow':
                        return self.__create_shadow_priest()
            case 'Mage':
                match hero_role:
                    case 'Elemental':
                        return self.__create_elemental_shaman()
                    case 'Enhancement':
                        return self.__create_enhancement_shaman()
            case 'Monk':
                match hero_role:
                    case 'Brewmaster':
                        return self.__create_brewmaster_monk()
                    case 'Windweaver':
                        return self.__create_windwalker_monk()

    # ------------------------------------------------------------------------ #
    def __create_retribution_paladin(self):
        cls_instance = RetributionPaladinSpells()

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_protection_paladin(self):
        cls_instance = ProtectionPaladinSpells()

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

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_elemental_shaman(self):
        cls_instance = ElementalShamanSpells()

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_windwalker_monk(self):
        cls_instance = WindwalkerMonkSpells()

        return cls_instance

    # ------------------------------------------------------------------------ #
    def __create_brewmaster_monk(self):
        cls_instance = BrewmasterMonkSpells()

        return cls_instance

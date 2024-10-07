"""
Base class with attributes, which are similar for every hero.
It is to be used to construct every hero type.
"""

# TODO: implement factory design pattern and a better base class
from Spells.paladin_spell_handler import RetributionPaladinSpells, ProtectionPaladinSpells
from Spells.warrior_spell_handler import FuryWarriorSpells, ProtectionWarriorSpells
from Spells.mage_spell_handler import FireMageSpells
from Spells.monk_spell_handler import WindwalkerMonkSpells, BrewmasterMonkSpells
from Spells.priest_spell_handler import ShadowPriestSpells
from Spells.shaman_spell_handler import ElementalShamanSpells, EnhancementShamanSpells


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class BaseHeroStats:
    def __init__(self):
        self._health            = 1000
        self._secondary_pool    = 500
        self._spell_power       = 10
        self._attack_power      = 10
        self._damage_reduction  = 0


# ---------------------------------------------------------------------------- #
class HeroFactory:
    # ------------------------------------------------------------------------ #
    def create_hero(self, type_and_role: tuple):
        if type_and_role == ("Paladin", "Protection"):
            return self.__create_protection_paladin()
        elif type_and_role == ("Paladin", "Retribution"):
            return self.__create_retribution_paladin()
        elif type_and_role == ("Warrior", "Protection"):
            return self.__create_fury_warrior()
        elif type_and_role == ("Warrior", "Fury"):
            return self.__create_protection_warrior()
        elif type_and_role == ("Priest", "Shadow"):
            return self.__create_shadow_priest()
        elif type_and_role == ("Mage", "Fire"):
            return self.__create_fire_mage()
        elif type_and_role == ("Shaman", "Elemental"):
            return self.__create_elemental_shaman()
        elif type_and_role == ("Shaman", "Enhancement"):
            return self.__create_enhancement_shaman()
        elif type_and_role == ("Monk", "Brewmaster"):
            return self.__create_brewmaster_monk()
        elif type_and_role == ("Monk", "Windweaver"):
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

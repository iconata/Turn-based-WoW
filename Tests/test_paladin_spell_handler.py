import unittest
from Spells.paladin_spell_handler import ProtectionPaladinSpells, RetributionPaladinSpells


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class TestRetributionPaladinSpells(unittest.TestCase):

    # ------------------------------------------------------------------------ #
    def setUp(self) -> None:
        self.cls_instance = RetributionPaladinSpells()

    # ------------------------------------------------------------------------ #
    def tearDown(self) -> None:
        del self.cls_instance

    # ------------------------------------------------------------------------ #
    def test_cast_divine_protection_raise_error(self):
        self.cls_instance._secondary_pool = 0

        with self.assertRaises(ValueError):
            self.cls_instance.cast_divine_shield()

    # ------------------------------------------------------------------------ #
    def test_blade_of_justice(self):
        pass

    # ------------------------------------------------------------------------ #
    def test_final_verdict(self):
        pass

    # ------------------------------------------------------------------------ #
    def test_wake_of_ashes(self):
        pass


# ---------------------------------------------------------------------------- #
#                                     Main                                     #
# ---------------------------------------------------------------------------- #
if __name__ == "__main__":
    unittest.main()

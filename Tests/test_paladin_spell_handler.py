import unittest
from Spells.paladin_spell_handler import (
    ProtectionPaladinSpells,
    RetributionPaladinSpells,
)


# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #
class TestRetributionPaladinSpells(unittest.TestCase):
    """Tests for RetributionPaladinSpells spell return contracts."""
    def setUp(self) -> None:
        """Create a fresh RetributionPaladinSpells instance before each test."""
        self.cls_instance = RetributionPaladinSpells()

    # ------------------------------------------------------------------------ #
    def tearDown(self) -> None:
        """Delete the hero instance after each test."""
        del self.cls_instance

    # ------------------------------------------------------------------------ #
    def test_cast_divine_protection_raise_error(self):
        """cast_divine_shield should return a dict with cooldown and turns_active."""
        info = self.cls_instance.cast_divine_shield()
        self.assertIsInstance(info, dict)
        self.assertIn("cooldown", info)
        self.assertIn("turns_active", info)

    # ------------------------------------------------------------------------ #
    def test_blade_of_justice(self):
        """cast_blade_of_justice should return damage and generate holy power."""
        before_hp = self.cls_instance._curr_holy_power
        info = self.cls_instance.cast_blade_of_justice()
        self.assertIsInstance(info, dict)
        self.assertGreater(info.get("spell_damage", 0), 0)
        self.assertGreater(self.cls_instance._curr_holy_power, before_hp)

    # ------------------------------------------------------------------------ #
    def test_final_verdict(self):
        """cast_final_verdict returns None without holy power, dict with enough."""
        # no holy power — should return None
        self.cls_instance._curr_holy_power = 0
        result = self.cls_instance.cast_final_verdict()
        self.assertIsNone(result)

        # give enough holy power
        self.cls_instance._curr_holy_power = 3
        result = self.cls_instance.cast_final_verdict()
        self.assertIsInstance(result, dict)
        self.assertGreater(result.get("spell_damage", 0), 0)

    # ------------------------------------------------------------------------ #
    def test_wake_of_ashes(self):
        """cast_wake_of_ashes should deal damage and generate 3 holy power."""
        before_hp = self.cls_instance._curr_holy_power
        info = self.cls_instance.cast_wake_of_ashes()
        self.assertIsInstance(info, dict)
        self.assertGreater(info.get("spell_damage", 0), 0)
        self.assertEqual(self.cls_instance._curr_holy_power, min(5, before_hp + 3))


# ---------------------------------------------------------------------------- #
#                                     Main                                     #
# ---------------------------------------------------------------------------- #
if __name__ == '__main__':
    unittest.main()

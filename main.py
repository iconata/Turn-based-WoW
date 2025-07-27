import argparse
from Heroes.hero_factory import HeroFactory

AVAILABLE_CLASSES = ["Warrior", "Mage", "Paladin", "Shaman", "Monk", "Priest"]
AVAILABLE_ROLES = [
    "\n" "Warrior: Fury",
    "\n" "Paladin/Warrior: Protection",
    "\n" "Paladin: Retribution",
    "\n" "Mage: Fire",
    "\n" "Shaman: Enhancement/Elemental",
    "\n" "Monk: Windwalker/Brewmaster",
    "\n" "Priest: Shadow",
]


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Turn-based WoW: Create two heroes by specifying their class and role. "
            "The first hero will be the attacker, and the second will be the defender. "
            "You can also run the script interactively without command line arguments."
        )
    )
    parser.add_argument(
        "--class",
        "-c",
        nargs="+",
        help="Specify hero classes for attacker and defender (e.g. Warrior Mage)",
    )
    parser.add_argument(
        "--role",
        "-r",
        nargs="+",
        help="Specify hero roles for attacker and defender (e.g. Fury Fire)",
    )
    parser.add_argument(
        "--show-classes",
        "-C",
        action="store_true",
        help="Show available hero classes and exit",
    )
    parser.add_argument(
        "--show-roles",
        "-R",
        action="store_true",
        help="Show available hero roles and exit",
    )
    args = parser.parse_args()

    if args.show_classes:
        print("Available classes:", ", ".join(AVAILABLE_CLASSES))
        return

    if args.show_roles:
        print("Available roles:", ", ".join(AVAILABLE_ROLES))
        return

    if args.classes and args.roles and len(args.classes) == 2 and len(args.roles) == 2:
        hero_factory = HeroFactory()
        attacker = hero_factory.create_hero(args.classes[0], args.roles[0])
        defender = hero_factory.create_hero(args.classes[1], args.roles[1])
        print(
            f"Created attacker: {attacker.get_name()}, defender: {defender.get_name()}"
        )
    else:
        print("Interactive mode:")
        first_hero_class = input(
            f"Enter the class of the first hero ({', '.join(AVAILABLE_CLASSES)}): "
        )
        first_hero_role = input(
            f"Enter the role of the first hero ({', '.join(AVAILABLE_ROLES)}): "
        )
        second_hero_class = input(
            f"Enter the class of the second hero ({', '.join(AVAILABLE_CLASSES)}): "
        )
        second_hero_role = input(
            f"Enter the role of the second hero ({', '.join(AVAILABLE_ROLES)}): "
        )

        hero_factory = HeroFactory()
        attacker = hero_factory.create_hero(first_hero_class, first_hero_role)
        defender = hero_factory.create_hero(second_hero_class, second_hero_role)
        print(
            f"Created attacker: {attacker.get_name()}, defender: {defender.get_name()}"
        )


if __name__ == "__main__":
    main()

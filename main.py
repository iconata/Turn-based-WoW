import argparse

from Heroes.hero_base_stats import IBaseHero
from Heroes.hero_factory import HeroFactory
from battles_handler import Attacking, Defending

# --------------------------------- Constants -------------------------------- #
AVAILABLE_CLASSES = ["Warrior", "Mage", "Paladin", "Shaman", "Monk", "Priest"]
AVAILABLE_ROLES = {
    "Paladin": {"Tank": "Protection", "Damage": "Retribution"},
    "Warrior": {"Tank": "Protection", "Damage": "Fury"},
    "Monk": {"Tank": "Brewmaster", "Damage": "Windwalker"},
    "Mage": {"Damage": "Fire"},
    "Shaman": {"Damage": "Enhancement"},
    "Priest": {"Damage": "Shadow"},
}


# ------------------------------ Parse argumets ------------------------------ #
def arg_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Turn-based WoW: Create two heroes by specifying their class and role. "
            "The first hero will be the attacker, and the second will be the defender. "
            "You can also run the script interactively without command line arguments."
        )
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

    return parser.parse_args()


# --------------------------- Create Hero Instance --------------------------- #
def create_hero_instance(hero_class: str, hero_role: str) -> IBaseHero:
    hero_factory = HeroFactory()
    return hero_factory.create_hero(hero_class, hero_role)


# -------------------------- Set Hero Class and Role ------------------------- #
def set_hero_class_and_role(position: int) -> tuple[str, str]:
    counter = 0
    hero_map = {1: "first", 2: "second"}
    hero_class = input(
        f"Enter the class of the {hero_map[position]} hero ({', '.join(AVAILABLE_CLASSES)}): "
    ).capitalize()
    while hero_class not in AVAILABLE_CLASSES:
        hero_class = input(
            f"Invalid class. Enter the class of the {hero_map[position]} hero ({', '.join(AVAILABLE_CLASSES)}): "
        ).capitalize()
        counter += 1
        if counter >= 3:
            print("Too many invalid attempts. Exiting.")
            exit(1)

    hero_role = input(
        f"Enter the role of the {hero_map[position]} hero ({', '.join(AVAILABLE_ROLES[hero_class])}): "
    ).capitalize()

    if len(AVAILABLE_ROLES[hero_class]) == 1:
        hero_role = "Damage"
        print(f"Automatically selected role: {hero_role}")
    else:
        while hero_role not in AVAILABLE_ROLES[hero_class]:
            counter += 1
            hero_role = input(
                f"Invalid role. Enter the role of the {hero_map[position]} hero ({', '.join(AVAILABLE_ROLES[hero_class])}): "
            ).capitalize()
            if counter >= 3:
                print("Too many invalid attempts. Exiting.")
                exit(1)

    return hero_class, hero_role


# ---------------------------------------------------------------------------- #
#                                     Main                                     #
# ---------------------------------------------------------------------------- #
def main() -> None:
    args = arg_parser()
    if args.show_classes:
        print("Available classes:", ", ".join(AVAILABLE_CLASSES))
        return

    if args.show_roles:
        print("Available roles:")
        for hero_class, roles in AVAILABLE_ROLES.items():
            print(f"{hero_class}: {', '.join(roles)}")
        return

    first_hero = set_hero_class_and_role(position=1)
    second_hero = set_hero_class_and_role(position=2)

    attacker = create_hero_instance(
        first_hero[0], AVAILABLE_ROLES[first_hero[0]][first_hero[1]]
    )
    defender = create_hero_instance(
        second_hero[0], AVAILABLE_ROLES[second_hero[0]][second_hero[1]]
    )
    print(f"Created attacker: {attacker.get_name()}, defender: {defender.get_name()}")

    while defender.get_current_health() > 0 or attacker.get_current_health() > 0:
        defending_handler = Defending(defender)
        attacking_handler = Attacking(attacker, defender)
        defending_handler.defend()
        attacking_handler.attack()


if __name__ == "__main__":
    main()

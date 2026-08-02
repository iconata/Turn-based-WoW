import argparse
import inspect
from typing import Optional

from ai_player import SimpleHeuristicAI
from battle_state import BattleState
from battles_handler import Attacking
from Heroes.hero_base_stats import IBaseHero
from Heroes.hero_factory import HeroFactory

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
    """Build and return the argument parser for the CLI.

    The parser exposes two convenience flags: ``--show-classes`` and
    ``--show-roles`` which print available options and exit. The function
    returns the parsed namespace.
    """
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
    """Create and return a hero instance for the given class and role.

    Args:
        hero_class: human-readable name of the class (e.g. "Mage")
        hero_role: role string mapped to a concrete specialization (e.g. "Fire")

    Returns:
        An ``IBaseHero`` concrete instance created by ``HeroFactory``.
    """
    hero_factory = HeroFactory()
    return hero_factory.create_hero(hero_class, hero_role)


# -------------------------- Set Hero Class and Role ------------------------- #
def set_hero_class_and_role(position: int) -> tuple[str, str]:
    """Interactively ask the user for a hero class and role.

    The function validates the input and allows up to three invalid
    attempts before exiting.
    """
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


def _get_health(hero: IBaseHero) -> int:
    """Return a hero's current health, using a getter when available.

    The concrete hero implementations store health in ``_curr_health``. If a
    more formal ``get_current_health`` method is present it will be used.
    """
    if hasattr(hero, "get_current_health"):
        try:
            return hero.get_current_health()
        except Exception:
            pass
    return int(getattr(hero, "_curr_health", getattr(hero, "max_health", 0)))


def _health_bar(current: int, maximum: int, length: int = 24) -> str:
    """Return a small ASCII health bar for terminal display.

    The function returns a string such as ``[██████------] 60/100``. ANSI
    color codes are intentionally omitted so terminals that do not support
    colors still render plain text.
    """
    if maximum <= 0:
        return "[----------] 0/0"
    filled = int(length * current / maximum)
    filled = max(0, min(length, filled))
    empty = length - filled
    bar = "█" * filled + "-" * empty
    return f"[{bar}] {current}/{maximum}"


# ---------------------------------------------------------------------------- #
#                                     Main                                     #
# ---------------------------------------------------------------------------- #
def main() -> None:
    """Entry point for the interactive CLI.

    The function supports two convenience flags (see ``arg_parser``). When
    running interactively two heroes are created and a very small turn loop
    runs that invokes the attacker's first available spell each turn. The
    combat log is printed to the terminal.
    """

    args = arg_parser()
    if args.show_classes:
        print("Available classes:", ", ".join(AVAILABLE_CLASSES))
        return

    if args.show_roles:
        print("Available roles:")
        for hero_class, roles in AVAILABLE_ROLES.items():
            print(f"{hero_class}: {', '.join(roles)}")
        return

    # choose mode: player vs player or player vs computer
    mode = input("Choose mode: (1) Local 2 players, (2) Play vs computer [2]: ").strip() or "2"
    while mode not in ("1", "2"):
        mode = input("Invalid selection. Choose mode 1 or 2: ").strip()

    first_hero = set_hero_class_and_role(position=1)
    second_hero = set_hero_class_and_role(position=2)

    attacker = create_hero_instance(
        first_hero[0], AVAILABLE_ROLES[first_hero[0]][first_hero[1]]
    )
    defender = create_hero_instance(
        second_hero[0], AVAILABLE_ROLES[second_hero[0]][second_hero[1]]
    )

    ai = SimpleHeuristicAI() if mode == "2" else None
    battle_state = BattleState()

    print(f"Created attacker: {attacker.get_name()}, defender: {defender.get_name()}")

    turn = 1
    active = attacker
    passive = defender

    def list_castable_spells(hero: IBaseHero):
        """Return zero-argument castable spells for the hero as (name, doc).

        The function filters out methods that require arguments.
        """
        spells = []
        for name in dir(hero):
            if not name.startswith("cast_"):
                continue
            method = getattr(hero, name)
            if not callable(method):
                continue
            try:
                sig = inspect.signature(method)
            except Exception:
                continue
            if len(sig.parameters) != 0:
                continue
            doc = (method.__doc__ or "").strip().splitlines()[0] if method.__doc__ else ""
            cd = battle_state.get_cooldown(hero, name) if battle_state is not None else 0
            spells.append((name, doc, int(cd)))
        return spells

    def choose_spell_interactive(hero: IBaseHero) -> Optional[str]:
        """Prompt the player to choose a spell and return the method name.

        Returns ``None`` when no castable spells are available.
        """
        spells = list_castable_spells(hero)
        if not spells:
            return None

        # if all spells are on cooldown, return None to indicate a skipped action
        if all(cd > 0 for (_, _, cd) in spells):
            print("All spells are currently on cooldown.")
            return None

        while True:
            print("Choose a spell:")
            for i, (name, doc, cd) in enumerate(spells, start=1):
                if cd > 0:
                    print(f" {i}) {name} - {doc} (on cooldown: {cd} turns)")
                else:
                    print(f" {i}) {name} - {doc}")
            choice = input("Enter number: ").strip()
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(spells):
                    name, _, cd = spells[idx]
                    if cd > 0:
                        print(f"Spell {name} is on cooldown ({cd} turns). Choose another.")
                        continue
                    return name
            except Exception:
                pass
            print("Invalid choice, please enter a valid spell number.")

    while _get_health(attacker) > 0 and _get_health(defender) > 0:
        print("-" * 60)
        print(f"Turn {turn}: {active.get_name()} vs {passive.get_name()}")

        # decide action
        if ai is not None and mode == "2" and active is defender:
            # AI controls the defender when playing vs computer and it's their turn
            selected = ai.choose_spell(active, passive, battle_state=battle_state)
        else:
            # interactive player: prompt; choose_spell_interactive already
            # avoids returning spells that are on cooldown
            selected = choose_spell_interactive(active)

        before_active = _get_health(active)
        before_passive = _get_health(passive)
        info = None

        if selected is not None:
            attacking_handler = Attacking(active, passive, battle_state=battle_state)
            passive, info = attacking_handler.attack(selected)
        else:
            # no available spell (or all on cooldown) -> skip action this turn
            print(f"[SKIP] {active.get_name()} has no available spells and skips their action.")

        after_active = _get_health(active)
        after_passive = _get_health(passive)

        # combat log
        if isinstance(info, dict):
            if info.get("spell_damage"):
                print(f"[ATTACK] {active.get_name()} deals {info['spell_damage']} damage")
            if info.get("turns_active") and info.get("damage_reduction"):
                print(f"[EFFECT] {passive.get_name()} affected: {info['damage_reduction']} DR for {info['turns_active']} turns")
            # reflect healing if present
            # some spells perform heals by mutating hero state; show delta
            if after_active > before_active:
                print(f"[HEAL] {active.get_name()} healed {after_active - before_active}")
        else:
            print(f"[ACTION] {active.get_name()} performed an action.")

        print(f"{active.get_name()} HP: {before_active} -> {after_active}")
        print(_health_bar(after_active, active.max_health))
        print(f"{passive.get_name()} HP: {before_passive} -> {after_passive}")
        print(_health_bar(after_passive, passive.max_health))

        # advance battle state (DOTs, cooldown ticks)
        battle_state.tick()

        # swap roles for next turn and continue
        active, passive = passive, active
        turn += 1


if __name__ == "__main__":
    main()

from pokemon_base import PokemonBase
from pokemon_base import GlitchMon
import random

"""
This file contains all the classes for the individual pokemon that inherit
the PokemonBase class and implement the features of the individual pokemon 
"""

__author__ = "Ollie Hiscoke", "Hirun Hettigoda", "Karim Hajlaoui", "Daniel Hong"


class Charmander(PokemonBase):
    """
    This class implements the methods unique to Charmanders
    """

    def __init__(self) -> None:
        """
        Calls the init method from the base class and passes hp = 7 and poke_type = "Fire"
        """
        PokemonBase.__init__(self, 7, "Fire")

    def getName(self) -> str:
        """
        Returns the name of the pokemon as a string

        complexity = O(1) as there is only a return statement
        """
        return "Charmander"

    def getSpeed(self) -> int:
        """
        Returns the speed of the pokemon

        complexity = O(1) as there is only a return statement
        """
        return 7 + self.level

    def getAttack(self) -> int:
        """
        Returns the attack damage of the pokemon

        complexity = O(1) as there is only a return statement
        """
        return 6 + self.level

    def getDefence(self) -> int:
        """
        Returns the defence of the pokemon

        complexity = O(1) as there is only a return statement
        """
        return 5

    def calculateDamage(self, attack_damage: int, damage_type: str):
        """
        Calculates the damage done to the pokemon after it has been attacked

        complexity = O(1) as there are only if statements and operations
        """
        # Attack damage is decreased by half if the attacker is a Grass type
        if damage_type == "Grass":
            attack_damage *= 0.5

        # Attack damage is increased by double if the attacker is a Water type
        elif damage_type == "Water":
            attack_damage *= 2

        # The pokemon will take less damage if their defence is higher than the attack damage
        if attack_damage > self.getDefence():
            self.hp -= attack_damage
        else:
            self.hp -= (attack_damage // 2)


class Bulbasaur(PokemonBase):
    def __init__(self) -> None:
        """
        Calls the init method from PokemonBase and passes hp = 9 and poke_type = "Grass"
        """
        PokemonBase.__init__(self, 9, "Grass")

    def getName(self) -> str:
        """
        Returns the name of the pokemon as a string

        complexity = O(1) as there is only a return statement
        """
        return "Bulbasaur"

    def getSpeed(self) -> int:
        """
        Returns the speed of the pokemon

        complexity = O(1) as there is only a return statement
        """
        return 7 + self.level // 2

    def getAttack(self) -> int:
        """
        Returns the attack damage of the pokemon

        complexity = O(1) as there is only a return statement
        """
        return 5

    def getDefence(self) -> int:
        """
        Returns the defence of the pokemon

        complexity = O(1) as there is only a return statement
        """
        return 5

    def calculateDamage(self, attack_damage: int, damage_type: str):
        """
        Calculates the damage done to the pokemon after it has been attacked

        complexity = O(1) as there are only if statements and operations
        """

        # Attack damage is increased by double if the attacker is a Fire type
        if damage_type == "Fire":
            attack_damage *= 2

        # Attack damage is decreased by half if the attacker is a Water type
        elif damage_type == "Water":
            attack_damage *= 0.5

        # The pokemon will take less damage if their defence is higher than the attack damage
        if attack_damage > self.getDefence() + 5:
            self.hp -= attack_damage
        else:
            self.hp -= attack_damage // 2


class Squirtle(PokemonBase):
    def __init__(self) -> None:
        """
        Calls the init method from PokemonBase and passes hp = 8 and poke_type = "Water"
        """
        PokemonBase.__init__(self, 8, "Water")

    def getName(self) -> str:
        """
        Returns the name of the pokemon as a string

        complexity = O(1) as there is only a return statement
        """
        return "Squirtle"

    def getSpeed(self) -> int:
        """
        Returns the speed of the pokemon

        complexity = O(1) as there is only a return statement
        """
        return 7

    def getAttack(self) -> int:
        """
        Returns the attack damage of the pokemon

        complexity = O(1) as there is only a return statement
        """
        return 4 + self.level // 2

    def getDefence(self) -> int:
        """
        Returns the defence of the pokemon

        complexity = O(1) as there is only a return statement
        """
        return 6 + self.level

    def calculateDamage(self, attack_damage: int, damage_type: str):
        """
        Calculates the damage done to the pokemon after it has been attacked

        complexity = O(1) as there are only if statements and operations
        """

        # Attack damage decreases by half if the attacker is a Fire type
        if damage_type == "Fire":
            attack_damage *= 0.5

        # Attack damage increases by double if the attacker is a Grass type
        elif damage_type == "Grass":
            attack_damage *= 2

        # The pokemon will take less damage if their defence is higher than the attack damage
        if attack_damage > self.getDefence() * 2:
            self.hp -= attack_damage
        else:
            self.hp -= attack_damage // 2


class MissingNo(GlitchMon):
    def __init__(self) -> None:
        """
        Calls the init method from GlitchMon and passes hp = (7+9+8)/3 = 8
        """
        GlitchMon.__init__(self, 8)

    def getName(self) -> str:
        """
        Returns the name of the pokemon as a string

        complexity = O(1) as there is only a return statement
        """
        return "MissingNo"

    def getSpeed(self) -> int:
        """
        Returns the speed of the pokemon

        complexity = O(1) as there is only a return statement
        """

        return round(22 / 3, 0) + (self.level - 1)

    def getAttack(self) -> int:
        """
        Returns the attack damage of the pokemon

        complexity = O(1) as there is only a return statement
        """
        return round(16 / 3, 0) + (self.level - 1)

    def getDefence(self) -> int:
        """
        Returns the defence of the pokemon

        complexity = O(1) as there is only a return statement
        """
        return round(16 / 3, 0) + (self.level - 1)

    def calculateDamage(self, attack_damage: int, damage_type: str):
        """
        Calculates the damage done to the pokemon after it has been attacked

        complexity = O(1) as there are only if statements and operations
        """
        # if there is 25% chance the superpower method is called, if not pokemon has to defend. (sourced from Edforums)
        percentage_chance = 0.25

        if random.random() <= percentage_chance:
            self.superpower()
        else:
            # The pokemon will take less damage if their defence is higher than the attack damage
            if attack_damage > self.getDefence():
                self.hp -= attack_damage
            else:
                self.hp -= attack_damage // 2



from abc import ABC, abstractmethod
import random

"""
This file contains an abstract base class for the pokemon to be built using. The class contains
methods common to all pokemon 
"""

__author__ = "Ollie Hiscoke", "Hirun Hettigoda", "Karim Hajlaoui", "Daniel Hong"


class PokemonBase(ABC):
    """
    An abstract class with methods common to all the pokemon class built in the pokemon.py file
    """

    def __init__(self, hp: int, poke_type: str) -> None:
        """
        Initialises the hp and poke_type to the provided values and level to 1
        """
        self.hp = hp
        self.poke_type = poke_type
        self.level = 1

    def getHp(self) -> int:
        """
        Returns the pokemon's HP

        complexity = O(1) as there is only a return statement
        """
        return self.hp

    def getLevel(self) -> int:
        """
        Returns the pokemon's level

        complexity = O(1) as there is only a return statement
        """
        return self.level

    def getPokeType(self) -> str:
        """
        Returns the pokemon's type

        complexity = O(1) as ther is only a return statement
        """
        return self.poke_type

    @abstractmethod
    def getName(self) -> str:
        pass

    @abstractmethod
    def getSpeed(self) -> str:
        pass

    @abstractmethod
    def getAttack(self) -> str:
        pass

    @abstractmethod
    def getDefence(self) -> str:
        pass

    def setHP(self, value) -> None:
        self.hp = value

    def setLevel(self, value) -> None:
        self.level = value

    @abstractmethod
    def calculateDamage(self, attack_damage: int, damage_type: str) -> None:
        pass

    def __str__(self) -> str:
        """
        Returns a string containing the pokemon's name, hp and level

        complexity = O(1) as there is only a return statement
        """
        return f"{self.getName()}'s HP = {self.getHp()} and level = {self.getLevel()}"


class GlitchMon(ABC):
    """
    An abstract class with methods common to the MissingNo pokemon
    """

    def __init__(self, hp: int) -> None:
        """
        Initialises the hp and poke_type to the provided values and level to 1
        """
        self.hp = hp
        self.level = 1

    def getHp(self) -> int:
        """
        Returns the pokemon's HP

        complexity = O(1) as there is only a return statement
        """
        return self.hp + (self.level - 1)

    def getLevel(self) -> int:
        """
        Returns the pokemon's level

        complexity = O(1) as there is only a return statement
        """
        return self.level

    def getPokeType(self):
        return None

    @abstractmethod
    def getName(self) -> str:
        pass

    @abstractmethod
    def getSpeed(self) -> str:
        pass

    @abstractmethod
    def getAttack(self) -> str:
        pass

    @abstractmethod
    def getDefence(self) -> str:
        pass

    def setHP(self, value) -> None:
        self.hp = value

    def setLevel(self, value) -> None:
        self.level = value

    @abstractmethod
    def calculateDamage(self, attack_damage: int) -> None:
        pass

    def IncreaseHP(self) -> None:
        """
        Increases the value of the pokemon's HP by 1

        complexity = O(1) as this is just a single operation
        """
        self.hp += 1

    def superpower(self) -> None:
        """
        has a random chance to choose 1 of the 3 effects

        has 25% chance of being called when pokemon is defending

        complexity = O(1) as there are only if statements and operations
        """
        rand_value = random.random()
        # option 1: Gain 1 level
        if rand_value <= 1 / 3:
            self.level += 1
        # option 2: Gain 1 HP
        elif 1 / 3 < rand_value < 2 / 3:
            self.IncreaseHP()
        # option 3: Gain 1 HP and 1 level
        else:
            self.IncreaseHP()
            self.level += 1

    def __str__(self) -> str:
        """
        Returns a string containing the pokemon's name, hp and level

        complexity = O(1) as there is only a return statement
        """
        return f"{self.getName()}'s HP = {self.getHp()} and level = {self.getLevel()}"





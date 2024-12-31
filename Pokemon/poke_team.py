from stack_adt import ArrayStack
from sorted_list import ListItem
from queue_adt import CircularQueue
from array_sorted_list import ArraySortedList
from pokemon import Charmander, Squirtle, Bulbasaur, MissingNo

"""
This file contains the PokeTeam class which creates a team of pokemon at a maximum length of 6 pokemon with any
number of charmanders, squirtles or bulbasaurs.
"""
__author__ = "Ollie Hiscoke", "Hirun Hettigoda", "Karim Hajlaoui", "Daniel Hong"


class PokeTeam:
    def __init__(self, name, battle_mode: int = 0, criterion: str = None):
        """
        Initialises the team to None and the battle to whatever is selected. If no battle mode is selected it will be set to 0
        """
        self.name = name
        self.team = None

    def choose_team(self, battle_mode: int, criterion: str = None):
        """
        Creates a pokemon team by asking to user how many of each pokemon they would like in their team then calling
        the assign_team function

        pre-condition = number of pokemon given is correct (maximum 6 pokemon) and the battle is valid (either 0, 1 or 2)

        complexity = O(n) where n is number of pokemon in the team
        """
        # Checks if the battle mode is valid
        self.battle_mode = battle_mode
        if self.battle_mode in [0, 1, 2]:
            self.battle_mode = battle_mode
        else:
            raise ValueError("Invalid battle mode")

        self.criterion = criterion

        valid_input = False

        # Prompts the user to input a team until valid input is given
        while valid_input != True:
            print("Howdy Trainer! Choose your team as C B S M")
            print("where C is the number of Charmanders")
            print("      B is the number Bulbasaurs")
            print("      S is the number of Squirtles")
            print("      M is the number of MissingNo")
            print("You can only have 1 MissingNo")

            # Splits the given input into the 3 values and sets the corresponding pokemon to that amount
            pokemon_team = input().split()
            c, b, s, m = int(pokemon_team[0]), int(pokemon_team[1]), int(pokemon_team[2]), int(pokemon_team[3])

            # Checks to see if there are 6 or less pokemon added to the team
            if c >= 0 and b >= 0 and s >= 0 and 0 <= m <= 1:
                valid_input = c + b + s + m <= 6

                # If it is not valid, print an error
            if valid_input == False:
                print("ERROR: Maximum 6 pokemon allowed in team and 1 MissingNo maximum")

            # Otherwise, call the assign_team function
            else:
                self.assign_team(c, b, s, m)

    def assign_team(self, charm: int, bulb: int, squir: int, missing: int) -> None:
        """
        Adds the pokemon to the chosen ADT based on the chosen battle mode. Stack for battle mode 0, circular queue for battle mode 1 and
        sorted list for battle mode 2.

        complexity = O(n) where n is the number of pokemon in the team
        """

        if self.battle_mode == 0:
            self.team = ArrayStack(6)

            for _ in range(missing):
                self.team.push(MissingNo())

            for _ in range(squir):
                self.team.push(Squirtle())

            for _ in range(bulb):
                self.team.push(Bulbasaur())

            for _ in range(charm):
                self.team.push(Charmander())


        elif self.battle_mode == 1:
            self.team = CircularQueue(6)

            for _ in range(charm):
                self.team.append(Charmander())

            for _ in range(bulb):
                self.team.append(Bulbasaur())

            for _ in range(squir):
                self.team.append(Squirtle())

            for _ in range(missing):
                self.team.append(MissingNo())


        elif self.battle_mode == 2:
            # For MissingNo in this battle mode, intialise the key of it's list item as the lowest value of the criterion of the other pokemon
            # This will mean that it will be at the end of the list and will come out last
            self.team = ArraySortedList(6)
            # When creating the teams a ListItem is created with the key being the value of the criterion and the value being the pokemon object
            if self.criterion == "hp":
                for _ in range(bulb):
                    bulbasaur = Bulbasaur()
                    new_pokemon = ListItem(bulbasaur, bulbasaur.getHp())
                    self.team.add(new_pokemon)
                for _ in range(squir):
                    squirtle = Squirtle()
                    new_pokemon = ListItem(squirtle, squirtle.getHp())
                    self.team.add(new_pokemon)
                for _ in range(charm):
                    charmander = Charmander()
                    new_pokemon = ListItem(charmander, charmander.getHp())
                    self.team.add(new_pokemon)
                for _ in range(missing):
                    missingno = MissingNo()
                    charmander = Charmander()
                    new_pokemon = ListItem(missingno, charmander.getHp())
                    self.team.add(new_pokemon)

            elif self.criterion == "lvl":
                for _ in range(charm):
                    charmander = Charmander()
                    new_pokemon = ListItem(charmander, charmander.getLevel())
                    self.team.add(new_pokemon)
                for _ in range(bulb):
                    bulbasaur = Bulbasaur()
                    new_pokemon = ListItem(bulbasaur, bulbasaur.getLevel())
                    self.team.add(new_pokemon)
                for _ in range(missing):
                    missingno = MissingNo()
                    squirtle = Squirtle()
                    new_pokemon = ListItem(missingno, squirtle.getLevel())
                    self.team.add(new_pokemon)
                for _ in range(squir):
                    squirtle = Squirtle()
                    new_pokemon = ListItem(squirtle, squirtle.getLevel())
                    self.team.add(new_pokemon)

            elif self.criterion == "attack":
                for _ in range(bulb):
                    bulbasaur = Bulbasaur()
                    new_pokemon = ListItem(bulbasaur, bulbasaur.getAttack())
                    self.team.add(new_pokemon)
                for _ in range(squir):
                    squirtle = Squirtle()
                    new_pokemon = ListItem(squirtle, squirtle.getAttack())
                    self.team.add(new_pokemon)
                for _ in range(charm):
                    charmander = Charmander()
                    new_pokemon = ListItem(charmander, charmander.getAttack())
                    self.team.add(new_pokemon)
                for _ in range(missing):
                    missingno = MissingNo()
                    squirtle = Squirtle()
                    new_pokemon = ListItem(missingno, squirtle.getAttack())
                    self.team.add(new_pokemon)

            elif self.criterion == "defence":
                for _ in range(bulb):
                    bulbasaur = Bulbasaur()
                    new_pokemon = ListItem(bulbasaur, bulbasaur.getDefence())
                    self.team.add(new_pokemon)
                for _ in range(squir):
                    squirtle = Squirtle()
                    new_pokemon = ListItem(squirtle, squirtle.getDefence())
                    self.team.add(new_pokemon)
                for _ in range(missing):
                    missingno = MissingNo()
                    charmander = Charmander()
                    new_pokemon = ListItem(missingno, charmander.getDefence())
                    self.team.add(new_pokemon)
                for _ in range(charm):
                    charmander = Charmander()
                    new_pokemon = ListItem(charmander, charmander.getDefence())
                    self.team.add(new_pokemon)

            elif self.criterion == "speed":
                for _ in range(bulb):
                    bulbasaur = Bulbasaur()
                    new_pokemon = ListItem(bulbasaur, bulbasaur.getSpeed())
                    self.team.add(new_pokemon)
                for _ in range(charm):
                    charmander = Charmander()
                    new_pokemon = ListItem(charmander, charmander.getSpeed())
                    self.team.add(new_pokemon)
                for _ in range(missing):
                    missingno = MissingNo()
                    squirtle = Squirtle()
                    new_pokemon = ListItem(missingno, squirtle.getSpeed())
                    self.team.add(new_pokemon)
                for _ in range(squir):
                    squirtle = Squirtle()
                    new_pokemon = ListItem(squirtle, squirtle.getSpeed())
                    self.team.add(new_pokemon)

            else:
                print("ERROR: invalid criterion chosen")

    def __str__(self) -> str:
        return str(self.team)


team = PokeTeam("Ash")
team.battle_mode = 2
team.criterion = 'lvl'
team.assign_team(1,1,1,1)
print(team.team)
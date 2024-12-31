from poke_team import PokeTeam

class Battle:
    def __init__(self, trainer_one_name: str, trainer_two_name: str) -> None:
        self.trainer_one_name = trainer_one_name
        self.trainer_two_name = trainer_two_name
        self.battle_mode = None
        self.team1 = None
        self.team2 = None

    def set_mode_battle(self) -> str:
        self.battle_mode = 0
        self.team1 = PokeTeam()
        self.team2 = PokeTeam()
        self.team1.choose_team(self.battle_mode)
        self.team2.choose_team(self.battle_mode)

        while not self.team2.team.is_empty() and not self.team1.team.is_empty():
            p1 = self.team1.team.pop()
            p2 = self.team2.team.pop()
            if p1.getSpeed() > p2.getSpeed():
                p2.calculateDamage(p1.getAttack(), p1.getPokeType())
                if p2.hp > 0:
                    p1.calculateDamage(p2.getAttack(), p2.getPokeType())
            elif p2.getSpeed() > p1.getSpeed():
                p1.calculateDamage(p2.getAttack(), p2.getPokeType())
                if p1.hp > 0:
                    p2.calculateDamage(p1.getAttack(), p1.getPokeType())
            else:
                p1.calculateDamage(p2.getAttack(), p2.getPokeType())
                p2.calculateDamage(p1.getAttack(), p1.getPokeType())

            if p1.hp > 0 and p2.hp > 0:
                p1.hp -= 1
                p2.hp -= 1
                if p1.hp <= 0 and p2.hp > 0:
                    p2.level += 1
                    self.team2.team.push(p2)
                elif p2.hp <= 0 and p1.hp > 0:
                    p1.level += 1
                    self.team1.team.push(p1)
                else:
                    self.team2.team.push(p2)
                    self.team1.team.push(p1)

            elif p1.hp > 0 and p2.hp <= 0:
                p1.level += 1
                self.team1.team.push(p1)
            elif p2.hp > 0 and p1.hp <= 0:
                p2.level += 1
                self.team2.team.push(p2)

        if self.team1.team.is_empty() and not self.team2.team.is_empty():
            return self.trainer_two_name
        elif self.team2.team.is_empty() and not self.team1.team.is_empty():
            return self.trainer_one_name
        else:
            return "Draw"

    def rotating_mode_battle(self) -> str:
        """
        Conducts the set battle and returns the winners name or Draw. This mode has the pokemon return to the back of team after attacking if they do not faint

        pre-condition = both teams are valid (maxmimum of 6 pokemon per team)

        complexity =
        """
        # Set the battle mode to 0 and create the pokemon teams
        self.battle_mode = 1
        self.team1 = PokeTeam()
        self.team2 = PokeTeam()
        self.team1.choose_team(self.battle_mode)
        self.team2.choose_team(self.battle_mode)

        while not self.team2.team.is_empty() and not self.team1.team.is_empty():

            # Get the first element of both queues
            p1 = self.team1.team.serve()
            p2 = self.team2.team.serve()

            print(self.team1.team)

            # If P1 is faster then P1 attacks and P2 defends
            if p1.getSpeed() > p2.getSpeed():
                p2.calculateDamage(p1.getAttack(), p1.getPokeType())

                # If P2 is still alive it returns with an attack of it's own
                if p2.hp > 0:
                    p1.calculateDamage(p2.getAttack(), p2.getPokeType())

            # If P2 is faster then P2 attacks
            elif p2.getSpeed() > p1.getSpeed():
                p1.calculateDamage(p2.getAttack(), p2.getPokeType())

                # If P1 is still alive it returns with an attack of it's own
                if p1.hp > 0:
                    p2.calculateDamage(p1.getAttack(), p1.getPokeType())

            # Otherwise, both pokemon attack simultaneously even if one of them faints
            else:
                p1.calculateDamage(p2.getAttack(), p2.getPokeType())
                p2.calculateDamage(p1.getAttack(), p1.getPokeType())

            # If both are still alive they both lose 1 hp
            if p1.hp > 0 and p2.hp > 0:
                p1.hp -= 1
                p2.hp -= 1

                # If P1 faints, P2 gains a level and is added back to the front of the team
                if p1.hp <= 0 and p2.hp > 0:
                    p2.level += 1
                    self.team2.team.append(p2)

                # If P2 faints, P1 gains a level and is added back to the front of the team
                elif p2.hp <= 0 and p1.hp > 0:
                    p1.level += 1
                    self.team1.team.append(p1)

                # If both are still alive, they are both added back to the start of their team
                else:
                    self.team2.team.append(p2)
                    self.team1.team.append(p1)

            # If P2 has fainted, P1 gains a level and is returned back to the front of the team
            elif p1.hp > 0 and p2.hp <= 0:
                p1.level += 1
                self.team1.team.append(p1)

            # If P1 has fainted, P2 gains a level and is returned to the front of the team
            elif p2.hp > 0 and p1.hp <= 0:
                p2.level += 1
                self.team2.team.append(p2)

            print(self.team1.team)

        # If team 1 is empty and team 2 is not, trainer 2 has won
        if self.team1.team.is_empty() and not self.team2.team.is_empty():
            return self.trainer_two_name

        # If team 2 is empty and team 1 is not, trainer 1 has won
        elif self.team2.team.is_empty() and not self.team1.team.is_empty():
            return self.trainer_one_name

        # If both are empty it is a draw
        else:
            return "Draw"

    def optimised_mode_battle(self, criterion_team1: str, criterion_team2: str) -> str:
        self.battle_mode = 2
        self.team1 = PokeTeam(self.trainer_one_name)
        self.team2 = PokeTeam(self.trainer_two_name)
        self.team1.choose_team(self.battle_mode, criterion_team1)
        self.team2.choose_team(self.battle_mode, criterion_team2)

        def update_criterion(team, pokemon):
            if team.criterion == "hp" and pokemon.key != pokemon.value.getHp():
                pokemon.key = pokemon.value.getHp()
                team.team.delete_at_index(len(team.team) - 1)
                team.team.add(pokemon)
            elif team.criterion == "lvl" and pokemon.key != pokemon.value.getLevel():
                pokemon.key = pokemon.value.getLevel()
                team.team.delete_at_index(len(team.team) - 1)
                team.team.add(pokemon)
            elif team.criterion == "attack" and pokemon.key != pokemon.value.getAttack():
                pokemon.key = pokemon.value.getAttack()
                team.team.delete_at_index(len(team.team) - 1)
                team.team.add(pokemon)
            elif team.criterion == "defence" and pokemon.key != pokemon.value.getDefence():
                pokemon.key = pokemon.value.getDefence()
                team.team.delete_at_index(len(team.team) - 1)
                team.team.add(pokemon)
            elif team.criterion == "speed" and pokemon.key != pokemon.value.getSpeed():
                pokemon.key = pokemon.value.getSpeed()
                team.team.delete_at_index(len(team.team) - 1)
                team.team.add(pokemon)

        while not self.team2.team.is_empty() and not self.team1.team.is_empty():

            # Get the last element of both lists
            list_item1 = self.team1.team[len(self.team1.team) - 1]
            list_item2 = self.team2.team[len(self.team2.team) - 1]

            p1 = list_item1.value
            p2 = list_item2.value

            # If P1 is faster then P1 attacks and P2 defends
            if p1.getSpeed() > p2.getSpeed():
                p2.calculateDamage(p1.getAttack(), p1.getPokeType())

                # If P2 is still alive it returns with an attack of it's own
                if p2.hp > 0:
                    p1.calculateDamage(p2.getAttack(), p2.getPokeType())

            # If P2 is faster then P2 attacks
            elif p2.getSpeed() > p1.getSpeed():
                p1.calculateDamage(p2.getAttack(), p2.getPokeType())

                # If P1 is still alive it returns with an attack of it's own
                if p1.hp > 0:
                    p2.calculateDamage(p1.getAttack(), p1.getPokeType())

            # Otherwise, both pokemon attack simultaneously even if one of them faints
            else:
                p1.calculateDamage(p2.getAttack(), p2.getPokeType())
                p2.calculateDamage(p1.getAttack(), p1.getPokeType())

            # If both are still alive they both lose 1 hp
            if p1.hp > 0 and p2.hp > 0:
                p1.hp -= 1
                p2.hp -= 1

            # If P1 faints, P2 gains a level and P1 is removed from it's team while P2 is re-sorted into the list
            if p1.hp <= 0 and p2.hp > 0:
                p2.level += 1
                self.team1.team.delete_at_index(len(self.team1.team) - 1)
                update_criterion(self.team2, list_item2)

            # If P2 faints, P1 gains a level and is added back to the front of the team
            elif p2.hp <= 0 and p1.hp > 0:
                p1.level += 1
                self.team2.team.delete_at_index(len(self.team2.team) - 1)
                update_criterion(self.team1, list_item1)

            # If both are still alive, they are both added back to the start of their team
            else:
                update_criterion(self.team2, list_item2)
                update_criterion(self.team1, list_item1)

            # If team 1 is empty and team 2 is not, trainer 2 has won
        if self.team1.team.is_empty() and not self.team2.team.is_empty():
            return self.trainer_two_name

            # If team 2 is empty and team 1 is not, trainer 1 has won
        elif self.team2.team.is_empty() and not self.team1.team.is_empty():
            return self.trainer_one_name

            # If both are empty it is a draw
        else:
            return "Draw"


battle = Battle("Ash", "Brock")
print(battle.optimised_mode_battle("hp","lvl"))

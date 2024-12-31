import unittest
from tester_base import TesterBase, captured_output
from poke_team import PokeTeam
from stack_adt import ArrayStack


class TestPokemonTeam(TesterBase):
    def test_choose_team(self):
        try:
            team = PokeTeam("Ash")
            team.battle_mode = 0
        except Exception as e:
            self.verificationErrors.append(f"Team could not be instantiated: {str(e)}.")
            return
        try:
            with captured_output("4 0 1 0\n1 1 1 0") as (inp, out, err):
                team.choose_team(team.battle_mode)
        except Exception as e:
            self.verificationErrors.append(f"Team could not be picked: {str(e)}.")

        output = out.getvalue().strip()
        try:
            assert "Howdy Trainer! Choose your team as C B S M" in output
            assert "where C is the number of Charmanders" in output
            assert "      B is the number Bulbasaurs" in output
            assert "      S is the number of Squirtles" in output
            assert "      M is the number of MissingNo" in output
            assert "You can only have 1 MissingNo" in output
        except AssertionError:
            self.verificationErrors.append(f"Prompt was not printed correctly")
            return

    def test_assign_team(self):
        try:
            team = PokeTeam("Ash")
        except Exception as e:
            self.verificationErrors.append(f"Team could not be instantiated: {str(e)}.")

        try:  # battle mode 0
            with captured_output("2 2 2 0") as (inp, out, err):
                team.battle_mode = 0
                builtTeam = team.assign_team(1, 1, 1, 1)
        except Exception as e:
            self.verificationErrors.append(f"Team could not be allocated in battle mode 0: {str(e)}.")

        try:  # battle mode 1
            with captured_output("2 2 2 0") as (inp, out, err):
                team.battle_mode = 1
                builtTeam = team.assign_team(1, 1, 1, 1)
        except Exception as e:
            self.verificationErrors.append(f"Team could not be allocated correctly in battle mode 1: {str(e)}.")

        # battle mode 2- Missing No is in the first position
        # criterion- lvl,attack, hp, defence and speed
        try:
            with captured_output("2 2 2 0") as (inp, out, err):
                team.battle_mode = 2
                team.criterion = 'lvl'
                builtTeam = team.assign_team(1, 1, 1, 1)
        except Exception as e:
            self.verificationErrors.append(f"Team could not be allocated based on lvl:{str(e)}.")

        try:
            with captured_output("2 2 2 0") as (inp, out, err):
                team.battle_mode = 2
                team.criterion = 'attack'
                builtTeam = team.assign_team(1, 1, 1, 1)
        except Exception as e:
            self.verificationErrors.append(f"Team could not be allocated based on attack:{str(e)}.")

        try:
            with captured_output("2 2 2 0") as (inp, out, err):
                team.battle_mode = 2
                team.criterion = 'hp'
                builtTeam = team.assign_team(1, 1, 1, 1)
        except Exception as e:
            self.verificationErrors.append(f"Team could not be allocated based on hp:{str(e)}.")

        try:
            with captured_output("2 2 2 0") as (inp, out, err):
                team.battle_mode = 2
                team.criterion = 'defence'
                builtTeam = team.assign_team(1, 1, 1, 1)
        except Exception as e:
            self.verificationErrors.append(f"Team could not be allocated based on defence:{str(e)}.")

        try:
            with captured_output("2 2 2 0") as (inp, out, err):
                team.battle_mode = 2
                team.criterion = 'speed'
                builtTeam = team.assign_team(2, 2, 2, 0)
        except Exception as e:
            self.verificationErrors.append(f"Team could not be allocated based on speed:{str(e)}.")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPokemonTeam)
    unittest.TextTestRunner(verbosity=0).run(suite)
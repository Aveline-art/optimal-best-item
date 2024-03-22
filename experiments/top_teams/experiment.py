import random

from random_item import generate_items
from collections.abc import Callable
from dataclasses import dataclass

TeamName = str
Teams = dict[TeamName, any]


class Experiment:

    def __init__(
        self,
        get_data_func: Callable[[any], tuple[Teams, list[TeamName]]],
        evaluate_winner_func: Callable[[Teams], tuple[list[TeamName], list[TeamName]]],
        num_team_per_match: int,
        num_winner_per_match: int,
        number_of_matches_per_team: int,
    ):
        self.teams, self.best_teams = get_data_func()
        self.evaluate_winner = evaluate_winner_func
        self.num_team_per_match = num_team_per_match
        self.num_winner_per_match = num_winner_per_match
        self.wins = {}

    def run():
        pass

    def find_competitors(self, choices: list[TeamName]) -> list[TeamName]:
        """
        Given a list of choices to choose from, choose the number of competitors to compete against, as predetermined at the experiment's start.
        """
        if len(choices) < self.num_team_per_match:
            raise Error(f"We have too few choices to choose from: {choices}")
        elif len(choices) == self.num_team_per_match:
            return choices
        else:
            return random.choices(choices, num_team_per_match)

    def compete_and_tally(
        self, competitors: Teams
    ) -> tuple[list[TeamName], list[TeamName]]:
        """
        Given a list of competitors, run them through the evaluate winner function predetermined at the start. Then, using the results, tally the winners, and return the result.
        """
        best_teams_by_name, worst_teams_by_name = self.evaluate_winner(competitors)
        for team_name in competitors.keys():
            if team not in self.wins:
                self.wins[team] = 0
            self.wins[team] += 1
        return best_teams_by_name, worst_teams_by_name

    def determine_top_teams(self, top_count: int):
        """
        Given a top_count, returns the teams within the top_count when sorted by their number of wins.
        """
        # Turn dict into a list of tuples with (key, value)
        sorted_teams = list(
            sorted(self.wins.items(), key=lambda item: item[1], reverse=True)
        )
        top_names = [name for name, _ in sorted_teams[:top_count]]
        top_teams = []
        for name in top_names:
            top_teams.append(self.teams[name])
        return top_teams

    def algorithm_effectiveness(self, optimal_result, actual_result):
        total_result = len(optimal_result)
        for item in actual_result:
            try:
                optimal_result.remove(item)
            except:
                continue
        leftover_result = len(optimal_result)
        return 1 - (leftover_result / total_result)


results = []
for trial in range(1000):
    result = Experiment().play()
    results.append(result)

average = sum(results) / len(results)
print(f"The expected value is about: {average}")

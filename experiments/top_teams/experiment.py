import random

from collections.abc import Callable
from dataclasses import dataclass

TeamName = str
Teams = dict[TeamName, any]


class Experiment:

    def __init__(
        self,
        teams: Teams,
        best_teams: list[TeamName],
        choose_opponents_func: Callable[
            [TeamName, Teams, list[TeamName]], list[TeamName]
        ],
        evaluate_winner_func: Callable[[Teams], tuple[list[TeamName], list[TeamName]]],
        num_of_matches_per_team: int,
    ):
        self.teams = teams
        self.best_teams = best_teams
        self.choose_opponents_func = choose_opponents_func
        self.evaluate_winners = evaluate_winner_func
        self.num_of_matches_per_team = num_of_matches_per_team
        self.wins = {key: 0 for key in self.teams.keys()}

    def run(self):
        for current_team, team_data in self.teams.items():
            past_losers = []
            for i in range(self.num_of_matches_per_team):
                competitors_for_round = {current_team: team_data}

                # Choose opponents
                opponent_names = self.choose_opponents_func(
                    current_team, self.teams, past_losers
                )

                # Add opponents to this round
                for opponent_name in opponent_names:
                    competitors_for_round[opponent_name] = self.teams[opponent_name]

                # Determine a list of winners and losers
                winners, losers = self.evaluate_winners(competitors_for_round)
                past_losers += losers
                for winner in winners:
                    self.wins[winner] += 1

    def determine_top_teams(self, top_count: int):
        """
        Given a top_count, returns the teams within the top_count when sorted by their number of wins.
        """
        # Turn dict into a list of tuples with (key, value)
        sorted_teams = list(
            sorted(self.wins.items(), key=lambda item: item[1], reverse=True)
        )
        top_names = [name for name, _ in sorted_teams[:top_count]]
        return top_names

    def algorithm_effectiveness(self, optimal_result, actual_result):
        total_result = len(optimal_result)
        for item in actual_result:
            try:
                optimal_result.remove(item)
            except:
                continue
        leftover_result = len(optimal_result)
        return 1 - (leftover_result / total_result)

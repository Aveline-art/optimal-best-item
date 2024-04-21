import random
from collections.abc import Callable
from dataclasses import dataclass

TeamName = str
TeamData = any
Teams = dict[TeamName, TeamData]


class Experiment:

    def __init__(
        self,
        teams: Teams,
        best_teams: list[TeamName],
        num_of_matches_per_team: int,
    ):
        self.teams = teams
        self.best_teams = best_teams
        self.num_of_matches_per_team = num_of_matches_per_team
        self.wins = {key: 0 for key in self.teams.keys()}

    def run(self):
        for current_team, team_data in self.teams.items():
            past_losers = []
            for i in range(self.num_of_matches_per_team):
                competitors_for_round = {current_team: team_data}

                # Choose opponents
                opponent_names = self.choose_opponents(
                    current_team, self.teams, past_losers
                )

                # Add opponents to this round
                for opponent_name in opponent_names:
                    competitors_for_round[opponent_name] = self.teams[opponent_name]

                # Determine a list of winners and losers
                winners, losers = self.evaluate_winner(competitors_for_round)
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

    def algorithm_effectiveness(self, actual_result: list[TeamName]):
        if len(actual_result) == 0:
            return 0
        score = 0
        for team in actual_result:
            if team in self.best_teams:
                score += 1
        return score / len(actual_result)

    def choose_opponents(
        self,
        current_team: TeamName,
        all_teams: dict[TeamName, TeamData],
        past_losers: list[TeamName],
    ) -> list[TeamName]:
        raise NotImplementedError

    def evaluate_winner(
        self, teams: dict[TeamName, TeamData]
    ) -> tuple[list[TeamName], list[TeamName]]:
        raise NotImplementedError

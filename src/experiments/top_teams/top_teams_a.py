import random
from dataclasses import dataclass

from experiment_utils.random_data import get_data

from .experiment import Experiment, TeamData, TeamName


class TopTeamsA(Experiment):

    # These are the actual number of best teams and total teams to consider
    num_best_teams = 50
    num_total_teams = 100

    # This defines the nature of the competition
    num_rounds_per_team = 3
    num_competitors_per_round = 10
    num_winners_per_round = 3

    # This defines how many teams the strategy should return
    num_teams_in_result = 50

    # This defines the rate in which we can be incorrect when evaluating a winner
    false_positive = 0.27
    false_negative = 0.1

    def __init__(self, num_trials: int):
        self.num_trials = num_trials
        team_data, best_team_list = get_data(
            num_best_items=self.num_best_teams,
            num_total_items=self.num_total_teams,
            format_team_data=self.format_team_data,
        )
        super().__init__(
            teams=team_data,
            best_teams=best_team_list,
            num_of_matches_per_team=self.num_rounds_per_team,
        )

    def start(self):
        results = []
        for trial in range(self.num_trials):
            print(f"Now running trial no. {trial}")
            self.run()
            experiment_best_team_list = self.determine_top_teams(
                self.num_teams_in_result
            )
            result = self.algorithm_effectiveness(experiment_best_team_list)
            results.append(result)
        return results

    def choose_opponents(
        self,
        current_team: TeamName,
        all_teams: dict[TeamName, TeamData],
        past_losers: list[TeamName],
    ) -> list[TeamName]:
        all_teams_names = all_teams.keys()
        possible_opponents = [
            team_name
            for team_name in all_teams_names
            if team_name not in past_losers or team_name == current_team
        ]

        # There are enough teams we have not won against to keep competing
        if len(possible_opponents) > self.num_competitors_per_round - 1:
            return random.sample(
                possible_opponents, k=self.num_competitors_per_round - 1
            )

        # We will have to also add some past losers
        else:
            num_losers_to_add = num_competitors_per_round - (
                1 + len(possible_opponents)
            )
            additional_losers = random_choices(past_losers, k=num_losers_to_add)
            return possible_opponents + additional_losers

    def evaluate_winner(
        self, teams: dict[TeamName, TeamData]
    ) -> tuple[list[TeamName], list[TeamName]]:
        # These are what the ai thinks are winners, despite their actual status
        ai_winners = []
        # These are what the ai thinks are losers, despite their actual status
        ai_losers = []
        for team_name, team_data in teams.items():
            # Is actually the best.
            if team_data["is_best"]:
                ai_is_winner = random.choices(
                    (True, False),
                    weights=(1 - self.false_negative, self.false_negative),
                )[0]
            # Is actually not the best.
            else:
                ai_is_winner = random.choices(
                    (True, False),
                    weights=(self.false_positive, 1 - self.false_positive),
                )[0]
            if ai_is_winner:
                ai_winners.append(team_name)
            else:
                ai_losers.append(team_name)

        # Shuffle list to prevent bias to any item.
        random.shuffle(ai_winners)
        random.shuffle(ai_losers)
        combined_list = ai_winners + ai_losers

        return (
            combined_list[: self.num_winners_per_round],
            combined_list[self.num_winners_per_round :],
        )

    @staticmethod
    def format_team_data(team_name, is_best) -> TeamData:
        if is_best:
            return {"value": random.choice(range(100, 200)), "is_best": True}
        else:
            return {"value": random.choice(range(10, 20)), "is_best": False}

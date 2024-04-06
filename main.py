import random
import statistics
from dataclasses import dataclass

from data.random_data import get_data
from experiments.top_teams.experiment import Experiment as Top_Teams

# Declare presets

# These are the actual number of best teams and total teams to consider
num_best_teams = 90
num_total_teams = 100

# This defines the nature of the competition
num_rounds_per_team = 5
num_competitors_per_round = 10
num_winners_per_round = 3

# This defines how many teams the strategy should return
num_teams_in_result = 50

# This defines the number of trials to run each experiment
num_trials_to_run = 1000

# Declare typing
TeamName = str


@dataclass
class TeamData:
    value: int


def main():
    results = []
    for trial in range(num_trials_to_run):
        print(f"Now running trial no. {trial}")
        team_data, best_team_list = get_data(
            num_best_items=num_best_teams,
            num_total_items=num_total_teams,
            format_team_data=format_team_data,
        )
        experiment = Top_Teams(
            teams=team_data,
            best_teams=best_team_list,
            choose_opponents_func=choose_opponents_func,
            evaluate_winner_func=evaluate_winner_func,
            num_of_matches_per_team=num_rounds_per_team,
        )
        experiment.run()
        experiment_best_team_list = experiment.determine_top_teams(num_teams_in_result)
        result = algorithm_effectiveness(best_team_list, experiment_best_team_list)
        results.append(result)
    print(
        f"After {num_trials_to_run} trials, this strategy would generate a list of best teams that contains {statistics.fmean(results) * 100}% of items from the actual list of best teams."
    )


def choose_opponents_func(
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
    if len(possible_opponents) > num_competitors_per_round - 1:
        return random.sample(possible_opponents, k=num_competitors_per_round - 1)

    # We will have to also add some past losers
    else:
        num_losers_to_add = num_competitors_per_round - (1 + len(possible_opponents))
        additional_losers = random_choices(past_losers, k=num_losers_to_add)
        return possible_opponents + additional_losers


def evaluate_winner_func(
    teams: dict[TeamName, TeamData]
) -> tuple[list[TeamName], list[TeamName]]:
    sorted_teams = list(
        sorted(teams.items(), key=lambda team: team[1]["value"], reverse=True)
    )
    winners = sorted_teams[:num_winners_per_round]
    losers = sorted_teams[num_winners_per_round:]
    winner_names = [name for name, _ in winners]
    loser_names = [name for name, _ in losers]
    return winner_names, loser_names


def format_team_data(team_name, is_best) -> TeamData:
    if is_best:
        return {"value": random.choice(range(100, 200))}
    else:
        return {"value": random.choice(range(10, 20))}


def algorithm_effectiveness(
    optimal_result: list[TeamName], actual_result: list[TeamName]
) -> float:
    score = 0
    for team in actual_result:
        if team in optimal_result:
            score += 1
    return score / len(actual_result)


main()

import pytest

from experiments.top_teams.experiment import Experiment


@pytest.fixture
def demo_team_data():
    return {"a": 1, "b": 1, "c": 1}


@pytest.fixture
def demo_best_team():
    return ["a", "b"]


@pytest.fixture
def get_experiment(demo_team_data, demo_best_team):
    def inner(matches):
        return Experiment(demo_team_data, demo_best_team, matches)

    return inner


@pytest.fixture
def get_wins_and_top_teams():
    def inner(top_teams_count, total_teams_count):
        assert total_teams_count > top_teams_count
        top_teams = [str(i) for i in range(top_teams_count)]
        wins = {}
        for i in range(total_teams_count):
            if str(i) in top_teams:
                wins[str(i)] = 100
            else:
                wins[str(i)] = 50

        return wins, top_teams

    return inner


class TestExperiment:

    def test_presets(self, get_experiment, demo_team_data, demo_best_team):
        experiment = get_experiment(1)
        assert experiment.teams == demo_team_data
        assert experiment.best_teams == demo_best_team
        assert experiment.num_of_matches_per_team == 1
        assert experiment.wins == {"a": 0, "b": 0, "c": 0}

        experiment = get_experiment(3)
        assert experiment.num_of_matches_per_team == 3

    def test_top_teams(self, get_experiment, get_wins_and_top_teams):
        wins, top_teams = get_wins_and_top_teams(10, 20)
        experiment = get_experiment(1)
        experiment.wins = wins
        assert experiment.determine_top_teams(10) == top_teams
        assert experiment.determine_top_teams(5) == top_teams[:5]
        assert experiment.determine_top_teams(4) != top_teams[:5]

    def test_algorithm_effectiveness(self, get_experiment, demo_best_team):
        experiment = get_experiment(1)
        actual_result = demo_best_team.copy()
        assert experiment.algorithm_effectiveness(actual_result) == 2 / 2

        actual_result.append("c")
        assert experiment.algorithm_effectiveness(actual_result) == 2 / 3

        actual_result.pop(0)
        assert experiment.algorithm_effectiveness(actual_result) == 1 / 2

        actual_result.extend(["d", "e", "f"])
        assert experiment.algorithm_effectiveness(actual_result) == 1 / 5

        actual_result.append("a")
        assert experiment.algorithm_effectiveness(actual_result) == 2 / 6

    def test_not_implemeneted(self, get_experiment, demo_team_data):
        experiment = get_experiment(10)

        with pytest.raises(NotImplementedError):
            experiment.choose_opponents("a", demo_team_data, ["b"])

        with pytest.raises(NotImplementedError):
            experiment.evaluate_winner(demo_team_data)

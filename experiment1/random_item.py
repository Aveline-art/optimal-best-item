import random


# Note: 120 total teams because it is a very divisible number (2, 3, 4, 5, 6, 8, 10, 12...)
def generate_teams(num_best_teams: int= 20, num_total_teams: int = 120, best_team_range: tuple[int, int]= (50, 60), other_team_range: tuple[int, int]= (0, 10)) -> list[int]:
    best_team_min, best_team_max = best_team_range
    other_team_min, other_team_max = other_team_range

    assert best_team_min < best_team_max, f"best_team_max, {best_team_max} is less than best_team_min {best_team_min}"
    assert other_team_min < other_team_max, f"other_team_max, {other_team_max} is less than other_team_min {other_team_min}"
    assert other_team_max < best_team_min, f"best_team_max, {best_team_max} is less than other_team_min {other_team_min}"
    assert num_best_teams < num_total_teams, f"num_total_teams, {num_total_teams} is less than num_best_teams {num_best_teams}"

    best_teams = random.choices(range(best_team_min, best_team_max), k=num_best_teams)
    other_teams = random.choices(range(other_team_min, other_team_max), k=num_total_teams - num_best_teams)

    all_teams = best_teams + other_teams
    random.shuffle(all_teams)

    return all_teams, best_teams
import statistics

from top_teams import TopTeamsA


def main():
    top_teams_a = TopTeamsA(1000)
    results = top_teams_a.start()
    print(
        f"After {top_teams_a.num_trials} trials, this strategy would generate a list of {top_teams_a.num_teams_in_result} best teams where {statistics.fmean(results) * 100}% of items are from the actual list of best teams."
    )
    print(
        f"If this was done using AI, this would take {top_teams_a.num_rounds_per_team * top_teams_a.num_total_teams} API calls per {top_teams_a.num_total_teams} teams."
    )


main()

import random

from random_item import generate_teams


class Experiment:

    def __init__(self):
        self.teams, self.best_teams = generate_teams()
        self.wins = {}
        pass

    def find_victories(self, team, team_index, games=5):
        victory_count = 0
        seen_team_index = [team_index]
        for i in range(games):
            not_seem_teams = [
                (team_idx, team)
                for team_idx, team in enumerate(self.teams)
                if team_idx not in seen_team_index
            ]
            opponent_team_idx, opponent_team = random.choice(not_seem_teams)
            seen_team_index.append(opponent_team_idx)
            winner_idx = self.determine_winner(
                team, opponent_team, team_index, opponent_team_idx
            )
            if winner_idx == team_index:
                victory_count += 1
        self.wins[team_index] = victory_count

    def determine_winner(self, team_a, team_b, team_a_idx, team_b_idx):
        if team_a > team_b:
            return team_a_idx
        elif team_b > team_a:
            return team_b_idx
        else:
            return random.choice([team_a_idx, team_b_idx])

    def determine_top_teams(self, number_teams: int):
        sorted_teams = list(
            sorted(self.wins.items(), key=lambda item: item[1], reverse=True)
        )
        top_idx = [idx for idx, _ in sorted_teams[:number_teams]]
        top_teams = []
        for idx in top_idx:
            top_teams.append(self.teams[idx])
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

    def play(self):
        for idx, team in enumerate(self.teams):
            self.find_victories(team, idx)
        top_teams = self.determine_top_teams(40)
        result = self.algorithm_effectiveness(self.best_teams.copy(), top_teams)
        return result


results = []
for trial in range(1000):
    result = Experiment().play()
    results.append(result)

average = sum(results) / len(results)
print(f"The expected value is about: {average}")

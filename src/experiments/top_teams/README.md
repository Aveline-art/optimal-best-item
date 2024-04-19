## Experiment 1

In experiment 1, I will simulate match up between random "teams". Each team will have a value, determining how good a team is. A team with a higher value will always defeat a team with a lower value. I will attempt to find as many good teams as possible through a limited number of matchups and tallying the number of victories per team.

Result from brute force algorithm:
About 92% accurate with these parameters:

- There are 20 actual best teams, from a total teams of 120 teams (17% of teams are the best).
- For each team, we perform 5 games (4% of total comparisons) against a different team each\*. If a team wins, they score 1 point.
- We obtain the top 40 teams after the tallying the scores. (33% of total teams)

\*Note that we consider match (teamA, teamB) to be different from (teamB, teamA). This is a bug for now, but once fix, should only increase, rather than decrease accuracy.

from functions import player_stats, team_players

print("Enter team name: ")
team_name = input()
print("Enter the number of days you want the statictics to be shown: ")
days_ago = input()

for player in team_players(team_name):
    print(player_stats(player, days_ago))

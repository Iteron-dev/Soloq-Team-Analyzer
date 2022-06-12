from functions import player_stats, team_players
import pandas as pd

print("Enter team name: ")
team_name = input()
print("Enter the number of days you want the statistics to be shown: ")
days_ago = input()
df_list = []
for player in team_players(team_name):
    df = pd.DataFrame((player_stats(player, days_ago)))
    df_t = df.T
    df_t.columns = ['Games', 'Win ratio', 'KDA', 'CS', 'DMGD%', 'Gold%']
    df_t = df_t.sort_values(by="Games", ascending=False)
    df_t.name = player
    df_list.append(df_t)

excel_filename = input("Please type file name (with .xlsx file format): ")

try:
    with pd.ExcelWriter(excel_filename) as writer:
        for df in df_list:
            df.to_excel(writer, sheet_name=df.name)
        print("Excel file created!")
except ValueError:
    print("File name without .xlsx file format")


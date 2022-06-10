import requests
from bs4 import BeautifulSoup


def team_players(team_name):
    page_url = 'https://lol.fandom.com/wiki/%s' % team_name
    page = requests.get(page_url)

    soup = BeautifulSoup(page.content, 'html.parser')

    tab = soup.find("table", {"class": "wikitable sortable team-members hoverable-rows team-members-current"})

    players = tab.find_all("td", class_="team-members-player")
    role_player = tab.find_all("td", class_="team-members-role")
    player_nicknames = {}
    roles = []
    i = 0
    for role in role_player:
        roles.append(role.text)
        i += 1
    o = 0
    for key in players:
        if roles[o] != "Top Laner" and roles[o] != "Jungler" and roles[o] != "Mid Laner" and roles[o] != "Bot Laner" and \
                roles[o] != "Support":
            o += 1
            continue
        player_nicknames[key.text] = roles[o]
        o += 1
    return player_nicknames

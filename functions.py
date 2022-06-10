import requests
from bs4 import BeautifulSoup
import json

requests.packages.urllib3.disable_warnings()

# api key
with open('config.json') as conf:
    config_data = json.load(conf)

api_key = config_data['api_Key']


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


def player_nickname_to_lol_nickname(player):
    page_url = 'https://lolpros.gg/player/%s' % player
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    lol_nicknames = soup.find_all("div", class_="summoner-name")[0]
    lol_nickname = lol_nicknames.find("p").text
    return lol_nickname


def lol_nick_to_puuid(nick):
    url = 'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/%s' % nick

    response_puuid = requests.get(
        url,
        headers={'X-Riot-Token': api_key},
        verify=False
    )

    return response_puuid.json()["puuid"]


def matches_ago(puuid, unix_start_time):
    def next_matches(start, end):
        url = 'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/%s/ids?startTime=%s&queue=420&start=%s&count=%s' % (
            puuid, unix_start_time, start, end)
        response_ago = requests.get(
            url,
            headers={'X-Riot-Token': api_key},
            verify=False
        )

        return response_ago.json()

    empty_list = []
    start = 0
    count = 100
    matches_ago = next_matches(start, count)
    while next_matches(start, count) != empty_list:
        start += 100
        matches_ago.extend(next_matches(start, count))

    return matches_ago


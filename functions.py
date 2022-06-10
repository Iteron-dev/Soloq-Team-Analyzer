import requests
from bs4 import BeautifulSoup
import json
from time import sleep
from datetime import datetime
from datetime import timedelta

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
    sleep(1.2)
    url = 'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/%s' % nick
    response_puuid = requests.get(
        url,
        headers={'X-Riot-Token': api_key},
        verify=False
    )

    return response_puuid.json()["puuid"]


def matches_ago(puuid, unix_start_time):
    def next_matches(start, end):
        sleep(1.2)
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


def match_detail_fun(match_id):
    sleep(1.2)
    url = 'https://europe.api.riotgames.com/lol/match/v5/matches/%s' % match_id
    response_detail = requests.get(
        url,
        headers={'X-Riot-Token': api_key},
        verify=False
    )

    return response_detail.json()


def matches_stats(matches, puuid):
    champs_all = {}
    kill_all = {}
    deaths_all = {}
    assists_all = {}
    wins_all = {}
    loses_all = {}
    minion_all = {}
    minion_per = {}
    kda = {}
    winratio = {}

    dmgd_p = {}
    dmg_all = {}
    dmg_all_a = {}

    gold_p = {}
    gold_all = {}
    gold_all_a = {}

    p = 0
    for key in matches:
        p += 1

    match_index = 0
    while match_index < p:
        match_detail = match_detail_fun(matches[match_index])
        puuid_index = 0
        for puuid_cur in match_detail['metadata']['participants']:
            if puuid_cur == puuid:
                break
            else:
                puuid_index += 1

        champ = match_detail['info']['participants'][puuid_index]['championName']
        kills = match_detail['info']['participants'][puuid_index]['kills']
        deaths = match_detail['info']['participants'][puuid_index]['deaths']
        assists = match_detail['info']['participants'][puuid_index]['assists']
        minions = match_detail['info']['participants'][puuid_index]['totalMinionsKilled']
        neutralminions = match_detail['info']['participants'][puuid_index]['neutralMinionsKilled']
        totalminions = minions + neutralminions

        dmgd = match_detail['info']['participants'][puuid_index]['totalDamageDealtToChampions']

        gold = match_detail['info']['participants'][puuid_index]['goldEarned']

        win_boolean = match_detail['info']['participants'][puuid_index]['win']

        dmg_index = 0
        dmgd_a = 0
        while dmg_index < 10:
            if win_boolean == match_detail['info']['participants'][dmg_index]['win']:
                dmgd_a = match_detail['info']['participants'][dmg_index]['totalDamageDealtToChampions'] + dmgd_a
            dmg_index += 1

        gold_index = 0
        gold_a = 0
        while gold_index < 10:
            if win_boolean == match_detail['info']['participants'][gold_index]['win']:
                gold_a = match_detail['info']['participants'][gold_index]['goldEarned'] + gold_a
            gold_index += 1

        if win_boolean:
            wins = 1
            loses = 0
        else:
            wins = 0
            loses = 1

        try:
            champs_all[champ] += 1
        except KeyError:
            champs_all[champ] = 1
        try:
            kill_all[champ]
        except KeyError:
            kill_all[champ] = 0
        try:
            deaths_all[champ]
        except KeyError:
            deaths_all[champ] = 0
        try:
            assists_all[champ]
        except KeyError:
            assists_all[champ] = 0
        try:
            wins_all[champ]
        except KeyError:
            wins_all[champ] = 0
        try:
            loses_all[champ]
        except KeyError:
            loses_all[champ] = 0
        try:
            minion_all[champ]
        except KeyError:
            minion_all[champ] = 0
        try:
            dmg_all[champ]
        except KeyError:
            dmg_all[champ] = 0
        try:
            dmg_all_a[champ]
        except KeyError:
            dmg_all_a[champ] = 0
        try:
            dmgd_p[champ]
        except KeyError:
            dmgd_p[champ] = 0
        try:
            gold_all[champ]
        except KeyError:
            gold_all[champ] = 0
        try:
            gold_all_a[champ]
        except KeyError:
            gold_all_a[champ] = 0
        try:
            gold_p[champ]
        except KeyError:
            gold_p[champ] = 0

        kill_all[champ] = kills + kill_all[champ]
        deaths_all[champ] = deaths + deaths_all[champ]
        assists_all[champ] = assists + assists_all[champ]
        minion_all[champ] = totalminions + minion_all[champ]
        dmg_all[champ] = dmg_all[champ] + dmgd
        dmg_all_a[champ] = dmg_all_a[champ] + dmgd_a
        dmgd_p[champ] = str(round(dmg_all[champ] / dmg_all_a[champ], 2) * 100).split('.')[0] + "%"

        gold_all[champ] = gold_all[champ] + gold
        gold_all_a[champ] = dmg_all_a[champ] + gold_a
        gold_p[champ] = str(round(gold_all[champ] / gold_all_a[champ], 2) * 100).split('.')[0] + "%"

        wins_all[champ] = wins + wins_all[champ]
        loses_all[champ] = loses + loses_all[champ]

        if deaths_all[champ] == 0:
            kda[champ] = kill_all[champ] + assists_all[champ]
        else:
            kda[champ] = str(round(
                (kill_all[champ] + assists_all[champ]) / deaths_all[champ], 2))

        minion_per[champ] = str(round(minion_all[champ] / champs_all[champ], 0))[:-2]

        winratio[champ] = str(round(wins_all[champ] / champs_all[champ], 2) * 100)[:-2] + "%"

        match_index += 1

    return champs_all, winratio, kda, minion_per, dmgd_p, gold_p


def player_stats(player, days_ago):

    today = datetime.now()
    n_days = timedelta(days=int(days_ago))
    n_ago = today - n_days
    unix_timestamp_nd = datetime.timestamp(n_ago)
    n_ago_unix = str(round(unix_timestamp_nd))

    lol_nickname = player_nickname_to_lol_nickname(player)
    puuid = lol_nick_to_puuid(lol_nickname)
    matches = matches_ago(puuid, n_ago_unix)

    return matches_stats(matches, puuid)

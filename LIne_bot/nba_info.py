from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import configparser
import random
import requests
from nba_api.stats.endpoints import scoreboardv2
from nba_api.stats.static import teams
import datetime
from datetime import datetime as dt



def get_team_id_name_map():
    teams_list = teams.get_teams()
    return {team['id']: team['full_name'] for team in teams_list}

team_dic = {"ATL":'Atlanta Hawks',        "BOS":'Boston Celtics',         "CLE":'Cleveland Cavaliers',
            "NOP":'New Orleans Pelicans', "CHI":'Chicago Bulls',          "DAL":'Dallas Mavericks',
            "DEN":'Denver Nuggets',       "GSW":'Golden State Warriors',  "HOU":'Houston Rockets',
            "LAC":'Los Angeles Clippers', "LAL":'Los Angeles Lakers',     "MIA":'Miami Heat',
            "MIL":'Milwaukee Bucks',      "MIN":'Minnesota Timberwolves', "BKN":'Brooklyn Nets',
            "NYK":'New York Knicks',      "ORL":'Orlando Magic',          "IND":'Indiana Pacers',
            "PHI":'Philadelphia 76ers',   "PHX":'Phoenix Suns',           "POR":'Portland Trail Blazers',
            "SAC":'Sacramento Kings',     "SAS":'San Antonio Spurs',      "OKC":'Oklahoma City Thunder',
            "TOR":'Toronto Raptors',      "UTA":'Utah Jazz',              "MEM":'Memphis Grizzlies',
            "WAS":'Washington Wizards',   "DET":'Detroit Pistons',        "CHA":'Charlotte Hornets',
            "CHH":'Charlotte Hornets',    "SEA":"Seattle Supersonics",    "NJN":'New Jersey Nets',
            "VAN":"Vancouver Grizzlies", "WST":"WST","EST":"EST",
            "Unknown Team":"Unknown Team"}

team_dic_num = {
    1610612737: 'Atlanta Hawks', 
    1610612738: 'Boston Celtics', 
    1610612739: 'Cleveland Cavaliers',
    1610612740: 'New Orleans Pelicans', 
    1610612741: 'Chicago Bulls', 
    1610612742: 'Dallas Mavericks',
    1610612743: 'Denver Nuggets', 
    1610612744: 'Golden State Warriors', 
    1610612745: 'Houston Rockets',
    1610612746: 'Los Angeles Clippers', 
    1610612747: 'Los Angeles Lakers', 
    1610612748: 'Miami Heat',
    1610612749: 'Milwaukee Bucks', 
    1610612750: 'Minnesota Timberwolves', 
    1610612751: 'Brooklyn Nets',
    1610612752: 'New York Knicks',  
    1610612753: 'Orlando Magic', 
    1610612754: 'Indiana Pacers',
    1610612755: 'Philadelphia 76ers', 
    1610612756: 'Phoenix Suns', 
    1610612757: 'Portland Trail Blazers',
    1610612758: 'Sacramento Kings', 
    1610612759: 'San Antonio Spurs', 
    1610612760: 'Oklahoma City Thunder',
    1610612761: 'Toronto Raptors', 
    1610612762: 'Utah Jazz', 
    1610612763: 'Memphis Grizzlies',
    1610612764: 'Washington Wizards', 
    1610612765: 'Detroit Pistons', 
    1610612766: 'Charlotte Hornets'}

team_dic_tran = {
    'Atlanta Hawks': '老鷹',
    'Boston Celtics': '賽爾提克',
    'Cleveland Cavaliers': '騎士',
    'New Orleans Pelicans': '鵜鶘',
    'Chicago Bulls': '公牛',
    'Dallas Mavericks': '獨行俠',
    'Denver Nuggets': '金塊',
    'Golden State Warriors': '勇士😀',
    'Houston Rockets': '火箭',
    'Los Angeles Clippers': '快艇',
    'Los Angeles Lakers': '湖人',
    'Miami Heat': '熱火',
    'Milwaukee Bucks': '公鹿',
    'Minnesota Timberwolves': '灰狼',
    'Brooklyn Nets': '籃網',
    'New York Knicks' : '尼克',
    'Orlando Magic': '魔術',
    'Indiana Pacers': '溜馬',
    'Philadelphia 76ers': '76人',
    'Phoenix Suns': '太陽',
    'Portland Trail Blazers': '拓荒者',
    'Sacramento Kings': '國王',
    'San Antonio Spurs': '馬刺',
    'Oklahoma City Thunder': '雷霆',
    'Toronto Raptors': '暴龍',
    'Utah Jazz': '爵士',
    'Memphis Grizzlies': '灰熊',
    'Washington Wizards': '巫師',
    'Detroit Pistons': '活塞',
    'Charlotte Hornets': '黃蜂',
    'WST':"西區",
    'EST':"東區",
    "Unknown Team":"未知"
}



def get_games_info(day_of_game):
    try:
        date_obj = dt.strptime(day_of_game, '%Y-%m-%d')
        day_before = date_obj - datetime.timedelta(days=1)
        date_str = day_before.strftime('%Y-%m-%d')
    except:
        return


    team_id_name_map = get_team_id_name_map()
    
    try:
        scoreboard = scoreboardv2.ScoreboardV2(game_date=date_str)
        games = scoreboard.get_normalized_dict()['GameHeader']
    except Exception as e:
        print(f"Error fetching games for {date_str}: {e}")
        games = []

    # If games are found, return them with team names
    if games:
        games_with_names = []
        for game in games:
            home_team_name = team_id_name_map.get(game['HOME_TEAM_ID'], "Unknown Team")
            visitor_team_name = team_id_name_map.get(game['VISITOR_TEAM_ID'], "Unknown Team")
            matchup = f"{visitor_team_name} at {home_team_name}"
            games_with_names.append(matchup)
        games_on_date = games_with_names
    else:
        games_on_date = None


    games_info = "------------------\n"
    if games_on_date==None:
        total_games=0
    else:
        total_games = len(games_on_date)
    if games_on_date:
        for index, game in enumerate(games_on_date):
            str = (f"{team_dic_tran[game.split(' at ')[0]]}  v.s.  {team_dic_tran[game.split(' at ')[1]]}")
            # print(f"{game.split(' at ')}\n")
            games_info += str
            if index != total_games - 1:
                games_info += "\n"
    else:
        games_info += "今天沒有比賽QQ"

    return games_info


def complete_games(day_of_game):
    try:
        date_obj = dt.strptime(day_of_game, '%Y-%m-%d')
        day_before = date_obj - datetime.timedelta(days=1)
        date_str = day_before.strftime('%Y-%m-%d')
    except:
        return
    

    try:
        scoreboard = scoreboardv2.ScoreboardV2(game_date=date_str)
    except Exception as e:
        print(f"Error fetching scoreboard for {date_str}: {e}")
        final_scores = []

    # Extract game information and line scores from the response
    games_info = scoreboard.get_normalized_dict()['GameHeader']
    line_scores = scoreboard.get_normalized_dict()['LineScore']

    final_scores = []

    # Loop through games and compile final scores
    for game in games_info:
        if game['GAME_STATUS_TEXT'] == 'Final':
            game_id = game['GAME_ID']
            # Filter line scores for this specific game
            game_scores = [score for score in line_scores if score['GAME_ID'] == game_id]
            # Compile scores by team
            for team_score in game_scores:
                team_name = f"{team_score['TEAM_ABBREVIATION']}"
                pts = team_score['PTS']
                final_scores.append((team_name, pts))
    a = []
    b = {}
    games_info = "----------------------------\n"
    # Retrieve and display final scores
    scores = final_scores
    if scores:
        print(f"Final scores for {day_of_game}:\n")
        for idx, score in enumerate(scores, start=1):
            games_info +=(f"{team_dic_tran[team_dic[score[0]]]}: {score[1]} 分")
            a.append(int(score[1]))
            a = sorted(a,reverse=True)
            b[int(score[1])] = team_dic[score[0]]
            if idx%2==0:
                games_info +=(f"\n--> {team_dic_tran[b[a[0]]]} 贏了!!")
                if idx!=len(scores):
                    games_info += "\n\n"
                a.clear()
                b.clear()
            elif idx!=len(scores):
                games_info+=" v.s. "
    else:
        games_info += (f"比賽還沒開打:)")
    return games_info

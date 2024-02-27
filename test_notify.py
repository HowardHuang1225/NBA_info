import requests
from nba_api.stats.endpoints import scoreboardv2
from nba_api.stats.static import teams
import datetime
from datetime import datetime as dt


# Function to create a mapping of team IDs to team names
def get_team_id_name_map():
    teams_list = teams.get_teams()
    return {team['id']: team['full_name'] for team in teams_list}

team_dic = {
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
    'Golden State Warriors': '勇士',
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
    'Charlotte Hornets': '黃蜂'
}


# 假設這是你的賽程查詢功能
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
        games_info = "今天沒有比賽QQ"

    return games_info

# LINE Notify 發送功能
def send_line_notify(message):
    url = 'https://notify-api.line.me/api/notify'
    token = '36PyKmdWTeMbQd3988cFRKbTp2zfkJLxBLCAuwmznnA'  # 注意替換成你的 LINE Notify Token
    headers = {
        'Authorization': 'Bearer ' + token
    }
    data = {
        'message': message
    }
    data = requests.post(url, headers=headers, data=data)   # 使用 POST 方法


# 主程式
if __name__ == "__main__":
    day_of_game = dt.now().strftime("%Y-%m-%d")  # 使用今天的日期或者其他指定日期
    games_info = get_games_info(day_of_game)  # 獲取賽程資訊
    message = f"今日賽程！\n{games_info}"  # 訊息內容包含賽程資訊
    
    # 發送 LINE Notify 訊息
    try:
        status_code = send_line_notify(message)
        print("訊息發送成功 !!!")
    except:
        print("訊息發送失敗 QQ")

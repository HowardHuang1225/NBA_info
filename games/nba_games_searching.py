import datetime
from datetime import datetime as dt
from nba_api.stats.endpoints import scoreboardv2
from nba_api.stats.static import teams
import numpy


team_dic1 = {"ATL":'Atlanta Hawks',        "BOS":'Boston Celtics',         "CLE":'Cleveland Cavaliers',
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
            "VAN":"Vancouver Grizzlies"}



#############################################################################
def complete_games(day_of_game):
    try:
        date_obj = dt.strptime(day_of_game, '%Y-%m-%d')
        day_before = date_obj - datetime.timedelta(days=1)
        date_str = day_before.strftime('%Y-%m-%d')
    except:
        print("wrong format....")
        print('--------------------------------------------------------')
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
    # Retrieve and display final scores
    scores = final_scores
    if scores:
        print(f"Final scores for {day_of_game}:\n")
        for idx, score in enumerate(scores, start=1):
            print(f"{team_dic1[score[0]]:23}: {score[1]} points")
            a.append(int(score[1]))
            a = sorted(a,reverse=True)
            b[int(score[1])] = team_dic1[score[0]]
            if idx%2==0:
                print(f"--> {b[a[0]]} wins!!")
                print()
                a.clear()
                b.clear()
    else:
        print(f"No completed games or scores available for {day_of_game}.")


    print('--------------------------------------------------------')


def get_team_id_name_map():
    teams_list = teams.get_teams()
    return {team['id']: team['full_name'] for team in teams_list}

team_dic = {1610612737: 'Atlanta Hawks', 1610612738: 'Boston Celtics', 1610612739: 'Cleveland Cavaliers',
            1610612740: 'New Orleans Pelicans', 1610612741: 'Chicago Bulls', 1610612742: 'Dallas Mavericks',
            1610612743: 'Denver Nuggets', 1610612744: 'Golden State Warriors', 1610612745: 'Houston Rockets',
            1610612746: 'Los Angeles Clippers', 1610612747: 'Los Angeles Lakers', 1610612748: 'Miami Heat',
            1610612749: 'Milwaukee Bucks', 1610612750: 'Minnesota Timberwolves', 1610612751: 'Brooklyn Nets',
            1610612752: 'New York Knicks',  1610612753: 'Orlando Magic', 1610612754: 'Indiana Pacers',
            1610612755: 'Philadelphia 76ers', 1610612756: 'Phoenix Suns', 1610612757: 'Portland Trail Blazers',
            1610612758: 'Sacramento Kings', 1610612759: 'San Antonio Spurs', 1610612760: 'Oklahoma City Thunder',
            1610612761: 'Toronto Raptors', 1610612762: 'Utah Jazz', 1610612763: 'Memphis Grizzlies',
            1610612764: 'Washington Wizards', 1610612765: 'Detroit Pistons', 1610612766: 'Charlotte Hornets'}


def games(day_of_game):
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



    if games_on_date:
        print(f"Games on {day_of_game}:\n")
        n = 1
        for game in games_on_date:
            print(f"{game.split(' at')[0]:23}  vs.  {game.split(' at')[1]:23}")
            n += 1
        print(f"\nThere are {n-1} games on {day_of_game}.")
        
    else:
        print(f"No games found on {day_of_game}.")


    print('--------------------------------------------------------')

#LINE notify權證: 36PyKmdWTeMbQd3988cFRKbTp2zfkJLxBLCAuwmznnA

def game_news():
    print("Welcome to the NBA game_news!?\n")
    while 1:
        try:
            date = input("Enter the date you want to search (YYYY-MM-DD):\n")
            print('--------------------------------------------------------')
        except:
            print("quit....")
            exit()
        games(date)
        complete_games(date)



if __name__ == "__main__":
    game_news()
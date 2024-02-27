from nba_api.stats.endpoints import scoreboardv2
from nba_api.stats.static import teams
import datetime
from datetime import datetime as dt
# import queue

# Function to create a mapping of team IDs to team names
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
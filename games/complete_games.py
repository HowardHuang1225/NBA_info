from nba_api.stats.endpoints import scoreboardv2
import datetime
from datetime import datetime as dt

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
            print(f"{team_dic[score[0]]:23}: {score[1]} points")
            a.append(int(score[1]))
            a = sorted(a,reverse=True)
            b[int(score[1])] = team_dic[score[0]]
            if idx%2==0:
                print(f"--> {b[a[0]]} wins!!")
                print()
                a.clear()
                b.clear()
    else:
        print(f"No completed games or scores available for {day_of_game}.")


    print('--------------------------------------------------------')

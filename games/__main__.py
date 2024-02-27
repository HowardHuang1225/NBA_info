from nba_api.stats.endpoints import scoreboardv2
import datetime
from datetime import datetime as dt
from nba_api.stats.endpoints import scoreboardv2
from nba_api.stats.static import teams
from complete_games import complete_games
from games import games



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
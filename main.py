from nba_api.stats.endpoints import playercareerstats
import csv
# Nikola Jokić
career = playercareerstats.PlayerCareerStats(player_id='203999') 

# pandas data frames (optional: pip install pandas)
career.get_data_frames()[0]

# json
data = career.get_json()

# dictionary
career.get_dict()



result_set = data['resultSets'][0]  # Focus on the first result set for this example

# Specify the filename to write to
filename = 'nba_season_totals_regular_season.csv'

# Open the file for writing
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    # Create a CSV writer object
    csvwriter = csv.writer(csvfile)
    
    # Write the header row
    csvwriter.writerow(result_set['headers'])
    
    # Write the data rows
    for row in result_set['rowSet']:
        csvwriter.writerow(row)

print(f"Data has been successfully written to '{filename}'")

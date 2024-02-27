from nba_api.stats.static import players
import csv

nba_players = players.get_players()

# Adjusted CSV file headers (field names)
fieldnames = ['id', 'full_name', 'is_active']

# Writing data to a CSV file
with open('nba_players.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write the header
    writer.writeheader()
    
    # Write the data rows, excluding first_name and last_name
    for player in nba_players:
        # Create a new dictionary with only the desired fields
        row = {fieldname: player[fieldname] for fieldname in fieldnames}
        writer.writerow(row)

print("Data has been successfully written to 'nba_players.csv'")

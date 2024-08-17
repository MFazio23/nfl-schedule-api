from mappings import team_map

from datetime import datetime

file_name = "nfl-schedule-2024-raw.txt"
csv_file_name = "nfl-schedule-2024.csv"
season = 2024

reversed_team_map = dict(map(reversed, team_map.items()))

with open(file_name) as schedule_file:
    file_lines = schedule_file.readlines()

    current_week = 0
    game_of_week = 0
    games = []

    for line in file_lines:
        stripped_line = line.strip()

        if stripped_line.startswith("Week"):
            current_week = stripped_line.replace("Week ", "")
            game_of_week = 0
        elif stripped_line.startswith("Date"):
            continue
        else:
            print(stripped_line)
            date, time, away, home = stripped_line.split("\t")

            original_datetime = datetime.strptime(f'{date} {time}', "%a %b %d %I:%M %p")

            year = season if int(original_datetime.strftime("%m")) >= 7 else season + 1

            game_datetime = original_datetime.replace(year=year)

            home_id = reversed_team_map[home]
            away_id = reversed_team_map[away]

            game_of_week_string = f"0{game_of_week}" if game_of_week < 10 else str(game_of_week)

            games.append({
                "game_id": f"{season}_{current_week}_{away_id}_{home_id}",
                "season": season,
                "game_type": "REG",
                "week": current_week,
                "gameday": game_datetime.strftime("%m/%d/%y"),
                "weekday": game_datetime.strftime("%A"),
                "gametime": game_datetime.strftime("%H:%M"),
                "away_team": away_id,
                "home_team": home_id,
                "old_game_id": game_datetime.strftime("%Y%m%d") + game_of_week_string
            })

            game_of_week = game_of_week + 1

    with open(csv_file_name, "w") as output_csv:
        for header in games[0].keys():
            output_csv.write(f"{header},")
        output_csv.write("\n")
        for game in games:
            for value in game.values():
                output_csv.write(f"{value},")
            output_csv.write("\n")

        output_csv.close()

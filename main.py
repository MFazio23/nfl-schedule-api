from datetime import date
from mappings import team_map

from flask import jsonify
import csv

min_year = 1999
max_year = 2024


def get_schedule_http(request):
    year = int(get_input_params(request, 'year', date.today().year))
    full = bool(get_input_params(request, 'fullData', False))

    print(f'Full? = {full}')

    if min_year <= year <= max_year:
        schedule = get_schedule_for_year(year)
        if full:
            return jsonify(schedule)
        return jsonify(get_basic_schedule(schedule))

    return f'Invalid year entered: {year}'


def get_input_params(request, field, default=None):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and field in request_json:
        return request_json[field]
    elif request_args and field in request_args:
        return request_args[field]

    return default


def get_schedule_for_year(year: int):
    current_year_games = []

    if year == 2023 or year == 2024:
        file = f'nfl-schedule-{year}.csv'
        with open(file, mode='r') as csvfile:
            schedule_csv = csv.DictReader(csvfile)
            line_num = 0
            for game in schedule_csv:
                if int(game['season']) == year:
                    current_year_games.append(game)

                line_num += 1
    else:
        with open('nfl-1999-2022-schedule.csv', mode='r') as csvfile:
            schedule_csv = csv.DictReader(csvfile)
            line_num = 0
            for game in schedule_csv:
                if line_num > 0 and int(game['season']) == year:
                    current_year_games.append(game)

                line_num += 1

    return current_year_games


def get_basic_schedule(schedule: list):
    grouped_games = {}

    for game in schedule:
        week = game['week']
        if week not in grouped_games:
            grouped_games[week] = []
        game_id = game.get('espn', game.get('game_id'))
        if game_id:
            grouped_games[week].append(
                {
                    'gameId': game_id,
                    'homeTeam': team_map[game['home_team']],
                    'awayTeam': team_map[game['away_team']],
                }
            )

    return grouped_games

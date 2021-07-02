import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from .database import DB

# check this, in case you are not
# familiar with google spreadsheets
# https://github.com/burnash/gspread


def spreadsheet(tab: int) -> object:
    """ return one of two spreadsheets """
    if tab == 0:
        table = os.getenv("GAMES")
    elif tab == 1:
        table = os.getenv("PAYMENTS")
    else:
        return "fuck you"

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    path = "Vargan-API.json"
    full_path = os.path.abspath(os.path.expanduser(os.path.expandvars(path)))
    creds = ServiceAccountCredentials.from_json_keyfile_name(full_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(table)
    sheet = sheet.get_worksheet(0)
    return sheet


# update Games database from Content spreadsheet
def update_games():
    """ drops bd and write data from spreadsheet """
    sheet = spreadsheet(0)
    games = sheet.get_all_values()
    games_num = len(games)
    try:
        DB.delete_games()
        games_to_insert = [[game[-1].strip()] + game[:5] for game in games]
        DB.set_games(games_to_insert)
    except Exception as error:
        return "Failed with " + str(error)
    return f"Games database was succesfully updated with {games_num} games"


if __name__ == "__main__":
    print(update_games())

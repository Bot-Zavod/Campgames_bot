import gspread
from oauth2client.service_account import ServiceAccountCredentials

from bot.config import settings
from bot.database import db_interface

# check this, in case you are not
# familiar with google spreadsheets
# https://github.com/burnash/gspread


def spreadsheet() -> object:
    """return one of two spreadsheets"""

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds_path = settings.APP_DIR / "google_api.json"
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    table = settings.GAMES_TABLE_KEY
    # If you want to be specific, use a key (which can be extracted from
    # the spreadsheet's url)
    sheet = client.open_by_key(table)
    # Select worksheet by index. Worksheet indexes start from zero
    worksheet = sheet.get_worksheet(0)
    return worksheet


def update_spreadsheet_from_db():
    worksheet = spreadsheet()
    games = db_interface.get_all_games()
    worksheet.update(f"A2:I{len(games)+1}", games)  # except headings


def update_games_in_db():
    """drops bd and write data from spreadsheet"""
    worksheet = spreadsheet()
    games = worksheet.get_all_values()
    games = games[1:]  # remove header
    # update_spreadsheet_from_db()
    num_rows_deleted = db_interface.delete_games()
    db_interface.set_games(games)
    return num_rows_deleted, len(games)

import gspread
from google.oauth2.service_account import credentials

SCOPE = ["https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"]

ENTRIES = credentials.from_service_account_file('entries.json')  
SCOPED_ENTRIES = ENTRIES.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.autorize(SCOPED_ENTRIES)
SHEET = GSPREAD_CLIENT.open('event_reminder') 

user_imputs = SHEET.worksheet('user_inputs')

data = 
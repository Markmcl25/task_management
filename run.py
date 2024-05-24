import 
import gspread
from google.oauth2.service_account import credentials

SCOPE = ["https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"]

ENTRIES = credentials.from_service_account_file('entries.json')  
SCOPED_ENTRIES = ENTRIES.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.autorize(SCOPED_ENTRIES)
SHEET = GSPREAD_CLIENT.open('event_reminder') 

class Event:
    def __init__(self, first_name, second_name, event_type, email):
        self.first_name = first_name
        self.second_name = second_name
        self.event_type = event_type
        self.email = email

    def to_list(self):
        return [self.first_name, self.second_name, self.event_type, self.email]    

    def from_list(data):
        return Event(
            first_name=data[0],
            second_name=data[1],
            event_type=data[2],
            email=data[3]
        )
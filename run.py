import cgi
import cgitb
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
        # Initialize an Event object with the provided details
        self.first_name = first_name
        self.second_name = second_name
        self.event_type = event_type
        self.email = email

    def to_list(self):
        # Convert the Event object to a list of its attributes
        return [self.first_name, self.second_name, self.event_type, self.email]    

    def from_list(data):
        # Create an Event object
        return Event(
            first_name=data[0],
            second_name=data[1],
            event_type=data[2],
            email=data[3]
        )
        # Load events from the Google Sheet
    def load_events():
        events = []  
        records = USER_INPUTS.get_all_values
        # Skip the header row and convert each row to an Event object
    for row in records[1:]:
        events.append(Event.from_list(row))
    return events

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/events':
        # Load events and convert them to dictionaries
            events = load_events()
            events_dict = [event.__dict__ for event in events]
        # Send JSON response with event data
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(events_dict).encode())

        else:
            # Serve static files for other paths
            super().do_GET()

      # Create an HTTP server with the custom handler
        Handler = MyHandler
        Handler.cgi_directories = ['/cgi-bin']      
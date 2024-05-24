import cgi
import cgitb
import gspread
from google.oauth2.service_account import Credentials
import http.server
import socketserver
import json

SCOPE = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

ENTRIES = Credentials.from_service_account_file('entries.json')  
SCOPED_ENTRIES = ENTRIES.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_ENTRIES)
SHEET = GSPREAD_CLIENT.open('event_reminder') 
USER_INPUTS = SHEET.worksheet('user_inputs')  # Define the worksheet

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

    @staticmethod
    def from_list(data):
        # Create an Event object from a list
        return Event(
            first_name=data[0],
            second_name=data[1],
            event_type=data[2],
            email=data[3]
        )

    @staticmethod
    def load_events():
        # Load events from the Google Sheet
        events = []  
        records = USER_INPUTS.get_all_values()
        # Skip the header row and convert each row to an Event object
        for row in records[1:]:
            events.append(Event.from_list(row))
        return events

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/events':
            # Load events and convert them to dictionaries
            events = Event.load_events()
            events_dict = [event.__dict__ for event in events]
            # Send JSON response with event data
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(events_dict).encode())
        else:
            # Serve static files for other paths
            super().do_GET()

# Define the port
PORT = 8000
# Create an HTTP server with the custom handler
Handler = MyHandler
Handler.cgi_directories = ['/cgi-bin']

# Create and start the server
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()

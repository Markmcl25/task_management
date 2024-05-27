import gspread
from google.oauth2.service_account import Credentials
import http.server
import socketserver
import json

# Define the scope and authorize the client
SCOPE = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

# Load the credentials from the JSON file
CREDENTIALS = Credentials.from_service_account_file('creds.json') 
SCOPED_CREDENTIALS = CREDENTIALS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDENTIALS)

# Open the Google Sheet by name and get the specific worksheet
SHEET = GSPREAD_CLIENT.open('event_reminder')
EVENT_REMINDER = SHEET.worksheet('event_reminder')

class Event:
    def __init__(self, first_name, second_name, event_type, email):
        self.first_name = first_name
        self.second_name = second_name
        self.event_type = event_type
        self.email = email

    def to_list(self):
        return [self.first_name, self.second_name, self.event_type, self.email]    

    @staticmethod
    def from_list(data):
        return Event(
            first_name=data[0],
            second_name=data[1],
            event_type=data[2],
            email=data[3]
        )

    @staticmethod
    def load_events():
        events = []  
        records = EVENT_REMINDER.get_all_values()
        for row in records[1:]:
            events.append(Event.from_list(row))
        return events

    @staticmethod
    def append_event(event_details):
        EVENT_REMINDER.append_row(event_details)

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/events':
            events = Event.load_events()
            events_dict = [event.__dict__ for event in events]
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(events_dict).encode())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/events':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            event_data = json.loads(post_data)
            event = Event(
                first_name=event_data['first_name'],
                second_name=event_data['second_name'],
                event_type=event_data['event_type'],
                email=event_data['email']
            )
            Event.append_event(event.to_list())
            self.send_response(201)
            self.end_headers()
            self.wfile.write(b'Event added successfully')
        else:
            self.send_response(404)
            self.end_headers()

# Define the port
PORT = 8000

# Create an HTTP server with the custom handler
Handler = MyHandler
Handler.cgi_directories = ['/cgi-bin']

# Create and start the server
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)

# Main function
def main():
    httpd.serve_forever()

if __name__ == "__main__":
    main()

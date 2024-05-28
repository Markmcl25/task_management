import http.server
import socketserver
import gspread
from google.oauth2 import service_account
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = service_account.Credentials.from_service_account_file("creds.json", scopes=scope)
client = gspread.authorize(creds)

# Open the spreadsheet
spreadsheet_name = "event_reminder"
worksheet_name = "event_reminder"

try:
    spreadsheet = client.open(spreadsheet_name)
    worksheet = spreadsheet.worksheet(worksheet_name)
    logging.info(f"Successfully opened spreadsheet '{spreadsheet_name}' and worksheet '{worksheet_name}'")
except gspread.exceptions.SpreadsheetNotFound:
    logging.error(f"Spreadsheet '{spreadsheet_name}' not found")
    raise
except gspread.exceptions.WorksheetNotFound:
    logging.error(f"Worksheet '{worksheet_name}' not found")
    raise

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/submit':
            try:
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('name')[0].decode('utf-8')
                    amount = fields.get('amount')[0].decode('utf-8')
                    date = fields.get('date')[0].decode('utf-8')
                    type_ = fields.get('type')[0].decode('utf-8')
                    on_bill = fields.get('on_bill')[0].decode('utf-8')
                    
                    # Append data to Google Sheet
                    worksheet.append_row([name, amount, date, type_, on_bill])
                    
                    logging.info(f"Added row to spreadsheet: {[name, amount, date, type_, on_bill]}")
                    
                    self.send_response(303)
                    self.send_header('Location', '/')
                    self.end_headers()
                else:
                    logging.error("Invalid content type")
                    self.send_response(400)
                    self.end_headers()
            except Exception as e:
                logging.error(f"Failed to add event: {e}")
                self.send_response(500)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write("Internal Server Error".encode())

httpd = socketserver.TCPServer(("", PORT), Handler)

print("Serving at port", PORT)
httpd.serve_forever()

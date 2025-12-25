import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def test_sheet():
    try:
        # 1. Load the Secret from the environment
        creds_json = os.environ.get("GOOGLE_CREDENTIALS")
        if not creds_json:
            print("ERROR: GOOGLE_CREDENTIALS secret not found!")
            return

        # 2. Setup permissions
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = json.loads(creds_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        
        # 3. Try to open the sheet
        client = gspread.authorize(creds)
        # HUSTLER: Make sure the name below matches your Google Sheet exactly!
        sheet = client.open("Humanoid-Robotics-Data-2025").sheet1
        
        # 4. Write a test row
        sheet.append_row(["Connection Test", "Success", "2025-12-25"])
        print("SUCCESS: Check your Google Sheet now!")
        
    except Exception as e:
        print(f"FAILED: {e}")

if __name__ == "__main__":
    test_sheet()

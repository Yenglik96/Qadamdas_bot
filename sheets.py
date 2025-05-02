# sheets.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "/etc/secrets/credentials.json"  # Render ішіндегі қауіпсіз жол
SHEET_NAME = "Qadamdas Bot"  # Sheets құжатының атауы

creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1

user_names = {}

def register_user(user_id, full_name, username):
    user_names[user_id] = {
        "name": full_name,
        "username": username or ""
    }

def get_user_fullname(user_id):
    return user_names.get(user_id, {}).get("name")

def add_entry_to_sheet(full_name, telegram_username, date, distance):
    try:
        row = [full_name, f"@{telegram_username}" if telegram_username else "", date, distance]
        sheet.append_row(row)
    except Exception as e:
        print(f"Sheets error: {e}")


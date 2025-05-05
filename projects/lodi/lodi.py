import os
import json
import ast
import re
import requests
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Default checklist tasks
DEFAULT_TASKS = {
    "updated_address": False,
    "find_long_distance_movers": False,
    "booked_movers": False,
    "set_up_utilities": False,
    "transferred_internet_service": False,
    "change_driver_license": False,
    "found_local_services": False
}

# Progress tracking
PROGRESS_FILE = "lodi_progress.json"
SERPER_LOG_FILE = "serper_log.json"

# Load task progress
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_TASKS.copy()

# Save task progress
def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)

# Log Serper search count
def log_serper_search():
    log = {"month": datetime.now().strftime("%Y-%m"), "count": 0}

    if os.path.exists(SERPER_LOG_FILE):
        try:
            with open(SERPER_LOG_FILE, "r") as f:
                existing = json.load(f)
            if existing.get("month") == log["month"]:
                log["count"] = existing.get("count", 0) + 1
            else:
                log["count"] = 1
        except Exception:
            log["count"] = 1

    with open(SERPER_LOG_FILE, "w") as f:
        json.dump(log, f, indent=2)

    print(f"\U0001F50D [Serper] Searches this month: {log['count']} / 100 (free tier)")

# Scrape contact info from a website
def extract_contact_info(url):
    try:
        resp = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text()

        phone_match = re.search(r'(\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4})', text)
        phone = phone_match.group(1).strip() if phone_match else "n/a"

        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        email = email_match.group(0).strip() if email_match else "n/a"

        return phone, email
    except Exception as e:
        print(f"  \u26a0\ufe0f Could not scrape {url}: {e}")
        return "n/a", "n/a"

# Search movers with Serper
def search_movers_web():
    from urllib.parse import urlencode

    log_serper_search()  # Still tracks usage

    api_key = os.getenv("SERPAPI_KEY")
    query = "full-service long-distance movers from New York City to Atlanta"

    params = {
        "q": query,
        "engine": "google",
        "api_key": api_key
    }

    try:
        res = requests.get("https://serpapi.com/search", params=params)
        res.raise_for_status()
        data = res.json()

        results = data.get("organic_results", [])[:5]
        movers = []

        for result in results:
            name = result.get("title", "").strip() or "n/a"
            website = result.get("link", "").strip() or "n/a"
            description = result.get("snippet", "").strip() or "n/a"
            phone, email = extract_contact_info(website)

            movers.append({
                "name": name,
                "phone": phone,
                "email": email,
                "website": website,
                "description": description
            })

        return movers

    except Exception as e:
        print(f"Error fetching movers from SerpAPI: {e}")
        return []


# GPT-powered fallback for other tasks
def get_gpt_help(task):
    prompt = f"I'm moving from New York City to Atlanta. Can you help me with: {task.replace('_', ' ')}? Give clear steps."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are Lodi, a helpful assistant for someone planning a move."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Google Sheets writer
def write_movers_to_sheet(movers):
    SHEET_NAME = "Lodi Movers"
    CREDS_FILE = "creds/lodi-key.json"
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME).sheet1

    headers = ["Name", "Phone", "Email", "Website", "Description"]
    sheet.update(range_name="A1", values=[headers])

    rows = [[
        m.get("name", "n/a"),
        m.get("phone", "n/a"),
        m.get("email", "n/a"),
        m.get("website", "n/a"),
        m.get("description", "n/a")
    ] for m in movers]

    sheet.update(range_name=f"A2:E{len(rows)+1}", values=rows)
    sheet.resize(rows=len(rows)+1, cols=5)

# Main CLI flow
def run():
    print("\nLodi – Your Personal Moving Assistant\n")
    progress = load_progress()

    for task, done in progress.items():
        if not done:
            print(f"Task: {task.replace('_', ' ').title()}")
            answer = input("Have you completed this? (yes/no/help): ").strip().lower()

            if answer == "yes":
                progress[task] = True
                print("Marked as done.\n")

            elif answer == "help":
                print("\nLodi says:\n")

                if task == "find_long_distance_movers":
                    movers = search_movers_web()
                    if movers:
                        print(json.dumps(movers, indent=2) + "\n")
                        do_sheet = input("Would you like to save the suggested movers to Google Sheets? (yes/no): ").strip().lower()
                        if do_sheet == "yes":
                            try:
                                write_movers_to_sheet(movers)
                                print("Movers written to sheet.\n")
                            except Exception as e:
                                print(f"Error writing to sheet: {e}\n")
                    else:
                        print("Could not retrieve moving companies.\n")
                else:
                    advice = get_gpt_help(task)
                    print(advice + "\n")

            else:
                print("Task left pending.\n")

    save_progress(progress)
    print("Progress saved to lodi_progress.json\n")

if __name__ == "__main__":
    run()

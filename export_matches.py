import os
import re
import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

TEAM_SELECTOR = '.match-table-item__title'
DATE_SELECTOR = '.match-table-item__date'
STORAGE_DIR = 'storage'
FILE_NAME = 'Matches.xlsx'

def scroll_to_bottom(page):
    previous_height = page.evaluate("document.body.scrollHeight")
    while True:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == previous_height:
            break
        previous_height = new_height

def fetch_page_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        with browser.new_page() as page:
            page.goto(url)
            scroll_to_bottom(page)
            content = page.content()
    return content

def extract_division_from_url(url):
    match = re.search(r'division-[\w-]+', url)
    return match.group(0) if match else "Unbekannte Division"

def parse_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    team_divs = soup.select(TEAM_SELECTOR)
    date_divs = soup.select(DATE_SELECTOR)
    return team_divs, date_divs

def extract_match_data(team_divs, date_divs):
    teams = [div.text.strip() for div in team_divs]
    dates = [div.text.strip().split() for div in date_divs]
    data = []
    for i in range(0, len(teams), 2):
        match_date = dates[i // 2]
        date = match_date[0]
        time = match_date[1]
        team1 = teams[i]
        team2 = teams[i + 1]
        data.append([date, time, team1, team2])
    return data

def save_to_excel(data, file_path):
    df = pd.DataFrame(data, columns=['Datum', 'Uhrzeit', 'Team 1', 'Team 2'])
    df.to_excel(file_path, index=False)
    
def main(url):    
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)

    division = extract_division_from_url(url)
    html_content = fetch_page_content(url)
    team_divs, date_divs = parse_html_content(html_content)
    data = extract_match_data(team_divs, date_divs)
    file_path = os.path.join(STORAGE_DIR, FILE_NAME)
    save_to_excel(data, file_path)

    message = f"Matches für {division} sind zum Download bereit:"
    return message, file_path
import os
import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

team_selector = '.match-table-item__title'
date_selector = '.match-table-item__date'

def scroll_to_bottom(page):
    previous_height = page.evaluate("document.body.scrollHeight")
    while True:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)  # neue Inhalte laden
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == previous_height:
            break
        previous_height = new_height

def fetch_page_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        with browser.new_page() as page:
            page.goto(url)
            scroll_to_bottom(page)
            content = page.content()
    return content
    
def main(url):
    storage_dir = 'storage' # Speicherort 
    
    if not os.path.exists(storage_dir):
        os.makedirs(storage_dir)
    
    # Datenverarbeitung
    html_content = fetch_page_content(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    team_divs = soup.select(team_selector)
    date_divs = soup.select(date_selector)

    # Teamnamen und Daten extrahieren
    teams = [div.text.strip() for div in team_divs]
    dates = [div.text.strip().split() for div in date_divs]

    # Daten in ein DataFrame speichern
    data = []
    for i in range(0, len(teams), 2):
        match_date = dates[i // 2]
        date = match_date[0]
        time = match_date[1]
        team1 = teams[i]
        team2 = teams[i + 1]
        data.append([date, time, team1, team2])

    df = pd.DataFrame(data, columns=['Datum', 'Uhrzeit', 'Team 1', 'Team 2'])

    # Datei in 'storage' exportieren
    file_path = os.path.join(storage_dir, 'matches.xlsx')
    df.to_excel(file_path, index=False)

    message = "Matches stehen zum Download bereit:"

    return message, file_path
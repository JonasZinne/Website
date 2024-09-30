import os
import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

TEAM_SELECTOR = '.match-table-item__title'
DATE_SELECTOR = '.match-table-item__date'

def scroll_to_bottom(page):
    previous_height = page.evaluate("document.body.scrollHeight")
    while True:
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(500)
        new_height = page.evaluate("document.body.scrollHeight")
        if new_height == previous_height:
            break
        previous_height = new_height

def parse_html_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    team_divs = soup.select(TEAM_SELECTOR)
    date_divs = soup.select(DATE_SELECTOR)

    teams = [team.text for team in team_divs]
    dates = [date.text for date in date_divs]

    structured_data = []
    for i in range(len(dates)):
        team1 = teams[2 * i]
        team2 = teams[2 * i + 1]
        structured_data.append({'Date': dates[i], 'Team 1': team1, 'Team 2': team2})

    return structured_data
    
def main(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        with browser.new_page() as page:
            page.goto(url)
            scroll_to_bottom(page)
            content = page.content()

    structured_data = parse_html_content(content)
    df = pd.DataFrame(structured_data)

    storage_dir = 'storage'
    os.makedirs(storage_dir, exist_ok=True)
    excel_file = os.path.join(storage_dir, 'Matches.xlsx')
    df.to_excel(excel_file, index=False)

    return excel_file
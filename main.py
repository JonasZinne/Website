from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

url = 'https://projectv.gg/tournaments/q-division-2-3-2024?stage=matches'
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
    
def main():
    html_content = fetch_page_content(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    team_divs = soup.select(team_selector)
    date_divs = soup.select(date_selector)

    # Teamnamen und Daten extrahieren
    teams = [div.text.strip() for div in team_divs]
    dates = [div.text.strip().split()[0] + ' ' + div.text.strip().split()[1] for div in date_divs]

    # Teams und Daten ausgeben
    for i in range(0, len(teams), 2):
        match_date = dates[i // 2]
        print(f"{match_date} - {teams[i]} vs. {teams[i + 1]}")

main()
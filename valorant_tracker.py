from playwright.sync_api import sync_playwright

def get_valorant_data(player_name, player_tag):
    selectors = {
        "rank": "#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.area-main > div.area-main-stats > div.card.bordered.header-bordered.responsive.segment-stats > div.highlighted.highlighted--giants > div.highlighted__content > div > div.trn-profile-highlighted-content__stats > div > div:nth-child(1) > span.stat__value",
        "kd": "#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.area-main > div.area-main-stats > div.card.bordered.header-bordered.responsive.segment-stats > div.giant-stats > div:nth-child(2) > div > div.numbers > span.flex.items-center.gap-2 > span",
        "kad": "#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.area-main > div.area-main-stats > div.card.bordered.header-bordered.responsive.segment-stats > div.main > div:nth-child(8) > div > div.numbers > span.flex.items-center.gap-2 > span",
        "damage_round": "#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.area-main > div.area-main-stats > div.card.bordered.header-bordered.responsive.segment-stats > div.giant-stats > div:nth-child(1) > div > div.numbers > span.flex.items-center.gap-2 > span",
        "dd_delta": "#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.area-main > div.area-main-stats > div.card.bordered.header-bordered.responsive.segment-stats > div.main > div:nth-child(3) > div > div.numbers > span.flex.items-center.gap-2 > span",
        "acs": "#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.area-main > div.area-main-stats > div.card.bordered.header-bordered.responsive.segment-stats > div.main > div:nth-child(7) > div > div.numbers > span.flex.items-center.gap-2 > span",
        "kast": "#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.area-main > div.area-main-stats > div.card.bordered.header-bordered.responsive.segment-stats > div.main > div:nth-child(2) > div > div.numbers > span.flex.items-center.gap-2 > span",
        "headshot": "#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.area-main > div.area-main-stats > div.card.bordered.header-bordered.responsive.segment-stats > div.giant-stats > div:nth-child(3) > div > div.numbers > span.flex.items-center.gap-2 > span"
    }

    url = f"https://tracker.gg/valorant/profile/riot/{player_name}%23{player_tag}/overview"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        with browser.new_page() as page:
            page.goto(url)

            def get_inner_text(selector, default_text):
                element = page.query_selector(selector)
                return element.inner_text() if element else default_text
            
            results = {
                key: get_inner_text(selector, f"{key} nicht gefunden")
                for key, selector in selectors.items()
            }
        
        return results

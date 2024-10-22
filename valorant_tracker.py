from playwright.sync_api import sync_playwright

def get_valorant_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Browser ohne GUI starten
        page = browser.new_page()
        page.goto("https://tracker.gg/valorant/profile/riot/Kampfi%23Fire/overview")

        # Damage/Round
        damage_selector = "#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.area-main > div.area-main-stats > div.card.bordered.header-bordered.responsive.segment-stats > div.giant-stats > div:nth-child(1) > div > div.numbers > span.flex.items-center.gap-2 > span"
        damage = page.query_selector(damage_selector)
        damage_text = damage.inner_text() if damage else "Damage/Round nicht gefunden"

        # K/D Ratio
        kd_selector = "#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.area-main > div.area-main-stats > div.card.bordered.header-bordered.responsive.segment-stats > div.giant-stats > div:nth-child(2) > div > div.numbers > span.flex.items-center.gap-2 > span"
        kd = page.query_selector(kd_selector)
        kd_text = kd.inner_text() if kd else "K/D nicht gefunden"

        # KAD (Kills + Assists + Deaths)
        kad_selector = "#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.area-main > div.area-main-stats > div.card.bordered.header-bordered.responsive.segment-stats > div.main > div:nth-child(8) > div > div.numbers > span.flex.items-center.gap-2 > span"
        kad = page.query_selector(kad_selector)
        kad_text = kad.inner_text() if kad else "KAD nicht gefunden"

        # Headshot %
        hs_selector = "#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.area-main > div.area-main-stats > div.card.bordered.header-bordered.responsive.segment-stats > div.giant-stats > div:nth-child(3) > div > div.numbers > span.flex.items-center.gap-2 > span"
        hs = page.query_selector(hs_selector)
        hs_text = hs.inner_text() if hs else "Headshot % nicht gefunden"

        # KAST (Kill, Assist, Survive, Trade)
        kast_selector = "#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.area-main > div.area-main-stats > div.card.bordered.header-bordered.responsive.segment-stats > div.main > div:nth-child(2) > div > div.numbers > span.flex.items-center.gap-2 > span"
        kast = page.query_selector(kast_selector)
        kast_text = kast.inner_text() if kast else "KAST nicht gefunden"

        # DD (Delta Damage)
        dd_selector = "#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.area-main > div.area-main-stats > div.card.bordered.header-bordered.responsive.segment-stats > div.main > div:nth-child(3) > div > div.numbers > span.flex.items-center.gap-2 > span"
        dd = page.query_selector(dd_selector)
        dd_text = dd.inner_text() if dd else "DD nicht gefunden"

        # ACS (Average Combat Score)
        acs_selector = "#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.area-main > div.area-main-stats > div.card.bordered.header-bordered.responsive.segment-stats > div.main > div:nth-child(7) > div > div.numbers > span.flex.items-center.gap-2 > span"
        acs = page.query_selector(acs_selector)
        acs_text = acs.inner_text() if acs else "ACS nicht gefunden"

        # Rank
        rank_selector = "#app > div.trn-wrapper > div.trn-container > div > main > div.content.no-card-margin > div.site-container.trn-grid.trn-grid--vertical.trn-grid--small > div.trn-grid.container > div.area-main > div.area-main-stats > div.card.bordered.header-bordered.responsive.segment-stats > div.highlighted.highlighted--giants > div.highlighted__content > div > div.trn-profile-highlighted-content__stats > div > div:nth-child(1) > span.stat__value"
        rank = page.query_selector(rank_selector)
        rank_text = rank.inner_text() if rank else "Rank nicht gefunden"

        # Schließe den Browser
        browser.close()

        # Gib die gesammelten Daten zurück
        return {
            "damage_per_round": damage_text,
            "kd_ratio": kd_text,
            "kad_ratio": kad_text,
            "headshot_percent": hs_text,
            "kast_percent": kast_text,
            "dd_delta": dd_text,
            "acs_score": acs_text,
            "rank": rank_text
        }

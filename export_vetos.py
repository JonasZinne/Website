MAPS = ["Abyss", "Ascent", "Bind", "Haven", "Icebox", "Lotus", "Sunset"]
TEAMS = ["ATN", "FOKUS", "PXU", "RZN", "Scald", "SK", "SSP", "TOG"]

def choose_side(side_choice):
    return "Att" if side_choice == 'att' else "Def"

def perform_veto_process(data, index):
    team_a = data.get(f'team_a_{index}')
    team_b = data.get(f'team_b_{index}')
    matchday = data.get('matchday')

    available_maps = MAPS.copy()

    # Eingaben verarbeiten
    ban_a1 = data.get(f'ban_a1_{index}')
    ban_b1 = data.get(f'ban_b1_{index}')
    pick_a = data.get(f'pick_a_{index}')
    side_b1 = choose_side(data.get(f'side_b1_{index}'))
    pick_b = data.get(f'pick_b_{index}')
    side_a1 = choose_side(data.get(f'side_a1_{index}'))
    ban_a2 = data.get(f'ban_a2_{index}')
    ban_b2 = data.get(f'ban_b2_{index}')

    # Maps aus Pool entfernen
    available_maps.remove(ban_a1)
    available_maps.remove(ban_b1)
    available_maps.remove(pick_a)
    available_maps.remove(pick_b)
    available_maps.remove(ban_a2)
    available_maps.remove(ban_b2)

    # Decider festlegen
    decider = available_maps[0]
    side_a2 = choose_side(data.get(f'side_a2_{index}'))

    # Ergebnisse zurückgeben
    return {
        "team_a": team_a,
        "team_b": team_b,
        "matchday": matchday,
        "bans": {
            "A": [ban_a1, ban_a2],
            "B": [ban_b1, ban_b2]
        },
        "picks": {
            "A": pick_a,
            "B": pick_b
        },
        "sides": {
            "pick_a": side_b1,
            "pick_b": side_a1,
            "decider": side_a2
        },
        "decider": decider
    }

def main(data=None):
    if data:
        results = []
        for i in range(4):
            result = perform_veto_process(data, i)
            results.append(result)
        return results
from flask import render_template

MAPS = ["Abyss", "Ascent", "Bind", "Haven", "Icebox", "Lotus", "Sunset"]
TEAMS = ["ATN", "FOKUS", "PXU", "RZN", "Scald", "SK", "SSP", "TOG"]

def choose_side(side_choice):
    return "Att" if side_choice == 'att' else "Def"

def perform_veto_process(data):
    team_a = data.get('team_a')
    team_b = data.get('team_b')

    available_maps = MAPS.copy()

    # Eingaben verarbeiten
    ban_a1 = data.get('ban_a1')
    ban_b1 = data.get('ban_b1')
    pick_a = data.get('pick_a')
    side_b1 = choose_side(data.get('side_b1'))
    pick_b = data.get('pick_b')
    side_a1 = choose_side(data.get('side_a1'))
    ban_a2 = data.get('ban_a2')
    ban_b2 = data.get('ban_b2')

    # Maps aus Pool entfernen
    available_maps.remove(ban_a1)
    available_maps.remove(ban_b1)
    available_maps.remove(pick_a)
    available_maps.remove(pick_b)
    available_maps.remove(ban_a2)
    available_maps.remove(ban_b2)

    # Decider festlegen
    decider = available_maps[0]
    side_a2 = choose_side(data.get('side_a2'))

    # Ergebnisse zurückgeben
    return {
        "team_a": team_a,
        "team_b": team_b,
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
        result = perform_veto_process(data)
        return result
import os
from flask import Flask, render_template, request, send_file, session
from export_matches import main as export_matches_main
from export_vetos import main as export_vetos_main, MAPS, TEAMS_DIV1, TEAMS_DIV2

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Dashboard (Index)
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

# Export Vetos
@app.route("/export_vetos", methods=["GET", "POST"])
def export_vetos():
    veto_results = []

    division = request.args.get('division', '1')
    teams = TEAMS_DIV1 if division == '1' else TEAMS_DIV2
    num_matches = len(teams) // 2

    if request.method == "POST":
        veto_results = export_vetos_main(request.form, num_matches)

    return render_template("export_vetos.html", maps=MAPS, teams=teams, veto_results=veto_results, division=division, num_matches=num_matches)

# Export Matches
@app.route("/export_matches", methods=["GET", "POST"])
def export_matches():
    if request.method == "POST":
        url = request.form['url']
        excel_file = export_matches_main(url)
        session['excel_file'] = excel_file
        session['file_exported'] = True

    file_exported = session.get('file_exported', False)
    return render_template("export_matches.html", file_exported=file_exported)
    
@app.route("/download_matches")
def download_matches():
    if not session.get('file_exported'):
        return render_template("error.html", error_code=403, error_message="Download nicht verfügbar"), 403
    
    file_path = session.get('excel_file')
    
    if file_path and os.path.exists(file_path):
        session.pop('file_exported', None)
        return send_file(file_path, as_attachment=True)
    else:
        return render_template("error.html", error_code=404, error_message="Datei nicht gefunden"), 404

# Turnier anlegen
@app.route("/create_tournament", methods=["GET"])
def create_tournament():
    return render_template("create_tournament.html")

if __name__ == "__main__":
    app.run(debug=True)
import os
from flask import Flask, render_template, request, send_file, session, redirect, url_for
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
    division = request.args.get('division', session.get('division', '1'))
    teams = TEAMS_DIV1 if division == '1' else TEAMS_DIV2
    num_matches = len(teams) // 2

    if request.method == "POST":
        veto_results = export_vetos_main(request.form, num_matches)
        session['veto_results'] = veto_results
        session['division'] = division
        return redirect(url_for('export_vetos', division=division))

    veto_results = session.pop('veto_results', [])
    division = session.get('division', division)

    return render_template("export_vetos.html", maps=MAPS, teams=teams, veto_results=veto_results, division=division, num_matches=num_matches)

# Export Matches
@app.route("/export_matches", methods=["GET", "POST"])
def export_matches():
    if request.method == "POST":
        url = request.form['url']
        excel_file = export_matches_main(url)
        session['excel_file'] = excel_file
        session['file_exported'] = True
        
        return redirect(url_for('export_matches'))

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

# 404 - Not Found
@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", error_code=404, error_message="URL nicht gefunden"), 404

# 403 - Forbidden
@app.errorhandler(403)
def forbidden(error):
    return render_template("error.html", error_code=403, error_message="Zugriff wurde verweigert"), 403

# 500 - Internal Server Error
@app.errorhandler(500)
def internal_error(error):
    return render_template("error.html", error_code=500, error_message="interner Serverfehler ist aufgetreten"), 500

if __name__ == "__main__":
    app.run(debug=True)
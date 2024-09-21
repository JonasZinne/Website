import os
from flask import Flask, render_template, request, send_file, session
from export_matches import main as export_matches_main
from export_vetos import main as export_vetos_main

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Dashboard (Index)
@app.route("/", methods=["GET"])
def index():
    session['can_download_matches'] = False
    return render_template("index.html")

# Export Matches
@app.route("/export_matches", methods=["GET", "POST"])
def export_matches():
    session['can_download_matches'] = True
    message = None
    file_path = None
    
    if request.method == "POST":
        url = request.form.get('url')
        
        message, file_path = export_matches_main(url)      
        session['message'] = message
        session['file_path'] = file_path
    
    return render_template("export_matches.html", message=message, file_ready=(file_path is not None))

# Download der Datei
@app.route("/download_matches")
def download_matches():
    if not session.get('can_download_matches'):
        return render_template("error.html", error_code=403, error_message="Download nicht verfügbar"), 403
    
    file_path = session.get('file_path')
    
    if file_path and os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return render_template("error.html", error_code=404, error_message="Datei nicht gefunden"), 404

# Export Vetos
@app.route("/export_vetos", methods=["GET", "POST"])
def export_vetos():
    session['can_download_matches'] = False
    message = None
    file_path = None
    
    if request.method == "POST":       
        message, file_path = export_vetos_main()      
        session['message'] = message
        session['file_path'] = file_path
    
    return render_template("export_vetos.html", message=message, file_ready=(file_path is not None))

# Turnier anlegen
@app.route("/create_tournament", methods=["GET"])
def create_tournament():
    session['can_download_matches'] = False
    return render_template("create_tournament.html")

if __name__ == "__main__":
    app.run(debug=True)